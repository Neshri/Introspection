#
# _llm_service_utils.py (LLM Service Utilities)
# Utility functions for LLM chat operations with error handling and response processing.
#

import logging
from .agent_config import config  # Configuration for LLM model settings

logger = logging.getLogger(__name__)


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
        import ollama  # Import here to avoid circular imports

        # The 'options' parameter is added here to prevent the LLM from
        # cutting off its response prematurely.
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            options={
                'num_predict': config.CONTEXT_LIMIT  # Max tokens for the LLM's response
            }
        )

        # Robust error handling for malformed Ollama API responses
        # Ollama returns a ChatResponse object, not a dict, so convert it to dict
        if hasattr(response, '__dict__'):
            response = response.__dict__
        elif hasattr(response, '_asdict'):
            response = response._asdict()
        elif not isinstance(response, dict):
            logger.error(f"Unexpected response type: {type(response)}, response: {response}")
            raise Exception(f"LLM returned non-dict response: {response}")

        if 'message' not in response:
            logger.error(f"Response missing 'message' key: {response}")
            raise Exception(f"LLM response missing 'message' key: {response}")

        message = response.get('message')
        if message is None:
            logger.error(f"Response 'message' is None: {response}")
            raise Exception(f"LLM response 'message' is None: {response}")

        # Convert message object to dict if it's not already
        if hasattr(message, '__dict__'):
            message = message.__dict__
        elif hasattr(message, '_asdict'):
            message = message._asdict()
        elif not isinstance(message, dict):
            logger.error(f"Response 'message' is not a dict: {type(message)}, message: {message}")
            raise Exception(f"LLM response 'message' is not a dict: {message}")

        if 'content' not in message:
            logger.error(f"Response 'message' missing 'content' key: {message}")
            raise Exception(f"LLM response 'message' missing 'content' key: {message}")

        content = message['content']
        if content is None:
            logger.error("LLM response 'content' is None")
            raise Exception("LLM response 'content' is None")

        if not isinstance(content, str):
            logger.error(f"LLM response 'content' is not a string: {type(content)}, content: {content}")
            raise Exception(f"LLM response 'content' is not a string: {content}")

        content = content.strip()

        # Extract JSON from potentially messy response
        json_start = content.find('{')
        json_end = content.rfind('}')
        if json_start != -1 and json_end != -1 and json_end > json_start:
            extracted_json = content[json_start:json_end + 1]
            return extracted_json
        else:
            return content
    except Exception as e:
        logger.error(f"LLM chat failed: {str(e)}")
        raise Exception(f"LLM chat failed: {str(e)}")