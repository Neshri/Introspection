"""Rule for checking code duplication."""

import os  # filesystem operations
from collections import defaultdict  # default dictionary factory

from ..utils import is_import_or_comment  # shared utility function


def check_duplication():
    """Detect potential code duplication."""
    agenttree_dir = 'AgentTree'
    line_to_files = defaultdict(list)

    # Walk through all Python files in AgentTree recursively
    for root, dirs, files in os.walk(agenttree_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if not is_import_or_comment(line):
                                stripped_line = line.strip()
                                if stripped_line:  # Skip empty lines
                                    line_to_files[stripped_line].append(filepath)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    # Find lines in 3 or more files
    duplications = {line: files for line, files in line_to_files.items() if len(files) >= 3}
    return duplications