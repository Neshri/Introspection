"""Rule for checking import compliance."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code

from ..utils import is_standard_library  # shared utility function


def check_imports_compliance():
    """Check import compliance rules and controlled API exposure."""
    violations = []
    for root, dirs, files in os.walk('AgentTree'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        source = f.read()
                    tree = ast.parse(source, filepath)
                except (SyntaxError, UnicodeDecodeError):
                    continue  # Skip files with syntax errors or encoding issues
                is_init = file == '__init__.py'
                is_root_init = filepath == os.path.join('AgentTree', '__init__.py')
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            name = alias.name
                            if is_init:
                                if not name.startswith('.'):
                                    violations.append((filepath, f"import {name}", "Absolute import in __init__.py"))
                            # Check root __init__.py for single entry-point
                            if is_root_init and not is_standard_library(name):
                                violations.append((filepath, f"import {name}", "Root __init__.py should only expose a single entry-point"))
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module
                        names = ', '.join(alias.name for alias in node.names)
                        import_stmt = f"from {module if module is not None else '.'} import {names}"
                        if module and module.startswith('..'):
                            violations.append((filepath, import_stmt, "Forbidden .. import syntax"))
                        if is_init:
                            if module is not None and not module.startswith('.'):
                                violations.append((filepath, import_stmt, "Non-relative import in __init__.py"))
                        else:
                            if module is None or (module is not None and module.startswith('.')):
                                violations.append((filepath, import_stmt, "Relative import in non-__init__.py file"))
                            elif module and (module.startswith('agent.') or module.startswith('AgentTree.')):
                                dots = module.count('.')
                                if dots > 1:
                                    violations.append((filepath, import_stmt, "Deep import path (imports must be from the shallowest possible package)"))
                                # Additional check for external absolute imports targeting shallowest package
                                elif not module.startswith('.'):
                                    # This is an external absolute import, ensure it's shallow
                                    if dots > 0:  # More than just 'agent' or 'AgentTree'
                                        violations.append((filepath, import_stmt, "External absolute imports must target the shallowest possible package"))
    return violations