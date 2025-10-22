#
# llm_handler.py (A Leaf)
# This module is responsible for all direct communication with the Ollama LLM.
# It abstracts away the API calls.
#
# It uses the following modules:
# - agent.utils.config: To get the model name and prompt templates.
#

import ollama
from agent.utils import config

def get_executor_response(goal, document):
    """Generates the next story paragraph using the Executor prompt."""
    prompt = config.EXECUTOR_PROMPT_TEMPLATE.format(goal=goal, document=document)
    response = ollama.chat(model=config.MODEL, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content'].strip()

def get_critic_score(goal, document):
    """Evaluates the story so far using the Critic prompt."""
    prompt = config.CRITIC_PROMPT_TEMPLATE.format(goal=goal, document=document)
    response = ollama.chat(model=config.MODEL, messages=[{'role': 'user', 'content': prompt}])
    try:
        return int(response['message']['content'].strip())
    except ValueError:
        return 1