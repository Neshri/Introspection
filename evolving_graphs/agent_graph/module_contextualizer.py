import os
from typing import Any, Dict, List

from .summary_models import ModuleContext, Alert, Claim
from .semantic_gatekeeper import SemanticGatekeeper

from .module_classifier import ModuleClassifier, ModuleArchetype
from .component_analyst import ComponentAnalyst
from .dependency_analyst import DependencyAnalyst

class ModuleContextualizer:
    def __init__(self, file_path: str, graph_data: Dict[str, Any], dep_contexts: Dict[str, ModuleContext]):
        self.file_path = file_path
        self.full_graph = graph_data
        self.data = graph_data.get(file_path, {})
        self.dep_contexts = dep_contexts
        self.context = ModuleContext(file_path=file_path)
        self.module_name = os.path.basename(file_path)
        
        self.gatekeeper = SemanticGatekeeper()
        self.classifier = ModuleClassifier(self.module_name, self.data)
        self.archetype = self.classifier.classify()
        
        self.comp_analyst = ComponentAnalyst(self.gatekeeper)
        self.dep_analyst = DependencyAnalyst(self.gatekeeper)

        # Hard Data: Who calls me? (Calculated once at init)
        self.usage_map = self._build_usage_map()

    def contextualize_module(self) -> ModuleContext:
        if "error" in self.data:
            self.context.add_alert(Alert("AnalysisError", self.data['error'], "GraphAnalyzer"))
            return self.context

        # Use the class-level usage_map we calculated in __init__
        self.working_memory = self.comp_analyst.analyze_components(
            self.context, 
            self.data.get('entities', {}), 
            self.file_path,
            usage_map=self.usage_map
        )

        self.dep_analyst.analyze_dependencies(
            self.context, 
            self.data.get('dependencies', set()), 
            self.dep_contexts, 
            self.module_name, 
            self.file_path,
            interactions=self.data.get('interactions', [])
        )

        self._pass_systemic_synthesis()
        self._pass_alerts()
        
        return self.context

    def _build_usage_map(self) -> Dict[str, List[str]]:
        """
        Scans the ENTIRE project graph to find who calls symbols in THIS module.
        Returns: { 'my_function_name': ['external_module.py', 'other_module.py'] }
        """
        usage_map = {}
        
        for other_path, other_data in self.full_graph.items():
            if other_path == self.file_path: continue
            
            interactions = other_data.get('interactions', [])
            caller_file = os.path.basename(other_path)

            for interaction in interactions:
                if interaction.get('target_module') == self.module_name:
                    symbol_used = interaction.get('symbol')
                    if not symbol_used: continue
                    
                    if symbol_used not in usage_map:
                        usage_map[symbol_used] = []
                    
                    if caller_file not in usage_map[symbol_used]:
                        usage_map[symbol_used].append(caller_file)
        
        return usage_map

    def _gather_upstream_knowledge(self) -> str:
        knowledge = []
        for dep_path, dep_ctx in self.dep_contexts.items():
            if not dep_ctx: continue
            dep_name = os.path.basename(dep_path)
            for api_name, grounded_text in dep_ctx.public_api.items():
                desc = grounded_text.text.lower()
                # Filter for relevant state definitions to keep context focused but accurate
                if "stores" in desc or "defines" in desc or "configuration" in desc or "value" in desc:
                    knowledge.append(f"- {dep_name} exports `{api_name}`: {grounded_text.text}")
        return chr(10).join(knowledge)

    def _pass_systemic_synthesis(self):
        local_caps = [f"- {k}: {v.text}" for k, v in self.context.public_api.items()]
        local_caps = [f"- {k}: {v.text}" for k, v in self.context.public_api.items()]
        upstream_knowledge = self._gather_upstream_knowledge()
        
        # Add External Imports to Context
        external_imports = sorted(list(self.data.get('external_imports', [])))
        imports_context = f"External Imports: {', '.join(external_imports)}" if external_imports else "(None)"
        
        # --- DETERMINISTIC IMPACT ANALYSIS ---
        # Derive the impact list from the Usage Map (Hard Data), not file dependencies.
        all_callers = set()
        for callers in self.usage_map.values():
            all_callers.update(callers)
        
        impact_footer = ""
        if all_callers:
            impact_footer = f"\n\n**Impact Analysis:** Changes to this module will affect: {', '.join(sorted(all_callers))}"

        if self.archetype == ModuleArchetype.CONFIGURATION:
            role = f"Defines configuration constants."
            self.context.set_module_role(role + impact_footer, [Claim(role, "Archetype", self.file_path)])
            return
        
        prompt = f"""
        Task: Synthesize the High-Level Purpose of `{self.module_name}`.
        Archetype: {self.archetype.value}
        
        Local Capabilities:
        {chr(10).join(local_caps)}
        
        Upstream Context (Knowledge from Dependencies):
        Upstream Context (Knowledge from Dependencies):
        {upstream_knowledge if upstream_knowledge else "(None)"}
        
        External Dependencies (Imports):
        {imports_context}
        
        Instruction: Return a JSON object with field "role".
        1. Value MUST be a single string starting with a VERB (e.g. "Manages", "Analyzes").
        2. FORBIDDEN: Do not use the module name "{self.module_name}" in the description.
        3. FORBIDDEN: Do not use words like "efficient", "seamless", "robust", "facilitate".
        4. Describe the BUSINESS LOGIC directly.
        5. If this module uses a specific configuration (like a model name found in Upstream Context), MENTION IT.
        """
        
        # Pass the SKELETON + WORKING MEMORY for verification (Recursive Verification).
        skeleton = self.comp_analyst.generate_module_skeleton(self.data.get('source_code', ''))
        working_memory_str = "\n".join(getattr(self, 'working_memory', []))
        
        verification_evidence = f"--- MODULE SKELETON ---\n{skeleton}\n\n--- CHILD SUMMARIES (Working Memory) ---\n{working_memory_str}\n\n--- UPSTREAM ---\n{upstream_knowledge}\n\n--- IMPORTS ---\n{imports_context}"
        
        context_label = f"SystemicSynthesis:{self.module_name}"
        
        role_text = self.gatekeeper.execute_with_feedback(
            prompt, 
            "role", 
            forbidden_terms=[self.module_name], 
            verification_source=verification_evidence,
            log_context=context_label
        )
        
        full_role = f"The module `{self.module_name}` {role_text}{impact_footer}"
        self.context.set_module_role(full_role, [Claim(role_text, "Synthesis", self.file_path)])

    def _pass_alerts(self):
        for todo in self.data.get('todos', []):
            self.context.add_alert(Alert("TODO", todo, "Comment"))
        entities = self.data.get('entities', {})
        for func in entities.get('functions', []):
            if func.get('is_unimplemented'):
                self.context.add_alert(Alert("Incomplete", "Function not implemented", func['signature']))
        for class_data in entities.get('classes', {}).values():
            for method in class_data.get('methods', []):
                if method.get('is_unimplemented'):
                    self.context.add_alert(Alert("Incomplete", "Method not implemented", method['signature']))