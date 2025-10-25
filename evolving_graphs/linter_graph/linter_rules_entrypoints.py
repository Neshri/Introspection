"""Rule for checking designated entry points ([context]_main.py)."""

import os  # filesystem operations


def check_entry_points(target_files=None):
    """Check that each graph has a designated entry point ([context]_main.py)."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all files in evolving_graphs
        files_to_check = []
        for root, dirs, files in os.walk('evolving_graphs'):
            for file in files:
                if file.endswith('.py'):
                    files_to_check.append(os.path.join(root, file))
    else:
        # Single-file mode: only check specified files
        files_to_check = target_files

    # Find all graphs (directories under evolving_graphs that contain potential entry points)
    graphs = []
    for item in os.listdir('evolving_graphs'):
        path = os.path.join('evolving_graphs', item)
        if os.path.isdir(path) and not item.startswith('.') and item != '__pycache__':
            # Only consider directories that contain at least one .py file (potential entry points)
            has_py_files = False
            for sub_item in os.listdir(path):
                if sub_item.endswith('.py'):
                    has_py_files = True
                    break
            if has_py_files:
                graphs.append(item)

    # Check each graph has an entry point
    for graph in graphs:
        graph_path = os.path.join('evolving_graphs', graph)
        entry_point = f"{graph}_main.py"
        entry_point_path = os.path.join(graph_path, entry_point)

        if not os.path.exists(entry_point_path):
            violations.append((
                graph_path,
                entry_point,
                f"Designated Entry Points: Graph '{graph}' must have entry point '{entry_point}'."
            ))

    # Check that entry points are actually in the files being scanned
    entry_points_found = []
    for filepath in files_to_check:
        filename = os.path.basename(filepath)
        if filename.endswith('_main.py'):
            # Verify it matches the graph name
            dirname = os.path.basename(os.path.dirname(filepath))
            expected_name = f"{dirname}_main.py"
            if filename != expected_name:
                violations.append((
                    filepath,
                    filename,
                    f"Entry point name mismatch: expected '{expected_name}', found '{filename}'."
                ))
            else:
                entry_points_found.append(dirname)

    return violations