"""Rule for checking import comments."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code

from .linter_utils_core import (  # To check for inline and following comments on imports.
    has_inline_comment,
    has_following_comment,
)


def check_import_comments(target_files=None):
    """Check for missing explanatory comments on specific import statements."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all .py files in agent_tree
        files_to_check = []
        agenttree_dir = 'agent_tree'
        for root, dirs, files in os.walk(agenttree_dir):
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
                except Exception as e:
                    violations.append((filepath, f"Error reading file: {e}"))
                    continue

                lines = source.splitlines()
                try:
                    tree = ast.parse(source, filepath)
                except SyntaxError:
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        # Determine module name correctly
                        if isinstance(node, ast.Import):
                            # import foo, bar - check each alias
                            for alias in node.names:
                                module_name = alias.name.split('.')[0]
                                if module_name in ['agent_tree', 'agent']:
                                    # Get the line where the import is
                                    import_line = lines[node.lineno - 1]
                                    # Check for inline comment on the same line
                                    if not has_inline_comment(import_line):
                                        # Format the import statement
                                        import_str = f"import {', '.join(alias.name for alias in node.names)}"
                                        violations.append((filepath, import_str))
                                        break  # Only report once per import statement
                        else:
                            # from foo import bar
                            module_name = node.module.split('.')[0] if node.module else ''
                            # Check if it's an import starting with 'AgentTree.' or 'agent.'
                            if module_name in ['agent_tree', 'agent']:
                                # Get the line where the import is
                                import_line = lines[node.lineno - 1]
                                # Check for inline comment on the same line
                                if not has_inline_comment(import_line):
                                    # Format the import statement
                                    import_str = f"from {node.module} import {', '.join(alias.name for alias in node.names)}"
                                    violations.append((filepath, import_str))

    return violations