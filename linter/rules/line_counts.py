"""Rule for analyzing line counts."""

import os  # filesystem operations


def analyze_lines_count():
    """Analyze total line counts in Python files."""
    directory = 'AgentTree'
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                    results.append((path, lines))
                except Exception as e:
                    results.append((path, f"Error: {e}"))

    # Sort by line count descending
    results.sort(key=lambda x: x[1] if isinstance(x[1], int) else 0, reverse=True)
    return results