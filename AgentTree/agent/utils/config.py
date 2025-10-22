#
# config.py (A Leaf)
# This module contains all static configuration variables and prompt templates.
# It centralizes settings for easy modification.
#

MODEL = 'gemma3:4b-it-qat'
INITIAL_GOAL = "Write a short, engaging story about a robot who discovers music."
MCTS_ITERATIONS_PER_STEP = 10

CURRENT_DOC_FILENAME = "../agent_memory_current.txt"
PREVIOUS_DOC_FILENAME = "../agent_memory_previous.txt"

EXECUTOR_PROMPT_TEMPLATE = """
You are a creative Executor. Your job is to generate the *next logical paragraph or section* to continue the story.

**Main Goal:** {goal}
**Working Document (Current Story):**
---
{document}
---

**Task:**
Write the next single paragraph to continue the story. Be creative and build upon what is already there. Your output must be ONLY the new paragraph.
"""

CRITIC_PROMPT_TEMPLATE = """
You are a literary Critic. Your job is to evaluate the quality of a story-in-progress.

**Main Goal:** {goal}

**Story So Far:**
---
{document}
---

**Task:**
Read the story so far. On a scale of 1 to 10, how engaging, coherent, and promising is it?
- 1: A complete dead end, incoherent.
- 5: Has some potential but is flawed.
- 10: Brilliant, a compelling foundation for a great story.

Your output must be ONLY a single integer score from 1 to 10.
"""