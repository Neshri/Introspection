import os
import ast
import json
from typing import Any, Dict, List, Optional
from enum import Enum

from .summary_models import ModuleContext, Claim, Alert
from .semantic_gatekeeper import SemanticGatekeeper

# --- Architectural Definitions ---

class ModuleArchetype(Enum):
    CONFIGURATION = "Configuration"     
    DATA_MODEL = "Data Model"           
    UTILITY = "Utility"                 
    SERVICE = "Service"                 
    ENTRY_POINT = "Entry Point"              

class ModuleClassifier:
    def __init__(self, module_name: str, graph_data: Dict[str, Any]):
        self.module_name = module_name
        self.data = graph_data
        
    def classify(self) -> ModuleArchetype:
        if self.module_name.endswith("_main.py") or self.module_name == "__main__.py":
            return ModuleArchetype.ENTRY_POINT
        
        source = self.data.get('source_code', '')
        entities = self.data.get('entities', {})
        deps = len(self.data.get('dependencies', []))
        
        funcs = len(entities.get('functions', []))
        classes = len(entities.get('classes', {}))
        
        has_globals = False
        try:
            tree = ast.parse(source)
            for node in tree.body:
                if isinstance(node, (ast.Assign, ast.AnnAssign)):
                    has_globals = True
        except:
            pass

        if classes > 0 and funcs == 0 and deps == 0:
            return ModuleArchetype.DATA_MODEL
        
        if classes == 0 and funcs > 0 and deps == 0:
            return ModuleArchetype.UTILITY

        if deps == 0:
            if funcs == 0 and classes == 0 and has_globals:
                return ModuleArchetype.CONFIGURATION
            if classes > 0:
                return ModuleArchetype.DATA_MODEL
            return ModuleArchetype.UTILITY

        return ModuleArchetype.SERVICE

class ModuleContextualizer:
    def __init__(self, file_path: str, graph_data: Dict[str, Any], dep_contexts: Dict[str, ModuleContext]):
        self.file_path = file_path
        self.full_graph = graph_data
        self.data = graph_data.get(file_path, {})
        self.dep_contexts = dep_contexts
        self.context = ModuleContext(file_path=file_path)
        self.module_name = os.path.basename(file_path)
        
        classifier = ModuleClassifier(self.module_name, self.data)
        self.archetype = classifier.classify()
        
        self.gatekeeper = SemanticGatekeeper()

    def contextualize_module(self) -> ModuleContext:
        if "error" in self.data:
            self.context.add_alert(Alert("AnalysisError", self.data['error'], "GraphAnalyzer"))
            return self.context

        self._pass_components()
        self._pass_dependencies()
        self._pass_systemic_synthesis()
        self._pass_alerts()
        return self.context

    # --- Helper: Usage Tracing ---

    def _get_downstream_dependents(self) -> List[str]:
        dependents = []
        for mod_path, mod_data in self.full_graph.items():
            if mod_path == self.file_path: continue
            deps = mod_data.get('dependencies', [])
            if self.file_path in deps:
                dependents.append(os.path.basename(mod_path))
        return sorted(dependents)

    def _find_symbol_usages(self, symbol: str) -> List[str]:
        """
        Finds which other modules specifically use this symbol.
        """
        consumers = set()
        for mod_path, data in self.full_graph.items():
            if mod_path == self.file_path: continue
            
            interactions = data.get('interactions', [])
            for i in interactions:
                # i = {context, target_module, symbol}
                if i.get('target_module') == self.module_name and i.get('symbol') == symbol:
                    consumers.add(os.path.basename(mod_path))
        return sorted(list(consumers))

    # --- 1. Component Analysis (Public + Internal + Usage) ---

    def _pass_components(self):
        entities = self.data.get('entities', {})

        # A. Globals (New)
        for glob in entities.get('globals', []):
            name = glob['name']
            is_internal = glob.get('is_private', False)
            
            summary = self._analyze_code_mechanism("Constant", name, glob.get('source_code', ''), forbidden_terms=[name])
            
            # Add Usage Info
            consumers = self._find_symbol_usages(name)
            if consumers:
                summary += f" *(Used by: {', '.join(consumers)})*"
            
            display_name = f"🔒 {name}" if is_internal else f"🔌 {name}"
            self._add_api(display_name, summary, glob.get('signature', name))

        # B. Functions
        for func in entities.get('functions', []):
            name = func['signature'].split('(')[0].replace('def ', '')
            is_internal = name.startswith('_')
            
            summary = self._analyze_code_mechanism("Function", name, func.get('source_code', ''), forbidden_terms=[name])
            
            # Add Usage Info
            consumers = self._find_symbol_usages(name)
            if consumers:
                summary += f" *(Used by: {', '.join(consumers)})*"

            display_name = f"🔒 {name}" if is_internal else f"🔌 {name}"
            self._add_api(display_name, summary, func['signature'])

        # C. Classes
        for class_name, class_data in entities.get('classes', {}).items():
            method_summaries = []
            methods = class_data.get('methods', [])
            
            for method in methods:
                m_name = method['signature'].split('(')[0].replace('def ', '')
                action = self._analyze_code_mechanism("Method", f"{class_name}.{m_name}", method.get('source_code', ''), forbidden_terms=[m_name])
                method_summaries.append(f"- {m_name}: {action}")

            if not method_summaries:
                class_summary = f"Stores structured data for {class_name}."
            else:
                class_summary = self._synthesize_class_role(class_name, method_summaries)
            
            # Add Usage Info (Class Level)
            consumers = self._find_symbol_usages(class_name)
            if consumers:
                class_summary += f" *(Used by: {', '.join(consumers)})*"
            
            is_internal = class_name.startswith('_')
            display_name = f"🔒 class {class_name}" if is_internal else f"🔌 class {class_name}"
            
            self._add_api(display_name, class_summary, f"class {class_name}")

    def _analyze_code_mechanism(self, type_label: str, name: str, source: str, forbidden_terms: List[str] = []) -> str:
        prompt = f"""
        Task: Analyze the code of {type_label} `{name}`.
        Code:
        ```python
        {source}
        ```
        Constraint: STRICTLY FORBIDDEN to use subjective adjectives.
        Constraint: Do NOT use future tense.
        
        Instruction: Return a JSON object with a single field "action".
        The "action" must be a specific "Verb + Noun" phrase in the PRESENT TENSE.
        """
        return self.gatekeeper.execute_with_feedback(prompt, "action", forbidden_terms)

    def _synthesize_class_role(self, class_name: str, method_summaries: List[str]) -> str:
        methods_block = chr(10).join(method_summaries)
        prompt = f"""
        Task: Synthesize the mechanism of Class `{class_name}`.
        Verified Behaviors:
        {methods_block}
        Constraint: No marketing fluff. Be precise.
        Constraint: Do NOT use future tense.
        
        Instruction: Return a JSON object with a single field "role".
        The "role" must be a single sentence starting with a 3rd-person present tense verb.
        """
        return self.gatekeeper.execute_with_feedback(prompt, "role", forbidden_terms=[class_name])

    # --- 2. Dependency Analysis ---

    def _pass_dependencies(self):
        dependencies = self.data.get('dependencies', set())
        
        for dep_path in dependencies:
            dep_name = os.path.basename(dep_path)
            upstream_ctx = self.dep_contexts.get(dep_path)
            
            explanation = f"Imports `{dep_name}`."
            
            if upstream_ctx and upstream_ctx.module_role.text:
                child_role = upstream_ctx.module_role.text
                clean_dep_name = dep_name.replace('.py', '')
                
                prompt = f"""
                Task: Define the specific service `{dep_name}` provides to `{self.module_name}`.
                Dependency Capability: "{child_role}"
                Constraint: Do NOT mention the module name `{dep_name}` in the output.
                
                Instruction: Return a JSON object with a single field "intent".
                The "intent" must be a short INFINITIVE verb phrase (e.g., "calculate metrics").
                """
                
                intent = self.gatekeeper.execute_with_feedback(prompt, "intent", forbidden_terms=[clean_dep_name, "uses", "using"])
                explanation = f"Uses `{dep_name}` to {intent}."

            self.context.add_dependency_context(dep_path, explanation, [Claim(explanation, f"Import {dep_name}", self.file_path)])

    # --- 3. Systemic Synthesis ---

    def _pass_systemic_synthesis(self):
        local_caps = [f"- {k}: {v.text}" for k, v in self.context.public_api.items()]
        
        dependents = self._get_downstream_dependents()
        impact_str = ", ".join(dependents) if dependents else "(None)"
        impact_footer = ""
        if dependents:
            impact_footer = f"\n\n**Used By:** {impact_str}"

        if self.archetype == ModuleArchetype.CONFIGURATION:
            role = f"The module `{self.module_name}` defines configuration constants and settings."
            full_role = role + impact_footer
            self.context.set_module_role(full_role, [Claim(role, "Archetype Analysis", self.file_path)])
            return
        
        if self.archetype == ModuleArchetype.DATA_MODEL:
            role = f"The module `{self.module_name}` defines data structures and schemas."
            if local_caps:
                 # Cleanup key names for clean output
                 clean_keys = [k.replace('🔌 ', '').replace('🔒 ', '') for k in list(self.context.public_api.keys())[:3]]
                 role = f"The module `{self.module_name}` defines data structures including: {', '.join(clean_keys)}."
            full_role = role + impact_footer
            self.context.set_module_role(full_role, [Claim(role, "Archetype Analysis", self.file_path)])
            return

        child_caps = []
        for dep_path in self.data.get('dependencies', []):
            dep_name = os.path.basename(dep_path)
            ctx = self.dep_contexts.get(dep_path)
            if ctx and ctx.module_role.text:
                clean_role = ctx.module_role.text.split('\n\n**Used By:**')[0]
                child_caps.append(f"- `{dep_name}` (Tool): {clean_role}")

        if not local_caps and not child_caps:
            role = f"The module `{self.module_name}` contains internal utility logic."
            self.context.set_module_role(role + impact_footer, [Claim(role, "Default", self.file_path)])
            return

        prompt = f"""
        Task: Synthesize the High-Level Purpose of `{self.module_name}`.
        
        Archetype: {self.archetype.value}
        
        Tools Used (Dependencies):
        {chr(10).join(child_caps) if child_caps else "(None)"}
        
        Core Actions (Public & Internal):
        {chr(10).join(local_caps) if local_caps else "(Internal Logic)"}
        
        Context - Downstream Consumers (This module is used by):
        {impact_str}
        
        Instruction: Return a JSON object with a single field "role".
        The "role" must be a single sentence describing what the module ACHIEVES (Present Tense).
        Do NOT use "will", "shall", or "to".
        """
        role_text = self.gatekeeper.execute_with_feedback(prompt, "role", forbidden_terms=[self.module_name])
        
        full_role = f"The module `{self.module_name}` {role_text}{impact_footer}"
        self.context.set_module_role(full_role, [Claim(full_role, "Recursive Synthesis", self.file_path)])

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

    def _add_api(self, name: str, text: str, ref: str):
        self.context.add_public_api_entry(name, text, [Claim(text, ref, self.file_path)])