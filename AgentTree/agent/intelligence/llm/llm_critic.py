#
# llm_critic.py (A Leaf)
# This module evaluates code quality using the Critic prompt.
#
# It uses the following modules:
# - agent.utils.config: To get the model name and prompt templates.
#

import ollama  # Main LLM interface library for model interactions and API calls
from AgentTree.agent.utils import config  # Configuration module for model, prompt templates, and system settings

def get_critic_score(goal, document, backpack=None):
    """Evaluates the code so far using the Critic prompt."""
    # Format backpack context
    backpack_context = ""
    if backpack:
        for i, item in enumerate(backpack):
            backpack_context += f"**File {i+1}: {item.get('file_path', 'Unknown')}**\n"
            backpack_context += f"Justification: {item.get('justification', 'N/A')}\n"
            backpack_context += f"Code:\n{item.get('full_code', '')}\n\n"

    prompt = config.CRITIC_PROMPT_TEMPLATE.format(goal=goal, document=document, backpack_context=backpack_context)
    response = ollama.chat(model=config.MODEL, messages=[{'role': 'user', 'content': prompt}])
    try:
        return int(response['message']['content'].strip())
    except ValueError:
        return 1