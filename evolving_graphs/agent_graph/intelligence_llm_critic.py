#
# llm_critic.py (A Leaf)
# This module evaluates code quality using the Critic prompt.
#
# It uses the following modules:
# - agent.utils.config: To get the model name and prompt templates.
#

import ollama  # LLM interface for code criticism
from .agent_backpack_formatter import format_backpack_context  # Formats context for backpack items
from .intelligence_llm_service import chat_llm  # Standardized LLM chat service
from .agent_config import config  # Configuration for model and prompt templates

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