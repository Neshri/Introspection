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

    # Command-based Plan Building: Prompt for incremental plan construction using commands.
    PLANNER_COMMAND_PROMPT_TEMPLATE = """
    You are a software architect building a hierarchical plan incrementally using simple commands. You MUST follow strict hierarchical decomposition rules:

    AVAILABLE COMMANDS:
    - ADD_OBJECTIVE <description> [-> <parent_id>]: Add a new objective node (defaults to root if no parent specified)
    - ADD_ACTION <objective_id> <role> <description> [justification]: Add an action to an existing objective (ONLY when objectives reach sufficient specificity)
    - EDIT_OBJECTIVE <objective_id> <new_description>: Modify an existing objective's description
    - EDIT_ACTION <action_id> <new_description> [new_justification]: Modify an existing action
    - LIST [objectives|actions|all]: Display current plan structure (defaults to all)
    - DONE: Signal that objective decomposition is complete and actions can now be added

    HIERARCHICAL DECOMPOSITION RULES:
    1. ONLY ALLOW ADD_OBJECTIVE commands until objectives reach sufficient specificity (targeting specific functions/files)
    2. Objectives must reference specific functions, classes, imports, or files before allowing actions
    3. Only allow ADD_ACTION after objectives become specific (e.g., "Update import section in agent_core.py" not "implement changes")
    4. ADD_ACTION is ONLY permitted at leaf nodes with specific, actionable objectives
    5. Use DONE to signal completion of objective decomposition phase
    6. Continue decomposing recursively until DONE is issued or sufficient granularity reached

    CRITICAL INSTRUCTIONS:
    - Use commands to build the plan step by step
    - Each response should contain ONE command only
    - Commands should be on a single line
    - Focus on the most immediate next step toward the goal
    - Make objectives specific (target particular functions/classes/files)
    - Make actions executable (clear, specific commands)
    - Use proper file references from the codebase context
    - Enforce hierarchical decomposition: objectives first, then actions at leaves

    Current Plan Context:
    {plan_context}

    Primary Goal: "{goal}"

    Codebase Context:
    ---
    {code_context}
    ---

    What is the single most important command to execute next to progress toward the goal? Respond with ONLY the command, no explanations.
    """

    # Iterative Refinement Phase: Prompt for refining objectives to be more specific (single sub-objective)
    PLANNER_REFINEMENT_PROMPT_TEMPLATE = """
    You are a software engineering expert specializing in task decomposition. Your task is to refine a high-level objective into exactly one more specific, actionable sub-objective that targets a particular Python function, class, or import section in a specific file.

    IMPORTANT: Your response must be ONLY valid JSON. Do not include any text before or after the JSON. Do not use markdown code blocks. The JSON must start with [ and end with ].

    The refined objective must be an array with exactly one JSON object with the following structure:
    [
      {{
        "description": "Single highly specific objective targeting a particular function/class/import in a specific file, e.g., 'Update the import section in evolving_graphs/agent_graph/agent_core.py to include new logging utilities'"
      }}
    ]

    Original Objective: "{objective_description}"
    Parent Context: "{parent_context}"
    Main Goal: "{main_goal}"
    Codebase Context: "{code_context}"

    Refine this objective into exactly one more specific sub-objective. The sub-objective must target a specific Python function, class, or import section in a particular file. Avoid vague descriptions like "implement changes" - be precise about what function/class/import to modify and in which file. Output ONLY valid JSON array with exactly one object, no extra text.
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