"""
intelligence_import_utils.py - Import analysis utilities for project scouting.

Provides functions for extracting imported modules from Python code using AST parsing.
"""

import ast  # Abstract syntax tree parsing for code analysis
import os  # File system operations for path handling


def extract_imported_modules(code, current_path, all_modules):
    """
    Extract imported modules from Python code using AST parsing.

    Args:
        code (str): The Python code to analyze
        current_path (str): Path to the current file being analyzed
        all_modules (dict): Dictionary of all available modules in the project

    Returns:
        list: List of tuples (module_name, import_reason)
    """
    # Get relative path information
    current_rel_path = os.path.relpath(current_path, os.path.dirname(current_path))
    current_module = current_rel_path.replace(os.sep, '.').replace('.py', '')
    current_package_parts = current_module.split('.')[:-1]

    imported = set()
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    level = node.level if hasattr(node, 'level') and node.level else 0
                    mod_name = node.module
                    if level == 0:
                        possible = [mod_name, mod_name.split('.')[-1]]
                    elif level == 1:
                        possible = ['.'.join(current_package_parts + [mod_name]), mod_name]
                    elif level == 2:
                        parent_parts = current_package_parts[:-1] if len(current_package_parts) > 0 else []
                        possible = ['.'.join(parent_parts + [mod_name]), mod_name]
                    else:
                        possible = [mod_name]
                    for p in possible:
                        if p in all_modules:
                            imported.add((p, f"imported {node.module}"))
                            break
    except Exception:
        # Return empty list on parsing error
        pass
    return list(imported)


def extract_elements(tree):
    """
    Extract function and class names from an AST tree.

    Args:
        tree (ast.AST): The parsed AST tree

    Returns:
        list: List of extracted element names
    """
    elements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            elements.append(node.name)
        elif isinstance(node, ast.ClassDef):
            elements.append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                elements.append(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                elements.append(node.module.split('.')[0])
            for alias in node.names:
                elements.append(alias.name)
    return elements