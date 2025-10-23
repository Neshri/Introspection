"""Rule for checking file sizes."""

import os  # filesystem operations

from ..utils import count_code_lines  # shared utility function


def check_file_sizes():
    """Check file sizes against the 300 line limit, excluding comment lines."""
    violations = []
    base_dir = 'AgentTree'
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
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