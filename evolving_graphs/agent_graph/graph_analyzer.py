import os
import re
import libcst
import logging

class CodeEntityVisitor(libcst.CSTVisitor):
    def __init__(self, file_path: str, all_project_files: set, module_node: libcst.Module):
        self.file_path = file_path
        self.all_project_files = all_project_files
        self.module_dir = os.path.dirname(os.path.abspath(file_path))
        self.module_node = module_node # Keep a reference to the root module node
        
        self.relative_imports = set()
        self.external_imports = set()
        self.import_map = {}
        self.cross_module_interactions = []
        self.entities = {"functions": [], "classes": {}}
        self.current_context = []

    def visit_Import(self, node: libcst.Import) -> None:
        for alias in node.names:
            module_name = self.module_node.code_for_node(alias.name)
            self.external_imports.add(module_name)

    def visit_ImportFrom(self, node: libcst.ImportFrom) -> None:
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
            while isinstance(current, libcst.Attribute):
                module_name_parts.insert(0, current.attr.value)
                current = current.value
            module_name_parts.insert(0, current.value)
        
        module_name_str = ".".join(module_name_parts)
        imported_path_base = os.path.normpath(os.path.join(base_path, module_name_str.replace('.', os.sep)))
        
        potential_file_path = f"{imported_path_base}.py"
        if potential_file_path in self.all_project_files:
            self.relative_imports.add(potential_file_path)
            if isinstance(node.names, (list, tuple)):
                for name_node in node.names: self.import_map[name_node.name.value] = potential_file_path
        elif os.path.isdir(imported_path_base) and isinstance(node.names, (list, tuple)):
            for name_node in node.names:
                imported_file = os.path.join(imported_path_base, f"{name_node.name.value}.py")
                if imported_file in self.all_project_files:
                    self.relative_imports.add(imported_file); self.import_map[name_node.name.value] = imported_file

        
    def _analyze_function_body(self, node: libcst.FunctionDef) -> bool:
        body = node.body
        if isinstance(body, libcst.SimpleStatementSuite):
            return any(isinstance(stmt, libcst.Pass) for stmt in body.body)
        
        if isinstance(body, libcst.IndentedBlock):
            statements = [stmt for stmt in body.body if not (isinstance(stmt, libcst.SimpleStatementLine) and isinstance(stmt.body[0], libcst.Expr))]
            if not statements: return False
            if len(statements) == 1:
                stmt = statements[0]
                if isinstance(stmt, libcst.SimpleStatementLine) and len(stmt.body) == 1:
                    actual_stmt = stmt.body[0]
                    if isinstance(actual_stmt, libcst.Pass): return True
                    if isinstance(actual_stmt, libcst.Raise) and isinstance(actual_stmt.exc, libcst.Name) and actual_stmt.exc.value == "NotImplementedError":
                        return True
        return False

    def visit_ClassDef(self, node: libcst.ClassDef) -> None:
        self.current_context.append(node.name.value)
        # CORRECTED: Use the official libcst method to get the source code for the node.
        class_source = self.module_node.code_for_node(node)
        self.entities["classes"][node.name.value] = {
            "source_code": class_source,
            "methods": []
        }

    def leave_ClassDef(self, original_node: libcst.ClassDef) -> None:
        self.current_context.pop()

    def visit_FunctionDef(self, node: libcst.FunctionDef) -> None:
        self.current_context.append(node.name.value)
        
        # CORRECTED: Use the official libcst method to get the source code.
        func_source = self.module_node.code_for_node(node)
        params = self.module_node.code_for_node(node.params)
        returns = f" -> {self.module_node.code_for_node(node.returns.annotation)}" if node.returns else ""
        signature = f"def {node.name.value}({params}){returns}:"
        is_unimplemented = self._analyze_function_body(node)
        
        component_data = {
            "signature": signature,
            "source_code": func_source,
            "is_unimplemented": is_unimplemented
        }

        is_method = len(self.current_context) > 1 and self.current_context[-2] in self.entities["classes"]
        is_private = node.name.value.startswith('_')

        if not is_private:
            if is_method:
                class_name = self.current_context[-2]
                self.entities["classes"][class_name]["methods"].append(component_data)
            else:
                self.entities["functions"].append(component_data)
    
    def leave_FunctionDef(self, original_node: libcst.FunctionDef) -> None:
        if self.current_context:
            self.current_context.pop()
        
    def _record_interaction(self, symbol: str):
        if symbol in self.import_map:
            target_module_path = self.import_map[symbol]
            context = ".".join(self.current_context) or "module_level"
            self.cross_module_interactions.append({"context": context, "target_module": os.path.basename(target_module_path), "symbol": symbol})

    def visit_Call(self, node: libcst.Call) -> None:
        if isinstance(node.func, libcst.Name): self._record_interaction(node.func.value)

    def visit_Name(self, node: libcst.Name) -> None:
        if self.current_context and self.current_context[-1] == node.value: return
        self._record_interaction(node.value)

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
            module_node = libcst.parse_module(source_code)
            visitor = CodeEntityVisitor(abs_path, self.all_project_files, module_node)
            module_node.visit(visitor)
            todos = self._find_todos(source_code)
            self.graph[abs_path] = {
                "path": abs_path, "file_name": file_name, "source_code": source_code,
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