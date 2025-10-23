"""Rule for checking import compliance."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code
import logging  # for diagnostic logging

def is_external_package(module_name):
    """Check if a module is an external package (not part of AgentTree source code)."""
    return not (module_name.startswith('agent.') or module_name.startswith('AgentTree.'))


from ..utils import is_standard_library  # shared utility function


def check_imports_compliance():
    """Check import compliance rules and controlled API exposure."""
    violations = []
    logger = logging.getLogger(__name__)

    # Special handling for root __init__.py to ensure single entry-point
    root_init_path = os.path.join('AgentTree', '__init__.py')
    if os.path.exists(root_init_path):
        try:
            with open(root_init_path, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, root_init_path)

            # Extract __all__ list to check for single entry-point
            all_exports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == '__all__':
                            if isinstance(node.value, ast.List):
                                all_exports = [elt.s for elt in node.value.elts if isinstance(elt, ast.Str)]
                            elif isinstance(node.value, ast.List) and all(isinstance(elt, ast.Constant) for elt in node.value.elts):
                                all_exports = [elt.value for elt in node.value.elts if isinstance(elt.value, str)]
                            break

            if len(all_exports) != 1:
                violations.append((root_init_path, f"__all__ = {all_exports}", "Root __init__.py must expose exactly one primary entry-point class"))
            else:
                logger.info(f"Root __init__.py correctly exposes single entry-point: {all_exports[0]}")

        except (SyntaxError, UnicodeDecodeError):
            violations.append((root_init_path, "parse error", "Unable to parse root __init__.py for entry-point validation"))

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
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            name = alias.name
                            # Exemption for external packages: skip import compliance checks
                            # to avoid false positives from third-party libraries
                            if is_external_package(name):
                                logger.debug(f"Skipping external package '{name}' in {filepath}")
                                continue
                            if is_init:
                                if not name.startswith('.'):
                                    violations.append((filepath, f"import {name}", "Absolute import in __init__.py"))
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module
                        if module is None:
                            continue  # Skip relative imports with no module (syntax like 'from . import ...')
                        names = ', '.join(alias.name for alias in node.names)
                        import_stmt = f"from {'.' * node.level}{module} import {names}"
                        # Exemption for external packages: skip import compliance checks
                        # to avoid false positives from third-party libraries
                        if is_external_package(module):
                            logger.debug(f"Skipping external package '{module}' in {filepath}")
                            continue
                        if node.level >= 2:
                            violations.append((filepath, import_stmt, "Forbidden .. import syntax"))
                        if is_init:
                            if node.level == 0:
                                violations.append((filepath, import_stmt, "Absolute import in __init__.py"))
                        else:
                            if node.level > 0:
                                violations.append((filepath, import_stmt, "Relative import in non-__init__.py file"))
                            elif module.startswith('agent.') or module.startswith('AgentTree.'):
                                dots = module.count('.')
                                if dots > 1:
                                    violations.append((filepath, import_stmt, "Deep import path (imports must be from the shallowest possible package)"))
    return violations