import os
import re
import libcst as cst
import logging

class CodeEntityVisitor(cst.CSTVisitor):
    def __init__(self, file_path: str, all_project_files: set, module_node: cst.Module):
        self.file_path = file_path
        self.all_project_files = all_project_files
        self.module_dir = os.path.dirname(os.path.abspath(file_path))
        self.module_node = module_node 
        
        self.relative_imports = set()
        self.external_imports = set()
        self.import_map = {}
        self.cross_module_interactions = []
        
        self.entities = {"functions": [], "classes": {}, "globals": []}
        self.current_context = []
        self.header_stack = []
        self.current_statement = None

    def visit_Import(self, node: cst.Import) -> None:
        for alias in node.names:
            module_name = self.module_node.code_for_node(alias.name)
            self.external_imports.add(module_name)

    def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
        if not node.relative:
            if node.module:
                module_name = self.module_node.code_for_node(node.module)
                self.external_imports.add(module_name)
            return

        level = len(node.relative); base_path = self.module_dir
        for _ in range(level - 1): base_path = os.path.dirname(base_path)
        
        module_name_parts = []
        if node.module:
            current = node.module
            while isinstance(current, cst.Attribute):
                module_name_parts.insert(0, current.attr.value)
                current = current.value
            module_name_parts.insert(0, current.value)
        
        module_name_str = ".".join(module_name_parts)
        imported_path_base = os.path.normpath(os.path.join(base_path, module_name_str.replace('.', os.sep)))
        
        potential_file_path = f"{imported_path_base}.py"
        target_file = None

        if potential_file_path in self.all_project_files:
            target_file = potential_file_path
            self.relative_imports.add(target_file)
        elif os.path.isdir(imported_path_base) and isinstance(node.names, (list, tuple)):
            # Fallback for 'from . import module'
            pass

        # FIX 1: Handle Aliases correctly
        if isinstance(node.names, (list, tuple)):
            for name_node in node.names:
                # Determine local name (alias or original)
                local_name = name_node.asname.name.value if name_node.asname else name_node.name.value
                
                if target_file:
                    self.import_map[local_name] = target_file
                elif os.path.isdir(imported_path_base):
                    # Check if the imported name is actually a file in the directory
                    imported_file = os.path.join(imported_path_base, f"{name_node.name.value}.py")
                    if imported_file in self.all_project_files:
                        self.relative_imports.add(imported_file)
                        self.import_map[local_name] = imported_file

    def visit_Assign(self, node: cst.Assign) -> None:
        if len(self.current_context) > 0: return
        for target in node.targets:
            if isinstance(target.target, cst.Name):
                name = target.target.value
                source = self.module_node.code_for_node(node)
                self.entities["globals"].append({
                    "name": name,
                    "source_code": source,
                    "signature": f"{name} = ...",
                    "is_private": name.startswith("_")
                })

    def visit_AnnAssign(self, node: cst.AnnAssign) -> None:
        if len(self.current_context) > 0: return
        if isinstance(node.target, cst.Name):
            name = node.target.value
            source = self.module_node.code_for_node(node)
            self.entities["globals"].append({
                "name": name,
                "source_code": source,
                "signature": f"{name}: {self.module_node.code_for_node(node.annotation.annotation)} = ...",
                "is_private": name.startswith("_")
            })

    def _analyze_function_body(self, node: cst.FunctionDef) -> bool:
        body = node.body
        if isinstance(body, cst.SimpleStatementSuite):
            return any(isinstance(stmt, cst.Pass) for stmt in body.body)
        if isinstance(body, cst.IndentedBlock):
            statements = [stmt for stmt in body.body if not (isinstance(stmt, cst.SimpleStatementLine) and isinstance(stmt.body[0], cst.Expr))]
            if not statements: return False
            if len(statements) == 1:
                stmt = statements[0]
                if isinstance(stmt, cst.SimpleStatementLine) and len(stmt.body) == 1:
                    actual_stmt = stmt.body[0]
                    if isinstance(actual_stmt, cst.Pass): return True
                    
                    # FIX 2: Handle both 'raise NotImplementedError' and 'raise NotImplementedError()'
                    if isinstance(actual_stmt, cst.Raise):
                        exc = actual_stmt.exc
                        # Case A: raise NotImplementedError
                        if isinstance(exc, cst.Name) and exc.value == "NotImplementedError":
                            return True
                        # Case B: raise NotImplementedError(...)
                        if isinstance(exc, cst.Call) and isinstance(exc.func, cst.Name) and exc.func.value == "NotImplementedError":
                            return True
                            
        return False

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        self.current_context.append(node.name.value)
        class_source = self.module_node.code_for_node(node)
        docstring = node.get_docstring()
        
        bases = [self.module_node.code_for_node(b.value) for b in node.bases]
        bases_str = f"({', '.join(bases)})" if bases else ""
        header = f"class {node.name.value}{bases_str}:"
        self.header_stack.append(header)
        
        self.entities["classes"][node.name.value] = {
            "source_code": class_source,
            "docstring": docstring,
            "methods": []
        }

    def leave_ClassDef(self, original_node: cst.ClassDef) -> None:
        self.current_context.pop()
        self.header_stack.pop()

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.current_context.append(node.name.value)
        
        func_source = self.module_node.code_for_node(node)
        params = self.module_node.code_for_node(node.params)
        returns = f" -> {self.module_node.code_for_node(node.returns.annotation)}" if node.returns else ""
        signature = f"def {node.name.value}({params}){returns}:"
        
        self.header_stack.append(signature)
        
        docstring = node.get_docstring()
        is_unimplemented = self._analyze_function_body(node)
        is_private = node.name.value.startswith('_') and not node.name.value.startswith('__')
        
        header = signature
        if docstring:
            header += f'\n    """{docstring}"""'

        component_data = {
            "signature": signature,
            "header": header,
            "docstring": docstring,
            "source_code": func_source,
            "is_unimplemented": is_unimplemented,
            "is_private": is_private,
            # nesting_level: 0 = Top Level, >0 = Nested inside another function
            "nesting_level": len([x for x in self.current_context[:-1] if x not in self.entities["classes"]])
        }

        is_method = len(self.current_context) > 1 and self.current_context[-2] in self.entities["classes"]
        
        if is_method:
            class_name = self.current_context[-2]
            self.entities["classes"][class_name]["methods"].append(component_data)
        else:
            self.entities["functions"].append(component_data)
    
    def leave_FunctionDef(self, original_node: cst.FunctionDef) -> None:
        if self.current_context:
            self.current_context.pop()
        self.header_stack.pop()
        
    def visit_SimpleStatementLine(self, node: cst.SimpleStatementLine) -> None:
        self.current_statement = node

    def leave_SimpleStatementLine(self, original_node: cst.SimpleStatementLine) -> None:
        self.current_statement = None

    def _record_interaction(self, symbol: str, node: cst.CSTNode):
        if symbol in self.import_map:
            target_module_path = self.import_map[symbol]
            context = ".".join(self.current_context) or "module_level"
            
            snippet_str = ""
            if self.current_statement:
                snippet_str = self.module_node.code_for_node(self.current_statement)
            elif self.header_stack:
                snippet_str = self.header_stack[-1]
            else:
                snippet_str = self.module_node.code_for_node(node)
                
            snippet = snippet_str.strip().replace('\n', ' ')
            
            self.cross_module_interactions.append({
                "context": context, 
                "target_module": os.path.basename(target_module_path), 
                "symbol": symbol,
                "snippet": snippet
            })

    def visit_Call(self, node: cst.Call) -> None:
        if isinstance(node.func, cst.Name): self._record_interaction(node.func.value, node)

    def visit_Name(self, node: cst.Name) -> None:
        if self.current_context and self.current_context[-1] == node.value: return
        self._record_interaction(node.value, node)

class GraphAnalyzer:
    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)
        self.project_root = os.path.dirname(self.root_path)
        self.all_project_files = {os.path.join(root, file) for root, _, files in os.walk(self.project_root) for file in files if file.endswith(".py")}
        self.graph = {}
        self.visited = set()

    def analyze(self) -> dict:
        self._build_graph_dfs(self.root_path)
        self._populate_dependents()
        return self.graph

    def _find_todos(self, source_code: str) -> list[str]:
        return re.findall(r'#\s*TODO:?\s*(.*)', source_code)

    def _build_graph_dfs(self, file_path: str):
        abs_path = os.path.abspath(file_path)
        if abs_path in self.visited: return
        self.visited.add(abs_path)
        file_name = os.path.basename(abs_path)
        logging.info(f"[GraphAnalyzer] Statically analyzing: {file_name}")
        try:
            with open(abs_path, 'r', encoding='utf-8') as f: source_code = f.read()
            module_node = cst.parse_module(source_code)
            visitor = CodeEntityVisitor(abs_path, self.all_project_files, module_node)
            module_node.visit(visitor)
            todos = self._find_todos(source_code)
            
            module_docstring = module_node.get_docstring()

            self.graph[abs_path] = {
                "path": abs_path, "file_name": file_name, 
                "source_code": source_code,
                "docstring": module_docstring,
                "dependencies": visitor.relative_imports, "dependents": set(),
                "interactions": visitor.cross_module_interactions,
                "external_imports": visitor.external_imports,
                "entities": visitor.entities, "todos": todos
            }
        except Exception as e:
            logging.error(f"Failed to parse {file_name}: {e}", exc_info=True)
            self.graph[abs_path] = {"path": abs_path, "file_name": file_name, "source_code": "", "dependencies": set(), "dependents": set(), "interactions": [], "external_imports": set(), "entities": {}, "todos": [], "error": str(e)}
        for dep_path in self.graph.get(abs_path, {}).get("dependencies", set()):
            self._build_graph_dfs(dep_path)

    def _populate_dependents(self):
        for path, data in self.graph.items():
            for dep_path in data["dependencies"]:
                if dep_path in self.graph:
                    self.graph[dep_path]["dependents"].add(path)