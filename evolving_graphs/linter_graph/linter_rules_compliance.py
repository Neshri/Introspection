"""Rule for final compliance check (Rule: The Final Compliance Check)."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code


def check_final_compliance(target_files=None):
    """
    Perform final compliance check on changed files to ensure all import statements comply with rules.

    The Final Compliance Check: Before completing any task, re-read every file you have changed
    and verify that every single import statement fully complies with these rules.
    """
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
                # Check for .. imports using level
                if node.level > 1:  # level > 1 means .. or more dots
                    # Reconstruct the import statement with dots
                    dots = '.' * node.level
                    module_part = f"{dots}{node.module}" if node.module else dots
                    names = ', '.join(alias.name for alias in node.names)
                    import_stmt = f"from {module_part} import {names}"
                    file_violations.append((
                        filepath,
                        import_stmt,
                        "Forbidden .. import syntax - no parent directories in flat architecture"
                    ))
                elif node.level == 0 and node.module and (node.module.startswith('agent.') or node.module.startswith('agent_tree.')):
                    # Check for absolute imports of project modules
                    names = ', '.join(alias.name for alias in node.names)
                    import_stmt = f"from {node.module} import {names}"
                    file_violations.append((
                        filepath,
                        import_stmt,
                        "Forbidden absolute import of project modules - use relative imports only"
                    ))
                elif node.module and (node.module.startswith('agent.') or node.module.startswith('agent_tree.')):
                    # Check for import comment on project modules (relative imports only)
                    if not has_import_comment(node, source):
                        names = ', '.join(alias.name for alias in node.names)
                        import_stmt = f"from {node.module} import {names}"
                        file_violations.append((
                            filepath,
                            import_stmt,
                            "Missing explanatory comment on Project Module import"
                        ))
        return file_violations

    def has_import_comment(node, source):
        """Check if an ImportFrom node has a comment on the same line."""
        lines = source.splitlines()
        if node.lineno - 1 < len(lines):
            line = lines[node.lineno - 1]
            # Check if there's a '#' in the line (comment indicator)
            return '#' in line
        return False

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

    for filepath in files_to_check:
        if os.path.exists(filepath) and filepath.endswith('.py'):
            file_violations = check_file_imports(filepath)
            violations.extend(file_violations)

    return violations