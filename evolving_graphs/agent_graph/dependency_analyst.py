import os
from typing import Set, Dict

from .semantic_gatekeeper import SemanticGatekeeper
from .summary_models import ModuleContext, Claim

class DependencyAnalyst:
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def analyze_dependencies(self, context: ModuleContext, dependencies: Set[str], dep_contexts: Dict[str, ModuleContext], module_name: str, file_path: str, interactions: list = []):
        """
        Analyzes imports to determine intent, utilizing upstream knowledge for context.
        """
        for dep_path in dependencies:
            dep_name = os.path.basename(dep_path)
            upstream_ctx = dep_contexts.get(dep_path)
            
            explanation = f"Imports `{dep_name}`."
            
            # Only analyze if we have context for the dependency
            if upstream_ctx and upstream_ctx.module_role.text:
                child_role = upstream_ctx.module_role.text
                
                # --- 1. State Propagation: Extract Known Values ---
                state_markers = ["stores", "defines", "configuration", "value", "data container", "enum", "constant", "variable", "setting", "limit", "threshold"]
                
                known_state = []
                known_logic = []
                
                for api_desc in upstream_ctx.public_api.values():
                    desc_lower = api_desc.text.lower()
                    if any(m in desc_lower for m in state_markers):
                         known_state.append(f"- {api_desc.text}")
                    else:
                         known_logic.append(f"- {api_desc.text}")
                
                # --- 2. Format Context ---
                state_context = ""
                if known_state:
                    state_context = "\nExported Data/State:\n" + "\n".join(known_state[:5])
                    
                logic_context = ""
                if known_logic:
                    logic_context = "\nExported Capabilities/Logic:\n" + "\n".join(known_logic[:5])

                # --- 3. Prepare Verification Evidence ---
                used_symbols = sorted(list(set([i['symbol'] for i in interactions if i['target_module'] == dep_name])))
                
                # Extract and deduplicate snippets
                raw_snippets = [i.get('snippet', '') for i in interactions if i['target_module'] == dep_name and i.get('snippet')]
                unique_snippets = sorted(list(set(raw_snippets)))
                
                snippet_text = ""
                if unique_snippets:
                    snippet_text = "\nUsage Snippets:\n" + "\n".join([f"- {s}" for s in unique_snippets])
                
                usage_context = f"Used Symbols: {', '.join(used_symbols)}{snippet_text}" if used_symbols else "Used Symbols: (None detected)"

                verification_source = f"Dependency Role: {child_role}\n{state_context}\n{logic_context}\n{usage_context}"
                label = f"Dep:{module_name}->{dep_name}"

                # --- 5. Execute LLM (Split Analysis) ---
                
                # A. Data Usage Analysis
                data_intent = ""
                if known_state:
                    # FIX: Ask for a full sentence to satisfy Gatekeeper word count (Avoids 'None' Style Fail)
                    prompt_data = f"""
                    Context: Module `{module_name}` imports `{dep_name}`.
                    `{dep_name}` Exports Data:
                    {state_context}
                    
                    Task: Does `{module_name}` import or use any of these constants/types?
                    If yes, describe the MECHANISM and INTENT in 1 short sentence starting with a verb.
                    Example: "Retrieves the MAX_RETRIES constant to configure the connection timeout."
                    
                    If no, state "Does not access any exported data."
                    """
                    data_intent = self.gatekeeper.execute_with_feedback(
                        prompt_data, "intent", [dep_name, "uses functionality", "utilizes"], verification_source=verification_source, log_context=f"{label}:Data"
                    )
                
                # B. Logic Invocation Analysis
                logic_intent = ""
                if known_logic:
                    # FIX: Ask for a full sentence
                    prompt_logic = f"""
                    Context: Module `{module_name}` imports `{dep_name}`.
                    `{dep_name}` Exports Logic:
                    {logic_context}
                    {usage_context}
                    
                    Task: Does `{module_name}` call or use any of these functions/classes/logic?
                    If yes, describe the MECHANISM and INTENT in 1 short sentence starting with a verb.
                    Example: "Calls the `connect` function to establish a secure websocket link."
                    
                    If no, state "Does not access any exported logic."
                    """
                    logic_intent = self.gatekeeper.execute_with_feedback(
                        prompt_logic, "intent", [dep_name, "uses functionality", "utilizes"], verification_source=verification_source, log_context=f"{label}:Logic"
                    )

                # Combine & Filter the "Negative" responses
                intents = []
                
                # Check for Data Intent valid response
                if data_intent and "does not access" not in data_intent.lower() and "none" not in data_intent.lower():
                    intents.append(data_intent)
                    
                # Check for Logic Intent valid response
                if logic_intent and "does not access" not in logic_intent.lower() and "none" not in logic_intent.lower():
                    intents.append(logic_intent)
                
                if not intents:
                    explanation = f"Imports `{dep_name}`."
                else:
                    explanation = f"Uses `{dep_name}`: {'; '.join(intents)}."

            context.add_dependency_context(dep_path, explanation, [Claim(explanation, f"Import {dep_name}", file_path)])