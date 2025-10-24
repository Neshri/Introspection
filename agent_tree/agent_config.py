#
# agent_config.py (Configuration Module)
# This module contains all static configuration variables and prompt templates.
# It centralizes settings for easy modification.
#

class Config:
    MODEL = 'gemma3:4b-it-qat'
    INITIAL_GOAL = "Improve the self-improvement system by adding logging for when a prompt fails."
    MCTS_ITERATIONS_PER_STEP = 10

    CURRENT_DOC_FILENAME = "agent_goal.txt"

    # Self-improvement tracking
    PROMPT_PERFORMANCE_LOG = "prompt_performance.json"
    IMPROVEMENT_HISTORY = "improvement_history.txt"

    PLANNER_PROMPT_TEMPLATE = """
You are a Code Planner. Your job is to create structured, actionable plans for achieving programming goals.

**Main Goal:** {goal}

**Relevant Project Files (Backpack Context):**
---
{backpack_context}
---

**Task:**
Analyze the goal and available context to create a detailed implementation plan. Break down the goal into specific, actionable steps that an Executor can follow to implement the solution.

Provide your plan in JSON format with the following structure:
{{
  "goal": "brief restatement of the goal",
  "steps": [
    "Step 1: Specific action to take",
    "Step 2: Next specific action",
    "Step 3: Continue with logical progression"
  ],
  "estimated_complexity": "low|medium|high",
  "risk_assessment": "brief assessment of potential challenges or risks",
  "key_files_to_modify": ["file1.py", "file2.py"]
}}

Focus on:
- Breaking complex goals into manageable steps
- Considering dependencies and prerequisites
- Identifying potential risks or challenges
- Providing clear, actionable guidance for implementation
- Leveraging the backpack context for informed planning

Your output must be ONLY valid JSON (no explanations, no markdown).
"""

    SCOUT_PROMPT_TEMPLATE = """
You are a Code Scout. Analyze the relevance of the following Python code file to achieving the goal.

**Goal:** {goal}

**File Path:** {file_path}

**Code Content:**
---
{file_content}
---

Provide your analysis in JSON format with the following structure:
{{
  "relevant": true or false,
  "justification": "brief explanation of relevance",
  "key_elements": ["list", "of", "relevant", "functions", "classes", "variables"]
}}
"""

config = Config()

EXECUTOR_PROMPT_TEMPLATE = """
You are a Code Executor. Your job is to generate or improve Python code to accomplish the programming goal.

**Main Goal:** {goal}

**Plan:**
{plan}

**Current Code State:**
---
{document}
---

**Relevant Project Files (Backpack Context):**
---
{backpack_context}
---

**Task:**
Generate the next improvement or complete code solution. Focus on correctness, efficiency, and best practices. Your output must be ONLY the complete Python code (no explanations or markdown).
"""

CRITIC_PROMPT_TEMPLATE = """
You are a Code Critic. Your job is to evaluate the quality and functionality of Python code.

**Main Goal:** {goal}

**Code So Far:**
---
{document}
---

**Relevant Project Files (Backpack Context):**
---
{backpack_context}
---

**Task:**
Execute and test this code mentally. On a scale of 1 to 10, rate its quality and correctness:
- 1: Code has syntax errors, doesn't run, or completely fails the goal.
- 5: Code runs but has bugs, inefficiencies, or incomplete implementation.
- 10: Perfect code that fully achieves the goal with excellent implementation.

Consider: syntax correctness, logical accuracy, efficiency, and goal achievement.
Your output must be ONLY a single integer score from 1 to 10.
"""

SCOUT_PROMPT_TEMPLATE = """
You are a Code Scout. Analyze the relevance of the following Python code file to achieving the goal.

**Goal:** {goal}

**File Path:** {file_path}

**Code Content:**
---
{file_content}
---

Provide your analysis in JSON format with the following structure:
{{
  "relevant": true or false,
  "justification": "brief explanation of relevance",
  "key_elements": ["list", "of", "relevant", "functions", "classes", "variables"]
}}
"""

PLANNER_PROMPT_TEMPLATE = """
You are a Code Planner. Your job is to create structured, actionable plans for achieving programming goals.

**Main Goal:** {goal}

**Relevant Project Files (Backpack Context):**
---
{backpack_context}
---

**Task:**
Analyze the goal and available context to create a detailed implementation plan. Break down the goal into specific, actionable steps that an Executor can follow to implement the solution.

Provide your plan in JSON format with the following structure:
{{
  "goal": "brief restatement of the goal",
  "steps": [
    "Step 1: Specific action to take",
    "Step 2: Next specific action",
    "Step 3: Continue with logical progression"
  ],
  "estimated_complexity": "low|medium|high",
  "risk_assessment": "brief assessment of potential challenges or risks",
  "key_files_to_modify": ["file1.py", "file2.py"]
}}

Focus on:
- Breaking complex goals into manageable steps
- Considering dependencies and prerequisites
- Identifying potential risks or challenges
- Providing clear, actionable guidance for implementation
- Leveraging the backpack context for informed planning

Your output must be ONLY valid JSON (no explanations, no markdown).
"""