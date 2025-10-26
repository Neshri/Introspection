"""Rule for checking code duplication."""

import os  # filesystem operations
from collections import defaultdict  # default dictionary factory

try:
    from .linter_utils_core import is_boilerplate, is_import_or_comment  # To identify boilerplate and import/comment lines.
except ImportError:
    # Fallback for standalone execution
    from linter_utils_core import is_boilerplate, is_import_or_comment


def check_duplication(target_files=None):
    """Detect potential code duplication in contiguous blocks."""
    violations = []
    blocks = defaultdict(list)  # signature -> list of (file, start_line, indent)

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all .py files in evolving_graphs
        files_to_check = []
        agenttree_dir = 'evolving_graphs'
        for root, dirs, files in os.walk(agenttree_dir):
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
                    current_block = []
                    current_indent = None
                    current_start_line = None
                    for line_num, line in enumerate(lines, 1):
                        stripped = line.strip()
                        if is_import_or_comment(line) or is_boilerplate(line) or stripped == '':
                            if current_block:
                                if len(current_block) >= 5:
                                    signature = (current_indent, tuple(current_block))
                                    blocks[signature].append((filepath, current_start_line, current_indent))
                                current_block = []
                                current_indent = None
                                current_start_line = None
                            continue
                        indent = len(line) - len(line.lstrip())
                        if current_indent is None or indent != current_indent:
                            if current_block:
                                if len(current_block) >= 5:
                                    signature = (current_indent, tuple(current_block))
                                    blocks[signature].append((filepath, current_start_line, current_indent))
                            current_block = [stripped]
                            current_indent = indent
                            current_start_line = line_num
                        else:
                            current_block.append(stripped)
                    # Process the last block if it exists
                    if current_block and len(current_block) >= 5:
                        signature = (current_indent, tuple(current_block))
                        blocks[signature].append((filepath, current_start_line, current_indent))
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    # Identify duplications across multiple files
    for signature, occurrences in blocks.items():
        if len(occurrences) >= 2:
            indent, block_lines = signature
            unique_files = set(f for f, s, i in occurrences)
            for file, start_line, _ in occurrences:
                other_files = unique_files - {file}
                message = f"Code duplication detected: block of {len(block_lines)} lines at indentation level {indent} also found in files: {', '.join(other_files)}"
                violations.append({'file': file, 'line': start_line, 'message': message})

    return violations