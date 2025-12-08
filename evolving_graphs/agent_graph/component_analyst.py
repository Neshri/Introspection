import os
import ast
from typing import List, Dict, Any
from .semantic_gatekeeper import SemanticGatekeeper
from .task_executor import TaskExecutor
from .summary_models import ModuleContext, Claim

class SkeletonTransformer(ast.NodeTransformer):
    """
    Strips function bodies and class docstrings to create a token-efficient skeleton.
    Updated to use ast.Constant for Python 3.8+ compatibility.
    """
    # Removed visit_FunctionDef and visit_AsyncFunctionDef to preserve function bodies.
    # The LLM needs to see the implementation to avoid hallucinations.


    def _remove_docstring(self, node):
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
            if isinstance(node.body[0].value.value, str):
                node.body.pop(0)
        return node

    def visit_FunctionDef(self, node):
        self._remove_docstring(node)
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._remove_docstring(node)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        self._remove_docstring(node)
        
        # If body is empty after removing docstring, add 'pass'
        if not node.body:
            node.body = [ast.Pass()]
            
        return self.generic_visit(node)

class ComponentAnalyst:
    def __init__(self, gatekeeper: SemanticGatekeeper, task_executor: TaskExecutor):
        self.gatekeeper = gatekeeper
        self.task_executor = task_executor

    def generate_module_skeleton(self, source_code: str) -> str:
        try:
            tree = ast.parse(source_code)
            transformer = SkeletonTransformer()
            new_tree = transformer.visit(tree)
            return ast.unparse(new_tree)
        except Exception:
            # Fallback to original source if parsing fails (Safety Net)
            return source_code

    def analyze_components(self, context: ModuleContext, entities: Dict[str, Any], file_path: str, usage_map: Dict[str, List[str]] = {}, interactions: List[Dict] = [], dep_contexts: Dict[str, ModuleContext] = {}) -> List[str]:
        """
        Analyzes components using ONLY code logic (No Docstrings).
        Uses TaskExecutor for complex logic to ensure grounding.
        """
        module_name = os.path.basename(file_path)
        working_memory = []
        
        # --- Step 1: Build Scope Context (Facts Only) ---
        scope_items = []

        for glob in entities.get('globals', []):
            name = glob['name']
            raw_source = glob.get('source_code', '').strip()
            clean_source = self._get_logic_only_source(raw_source)
            scope_items.append(f"Global `{name}` assignment: `{clean_source}`")

        for func in entities.get('functions', []):
            name = func['signature'].split('(')[0].replace('def ', '')
            scope_items.append(f"Function `{name}` defined.")

        base_scope_context = "\n".join(scope_items)

        # --- Step 2: Analyze Globals (OPTIMIZED) ---
        for glob in entities.get('globals', []):
            name = glob['name']
            source = glob.get('source_code', '')
            is_internal = glob.get('is_private', False)
            
            # Static Bypass for Constants (prevents LLM hallucinations on BANNED_ADJECTIVES)
            if name.isupper():
                description = f"Defines global constant `{name}`."
                if "CONFIG" in name or "SETTING" in name:
                    description = f"Defines configuration constant `{name}`."
                
                self._add_entry(context, name, description, is_internal, file_path)
                working_memory.append(f"Global `{name}`: {description}")
                continue

            # TaskExecutor for complex globals (e.g. calculated values)
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
            
            relevant_context = [base_scope_context]
            
            # NOTE: Caller Context removed to prevent Intent-over-Mechanism bias.
            
            # Fix: Skip nested functions to prevent double-counting
            # The parent function's analysis intentionally covers its internal helpers.
            if func.get("nesting_level", 0) > 0:
                continue

            
            dep_context = self._resolve_dependency_context(name, interactions, dep_contexts)
            if dep_context:
                relevant_context.append(f"Dependency Context:\n{dep_context}")

            log_label = f"{module_name}:{name}"
            # Fix: Simple, direct prompt to prevent model over-thinking or leakage.
            # Fix: Simple, direct prompt to prevent model over-thinking or leakage.
            prompt = f"Describe what `{name}` does."

            summary = self._analyze_mechanism(
                "Function", name, source, 
                prompt_override=prompt,
                scope_context="\n".join(relevant_context),
                log_label=log_label
            )
            self._add_entry(context, name, summary, is_internal, file_path)
            working_memory.append(f"Function `{name}`: {summary}")

        # --- Step 4: Analyze Classes ---
        for class_name, class_data in entities.get('classes', {}).items():
            is_internal = class_name.startswith('_')
            method_summaries = []
            methods = class_data.get('methods', [])
            
            raw_class_source = class_data.get('source_code', '')
            clean_class_source = self._get_logic_only_source(raw_class_source)
            
            # --- EXTRACT STATE FROM __init__ ---
            init_method = None
            for m in methods:
                sig_name = m.get('signature', '').split('(')[0].replace('def ', '').strip()
                if sig_name == '__init__':
                    init_method = m
                    break
            
            class_state_context = ""
            if init_method:
                clean_init = self._get_logic_only_source(init_method.get('source_code', ''))
                class_state_context = f"Class `{class_name}` State Definition (from __init__):\n```python\n{clean_init}\n```"
            
            for method in methods:
                m_name = method['signature'].split('(')[0].replace('def ', '')
                source = method.get('source_code', '')
                clean_method_source = self._get_logic_only_source(source)
                
                # Check for Abstract/Interface patterns statically
                is_abstract = False
                if ("pass" in clean_method_source or "..." in clean_method_source) and len(clean_method_source.split()) < 5:
                    is_abstract = True
                elif "NotImplementedError" in clean_method_source and len(clean_method_source.split()) < 15:
                    is_abstract = True

                if is_abstract:
                    action = "Defines interface signature (Abstract)."
                else:
                    log_label = f"{module_name}:{class_name}.{m_name}"
                    log_label = f"{module_name}:{class_name}.{m_name}"
                    m_prompt = "Describe this method."
                    
                    # --- INJECT STATE CONTEXT ---
                    combined_context = f"{base_scope_context}\n\n{class_state_context}"
                    
                    action = self._analyze_mechanism(
                        "Method", f"{class_name}.{m_name}", source,
                        prompt_override=m_prompt,
                        scope_context=combined_context, 
                        log_label=log_label
                    )
                
                method_summaries.append(f"- {m_name}: {action}")
                
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
            
            prefix = "class "
            display_name = f"🔒 {prefix}{class_name}" if is_internal else f"🔌 {prefix}{class_name}"
            context.add_public_api_entry(display_name, class_summary, [Claim(class_summary, f"{prefix}{class_name}", file_path)])
            working_memory.append(f"Class `{class_name}`: {class_summary}")
            
        return working_memory

    def _get_logic_only_source(self, source_code: str) -> str:
        """
        Removes docstrings to prevent 'Prompt Poisoning'.
        Updated to use ast.Constant for Py3.8+ compatibility.
        """
        try:
            parsed = ast.parse(source_code)
            for node in ast.walk(parsed):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
                    # Check for docstring (first item is Expr -> Constant(str))
                    if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                        if isinstance(node.body[0].value.value, str):
                            node.body.pop(0)
                            if not node.body:
                                node.body.append(ast.Pass())
            return ast.unparse(parsed)
        except:
            return source_code

    def _analyze_mechanism(self, type_label: str, name: str, source: str, prompt_override: str = None, scope_context: str = "", log_label: str = "General") -> str:
        
        clean_source = self._get_logic_only_source(source)

        main_goal = prompt_override if prompt_override else f"Analyze the PURPOSE and MECHANISM of this {type_label}."
        
        # Combine Source and Context for the TaskExecutor
        # EXPLICIT SEPARATION to prevent Hallucination of Context as Action
        context_data = f"### TARGET CODE (Analyze this strictly)\n{clean_source}\n\n### REFERENCE CONTEXT (Definitions/Globals - DO NOT ANALYZE)\n{scope_context}"
        
        # Use TaskExecutor to Plan-Solve-Refine
        summary = self.task_executor.solve_complex_task(
            main_goal=main_goal,
            context_data=context_data,
            log_label=log_label
        )
        
        return summary if summary else f"{type_label} analysis failed."

    def _synthesize_class_role(self, class_name: str, method_summaries: List[str], clean_source: str = "", log_label: str = "General") -> str:
        methods_block = chr(10).join(method_summaries)
        
        # Verified Pipeline Goal: Simple instruction
        main_goal = f"Summarize the responsibility of Class `{class_name}`. If it has an `__init__`, describe what attributes it initializes. Start directly with the summary."
        
        # We pass the method summaries as the 'Code Context' for the synthesizer
        context_data = f"Class Name: {class_name}\n\nMethod Summaries:\n{methods_block}\n\nCRITICAL: Do not repeat the instruction 'Describe the structural purpose'. Start with the class name or a verb."
        
        # Use TaskExecutor (now with Verified Pipeline)
        summary = self.task_executor.solve_complex_task(
            main_goal=main_goal,
            context_data=context_data,
            log_label=log_label
        )
        
        return summary if summary else f"Class {class_name} role synthesis failed."

    def _add_entry(self, ctx: ModuleContext, name: str, text: str, is_internal: bool, file_path: str):
        display = f"🔒 {name}" if is_internal else f"🔌 {name}"
        ctx.add_public_api_entry(display, text, [Claim(text, name, file_path)])

    def _resolve_dependency_context(self, function_name: str, interactions: List[Dict], dep_contexts: Dict[str, ModuleContext]) -> str:
        context_lines = []
        relevant = [i for i in interactions if i.get('context') == function_name]
        
        for interaction in relevant:
            target_mod = interaction.get('target_module')
            symbol = interaction.get('symbol')
            
            upstream_ctx = None
            for path, ctx in dep_contexts.items():
                if os.path.basename(path) == target_mod:
                    upstream_ctx = ctx
                    break
            
            if upstream_ctx:
                found_symbol = False
                for api_name, grounded_text in upstream_ctx.public_api.items():
                    if symbol in api_name:
                        context_lines.append(f"- Uses `{symbol}` from `{target_mod}`: {grounded_text.text}")
                        found_symbol = True
                        break
                
                if not found_symbol and upstream_ctx.module_role.text:
                    role_text = upstream_ctx.module_role.text
                    # Strip existing "Uses X" prefix from role if present to avoid "Uses X: Uses X"
                    role_text = re.sub(r"^Uses\s+`?" + re.escape(target_mod) + r"`?[:\s]*", "", role_text, flags=re.IGNORECASE).strip()
                    context_lines.append(f"- Uses `{target_mod}`: {role_text}")

        return "\n".join(list(set(context_lines)))