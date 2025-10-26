"""Rule for checking no cross-graph imports and strictly relative paths."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code


def check_cross_graph_imports(target_files=None):
    """Check for forbidden cross-graph imports and ensure strictly relative paths."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all .py files in evolving_graphs
        files_to_check = []
        for root, dirs, files in os.walk('evolving_graphs'):
            for file in files:
                if file.endswith('.py'):
                    files_to_check.append(os.path.join(root, file))
    else:
        # Single-file mode: only check specified files
        files_to_check = target_files

    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, filepath)
        except (SyntaxError, UnicodeDecodeError):
            continue

        # Get current file's graph (parent directory)
        file_dir = os.path.dirname(filepath)
        current_graph = os.path.basename(file_dir) if file_dir != 'evolving_graphs' else None

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module
                if module is None:
                    continue  # Skip relative imports with no module

                # Check for cross-graph imports
                if module.startswith(('agent_graph.', 'linter_graph.')) or module in ['agent_graph', 'linter_graph']:
                    # This is a cross-graph absolute import
                    names = ', '.join(alias.name for alias in node.names)
                    import_stmt = f"from {module} import {names}"
                    violations.append((
                        filepath,
                        import_stmt,
                        "Graph Decoupling: Direct cross-graph imports are forbidden. Use subprocess execution via entry points."
                    ))

                # Check for upward traversal (..)
                elif node.level >= 2:
                    # level >= 2 means .. or more dots
                    dots = '.' * node.level
                    module_part = f"{dots}{module}" if module else dots
                    names = ', '.join(alias.name for alias in node.names)
                    import_stmt = f"from {module_part} import {names}"
                    violations.append((
                        filepath,
                        import_stmt,
                        "Strictly Relative Paths: No upward traversal (../) allowed in Genome."
                    ))

            # Check for subprocess execution patterns
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr == 'run':
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == 'subprocess':
                        # This is subprocess.run() - check if it's importing cross-graph modules
                        # First, check if this file is importing cross-graph modules before subprocess.run()
                        has_cross_graph_imports = False
                        for prev_node in ast.walk(tree):
                            if isinstance(prev_node, ast.ImportFrom):
                                module = prev_node.module
                                if module and (module.startswith(('agent_graph.', 'linter_graph.')) or module in ['agent_graph', 'linter_graph']):
                                    has_cross_graph_imports = True
                                    break

                        if has_cross_graph_imports:
                            violations.append((
                                filepath,
                                "subprocess.run()",
                                "Graph Decoupling: subprocess.run() not allowed when file imports cross-graph modules."
                            ))
                        # Otherwise, subprocess.run() for external processes is allowed

    return violations