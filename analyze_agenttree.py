import os
import json
import re

def analyze_agenttree():
    base_dir = os.path.join(os.path.dirname(__file__), 'AgentTree')

    file_sizes = {}
    import_comments = []
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

        # Analyze each .py file
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.relpath(os.path.join(root, file), os.path.dirname(__file__))
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    line_count = len(lines)
                    violation_lines = line_count > 300

                    file_sizes[file_path] = {
                        "lines": line_count,
                        "violation": violation_lines
                    }

                    # Check imports
                    for i, line in enumerate(lines, 1):
                        stripped = line.strip()
                        # Check if it's a custom import: from AgentTree.xxx, from .xxx, from ..xxx, or import AgentTree.xxx
                        is_custom = False
                        if re.match(r'from (AgentTree\.|\.|\.\.)', stripped):
                            is_custom = True
                        elif re.match(r'import AgentTree\.', stripped):
                            is_custom = True
                        if is_custom:
                            # Check for comment after import statement starting with #
                            parts = line.split('#', 1)
                            has_comment = len(parts) > 1 and parts[1].strip()
                            import_comments.append({
                                "file": file_path,
                                "line": i,
                                "import": stripped,
                                "has_comment": has_comment
                            })

    # Output JSON
    report = {
        "file_sizes": file_sizes,
        "import_comments": import_comments,
        "directories": directories
    }
    print(json.dumps(report, indent=4))

if __name__ == "__main__":
    analyze_agenttree()