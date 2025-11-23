import ollama
import logging

def chat_llm(model: str, prompt: str) -> str:
    """
    Wrapper for the ollama chat LLM.

    Args:
        model (str): The model to use for the chat.
        prompt (str): The prompt to send to the LLM.

    Returns:
        str: The response from the LLM. If an error occurs, a string describing the error is returned.
    """
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        logging.info(prompt+ "\n\n"+ response['message']['content'].strip())
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error: LLM chat failed: {e}"
    