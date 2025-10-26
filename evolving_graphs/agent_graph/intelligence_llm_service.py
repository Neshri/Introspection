#
# llm_service.py (A Leaf)
# This module provides standardized LLM chat functionality with consistent error handling.
#

import ollama
from .agent_config import config  # Configuration settings for LLM model and API


def chat_llm(prompt, model=None):
    """
    Standardized function for LLM chat calls with consistent error handling.

    Args:
        prompt (str): The prompt to send to the LLM
        model (str, optional): Model name to use. Defaults to config.MODEL

    Returns:
        str: The LLM response content, stripped of whitespace

    Raises:
        Exception: If the LLM call fails
    """
    if model is None:
        model = config.MODEL

    try:
        # The 'options' parameter is added here to prevent the LLM from
        # cutting off its response prematurely.
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            options={
                'num_predict': config.CONTEXT_LIMIT  # Max tokens for the LLM's response
            }
        )
        content = response['message']['content'].strip()

        # Extract JSON from potentially messy response
        json_start = content.find('{')
        json_end = content.rfind('}')
        if json_start != -1 and json_end != -1 and json_end > json_start:
            extracted_json = content[json_start:json_end + 1]
            return extracted_json
        else:
            return content
    except Exception as e:
        raise Exception(f"LLM chat failed: {str(e)}")