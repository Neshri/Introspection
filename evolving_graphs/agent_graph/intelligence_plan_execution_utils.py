"""
intelligence_plan_execution_utils.py - Plan execution and refinement utilities.

Provides functions for generating insights from backpack batches, synthesizing plans
from insights, and refining objectives into more specific sub-objectives.
"""

import json  # JSON handling for structured plan output
import re  # Regular expressions for extracting JSON from markdown blocks
from .intelligence_llm_service import chat_llm  # Standardized LLM service
from .agent_config import config  # Configuration settings for model selection and prompt templates
from .llm_utils import make_llm_call_with_fallback, parse_llm_json_response  # LLM response processing utilities
from .json_utils import (validate_json_structure, repair_json_structure,
                         extract_json_from_markdown, safe_json_loads)  # JSON processing utilities
from .debug_utils import debug_print, log_error  # Debug logging utilities


def refine_objective(objective_description: str, parent_context: str, main_goal: str, code_context: str) -> list[str]:
    """
    Refines a high-level objective into more specific sub-objectives using LLM.

    Args:
        objective_description (str): The original objective to refine
        parent_context (str): Context from parent objectives
        main_goal (str): The overall main goal
        code_context (str): Relevant codebase context

    Returns:
        list[str]: List of refined objective descriptions
    """
    debug_print(f"Refining objective: {objective_description[:100]}...")

    prompt = config.PLANNER_REFINEMENT_PROMPT_TEMPLATE.format(
        objective_description=objective_description,
        parent_context=parent_context,
        main_goal=main_goal,
        code_context=code_context
    )

    llm_response = make_llm_call_with_fallback(prompt)
    debug_print(f"LLM refinement response: {llm_response[:200]}...")

    try:
        refined_objectives = json.loads(llm_response)
        if isinstance(refined_objectives, list):
            descriptions = [obj.get("description", "") for obj in refined_objectives if isinstance(obj, dict)]
            print(f"DEBUG: Successfully refined into {len(descriptions)} specific objectives")
            return descriptions
        else:
            print("DEBUG: LLM returned non-list response, using fallback")
            return [objective_description]  # Fallback
    except json.JSONDecodeError as e:
        print(f"DEBUG: Failed to parse refinement JSON: {e}")
        return [objective_description]  # Fallback


def generate_insights_from_batch(main_goal: str, batch_context: str, token_count: int) -> str:
    """
    Generates insights for a single batch of files using the planner insight prompt.

    Args:
        main_goal (str): The programming goal to achieve
        batch_context (str): The context from the current batch of files
        token_count (int): Estimated token count for the batch

    Returns:
        str: LLM-generated insights for the batch
    """
    debug_print(f"Generating insights for batch of ~{token_count} tokens (size {len(batch_context)} chars)")
    prompt = config.PLANNER_INSIGHT_PROMPT_TEMPLATE.format(
        goal=main_goal,
        backpack_context=batch_context
    )
    return make_llm_call_with_fallback(prompt)


def synthesize_plan_from_insights(main_goal: str, insights: list[str]) -> str:
    """
    Synthesizes a final plan from a collection of insights using reduce phase.

    Args:
        main_goal (str): The programming goal to achieve
        insights (list[str]): List of insights from all batches

    Returns:
        str: A structured plan in JSON format
    """
    debug_print("Synthesizing final plan from all generated insights...")
    formatted_insights = "\n---\n".join(insights)
    prompt = config.PLANNER_SYNTHESIS_PROMPT_TEMPLATE.format(
        goal=main_goal,
        insights=formatted_insights
    )

    llm_output = make_llm_call_with_fallback(prompt)
    debug_print(f"LLM generated raw output: {llm_output[:120]}...")

    # Clean the LLM output to remove unwanted prefixes like "<unused2557>"
    cleaned_output = llm_output.strip()
    if cleaned_output.startswith("<unused") and ">" in cleaned_output:
        # Remove the unwanted prefix
        cleaned_output = cleaned_output.split(">", 1)[1].strip()

    # Extract JSON using utility function
    plan = extract_json_from_markdown(cleaned_output)
    if not plan:
        # Try to find JSON object directly
        json_match = re.search(r'\{.*\}', cleaned_output, re.DOTALL)
        plan = json_match.group(0) if json_match else cleaned_output

    # Now, validate the cleaned plan
    if validate_json_structure(plan):
        debug_print("Generated plan is valid JSON")
        return plan
    else:
        debug_print(f"Plan JSON validation failed, attempting to repair...")
        # Attempt to repair common JSON issues
        repaired_plan = repair_json_structure(plan)
        if repaired_plan and validate_json_structure(repaired_plan):
            debug_print("Repaired plan is valid JSON")
            return repaired_plan
        else:
            debug_print("Plan JSON validation failed after repair, wrapping in basic structure")
        return json.dumps({
            "goal": main_goal,
            "objectives": [
                {
                    "description": f"Failed to parse LLM output: {str(e)[:100]}",
                    "actions": [
                        {
                            "role": "code_editor",
                            "command": {"description": "Analyze and fix plan generation"},
                            "justification": "LLM produced invalid JSON that needs to be repaired"
                        }
                    ]
                }
            ],
            "estimated_complexity": "high",
            "risk_assessment": "Failed to synthesize a structured plan from insights. The LLM's output was not valid JSON even after cleanup and repair attempts."
        })