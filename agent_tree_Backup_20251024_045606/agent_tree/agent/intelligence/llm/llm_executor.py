#
# llm_executor.py (A Leaf)
# This module handles code generation and execution using the LLM.
#
# It uses the following modules:
# - agent.utils.config: To get the model name and prompt templates.
#

import ollama  # Main LLM interface library for model interactions and API calls
import subprocess  # System process execution for safe code running and testing
import time  # Timing utilities for performance measurement and execution tracking
import tempfile  # Temporary file creation for safe code execution in isolated environment
import os  # File system operations for data persistence and temporary file management
import json  # JSON handling for structured plan output
from agent import format_backpack_context  # Shared utility functions
from ..llm_service import chat_llm  # Standardized LLM service
from agent import config  # Configuration module for model, prompt templates, and system settings

def get_executor_response(goal, document, backpack=None, plan=None):
    """Generates the next code improvement using the Executor prompt with self-improvement."""
    # Format backpack context
    backpack_context = format_backpack_context(backpack)

    # Get base prompt
    prompt = config.EXECUTOR_PROMPT_TEMPLATE.format(goal=goal, plan=plan, document=document, backpack_context=backpack_context)

    # Add plan context if provided
    if plan:
        plan_json = json.dumps(plan, indent=2)
        prompt += f"\n\n**Plan Context:**\n{plan_json}\n"

    # Add self-improvement context if we have historical data
    from .llm_tracker import get_best_prompt_variations  # Import here to avoid circular imports
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