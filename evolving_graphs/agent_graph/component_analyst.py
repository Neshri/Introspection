import os
import ast
from typing import List, Dict, Any
from .semantic_gatekeeper import SemanticGatekeeper
from .summary_models import ModuleContext, Claim

class ComponentAnalyst:
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def analyze_components(self, context: ModuleContext, entities: Dict[str, Any], file_path: str, usage_map: Dict[str, List[str]] = {}) -> List[str]:
        """
        Analyzes components and returns a list of verified summaries (Working Memory).
        """
        module_name = os.path.basename(file_path)
        working_memory = []
        
        # --- Step 1: Build Scope Context (Facts Only) ---
        # We list what exists, but we do NOT include docstrings in the context.
        scope_items = []
        global_defs = {} 

        for glob in entities.get('globals', []):
            name = glob['name']
            # Extract pure assignment logic
            raw_source = glob.get('source_code', '').strip()
            clean_source = self._get_logic_only_source(raw_source)
            global_defs[name] = clean_source
            scope_items.append(f"Global `{name}` assignment: `{clean_source}`")

        for func in entities.get('functions', []):
            name = func['signature'].split('(')[0].replace('def ', '')
            scope_items.append(f"Function `{name}` defined.")

        base_scope_context = "\n".join(scope_items)

        # --- Step 2: Analyze Globals ---
        for glob in entities.get('globals', []):
            name = glob['name']
            source = glob.get('source_code', '')
            is_internal = glob.get('is_private', False)
            
            # QUESTION: Identity
            prompt = f"Identify the specific data structure or literal value assigned to `{name}`."
            
            log_label = f"{module_name}:{name}"
            summary = self._analyze_mechanism(
                "Global/Constant", name, source, 
                docstring="", # Globals usually don't have docstrings in this structure
                prompt_override=prompt, 
                scope_context=base_scope_context, 
                log_label=log_label
            )
            self._add_entry(context, name, summary, is_internal, file_path)
            working_memory.append(f"Global `{name}`: {summary}")

        # --- Step 3: Analyze Functions ---
        for func in entities.get('functions', []):
            name = func['signature'].split('(')[0].replace('def ', '')
            is_internal = name.startswith('_')
            source = func.get('source_code', '')
            
            # Dynamic Context
            relevant_context = [base_scope_context]
            usages = usage_map.get(name, [])
            if usages:
                relevant_context.insert(0, f"Caller Context: Used by {', '.join(usages[:3])}")

            log_label = f"{module_name}:{name}"
            
            # QUESTION: Mechanism (Input -> Transformation -> Output)
            prompt = f"""
            Task: Describe the MECHANISM of function `{name}`.
            1. What arguments does it accept?
            2. What external functions does it call?
            3. What does it return?
            Ignore all comments. Focus ONLY on the code logic.
            """

            summary = self._analyze_mechanism(
                "Function", name, source, 
                docstring=func.get('docstring', ''),
                prompt_override=prompt,
                forbidden_terms=[name], 
                scope_context="\n".join(relevant_context),
                log_label=log_label
            )
            self._add_entry(context, name, summary, is_internal, file_path)
            working_memory.append(f"Function `{name}`: {summary}")

        # --- Step 4: Analyze Classes ---
        for class_name, class_data in entities.get('classes', {}).items():
            method_summaries = []
            methods = class_data.get('methods', [])
            
            # Sanitize class source: remove docstrings so we don't read the "marketing"
            raw_class_source = class_data.get('source_code', '')
            clean_class_source = self._get_logic_only_source(raw_class_source)
            
            for method in methods:
                m_name = method['signature'].split('(')[0].replace('def ', '')
                source = method.get('source_code', '')
                
                # Check for pure abstract methods
                clean_method_source = self._get_logic_only_source(source)
                if "pass" in clean_method_source and len(clean_method_source.split()) < 5:
                    action = "Defines interface signature (Abstract)."
                else:
                    log_label = f"{module_name}:{class_name}.{m_name}"
                    # QUESTION: State Mutation
                    m_prompt = f"What logic does method `{m_name}` execute? Does it modify `self` attributes?"
                    
                    action = self._analyze_mechanism(
                        "Method", f"{class_name}.{m_name}", source,
                        docstring=method.get('docstring', ''),
                        prompt_override=m_prompt,
                        forbidden_terms=[m_name, "init"],
                        scope_context=base_scope_context,
                        log_label=log_label
                    )
                
                method_summaries.append(f"- {m_name}: {action}")

            if not method_summaries:
                class_summary = f"Data container for {class_name} records."
            else:
                log_label = f"{module_name}:{class_name}"
                class_summary = self._synthesize_class_role(
                    class_name, 
                    method_summaries, 
                    clean_source=clean_class_source, 
                    log_label=log_label
                )
            
            is_internal = class_name.startswith('_')
            prefix = "class "
            display_name = f"🔒 {prefix}{class_name}" if is_internal else f"🔌 {prefix}{class_name}"
            context.add_public_api_entry(display_name, class_summary, [Claim(class_summary, f"{prefix}{class_name}", file_path)])
            working_memory.append(f"Class `{class_name}`: {class_summary}")
            
        return working_memory

    def generate_module_skeleton(self, source_code: str) -> str:
        """
        Generates a valid Python skeleton (Imports + Signatures + Globals) with bodies removed.
        This serves as the 'Structure' for Macro-Verification.
        """
        try:
            tree = ast.parse(source_code)
        except:
            return source_code # Fallback if parse fails

        class SkeletonTransformer(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                # Keep signature, replace body with '...'
                new_node = node
                new_node.body = [ast.Expr(value=ast.Constant(value=Ellipsis))]
                return new_node

            def visit_AsyncFunctionDef(self, node):
                new_node = node
                new_node.body = [ast.Expr(value=ast.Constant(value=Ellipsis))]
                return new_node

            def visit_ClassDef(self, node):
                # Visit methods to strip them, but keep the class structure
                self.generic_visit(node)
                return node

        transformer = SkeletonTransformer()
        new_tree = transformer.visit(tree)
        
        try:
            return ast.unparse(new_tree)
        except:
            return source_code

    def _get_logic_only_source(self, source_code: str) -> str:
        """
        Parses code and removes docstrings/comments to force the LLM to read Logic, not Intent.
        """
        try:
            parsed = ast.parse(source_code)
            # This walker strips docstrings.
            # However, Python's ast.unparse (3.9+) creates clean code. 
            # If < 3.9, we just return raw source, but assuming modern env:
            for node in ast.walk(parsed):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
                    if ast.get_docstring(node):
                        node.body = node.body[1:] # Remove docstring node
                        # Handle empty body case (e.g. only docstring)
                        if not node.body:
                            node.body.append(ast.Pass())
            return ast.unparse(parsed)
        except:
            # Fallback if partial code snippet fails parse
            return source_code

    def _analyze_mechanism(self, type_label: str, name: str, source: str, docstring: str = "", forbidden_terms: List[str] = [], prompt_override: str = None, scope_context: str = "", log_label: str = "General") -> str:
        
        # Sanitize the specific snippet being analyzed
        clean_source = self._get_logic_only_source(source)

        base_prompt = prompt_override if prompt_override else f"""
        Task: Analyze the PURPOSE and MECHANISM of {type_label} `{name}`.
        """
        
        instruction = f"""
        Context:
        {scope_context}
        
        Developer Intent (Docstring):
        "{docstring}"
        
        Code Logic (Docstrings Removed):
        ```python
        {clean_source}
        ```
        
        Instruction: Return a JSON object with field "description".
        1. Value MUST be a single string.
        2. Describe WHAT the code performs and WHY (Purpose).
        3. Use the Docstring as a hint for intent, but VERIFY it against the Code Logic.
        4. Start with a Verb.
        5. FORBIDDEN: Do not use the name "{name}" in the description.
        6. Constraint: Description must be at least 5 words long (Verb + Object + Detail).
        7. JSON Warning: If the code contains Regex or Windows paths, ESCAPE backslashes (e.g. use "\\\\s" instead of "\\s").
        """
        
        return self.gatekeeper.execute_with_feedback(
            base_prompt + instruction, 
            "description", 
            forbidden_terms, 
            verification_source=clean_source, # Verify against TRUTH (Code), not comments
            log_context=log_label
        )

    def _synthesize_class_role(self, class_name: str, method_summaries: List[str], clean_source: str = "", log_label: str = "General") -> str:
        methods_block = chr(10).join(method_summaries)
        
        prompt = f"""
        Task: Synthesize the structural role of Class `{class_name}`.
        
        Method Mechanisms:
        {methods_block}
        
        Instruction: Return a JSON object with field "role".
        1. Start with a VERB (e.g. "Manages", "Encapsulates").
        2. Describe what state/data this class owns based on the methods.
        3. FORBIDDEN: Do not use the class name "{class_name}" in the description.
        4. Constraint: Description must be at least 5 words long.
        """
        return self.gatekeeper.execute_with_feedback(
            prompt, 
            "role", 
            forbidden_terms=[class_name], 
            verification_source=clean_source,
            log_context=log_label
        )

    def _add_entry(self, ctx: ModuleContext, name: str, text: str, is_internal: bool, file_path: str):
        display = f"🔒 {name}" if is_internal else f"🔌 {name}"
        ctx.add_public_api_entry(display, text, [Claim(text, name, file_path)])