#
# intelligence_code_executor.py (Code Executor Role)
# This module handles code generation using the LLM with architectural compliance.
#
# It uses the following modules:
# - agent_config: Configuration for prompts and settings.
# - intelligence_llm_service: Standardized LLM service.
# - intelligence_backpack_utils: Backpack processing utilities.
# - intelligence_execution_utils: Safe code execution utilities.
#

import json  # JSON handling for plan data
from .agent_backpack_formatter import format_backpack_context  # Context formatting utility
from .intelligence_llm_service import chat_llm  # Standardized LLM service
from .agent_config import config  # Configuration for prompts and settings
from .intelligence_backpack_utils import (chunk_backpack_by_size, load_architectural_rules,
                                           _build_prompt_sections, BACKPACK_CHUNK_SIZE_LIMIT,
                                           MAX_ITERATION_LIMIT)  # Backpack processing utilities
from .intelligence_execution_utils import execute_code  # Safe code execution utilities
from .llm_utils import make_llm_call_with_fallback  # LLM response processing utilities
from .debug_utils import debug_print  # Debug logging utilities

def get_executor_response(goal, current_code=None, backpack=None, plan=None, working_dir=None):
    """Generates the next code improvement using the Executor prompt with self-improvement."""
    # Check if backpack needs chunking
    if backpack and len(backpack) > 1:
        chunks = chunk_backpack_by_size(backpack)
        print(f"DEBUG: Backpack has {len(backpack)} items, chunked into {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            chunk_size = sum(len(item.get('full_code', '')) + len(item.get('justification', '')) + len(item.get('file_path', '')) for item in chunk)
            print(f"DEBUG: Chunk {i+1} has {len(chunk)} items, total size: {chunk_size}")
        if len(chunks) > 1:
            print("DEBUG: Triggering iterative processing due to multiple chunks")
            return get_executor_response_iterative(goal, current_code, chunks, plan, working_dir)

    # Format backpack context (standard case)
    backpack_context = format_backpack_context(backpack)

    # Load architectural rules for context
    architectural_rules = load_architectural_rules()

    # Get base prompt and enhance with architectural context
    prompt = config.EXECUTOR_PROMPT_TEMPLATE.format(goal=goal, plan=plan, backpack_context=backpack_context)

    # Add common sections using helper function
    prompt += _build_prompt_sections(architectural_rules, plan, working_dir)

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

def get_executor_response_iterative(goal, current_code=None, backpack_chunks=None, plan=None, working_dir=None):
    """
    Handles iterative LLM calls when backpack is large, processing chunks sequentially.

    Args:
        goal: The main programming goal
        backpack_chunks: List of backpack chunks
        plan: Optional plan context
        working_dir: Optional working directory

    Returns:
        str: Combined code output from all iterations
    """
    total_chunks = len(backpack_chunks)
    print(f"DEBUG: Starting iterative processing with {total_chunks} chunks")

    for i, chunk in enumerate(backpack_chunks):
        if i >= MAX_ITERATION_LIMIT:
            print(f"DEBUG: Reached iteration limit ({MAX_ITERATION_LIMIT}), stopping")
            break  # Safety limit on iterations

        print(f"DEBUG: Processing iteration {i+1}/{total_chunks}, chunk has {len(chunk)} items")

        # Format backpack context for this chunk
        backpack_context = format_backpack_context(chunk, chunk_index=i, total_chunks=total_chunks)

        # Load architectural rules for context
        architectural_rules = load_architectural_rules()

        # Base prompt for iterative processing
        prompt = f"""
You are a Code Executor. Your job is to generate or improve Python code to accomplish the programming goal.
This is iteration {i+1} of {total_chunks} processing chunks from the project backpack.

**Main Goal:** {goal}


**Project Files Chunk {i+1} (Backpack Context):**
---
{backpack_context}
---
"""

        # Add plan context if provided
        if plan:
            plan_json = json.dumps(plan, indent=2)
            prompt += f"\n\n**Plan Context:**\n{plan_json}\n"

        # Add common sections using helper function
        prompt += _build_prompt_sections(architectural_rules, None, working_dir)

        # Iterative processing instructions
        if i == 0:
            prompt += f"""
**First Iteration Instructions:**
Process the first chunk of files to start building the code solution. Focus on core functionality and structure.
Generate ONLY complete Python code as output (no explanations, no markdown, no comments outside code).
"""
        else:
            prompt += f"""
**Iteration {i+1} Instructions:**
Integrate insights from this chunk of files to refine and complete the solution.
Generate ONLY complete Python code as output (no explanations, no markdown, no comments outside code).
"""

        # Add self-improvement context if we have historical data
        from .intelligence_prompt_tracker import get_best_prompt_variations  # Dynamic import to avoid circular dependency
        best_prompts = get_best_prompt_variations(limit=3)
        if best_prompts:
            improvement_context = "\n\n**Self-Improvement Insights:**\nBased on previous successful code generations:\n"
            for j, (prompt_key, data) in enumerate(best_prompts[:3]):
                avg_score = data.get('avg_score', 0)
                success_rate = data.get('success_count', 0) / max(1, data.get('total_attempts', 1))
                improvement_context += f"- High-performing approach (score: {avg_score:.1f}, success: {success_rate:.1%}): Try variations that improve accuracy and efficiency.\n"
            improvement_context += "\nUse these insights to generate better code variations."
            prompt += improvement_context

        # Get response for this chunk
        try:
            debug_print(f"Making LLM call for iteration {i+1}")
            response = make_llm_call_with_fallback(prompt)
            debug_print(f"LLM call successful for iteration {i+1}, response length: {len(response)}")
        except Exception as e:
            debug_print(f"LLM call failed for iteration {i+1}: {str(e)}")
            # Continue with previous accumulated code on failure
            continue

        # Use response as accumulated code
        accumulated_code = response
        debug_print(f"Accumulated code updated, new length: {len(accumulated_code)}")

    debug_print(f"Iterative processing completed, final code length: {len(accumulated_code)}")
    return accumulated_code
