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
        response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content'].strip()
    except Exception as e:
        raise Exception(f"LLM chat failed: {str(e)}")