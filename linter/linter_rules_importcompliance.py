"""Rule for checking import compliance."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code


def check_imports_compliance(target_files=None):
    """Check import compliance rules for flat architecture."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all .py files in agent_tree
        files_to_check = []
        for root, dirs, files in os.walk('agent_tree'):
            for file in files:
                if file.endswith('.py'):
                    files_to_check.append(os.path.join(root, file))
    else:
        # Single-file mode: only check specified files
        files_to_check = target_files

    # In flat architecture, we only check for proper relative imports
    # No deep import paths or hierarchical package structures

    for filepath in files_to_check:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        source = f.read()
                    tree = ast.parse(source, filepath)
                except (SyntaxError, UnicodeDecodeError):
                    continue  # Skip files with syntax errors or encoding issues

                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        module = node.module
                        if module is None:
                            continue  # Skip relative imports with no module (syntax like 'from . import ...')

                        names = ', '.join(alias.name for alias in node.names)
                        import_stmt = f"from {'.' * node.level}{module} import {names}"

                        # In flat architecture, imports should be simple and direct
                        if node.level >= 2:
                            violations.append((filepath, import_stmt, "Forbidden .. import syntax - no parent directories in flat architecture"))
                        elif node.level == 0 and (module.startswith('agent.') or module.startswith('agent_tree.')):
                            violations.append((filepath, import_stmt, "Forbidden absolute import of project modules - use relative imports only"))
                        elif node.level > 1:
                            violations.append((filepath, import_stmt, "Deep import path not allowed in flat architecture"))
    return violations