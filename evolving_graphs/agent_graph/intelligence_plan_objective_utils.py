"""
intelligence_plan_objective_utils.py - Objective analysis and specificity utilities.

Provides functions for determining if objectives are specific enough and related heuristics.
"""

import re  # Regular expressions for extracting file references


def is_specific_objective(description: str) -> bool:
    """
    Heuristic function to determine if an objective is specific enough.
    Checks if it references a specific function, class, or import section in a particular file.

    Args:
        description (str): The objective description to evaluate

    Returns:
        bool: True if the objective is specific enough, False otherwise
    """
    import re

    # Check for file references (e.g., .py files)
    file_references = re.findall(r'\b\w+\.py\b', description.lower())
    if not file_references:
        return False

    # Check for specific code elements
    specific_indicators = [
        'function', 'class', 'method', 'import', 'def ', 'class ',
        'modify', 'update', 'add to', 'change in', 'edit'
    ]

    description_lower = description.lower()
    has_specific_indicator = any(indicator in description_lower for indicator in specific_indicators)

    # Check for generic terms that indicate vagueness
    vague_indicators = [
        'implement changes', 'make improvements', 'fix issues', 'add features',
        'update code', 'modify code', 'analyze', 'review', 'examine'
    ]

    has_vague_indicator = any(vague in description_lower for vague in vague_indicators)

    return has_specific_indicator and not has_vague_indicator