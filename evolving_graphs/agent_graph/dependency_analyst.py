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
                # REMOVED: state_markers list and artificial separation of Data/Logic.
                
                relevant_entries = []
                general_context = []

                for api_name, grounded_text in upstream_ctx.public_api.items():
                    desc = self._sanitize_context(grounded_text.text)
                    
                    # Check if the API entry is relevant to the symbols we actually use
                    is_used = any(
                        sym == api_name or 
                        f" {sym}" in api_name or 
                        f".{sym}" in api_name 
                        for sym in used_symbols
                    )
                    
                    entry = f"- {desc}"
                    
                    if is_used:
                        relevant_entries.append(entry)
                    else:
                        if len(general_context) < 3: 
                            general_context.append(entry)

                # --- 3. Format Context Strings ---
                # Unified context block to prevent leading the witness.
                
                upstream_context_str = ""
                if relevant_entries:
                    upstream_context_str = "\nRelevant Upstream Context:\n" + "\n".join([clean_ref(s) for s in relevant_entries])
                elif general_context:
                    # Fallback: If we can't match symbols perfectly, show general exports so the LLM isn't flying blind.
                    upstream_context_str = "\nGeneral Exports (Unused/Unmatched):\n" + "\n".join([clean_ref(s) for s in general_context])

                # --- 4. Prepare Snippet Evidence ---
                raw_snippets = [i.get('snippet', '') for i in interactions if i['target_module'] == dep_name and i.get('snippet')]
                unique_snippets = sorted(list(set(raw_snippets)))
                
                snippet_text = ""
                if unique_snippets:
                    snippet_text = "\nUsage Snippets:\n" + "\n".join([f"- {s}" for s in unique_snippets])
                
                usage_context = f"Used Symbols: {', '.join(used_symbols)}{snippet_text}" if used_symbols else "Used Symbols: (None detected)"

                # Unified verification source
                verification_source = f"Dependency Role: {child_role}\n{upstream_context_str}\n{usage_context}"
                label = f"Dep:{module_name}->{dep_name}"

                # --- 5. Execute Plan-and-Solve Analysis ---
                intents = []
                
                if used_symbols:
                    # Single, neutral prompt. 
                    # We ask the LLM to determine the nature of the usage (Data vs Logic) based on evidence,
                    # rather than forcing it to fill a specific bucket.
                    intent = self.task_executor.solve_complex_task(
                        main_goal=f"Analyze the snippets to determine strictly how `{module_name}` utilizes `{dep_name}`. Specify if it accesses data, invokes logic, or inherits classes.",
                        context_data=verification_source,
                        log_label=f"{label}:Usage"
                    )
                    
                    # Filter out non-answers
                    if intent and "no evidence" not in intent.lower() and "unverified" not in intent.lower():
                        intents.append(intent)

                if not intents:
                    explanation = f"Imports `{dep_name}`."
                else:
                    explanation = f"Uses `{dep_name}`: {'; '.join(intents)}."

            context.add_dependency_context(dep_path, explanation, [Claim(explanation, f"Import {dep_name}", file_path)])