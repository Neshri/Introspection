"""Rule for checking empty __init__.py files."""

import os  # filesystem operations


def check_init_files(target_files=None):
    """Check that all __init__.py files are empty."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all __init__.py files in evolving_graphs
        files_to_check = []
        for root, dirs, files in os.walk('evolving_graphs'):
            for file in files:
                if file == '__init__.py':
                    files_to_check.append(os.path.join(root, file))
    else:
        # Single-file mode: only check specified files if they are __init__.py
        files_to_check = [f for f in target_files if os.path.basename(f) == '__init__.py']

    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    violations.append((
                        filepath,
                        content,
                        "Empty __init__.py: All __init__.py files must be empty."
                    ))
        except Exception as e:
            violations.append((filepath, f"Error: {e}", ""))

    return violations