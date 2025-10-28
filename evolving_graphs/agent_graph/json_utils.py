"""
json_utils.py - JSON processing utilities.

Provides common functions for JSON validation, repair, and processing
used across the agent graph components.
"""

import json
import re


def validate_json_structure(json_str: str) -> bool:
    """
    Validate if a string is valid JSON.

    Args:
        json_str: String to validate

    Returns:
        bool: True if valid JSON
    """
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


def repair_json_structure(plan_str: str) -> str:
    """
    Attempt to repair common JSON structure issues.

    Args:
        plan_str: Potentially malformed JSON string

    Returns:
        str: Repaired JSON string, or empty string if repair failed
    """
    try:
        plan_str = plan_str.strip()

        # Ensure it starts and ends with braces
        if not plan_str.startswith('{'):
            plan_str = '{' + plan_str
        if not plan_str.endswith('}'):
            plan_str = plan_str + '}'

        # Remove any text before the first {
        brace_start = plan_str.find('{')
        if brace_start > 0:
            plan_str = plan_str[brace_start:]

        # Remove any text after the last }
        brace_end = plan_str.rfind('}')
        if brace_end >= 0 and brace_end < len(plan_str) - 1:
            plan_str = plan_str[:brace_end + 1]

        # Ensure basic structure exists
        if '"goal"' not in plan_str:
            return ""

        json.loads(plan_str)
        return plan_str

    except json.JSONDecodeError:
        return ""


def extract_json_from_markdown(text: str) -> str:
    """
    Extract JSON from markdown code blocks.

    Args:
        text: Text that may contain JSON in markdown blocks

    Returns:
        str: Extracted JSON string
    """
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        return json_match.group(1)

    # Try to find JSON object directly
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)

    return text


def safe_json_loads(json_str: str, fallback: dict = None) -> dict:
    """
    Safely load JSON with a fallback value.

    Args:
        json_str: JSON string to parse
        fallback: Fallback value if parsing fails

    Returns:
        dict: Parsed JSON or fallback
    """
    if fallback is None:
        fallback = {}

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return fallback


def format_json_for_prompt(data: dict, indent: int = 2) -> str:
    """
    Format dictionary as JSON string for prompts.

    Args:
        data: Dictionary to format
        indent: Indentation level

    Returns:
        str: Formatted JSON string
    """
    return json.dumps(data, indent=indent)