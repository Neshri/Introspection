"""Rule for analyzing directory structure."""

import os  # filesystem operations


def analyze_directory_structure():
    """Analyze directory structure for cohesion violations."""
    base_dir = 'AgentTree'
    directories = {}

    # Walk through all directories and files
    for root, dirs, files in os.walk(base_dir):
        dir_path = os.path.relpath(root, os.path.dirname(__file__))
        py_files = [f for f in files if f.endswith('.py') and f != '__init__.py']
        file_count = len(py_files)
        violation = file_count > 7

        directories[dir_path] = {
            "file_count": file_count,
            "files": py_files,
            "violation": violation
        }
    return directories