#
# _import_analysis_utils.py (Import Analysis Utilities)
# Utility functions for analyzing and validating Python import statements.
#

import re  # For regex-based import statement validation
from typing import List, Dict, Any  # Type hints for function signatures


def validate_import_statement(line: str, line_number: int) -> List[str]:
    """
    Validates a single import statement for basic syntax and structure.

    Args:
        line: The line containing the import statement
        line_number: The line number for error reporting

    Returns:
        List of error messages, empty if valid
    """
    stripped = line.strip()
    errors = []

    # Basic structure check
    if 'import' not in stripped or (stripped.startswith('from ') and ' import ' not in stripped):
        errors.append(f'Invalid import statement structure on line {line_number}: {stripped}')
        return errors

    # Check for common typos or invalid syntax in import part
    if stripped.startswith('import '):
        import_part = stripped[7:].strip()  # Remove 'import '
        if re.search(r'^[^a-zA-Z_]', import_part):
            errors.append(f'Invalid characters at start of import on line {line_number}: {import_part}')
    elif stripped.startswith('from '):
        # Extract the module part (between 'from ' and ' import ')
        from_match = re.match(r'from\s+([^ ]+)\s+import', stripped)
        if from_match:
            module_part = from_match.group(1)
            if re.search(r'^[^a-zA-Z_.]', module_part):
                errors.append(f'Invalid characters in module name on line {line_number}: {module_part}')
        else:
            errors.append(f'Malformed from-import statement on line {line_number}: {stripped}')

    return errors


def extract_import_info(line: str) -> Dict[str, Any]:
    """
    Extracts structured information from an import statement.

    Args:
        line: The line containing the import statement

    Returns:
        Dictionary with import information or empty dict if not an import
    """
    stripped = line.strip()

    if not (stripped.startswith('import ') or stripped.startswith('from ')):
        return {}

    info = {
        'type': 'absolute_import' if stripped.startswith('import ') else 'relative_import',
        'line': stripped,
        'modules': [],
        'names': []
    }

    if stripped.startswith('import '):
        # Handle absolute imports like "import os, sys"
        import_part = stripped[7:].strip()
        modules = [mod.strip() for mod in import_part.split(',')]
        info['modules'] = modules
        info['names'] = modules  # For absolute imports, names are the modules
    elif stripped.startswith('from '):
        # Handle from imports like "from .module import func1, func2"
        from_match = re.match(r'from\s+([^ ]+)\s+import\s+(.+)', stripped)
        if from_match:
            info['module'] = from_match.group(1)
            names_part = from_match.group(2)
            info['names'] = [name.strip() for name in names_part.split(',')]
            info['level'] = info['module'].count('.') if info['module'].startswith('.') else 0

    return info


def check_import_comment(line: str, next_line: str = "") -> bool:
    """
    Checks if an import statement has a mandatory explanatory comment.

    Args:
        line: The import line
        next_line: The line following the import (if available)

    Returns:
        True if comment is present, False otherwise
    """
    stripped = line.strip()
    if not (stripped.startswith('import ') or stripped.startswith('from ')):
        return True  # Not an import, so no comment required

    # Check current line for comment
    if '#' in line:
        return True

    # Check next line for comment
    if next_line and next_line.strip().startswith('#'):
        return True

    return False


def categorize_imports(import_lines: List[str]) -> Dict[str, List[str]]:
    """
    Categorizes import statements into standard library, third-party, and local imports.

    Args:
        import_lines: List of import statement lines

    Returns:
        Dictionary with categorized imports
    """
    categories = {
        'stdlib': [],
        'third_party': [],
        'local': []
    }

    # Common standard library modules (subset)
    stdlib_modules = {
        'os', 'sys', 'json', 're', 'time', 'datetime', 'collections',
        'typing', 'dataclasses', 'enum', 'ast', 'inspect', 'functools',
        'itertools', 'pathlib', 'tempfile', 'subprocess', 'threading',
        'multiprocessing', 'logging', 'unittest', 'doctest'
    }

    for line in import_lines:
        info = extract_import_info(line)
        if not info:
            continue

        if info['type'] == 'absolute_import':
            module = info['modules'][0].split('.')[0] if info['modules'] else ''
        else:
            module = info.get('module', '').lstrip('.').split('.')[0]

        if module in stdlib_modules:
            categories['stdlib'].append(line)
        elif module and not module.startswith('.'):
            categories['third_party'].append(line)
        else:
            categories['local'].append(line)

    return categories