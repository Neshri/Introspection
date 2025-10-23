#
# llm_critic.py (A Leaf)
# This module evaluates code quality using the Critic prompt.
#
# It uses the following modules:
# - agent.utils.config: To get the model name and prompt templates.
#

import ollama  # Main LLM interface library for model interactions and API calls
from ..utils import format_backpack_context  # Shared utility functions
from ..llm_service import chat_llm  # Standardized LLM service
from ...utils import config  # Configuration module for model, prompt templates, and system settings

def get_critic_score(main_goal, document, backpack=None):
    """Evaluates the code so far using the Critic prompt."""
    # Format backpack context
    backpack_context = format_backpack_context(backpack)

    prompt = config.CRITIC_PROMPT_TEMPLATE.format(goal=main_goal, document=document, backpack_context=backpack_context)
    response = chat_llm(prompt)
    try:
        return int(response)
    except ValueError:
        return 1