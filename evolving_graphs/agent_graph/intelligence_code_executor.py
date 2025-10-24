#
# llm_executor.py (A Leaf)
# This module handles code generation and execution using the LLM.
#
# It uses the following modules:
# - agent.utils.config: To get the model name and prompt templates.
#

import ollama  # LLM interface for code generation
import subprocess  # Safe code execution in subprocess
import time  # Performance timing for execution
import tempfile  # Temporary file creation for safe execution
import os  # File system operations for temp files
import json  # JSON handling for plan data
from .agent_backpack_formatter import format_backpack_context  # Context formatting utility
from .intelligence_llm_service import chat_llm  # Standardized LLM service
from .agent_config import config  # Configuration for prompts and settings

def load_architectural_rules():
    """Load architectural rules from rules.md file for dynamic embedding."""
    try:
        with open('rules.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Architectural rules not found. Ensure rules.md exists in the project root."

def get_executor_response(goal, document, backpack=None, plan=None, working_dir=None):
    """Generates the next code improvement using the Executor prompt with self-improvement."""
    # Format backpack context
    backpack_context = format_backpack_context(backpack)

    # Load architectural rules for context
    architectural_rules = load_architectural_rules()

    # Get base prompt and enhance with architectural context
    prompt = config.EXECUTOR_PROMPT_TEMPLATE.format(goal=goal, plan=plan, document=document, backpack_context=backpack_context)

    # Embed architectural rules context
    prompt += f"\n\n**Architectural Rules (MANDATORY COMPLIANCE):**\n{architectural_rules}\n"

    # Add file reference guidance
    prompt += f"""
**File Naming and Reference Guidelines:**
- Use correct file names: e.g., 'agent_core.py' for Agent class, 'intelligence_plan_generator.py' for Planner, etc.
- Follow domain_responsibility.py pattern: e.g., 'pipeline_code_verifier.py', 'agent_backpack_formatter.py'
- Entry points: Use [context]_main.py format (e.g., 'agent_graph_main.py')
- Utility modules: Use [component]_utils_[purpose].py (e.g., 'utils_state_persistence.py')

**Import Guidelines:**
- Use ONLY relative imports: from .module_name import ClassName # Brief purpose comment
- Intra-component: from .sibling_module import X
- Inter-component: from ..directory_name.module_name import X
- Examples: from .agent_config import config # Configuration settings
- NO absolute imports except in entry point modules with mandatory comments
- NO __init__.py imports (all imports must be direct and explicit)

**Code Structure Requirements:**
- Files ≤ 300 non-empty, non-comment lines
- No duplicated logic blocks (5+ contiguous lines)
- Extract duplicates to utility modules like 'agent_graph_utils_core.py'
- Use semantic naming with clear responsibilities

"""

    # Add plan context if provided
    if plan:
        plan_json = json.dumps(plan, indent=2)
        prompt += f"\n\n**Plan Context:**\n{plan_json}\n"

    # Add working directory context if provided
    if working_dir:
        prompt += f"\n\n**Working Directory:**\nAll code changes should be generated relative to the working directory: {working_dir}\nIf writing files, ensure they target this candidate directory for consistency.\n"

    # Add clearer LLM generation instructions
    prompt += f"""
**LLM Code Generation Instructions:**
- Generate ONLY complete Python code as output (no explanations, no markdown, no comments outside code)
- Ensure all code follows the architectural rules above - violations will be rejected
- Use relative imports exclusively as specified (no absolute imports)
- Reference correct file names and follow naming conventions
- Maintain file size limits and avoid code duplication
- Include mandatory import comments on same line: from .module import Class # Purpose
- Extract any duplicated logic to appropriate utility modules
- Verify compliance with component architecture and directory structure rules

**Final Compliance Check:**
Before outputting code, mentally verify it adheres to ALL architectural rules listed above.
"""

    # Add self-improvement context if we have historical data
    from .intelligence_prompt_tracker import get_best_prompt_variations  # Dynamic import to avoid circular dependency
    best_prompts = get_best_prompt_variations(limit=3)
    if best_prompts:
        improvement_context = "\n\n**Self-Improvement Insights:**\nBased on previous successful code generations:\n"
        for i, (prompt_key, data) in enumerate(best_prompts[:3]):
            avg_score = data.get('avg_score', 0)
            success_rate = data.get('success_count', 0) / max(1, data.get('total_attempts', 1))
            improvement_context += f"- High-performing approach (score: {avg_score:.1f}, success: {success_rate:.1%}): Try variations that improve accuracy and efficiency.\n"
        improvement_context += "\nUse these insights to generate better code variations."
        prompt += improvement_context

    return chat_llm(prompt)

def execute_code(code):
    """
    Executes Python code safely using subprocess and returns execution results.

    Returns a dict with:
    - success: bool
    - output: str (stdout)
    - error: str (stderr)
    - execution_time: float (seconds)
    """
    result = {
        'success': False,
        'output': '',
        'error': '',
        'execution_time': 0.0
    }

    # Create temporary file for the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        start_time = time.time()

        # Execute with timeout and resource limits
        process = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
            cwd=os.path.dirname(temp_file)  # Run in temp directory
        )

        end_time = time.time()
        result['execution_time'] = end_time - start_time
        result['output'] = process.stdout.strip()
        result['error'] = process.stderr.strip()
        result['success'] = process.returncode == 0

    except subprocess.TimeoutExpired:
        result['error'] = "Execution timed out after 30 seconds"
        result['success'] = False
    except Exception as e:
        result['error'] = f"Execution failed: {str(e)}"
        result['success'] = False
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_file)
        except:
            pass

    return result