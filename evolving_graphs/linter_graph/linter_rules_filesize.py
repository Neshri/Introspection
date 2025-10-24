"""Rule for checking file sizes."""

import os  # filesystem operations

from .linter_utils_core import count_code_lines  # To count non-comment, non-empty lines of code.


def check_file_sizes(target_files=None):
    """Check file sizes against the 300 line limit, excluding comment lines."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all .py files in agent_tree
        files_to_check = []
        base_dir = 'agent_tree'
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.py'):
                    files_to_check.append(os.path.join(root, file))
    else:
        # Single-file mode: only check specified files
        files_to_check = target_files

    for filepath in files_to_check:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # Strip trailing empty lines first
                        while lines and lines[-1].strip() == '':
                            lines.pop()
                        # Count lines of code, excluding comments
                        count = count_code_lines(lines)
                        if count > 300:
                            violations.append((filepath, count, "OVER LIMIT"))
                        elif 250 <= count <= 299:
                            violations.append((filepath, count, "APPROACHING LIMIT"))
                except Exception as e:
                    violations.append((filepath, f"Error: {e}", ""))
    return violations