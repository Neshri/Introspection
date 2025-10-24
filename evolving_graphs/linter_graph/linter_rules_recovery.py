"""Rule for checking architectural recovery (Rule 0B)."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code


def check_architectural_recovery(target_files=None):
    """
    Diagnose and report architectural contradictions in flat architecture.

    In flat architecture, no sub-directories exist, so architectural contradictions
    are limited to improper module naming or direct circular imports that violate
    semantic naming principles.
    """
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all .py files in agent_tree
        files_to_check = []
        base_dir = 'agent_tree'
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    files_to_check.append(os.path.join(root, file))
    else:
        # Single-file mode: only check specified files
        files_to_check = target_files

    # Since architecture is now flat, check for improper module naming patterns
    # that might indicate architectural confusion

    for filepath in files_to_check:
        file = os.path.basename(filepath)
        module_name = file[:-3]  # Remove .py extension

        # Check for non-semantic naming (violates semantic naming rule)
        if '_' not in module_name and len(module_name) < 10:
            # Likely violates semantic naming: domain_responsibility pattern
            violations.append((
                filepath,
                module_name,
                f"Module '{module_name}' violates semantic naming rule. "
                "Use domain_responsibility.py pattern (e.g., agent_executor.py, user_model.py)."
            ))

        # Check for circular imports within flat structure
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, filepath)
        except (SyntaxError, UnicodeDecodeError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module
                if module and module.startswith('agent_tree.'):
                    # In flat architecture, imports should be simple relative
                    # Any AgentTree.* import indicates potential architectural confusion
                    names = ', '.join(alias.name for alias in node.names)
                    import_stmt = f"from {module} import {names}"
                    violations.append((
                        filepath,
                        import_stmt,
                        f"Architectural contradiction in flat structure: '{import_stmt}' "
                        "should be a simple relative import (from .module_name)."
                    ))

    return violations