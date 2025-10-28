"""
llm_utils.py - LLM response processing utilities.

Provides common functions for processing LLM responses, JSON extraction,
error handling, and response validation.
"""

import json
import logging
from .intelligence_llm_service import chat_llm  # Standardized LLM service


def clean_llm_json_response(raw_response: str) -> str:
    """
    Clean and extract JSON from LLM response, handling markdown fences and prefixes.

    Args:
        raw_response: Raw LLM response string

    Returns:
        str: Cleaned JSON string
    """
    if not raw_response:
        return "{}"

    resp = raw_response.strip()
    resp = resp.lstrip("```json").rstrip("```").strip()

    # Extract JSON from potentially messy response
    json_start = resp.find('{')
    json_end = resp.rfind('}')
    if json_start != -1 and json_end != -1 and json_end > json_start:
        return resp[json_start:json_end + 1]
    else:
        return resp


def parse_llm_json_response(raw_response: str) -> dict:
    """
    Parse LLM response as JSON with error handling.

    Args:
        raw_response: Raw LLM response string

    Returns:
        dict: Parsed JSON response or error fallback
    """
    try:
        cleaned = clean_llm_json_response(raw_response)
        return json.loads(cleaned)
    except (json.JSONDecodeError, Exception) as e:
        logging.error(f"LLM JSON parsing error: {e}")
        return {"error": str(e), "raw_response": raw_response[:200]}


def make_llm_call_with_fallback(prompt: str, model: str = None, max_retries: int = 1) -> str:
    """
    Make LLM call with basic error handling and fallback.

    Args:
        prompt: Prompt to send to LLM
        model: Optional model override
        max_retries: Maximum retry attempts

    Returns:
        str: LLM response or error message
    """
    for attempt in range(max_retries + 1):
        try:
            return chat_llm(prompt, model=model)
        except Exception as e:
            logging.error(f"LLM call failed (attempt {attempt + 1}): {e}")
            if attempt == max_retries:
                return f"Error: LLM call failed after {max_retries + 1} attempts: {e}"


def create_structured_prompt(base_prompt: str, context: dict = None, instructions: str = None) -> str:
    """
    Create a structured prompt with consistent formatting.

    Args:
        base_prompt: Base prompt content
        context: Optional context dictionary
        instructions: Optional additional instructions

    Returns:
        str: Formatted prompt
    """
    prompt_parts = [base_prompt]

    if context:
        prompt_parts.append("Context:")
        for key, value in context.items():
            prompt_parts.append(f"- {key}: {value}")
        prompt_parts.append("")

    if instructions:
        prompt_parts.append("Instructions:")
        prompt_parts.append(instructions)
        prompt_parts.append("")

    prompt_parts.append("Respond ONLY with the raw JSON object, without any introductory text, conversational pleasantries, or markdown formatting. Your entire response must be a single, valid JSON object.")

    return "\n".join(prompt_parts)


def validate_llm_response_structure(response: dict, required_keys: list) -> bool:
    """
    Validate that LLM response contains required structure.

    Args:
        response: Parsed LLM response dictionary
        required_keys: List of required keys

    Returns:
        bool: True if response has required structure
    """
    if not isinstance(response, dict):
        return False

    return all(key in response for key in required_keys)