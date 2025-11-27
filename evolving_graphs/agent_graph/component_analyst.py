import os
import ast
from typing import List, Dict, Any
from .semantic_gatekeeper import SemanticGatekeeper
from .summary_models import ModuleContext, Claim

class ComponentAnalyst:
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def analyze_components(self, context: ModuleContext, entities: Dict[str, Any], file_path: str, usage_map: Dict[str, List[str]] = {}, interactions: List[Dict] = [], dep_contexts: Dict[str, ModuleContext] = {}) -> List[str]:
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
            prompt = "Identify the specific data structure or literal value assigned in this statement."
            
            log_label = f"{module_name}:{name}"
            summary = self._analyze_mechanism(
                "Global/Constant", name, source, 
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

            # Dependency Context (Outgoing)
            dep_context = self._resolve_dependency_context(name, interactions, dep_contexts)
            if dep_context:
                relevant_context.append(f"Dependency Context:\n{dep_context}")

            log_label = f"{module_name}:{name}"

            # QUESTION: Mechanism (Input -> Transformation -> Output)
            prompt = """
            Task: Analyze the MECHANISM, INVARIANTS, and SIDE EFFECTS of this code block.
            1. Identify input arguments and return values.
            2. Identify **Side Effects** (e.g. I/O, global state changes, external API calls).
            3. Identify **Invariants** (e.g. assertions, raised exceptions, validation checks).
            
            Constraint: If you find a Side Effect or Invariant, you MUST explicitly state it in the description (e.g. "Enforces non-null input", "Mutates global configuration").
            Ignore all comments. Focus ONLY on the code logic.
            """

            summary = self._analyze_mechanism(
                "Function", name, source, 
                prompt_override=prompt,
                forbidden_terms=[name] if name != "main" else [], 
                scope_context="\n".join(relevant_context),
                log_label=log_label
            )
            self._add_entry(context, name, summary, is_internal, file_path)
            working_memory.append(f"Function `{name}`: {summary}")

# --- Step 4: Analyze Classes ---
        for class_name, class_data in entities.get('classes', {}).items():
            # FIX: Determine class visibility BEFORE iterating methods
            is_internal = class_name.startswith('_')
            
            method_summaries = []
            methods = class_data.get('methods', [])
            
            # Sanitize class source: remove docstrings so we don't read the "marketing"
            raw_class_source = class_data.get('source_code', '')
            clean_class_source = self._get_logic_only_source(raw_class_source)
            
            for method in methods:
                m_name = method['signature'].split('(')[0].replace('def ', '')
                source = method.get('source_code', '')
                
                # Check for pure abstract methods or NotImplementedError
                clean_method_source = self._get_logic_only_source(source)
                is_abstract = False
                
                # Check for 'pass' or '...'
                if ("pass" in clean_method_source or "..." in clean_method_source) and len(clean_method_source.split()) < 5:
                    is_abstract = True
                # Check for NotImplementedError
                elif "NotImplementedError" in clean_method_source and len(clean_method_source.split()) < 15:
                    is_abstract = True

                if is_abstract:
                    action = "Defines interface signature (Abstract)."
                else:
                    log_label = f"{module_name}:{class_name}.{m_name}"
                    # QUESTION: State Mutation
                    m_prompt = "Describe the actions performed by this method, including any side effects or state mutations. Start directly with the verb. Do not restate the method name."
                    
                    action = self._analyze_mechanism(
                        "Method", f"{class_name}.{m_name}", source,
                        prompt_override=m_prompt,
                        forbidden_terms=[m_name, "init"],
                        scope_context=base_scope_context,
                        log_label=log_label
                    )
                
                method_summaries.append(f"- {m_name}: {action}")
                
                # EXPOSE METHOD IN PUBLIC API
                # Now is_internal is correctly defined
                method_display_name = f"🔌 {class_name}.{m_name}"
                if not is_internal and not m_name.startswith('_'):
                     self._add_entry(context, method_display_name, action, False, file_path)

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
            
            # (Assignment used to be here - now removed or redundant if just used for prefix below)
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
                # Remove docstring if present
                if ast.get_docstring(node):
                    node.body = node.body[1:]
                    if not node.body:
                        node.body.append(ast.Pass())
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

    def _analyze_mechanism(self, type_label: str, name: str, source: str, forbidden_terms: List[str] = [], prompt_override: str = None, scope_context: str = "", log_label: str = "General") -> str:
        
        # Sanitize the specific snippet being analyzed
        clean_source = self._get_logic_only_source(source)

        specific_task = prompt_override if prompt_override else f"Analyze the PURPOSE and MECHANISM of this {type_label}."
        
        prompt = f"""
### ROLE
You are a Technical Code Analyst.

### CONTEXT
{scope_context}

### INPUT CODE
Code Logic:
```python
{clean_source}
```

### TASK
Generate a JSON object with a "description" field that describes the PURPOSE and MECHANISM of this code.
{specific_task}

### REQUIREMENTS
1. Output strictly valid JSON with key "description".
2. Start directly with a VERB (e.g. "Manages", "Parses").
3. Do NOT use the name "{name}". Do not even mention that you are avoiding it.
4. Description must be at least 5 words long.
5. If the code contains Regex or Windows paths, ESCAPE backslashes.

### EXAMPLE
Input Code: def add(a, b): return a + b
Output: {{"description": "Calculates the sum of two inputs and returns the result."}}
"""
        
        return self.gatekeeper.execute_with_feedback(
            prompt, 
            "description", 
            forbidden_terms, 
            verification_source=f"{clean_source}\n\n--- Context ---\n{scope_context}", # Verify against TRUTH (Code) + Context
            log_context=log_label
        )

    def _synthesize_class_role(self, class_name: str, method_summaries: List[str], clean_source: str = "", log_label: str = "General") -> str:
        methods_block = chr(10).join(method_summaries)
        
        prompt = f"""
### ROLE
You are a Technical Code Analyst.

### CONTEXT
Class Name: `{class_name}`
Method Summaries:
{methods_block}

### TASK
Generate a JSON object with a "role" field that synthesizes the structural role of this Class.
1. Start with a VERB (e.g. "Manages", "Encapsulates").
2. Describe what state/data this class owns based on the methods.

### REQUIREMENTS
1. Output strictly valid JSON with key "role".
2. Do NOT use the class name "{class_name}". Do not even mention that you are avoiding it.
3. Do NOT use marketing adjectives (e.g. "efficient", "seamless", "robust", "facilitate").
4. Description must be at least 5 words long.

### EXAMPLE
Input Methods:
- add: Adds item to list
- get: Returns item from list
Output: {{"role": "Manages a collection of items and provides access to them."}}
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

    def _resolve_dependency_context(self, function_name: str, interactions: List[Dict], dep_contexts: Dict[str, ModuleContext]) -> str:
        """
        Finds interactions originating from `function_name` and retrieves context from dependencies.
        """
        context_lines = []
        # Filter interactions where 'context' matches the function name
        relevant = [i for i in interactions if i.get('context') == function_name]
        
        for interaction in relevant:
            target_mod = interaction.get('target_module')
            symbol = interaction.get('symbol')
            
            # Find the dependency context
            # We need to match target_module (basename) to dep_contexts keys (full paths)
            upstream_ctx = None
            for path, ctx in dep_contexts.items():
                if os.path.basename(path) == target_mod:
                    upstream_ctx = ctx
                    break
            
            if upstream_ctx:
                # Try to find specific symbol in Public API
                found_symbol = False
                for api_name, grounded_text in upstream_ctx.public_api.items():
                    # api_name might be "🔌 CrawlerAgent" or "CrawlerAgent"
                    if symbol in api_name:
                        context_lines.append(f"- Uses `{symbol}` from `{target_mod}`: {grounded_text.text}")
                        found_symbol = True
                        break
                
                # If symbol not found, fall back to Module Role
                if not found_symbol and upstream_ctx.module_role.text:
                    context_lines.append(f"- Uses `{target_mod}`: {upstream_ctx.module_role.text}")

        return "\n".join(list(set(context_lines)))