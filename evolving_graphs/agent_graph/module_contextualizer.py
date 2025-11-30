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
        self.context.archetype = self.archetype.value # Store for Renderer
        
        self.comp_analyst = ComponentAnalyst(self.gatekeeper)
        self.dep_analyst = DependencyAnalyst(self.gatekeeper)

        # Hard Data: Who calls me? (Calculated once at init)
        self.usage_map = self._build_usage_map()

    def contextualize_module(self, critique_instruction: str = None) -> ModuleContext:
        if "error" in self.data:
            self.context.add_alert(Alert("AnalysisError", self.data['error'], "GraphAnalyzer"))
            return self.context

        # Use the class-level usage_map we calculated in __init__
        self.working_memory = self.comp_analyst.analyze_components(
            self.context, 
            self.data.get('entities', {}), 
            self.file_path,
            usage_map=self.usage_map,
            interactions=self.data.get('interactions', []),
            dep_contexts=self.dep_contexts
        )

        self.dep_analyst.analyze_dependencies(
            self.context, 
            self.data.get('dependencies', set()), 
            self.dep_contexts, 
            self.module_name, 
            self.file_path,
            interactions=self.data.get('interactions', [])
        )

        self._pass_systemic_synthesis(critique_instruction)
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

    def _gather_upstream_knowledge(self) -> Dict[str, str]:
        """
        Categorizes upstream dependencies into State (Data) and Logic (Capabilities).
        Returns a dictionary with formatted strings for each category.
        """
        state_knowledge = []
        logic_knowledge = []
        
        # Keywords that strongly suggest data/state
        state_markers = ["stores", "defines", "configuration", "value", "data container", "enum", "constant"]
        
        for dep_path, dep_ctx in self.dep_contexts.items():
            if not dep_ctx: continue
            dep_name = os.path.basename(dep_path)
            
            for api_name, grounded_text in dep_ctx.public_api.items():
                desc = grounded_text.text.lower()
                
                # Classification: Is it State or Logic?
                is_state = any(marker in desc for marker in state_markers)
                
                entry = f"- {dep_name} exports `{api_name}`: {grounded_text.text}"
                
                if is_state:
                    state_knowledge.append(entry)
                else:
                    logic_knowledge.append(entry)
                    
        return {
            "state": chr(10).join(state_knowledge),
            "logic": chr(10).join(logic_knowledge)
        }

    def _pass_systemic_synthesis(self, critique_instruction: str = None):
        local_caps = [f"- {k}: {v.text}" for k, v in self.context.public_api.items()]
        upstream_data = self._gather_upstream_knowledge()
        
        upstream_state = upstream_data["state"]
        upstream_logic = upstream_data["logic"]
        
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
        
        critique_section = ""
        if critique_instruction:
            critique_section = f"\n### CRITIQUE FEEDBACK\nThe previous analysis was criticized. Please address this specific instruction:\n**{critique_instruction}**\n"

        # --- ARCHETYPE-AWARE PROMPTING (Objective Truth) ---
        # We tailor the instructions to prevent "Hallucinated Agency"
        
        archetype_instructions = ""
        if self.archetype == ModuleArchetype.DATA_MODEL:
            archetype_instructions = """
            CONSTRAINT: You are describing a PASSIVE data structure. 
            - Use verbs like 'Defines', 'Stores', 'Encapsulates', 'Represent'.
            - Do NOT use active verbs like 'Orchestrates', 'Manages', 'Controls'.
            - Do NOT imply this module does anything on its own. It is just data.
            """
        elif self.archetype == ModuleArchetype.UTILITY:
            archetype_instructions = """
            CONSTRAINT: You are describing a PASSIVE utility library.
            - Use verbs like 'Provides', 'Offers', 'Contains'.
            - Focus on the *capabilities* it offers to others.
            """
        elif self.archetype == ModuleArchetype.ENTRY_POINT:
             archetype_instructions = """
            CONSTRAINT: You are describing an ENTRY POINT.
            - Use verbs like 'Orchestrates', 'Initializes', 'Runs'.
            - Focus on the high-level goal it executes.
            """
        else: # Service
             archetype_instructions = """
            CONSTRAINT: You are describing an ACTIVE service or agent.
            - Use verbs like 'Manages', 'Analyzes', 'Generates'.
            - Focus on its responsibility in the system.
            """

        prompt = f"""
### ROLE
You are a Technical System Architect.

### CONTEXT
Archetype: {self.archetype.value}

Local Capabilities:
{chr(10).join(local_caps)}

Upstream State (Data/Config):
{upstream_state if upstream_state else "(None)"}

Upstream Logic (Collaborators):
{upstream_logic if upstream_logic else "(None)"}

External Imports:
{imports_context}
{critique_section}
### TASK
Generate a JSON object with a "role" field that synthesizes the **Systemic Role** of `{self.module_name}`.

{archetype_instructions}

### REQUIREMENTS
1. Output strictly valid JSON with key "role".
2. Do NOT use the module name "{self.module_name}".
3. Do NOT use marketing adjectives (e.g. "efficient", "seamless", "robust"). Do not mention that you are avoiding them.
4. Description must be at least 5 words long.

### EXAMPLE
Input: (Context about a database module)
Output: {{"role": "Persists user data to disk and manages connection pooling."}}
"""
        
        # Pass the SKELETON + WORKING MEMORY for verification (Recursive Verification).
        skeleton = self.comp_analyst.generate_module_skeleton(self.data.get('source_code', ''))
        working_memory_str = "\n".join(getattr(self, 'working_memory', []))
        
        verification_evidence = f"--- MODULE SKELETON ---\n{skeleton}\n\n--- CHILD SUMMARIES (Working Memory) ---\n{working_memory_str}\n\n--- UPSTREAM STATE ---\n{upstream_state}\n\n--- UPSTREAM LOGIC ---\n{upstream_logic}\n\n--- IMPORTS ---\n{imports_context}"
        
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