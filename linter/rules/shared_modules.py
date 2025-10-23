"""Rule for checking shared module placement."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code
from collections import defaultdict  # default dictionary factory

from ..utils import is_standard_library  # shared utility function


def check_shared_module_placement():
    """Analyze import usage and verify modules shared by sibling directories are in the immediate parent directory."""
    violations = []
    base_dir = 'AgentTree'

    # Collect all imports per file
    file_imports = {}
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        source = f.read()
                    tree = ast.parse(source, filepath)
                    imports = []
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports.append(alias.name.split('.')[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imports.append(node.module.split('.')[0])
                    file_imports[filepath] = set(imports)
                except (SyntaxError, UnicodeDecodeError):
                    continue

    # Analyze shared modules
    # Group files by their parent directory
    parent_dirs = {}
    for filepath in file_imports:
        rel_path = os.path.relpath(filepath, base_dir)
        parts = rel_path.split(os.sep)
        if len(parts) > 2:  # Only consider files in subdirectories
            parent = os.sep.join(parts[:-1])
            if parent not in parent_dirs:
                parent_dirs[parent] = []
            parent_dirs[parent].append(filepath)

    # For each parent directory, check modules imported by multiple siblings
    for parent, files in parent_dirs.items():
        if len(files) > 1:  # Only if there are siblings
            module_usage = defaultdict(set)
            for file in files:
                for mod in file_imports[file]:
                    if not is_standard_library(mod) and not mod.startswith('.'):
                        module_usage[mod].add(file)

            # Find modules used by multiple files
            shared_modules = {mod: file_list for mod, file_list in module_usage.items() if len(file_list) > 1}

            # Check if shared modules are in the immediate parent directory
            parent_path = os.path.join(base_dir, parent)
            for mod, files_using in shared_modules.items():
                mod_file = os.path.join(parent_path, f'{mod}.py')
                if not os.path.exists(mod_file):
                    violations.append((parent_path, mod, list(files_using)))

    return violations