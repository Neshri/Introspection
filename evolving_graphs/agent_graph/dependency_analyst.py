import os
from typing import Set, Dict

from .semantic_gatekeeper import SemanticGatekeeper
from .summary_models import ModuleContext, Claim

class DependencyAnalyst:
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def analyze_dependencies(self, context: ModuleContext, dependencies: Set[str], dep_contexts: Dict[str, ModuleContext], module_name: str, file_path: str):
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
                # We look for "Exports" or specific values in the dependency's Public API.
                known_values = []
                for api_desc in upstream_ctx.public_api.values():
                    desc_lower = api_desc.text.lower()
                    if "stores" in desc_lower or "defines" in desc_lower or "value" in desc_lower:
                         known_values.append(f"- {api_desc.text}")
                
                # --- 2. Format Context ---
                values_context = ""
                if known_values:
                    values_context = "\nKnown Exported Values:\n" + "\n".join(known_values[:3])

                # --- 3. Prepare Verification Evidence ---
                # This is needed so the Auditor doesn't reject specific claims like "uses granite4:3b"
                verification_source = f"Dependency Role: {child_role}\n{values_context}"
                
                # --- 4. Prepare Log Label ---
                label = f"Dep:{module_name}->{dep_name}"

                # --- 5. Execute LLM ---
                prompt = f"""
                Context: Module `{module_name}` imports `{dep_name}`.
                `{dep_name}` Role: "{child_role}"
                {values_context}
                
                Task: Why does `{module_name}` need this dependency? 
                (If it uses a Known Exported Value, explicitly MENTION it).
                
                Instruction: Return a JSON object with field "intent" (Single string).
                """
                
                intent = self.gatekeeper.execute_with_feedback(
                    prompt, 
                    "intent", 
                    forbidden_terms=[dep_name],
                    verification_source=verification_source,
                    log_context=label
                )
                explanation = f"Uses `{dep_name}` {intent}."

            context.add_dependency_context(dep_path, explanation, [Claim(explanation, f"Import {dep_name}", file_path)])