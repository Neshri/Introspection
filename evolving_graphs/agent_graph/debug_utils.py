"""
debug_utils.py - Debug logging utilities.

Provides standardized debug logging functions used throughout the agent graph.
"""

import logging


def debug_log(message: str, *args, **kwargs):
    """
    Log a debug message with consistent formatting.

    Args:
        message: Debug message to log
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments
    """
    logging.debug(message, *args, **kwargs)


def debug_log_with_context(context: str, message: str, *args, **kwargs):
    """
    Log a debug message with context prefix.

    Args:
        context: Context string (e.g., "Scout", "Planner")
        message: Debug message to log
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments
    """
    logging.debug(f"[{context}] {message}", *args, **kwargs)


def debug_print(message: str, *args, **kwargs):
    """
    Print a debug message with "DEBUG:" prefix.

    Args:
        message: Debug message to print
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments
    """
    print(f"DEBUG: {message}", *args, **kwargs)


def debug_print_with_context(context: str, message: str, *args, **kwargs):
    """
    Print a debug message with context and "DEBUG:" prefix.

    Args:
        context: Context string (e.g., "Scout", "Planner")
        message: Debug message to print
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments
    """
    print(f"DEBUG: [{context}] {message}", *args, **kwargs)


def log_error(message: str, *args, **kwargs):
    """
    Log an error message.

    Args:
        message: Error message to log
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments
    """
    logging.error(message, *args, **kwargs)


def log_info(message: str, *args, **kwargs):
    """
    Log an info message.

    Args:
        message: Info message to log
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments
    """
    logging.info(message, *args, **kwargs)


def log_warning(message: str, *args, **kwargs):
    """
    Log a warning message.

    Args:
        message: Warning message to log
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments
    """
    logging.warning(message, *args, **kwargs)