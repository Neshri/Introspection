#
# agent_config.py (Configuration Module)
# This module contains all static configuration variables and prompt templates.
# It centralizes settings for easy modification.
#

class Config:
    MODEL = 'gemma3:4b-it-qat'
    # Context limit for a single request to avoid overloading the LLM.
    CONTEXT_LIMIT = 2048

    INITIAL_GOAL = "Improve the self-improvement system by adding logging for when a prompt fails."

    # Self-improvement tracking
    PROMPT_PERFORMANCE_LOG = "prompt_performance.json"

    # Scout configuration
    MAX_SCOUT_DEPTH = 5
    MAX_SCOUT_NODES = 50
    RELEVANCE_THRESHOLD = 15

    # Keyword matching configuration
    ENABLE_SYNONYM_EXPANSION = True
    ENABLE_CASE_VARIATIONS = True
    ENABLE_CONTEXT_PATTERN_MATCHING = True

    # --- Planner Configuration (Hierarchical Map-Reduce) ---
    # Map Phase: Prompt for generating insights from a batch of files.
    PLANNER_INSIGHT_PROMPT_TEMPLATE = """
    As a senior software architect, your task is to analyze a batch of code in relation to a primary goal.
    Do not generate a full plan. Instead, provide a concise analysis of these files.
    Your output should be a list of key insights, potential changes, and the overall role of these files for the main goal.

    Primary Goal: "{goal}"

    Code Context (Batch):
    ---
    {backpack_context}
    ---

    Based on the code context, what are the essential insights and required modifications in these specific files to achieve the primary goal?
    Be concise and focus on high-level strategy for this batch only.
    """

    # Reduce Phase: Prompt for synthesizing the final plan from all insights.
    PLANNER_SYNTHESIS_PROMPT_TEMPLATE = """
    You are a master software architect. You have been given a primary goal and a series of high-level insights from your team who have analyzed different parts of the codebase.
    Your job is to synthesize these analyses into a single, coherent, and structured JSON plan.

    The plan must be a JSON object with the following structure:
    {{
      "goal": "brief restatement of the goal",
      "steps": [
        "Step 1: Specific action to take",
        "Step 2: Next specific action"
      ],
      "estimated_complexity": "low|medium|high",
      "risk_assessment": "brief assessment of potential challenges or risks",
      "key_files_to_modify": ["file1.py", "file2.py"]
    }}

    Primary Goal: "{goal}"

    Architectural Insights from Code Analysis:
    ---
    {insights}
    ---

    Synthesize all the above insights into a final, structured JSON plan to achieve the primary goal. Your output must be ONLY valid JSON.
    """

    # --- Other Agent Prompts ---

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

    EXECUTOR_PROMPT_TEMPLATE = """
    You are a Code Executor. Your job is to generate or improve Python code to accomplish the programming goal.

    **Main Goal:** {goal}

    **Plan:**
    {plan}

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

    **Relevant Project Files (Backpack Context):**
    ---
    {backpack_context}
    ---

    **Task:**
    Evaluate the provided code mentally. On a scale of 1 to 10, rate its quality and correctness:
    - 1: Code has syntax errors, doesn't run, or completely fails the goal.
    - 5: Code runs but has bugs, inefficiencies, or incomplete implementation.
    - 10: Perfect code that fully achieves the goal with excellent implementation.

    Consider: syntax correctness, logical accuracy, efficiency, and goal achievement.
    Your output must be ONLY a single integer score from 1 to 10.
    """

config = Config()