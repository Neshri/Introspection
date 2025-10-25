"""Rule for checking file sizes."""

import os  # filesystem operations

try:
    from .linter_utils_core import count_code_lines  # To count non-comment, non-empty lines of code.
except ImportError:
    # Fallback for standalone execution
    from linter_utils_core import count_code_lines  # To count non-comment, non-empty lines of code.


def count_tokens(content):
    """Count tokens using tiktoken if available, otherwise approximate."""
    try:
        import tiktoken  # For token counting
        encoder = tiktoken.get_encoding("o200k_base")
        return len(encoder.encode(content))
    except ImportError:
        # Fallback to approximate token count (1 token ≈ 4 chars)
        return len(content) // 4


def check_file_sizes(target_files=None):
    """Check file sizes against the 3,000 token limit using tiktoken."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all .py files in evolving_graphs
        files_to_check = []
        base_dir = 'evolving_graphs'
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
                         content = f.read()
                         # Count tokens
                         count = count_tokens(content)
                         if count > 3000:
                             violations.append((filepath, count, "OVER LIMIT"))
                         elif 2500 <= count <= 2999:
                             violations.append((filepath, count, "APPROACHING LIMIT"))
                 except Exception as e:
                     violations.append((filepath, f"Error: {e}", ""))
    return violations