import os
import re
from typing import Set, Dict, List, Optional

# Import BANNED_ADJECTIVES to sanitize inputs
from .semantic_gatekeeper import SemanticGatekeeper, BANNED_ADJECTIVES
from .summary_models import ModuleContext, Claim
from .task_executor import TaskExecutor

class DependencyAnalyst:
    def __init__(self, gatekeeper: SemanticGatekeeper, task_executor: TaskExecutor):
        self.gatekeeper = gatekeeper
        self.task_executor = task_executor

    def _sanitize_context(self, text: str) -> str:
        """Removes banned adjectives from context string to prevent prompt poisoning."""
        if not text: return ""
        # Remove banned words case-insensitively
        pattern = r'\b(' + '|'.join(BANNED_ADJECTIVES) + r')\b'
        return re.sub(pattern, '', text, flags=re.IGNORECASE).strip()

    def analyze_dependencies(self, context: ModuleContext, dependencies: Set[str], dep_contexts: Dict[str, ModuleContext], module_name: str, file_path: str, interactions: list = []):
        """
        Analyzes imports using the TaskExecutor (Plan-and-Solve) to prevent hallucination.
        """
        for dep_path in dependencies:
            dep_name = os.path.basename(dep_path)
            upstream_ctx = dep_contexts.get(dep_path)
            
            explanation = f"Imports `{dep_name}`."
            
            # Helper to clean refs
            def clean_ref(text): 
                return re.sub(r'\[ref:[a-f0-9]+\]', '', text).strip()

            # Only analyze if we have context for the dependency
            if upstream_ctx and upstream_ctx.module_role.text:
                # SANITIZATION FIX: Clean the upstream role text
                child_role = self._sanitize_context(clean_ref(upstream_ctx.module_role.text))
                
                # --- 1. Identify Used Symbols (Hard Data) ---
                used_symbols = sorted(list(set([i['symbol'] for i in interactions if i['target_module'] == dep_name])))
                
                # --- 2. Smart Context Retrieval (Relevance Filtering) ---
                relevant_state = []
                relevant_logic = []
                general_context = []

                state_markers = ["stores", "defines", "configuration", "value", "data container", "enum", "constant", "variable", "setting", "limit", "threshold"]

                for api_name, grounded_text in upstream_ctx.public_api.items():
                    desc = self._sanitize_context(grounded_text.text)
                    
                    is_used = any(
                        sym == api_name or 
                        f" {sym}" in api_name or 
                        f".{sym}" in api_name 
                        for sym in used_symbols
                    )
                    
                    entry = f"- {desc}"
                    
                    if is_used:
                        if any(m in desc.lower() for m in state_markers):
                            relevant_state.append(entry)
                        else:
                            relevant_logic.append(entry)
                    else:
                        if len(general_context) < 3: 
                            general_context.append(entry)

                # --- 3. Format Context Strings ---

                state_context = ""
                if relevant_state:
                    state_context = "\nReferenced Data:\n" + "\n".join([clean_ref(s) for s in relevant_state])
                
                logic_context = ""
                if relevant_logic:
                    logic_context = "\nReferenced Logic:\n" + "\n".join([clean_ref(s) for s in relevant_logic])
                    
                if not relevant_state and not relevant_logic and general_context:
                    logic_context += "\nGeneral Exports (Unused):\n" + "\n".join([clean_ref(s) for s in general_context])

                # --- 4. Prepare Snippet Evidence ---
                raw_snippets = [i.get('snippet', '') for i in interactions if i['target_module'] == dep_name and i.get('snippet')]
                unique_snippets = sorted(list(set(raw_snippets)))
                
                snippet_text = ""
                if unique_snippets:
                    snippet_text = "\nUsage Snippets:\n" + "\n".join([f"- {s}" for s in unique_snippets])
                
                usage_context = f"Used Symbols: {', '.join(used_symbols)}{snippet_text}" if used_symbols else "Used Symbols: (None detected)"

                verification_source = f"Dependency Role: {child_role}\n{state_context}\n{logic_context}\n{usage_context}"
                label = f"Dep:{module_name}->{dep_name}"

                # --- 5. Execute Plan-and-Solve Analysis ---
                intents = []
                
                if used_symbols:
                    # A. Data Usage Analysis
                    if relevant_state:
                        intent = self.task_executor.solve_complex_task(
                            main_goal=f"Determine strictly how `{module_name}` uses the Data/Constants from `{dep_name}` based on the snippets.",
                            context_data=verification_source,
                            log_label=f"{label}:Data"
                        )
                        if intent and "no evidence" not in intent.lower() and "unverified" not in intent.lower():
                            intents.append(intent)

                    # B. Logic Usage Analysis
                    if relevant_logic:
                        intent = self.task_executor.solve_complex_task(
                            main_goal=f"Determine strictly how `{module_name}` uses the Logic/Capabilities of `{dep_name}` based on the snippets.",
                            context_data=verification_source,
                            log_label=f"{label}:Logic"
                        )
                        if intent and "no evidence" not in intent.lower() and "unverified" not in intent.lower():
                            intents.append(intent)

                if not intents:
                    explanation = f"Imports `{dep_name}`."
                else:
                    explanation = f"Uses `{dep_name}`: {'; '.join(intents)}."

            context.add_dependency_context(dep_path, explanation, [Claim(explanation, f"Import {dep_name}", file_path)])