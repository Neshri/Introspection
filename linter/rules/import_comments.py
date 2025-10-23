"""Rule for checking import comments."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code

from ..utils import (  # shared utility functions
    has_inline_comment,
    has_following_comment,
)


def check_import_comments():
    """Check for missing explanatory comments on specific import statements."""
    agenttree_dir = 'AgentTree'
    violations = []
    for root, dirs, files in os.walk(agenttree_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
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
                        # Determine module name
                        if isinstance(node, ast.Import):
                            # import foo, bar
                            for alias in node.names:
                                module_name = alias.name.split('.')[0]
                        else:
                            # from foo import bar
                            module_name = node.module.split('.')[0] if node.module else ''

                        # Check if it's an import starting with 'AgentTree.' or 'agent.'
                        if module_name and (module_name.startswith('AgentTree.') or module_name.startswith('agent.')):
                            # Get the line where the import is
                            import_line = lines[node.lineno - 1]
                            # Check for inline comment on the same line
                            if not has_inline_comment(import_line):
                                # Format the import statement
                                if isinstance(node, ast.Import):
                                    import_str = f"import {', '.join(alias.name for alias in node.names)}"
                                else:
                                    import_str = f"from {node.module} import {', '.join(alias.name for alias in node.names)}"
                                violations.append((filepath, import_str))

    return violations