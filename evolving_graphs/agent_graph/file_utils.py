"""
file_utils.py - Common file operations utilities.

Provides standardized functions for reading files, handling encoding,
and file system operations used across the agent graph.
"""

import os
import logging


def read_file_safely(file_path: str, encoding: str = 'utf-8') -> tuple[bool, str]:
    """
    Safely read a file with error handling.

    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)

    Returns:
        tuple: (success, content_or_error)
    """
    try:
        if not os.path.exists(file_path):
            return False, f"File does not exist: {file_path}"

        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        return True, content
    except Exception as e:
        error_msg = f"Error reading file {file_path}: {e}"
        logging.error(error_msg)
        return False, error_msg


def read_file_for_analysis(file_path: str) -> str:
    """
    Read file content for code analysis, with consistent error handling.

    Args:
        file_path: Path to the file to read

    Returns:
        str: File content or empty string on error
    """
    success, result = read_file_safely(file_path)
    if success:
        return result
    else:
        logging.error(f"Failed to read file for analysis: {result}")
        return ""


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to the file

    Returns:
        int: File size in bytes, or 0 on error
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logging.error(f"Error getting file size for {file_path}: {e}")
        return 0


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory

    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Error creating directory {directory_path}: {e}")
        return False


def is_python_file(file_path: str) -> bool:
    """
    Check if a file is a Python file based on extension.

    Args:
        file_path: Path to check

    Returns:
        bool: True if file has .py extension
    """
    return file_path.endswith('.py')