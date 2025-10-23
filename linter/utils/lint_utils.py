"""Utility functions for the linter package."""

import sys  # system-specific parameters and functions


def is_standard_library(module_name):
    """Check if a module is part of the standard library."""
    if module_name in sys.stdlib_module_names:
        return True
    # Handle submodules (e.g., os.path)
    parts = module_name.split('.')
    return any(part in sys.stdlib_module_names for part in parts)


def has_inline_comment(line):
    """Check if a line has an explanatory comment after the code."""
    stripped = line.strip()
    if '#' in stripped:
        code_part = stripped.split('#')[0].strip()
        comment_part = stripped.split('#', 1)[1].strip()
        # Check if there's code before the comment and comment is not empty
        return bool(code_part) and bool(comment_part)
    return False


def has_following_comment(lines, end_lineno):
    """Check if there's an explanatory comment immediately following the import."""
    if end_lineno >= len(lines):
        return False
    # Check the line right after the import
    line = lines[end_lineno].strip()
    if line.startswith('#'):
        return True
    return False


def is_import_or_comment(line):
    """Check if a line is an import statement or comment."""
    stripped = line.strip()
    return stripped.startswith('#') or stripped.startswith('import ') or stripped.startswith('from ')


def count_code_lines(lines):
    """Count lines of code, excluding comments and empty lines."""
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            count += 1
    return count