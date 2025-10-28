"""
intelligence_plan_json_utils.py - JSON repair and processing utilities for plans.

Provides functions for repairing common JSON structure issues in LLM-generated plans.
"""

import json  # JSON handling for structured plan output


def _repair_json_structure(plan_str: str) -> str:
    """
    Attempts to repair common JSON structure issues in LLM-generated plans.

    Args:
        plan_str (str): The potentially malformed JSON string

    Returns:
        str: The repaired JSON string, or empty string if repair failed
    """
    try:
        # Remove any trailing/leading non-JSON text
        plan_str = plan_str.strip()

        # Fix common issues: missing quotes around keys, trailing commas, etc.
        # This is a basic repair - in production, consider using a proper JSON repair library

        # Ensure it starts and ends with braces
        if not plan_str.startswith('{'):
            plan_str = '{' + plan_str
        if not plan_str.endswith('}'):
            plan_str = plan_str + '}'

        # Try parsing after basic fixes
        json.loads(plan_str)
        return plan_str

    except json.JSONDecodeError:
        # If basic repair fails, try more aggressive fixes
        try:
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