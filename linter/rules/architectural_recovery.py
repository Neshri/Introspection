"""Rule for checking architectural recovery (Rule 0B)."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code


def check_architectural_recovery():
    """
    Diagnose and report architectural contradictions like a package importing its own core identity from a sibling.

    Rule 0B: Before applying standard rules, first diagnose and resolve architectural contradictions like
    a package importing its own core identity from a sibling. Eliminate the source of the contradiction
    (e.g., an incorrect shared directory) before proceeding.
    """
    violations = []

    def get_package_path(filepath):
        """Get the package path for a given file."""
        rel_path = os.path.relpath(filepath, 'AgentTree')
        parts = rel_path.split(os.sep)[:-1]  # Remove filename
        return '.'.join(['AgentTree'] + parts)

    def is_core_identity(module_name, current_package):
        """
        Determine if the imported module represents the core identity of the current package.

        Core identity typically includes main classes, primary functions, or core components
        that define what the package is.
        """
        # Core identity indicators in module names
        core_indicators = ['core', 'main', 'class', 'agent', 'engine', '__init__']

        # If importing from a sibling package that contains core identity
        if module_name.startswith(current_package + '.'):
            imported_parts = module_name[len(current_package)+1:].split('.')
            return any(indicator in imported_parts[0].lower() for indicator in core_indicators)

        return False

    def is_sibling_import(module_name, current_package):
        """Check if the import is from a sibling package."""
        if not module_name.startswith('AgentTree.'):
            return False

        current_parts = current_package.split('.')
        module_parts = module_name.split('.')

        # Must be at the same level (same parent)
        if len(current_parts) < 2 or len(module_parts) < 2:
            return False

        # Same parent directory
        return ('.'.join(current_parts[:-1]) == '.'.join(module_parts[:-1]) and
                current_parts[-1] != module_parts[-1])

    # Walk through all Python files in AgentTree
    for root, dirs, files in os.walk('AgentTree'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                current_package = get_package_path(filepath)

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        source = f.read()
                    tree = ast.parse(source, filepath)
                except (SyntaxError, UnicodeDecodeError):
                    continue  # Skip files with syntax errors or encoding issues

                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        module = node.module
                        if module and module.startswith('AgentTree.'):
                            # Check for sibling import of core identity
                            if (is_sibling_import(module, current_package) and
                                is_core_identity(module, current_package)):
                                names = ', '.join(alias.name for alias in node.names)
                                import_stmt = f"from {module} import {names}"
                                violations.append((
                                    filepath,
                                    import_stmt,
                                    f"Architectural contradiction: Package '{current_package}' "
                                    f"imports core identity from sibling package via '{import_stmt}'. "
                                    "This violates Rule 0B (Architectural Recovery)."
                                ))

    return violations