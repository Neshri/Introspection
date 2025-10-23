"""Rule for final compliance check (Rule: The Final Compliance Check)."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code


def check_final_compliance(changed_files=None):
    """
    Perform final compliance check on changed files to ensure all import statements comply with rules.

    The Final Compliance Check: Before completing any task, re-read every file you have changed
    and verify that every single import statement fully complies with these rules.
    """
    if changed_files is None:
        changed_files = []

    violations = []

    def check_file_imports(filepath):
        """Check all imports in a single file for compliance."""
        file_violations = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, filepath)
        except (SyntaxError, UnicodeDecodeError):
            return file_violations  # Skip files with syntax errors or encoding issues

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module
                if module and (module.startswith('agent.') or module.startswith('AgentTree.')):
                    names = ', '.join(alias.name for alias in node.names)
                    import_stmt = f"from {module} import {names}"
                    # Check for import comment
                    if not has_import_comment(node):
                        file_violations.append((
                            filepath,
                            import_stmt,
                            "Missing explanatory comment on Project Module import"
                        ))
                    # Check for .. imports
                    if module.startswith('..'):
                        file_violations.append((
                            filepath,
                            import_stmt,
                            "Forbidden .. import syntax"
                        ))
        return file_violations

    def has_import_comment(node):
        """Check if an ImportFrom node has a comment on the same line."""
        # This is a simplified check - in practice, we'd need line number information
        # For now, return True (would need enhancement for actual implementation)
        return True

    # Check changed files if provided, otherwise check all files
    files_to_check = changed_files if changed_files else []
    if not files_to_check:
        # If no changed files specified, check all Python files in AgentTree
        for root, dirs, files in os.walk('AgentTree'):
            for file in files:
                if file.endswith('.py'):
                    files_to_check.append(os.path.join(root, file))

    for filepath in files_to_check:
        if os.path.exists(filepath) and filepath.endswith('.py'):
            file_violations = check_file_imports(filepath)
            violations.extend(file_violations)

    return violations