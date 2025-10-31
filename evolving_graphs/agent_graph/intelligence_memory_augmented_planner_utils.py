#
# intelligence_memory_augmented_planner_utils.py (Memory-Augmented Planner Utils)
# This module provides memory-enhanced planning utilities that integrate historical
# learning with the existing PlanGraph and command-based planning system.
#

from typing import Dict, List, Optional, Tuple, Any, Union  # Type hints for function signatures and data structures
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_COMPLETED  # PlanGraph data structures and status constants
from .intelligence_plan_memory_interface import planning_memory_interface  # Global memory interface instance for planning patterns
from .intelligence_plan_command_utils import command_parser  # Command parsing and execution for plan manipulation
from .intelligence_llm_service import chat_llm  # LLM service for generating planning commands
from .intelligence_plan_builder_graph_context_utils import _generate_plan_context  # Plan context generation for LLM prompts
from .intelligence_plan_objective_utils import is_specific_objective  # Objective specificity checking utilities
from .intelligence_plan_execution_utils import refine_objective  # Objective refinement and decomposition
from .agent_config import config  # Configuration constants and prompts for the planner


def memory_augmented_update_plan(main_goal: str, backpack: list[dict], plan: PlanGraph,
                                codebase_summary: str = "", query_answer: str = "") -> tuple[PlanGraph, list]:
    """
    Memory-augmented version of update_plan that leverages historical planning patterns
    to prevent unproductive loops and guide intelligent progression.

    Returns the updated PlanGraph and a list of planner memory IDs with full LLM response logging.
    """
    planner_memory_ids = []
    print(f"DEBUG: Starting memory-augmented update_plan with main_goal: '{main_goal}'")

    # Step 1: Input Validation (same as original)
    if not isinstance(plan, PlanGraph):
        raise ValueError("plan must be a PlanGraph instance")
    if not main_goal.strip():
        raise ValueError("main_goal cannot be empty")
    if not isinstance(backpack, list):
        raise TypeError("backpack must be a list of dicts")

    # Step 2: Update Root Objective Description to Match Main Goal
    root_node = plan.get_node(plan.root_id)
    if root_node.description != main_goal:
        root_node.description = main_goal
        print(f"DEBUG: Updated root objective description to match main goal")

    # Step 3: Context Inclusion - Prepare context prefix for all LLM calls
    context_prefix = ""
    if codebase_summary:
        context_prefix += f"Codebase Architecture Summary:\n{codebase_summary}\n\n"
    if query_answer:
        context_prefix += f"Additional Query Context:\n{query_answer}\n\n"

    # Step 4: Initialize Memory-Augmented Planning Session
    print("DEBUG: Initializing memory-augmented planning session")
    initial_context = _generate_plan_context(plan)
    session_id = planning_memory_interface.record_planning_session_start(main_goal, initial_context)

    # Step 5: Memory-Augmented Command-Based Incremental Plan Building
    print("DEBUG: Starting memory-augmented command-based incremental plan building")
    unfolding_steps = 0
    max_unfolding_steps = 50
    loop_detection_threshold = 3  # Commands without progress

    # Find initial pending objectives (those without children yet)
    pending_objectives = [node_id for node_id, node in plan.nodes.items()
                         if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children]
    print(f"DEBUG: Found {len(pending_objectives)} initial pending objectives to unfold")

    command_history = []
    loop_counter = 0
    start_time = __import__('time').time()

    while pending_objectives and unfolding_steps < max_unfolding_steps:
        unfolding_steps += 1
        print(f"DEBUG: Memory-augmented unfolding step {unfolding_steps}: processing objective {pending_objectives[0]}")

        # Process the first pending objective using memory-augmented approach
        current_obj_id = pending_objectives.pop(0)
        progress_made = _unfold_objective_memory_augmented(
            current_obj_id, main_goal, backpack, context_prefix, plan,
            command_history, session_id
        )

        if not progress_made:
            loop_counter += 1
            print(f"DEBUG: No progress made in step {unfolding_steps}, loop counter: {loop_counter}")
        else:
            loop_counter = 0  # Reset loop counter on progress

        # Detect loops using memory patterns
        if planning_memory_interface.detect_loop_pattern(command_history, _generate_plan_context(plan)):
            print(f"DEBUG: Loop pattern detected via memory analysis, attempting corrective action")
            loop_counter += 2  # Penalize more heavily

        # If we've been looping too long, try memory-guided intervention
        if loop_counter >= loop_detection_threshold:
            print(f"DEBUG: Loop threshold exceeded, applying memory-guided intervention")
            success = _apply_memory_guided_intervention(plan, current_obj_id, main_goal, backpack, context_prefix, command_history, session_id)
            if success:
                loop_counter = 0  # Reset on successful intervention
            else:
                break  # Give up if intervention fails

        # Find newly added pending objectives
        new_pending_objectives = [node_id for node_id, node in plan.nodes.items()
                                 if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children
                                 and node_id not in pending_objectives]
        if new_pending_objectives:
            pending_objectives.extend(new_pending_objectives)
            print(f"DEBUG: Added {len(new_pending_objectives)} new pending objectives to unfold")
            print(f"DEBUG: Total pending objectives remaining: {len(pending_objectives)}")

    # Record session outcome
    end_time = __import__('time').time()
    time_to_completion = end_time - start_time
    success = len([n for n in plan.nodes.values() if isinstance(n, ActionNode) and n.status == STATUS_PENDING]) > 0
    planning_memory_interface.record_session_outcome(
        session_id, success, len(command_history), loop_counter, time_to_completion
    )

    if unfolding_steps >= max_unfolding_steps:
        print(f"DEBUG: WARNING - Reached maximum unfolding steps ({max_unfolding_steps})")

    print(f"DEBUG: Memory-augmented incremental plan building completed after {unfolding_steps} steps")
    print(f"DEBUG: Session recorded with ID: {session_id}")
    print("DEBUG: Memory-enhanced approach prevented unproductive loops and enabled intelligent progression")

    # Log completion summary
    total_nodes = len(plan.nodes)
    objective_nodes = sum(1 for node in plan.nodes.values() if isinstance(node, ObjectiveNode))
    action_nodes = sum(1 for node in plan.nodes.values() if isinstance(node, ActionNode))
    print(f"DEBUG: Final plan has {total_nodes} total nodes ({objective_nodes} objectives, {action_nodes} actions)")

    return plan, planner_memory_ids


def _unfold_objective_memory_augmented(objective_id: str, main_goal: str, backpack: list,
                                     context_prefix: str, plan: PlanGraph, command_history: list,
                                     session_id: str) -> bool:
    """
    Memory-augmented version of objective unfolding with intelligent command selection.
    Returns True if progress was made, False if stuck.
    """
    objective = plan.get_node(objective_id)
    print(f"DEBUG: Starting memory-augmented unfolding of objective {objective_id}: '{objective.description}'")

    # Build parent context
    parent_context = []
    current_id = objective_id
    while current_id != plan.root_id:
        current_node = plan.get_node(current_id)
        parent_context.insert(0, current_node.description)
        current_id = current_node.parent_id
    parent_context_str = " -> ".join(parent_context) if parent_context else "Root Goal"

    # Build code context from backpack
    code_context_parts = []
    for item in backpack[:5]:
        content = item.get("content", str(item))[:1000]
        code_context_parts.append(content)
    code_context = "\n---\n".join(code_context_parts)

    # Generate plan context for LLM
    plan_context = _generate_plan_context(plan)

    # Use memory-enhanced prompt
    prompt = _generate_memory_enhanced_prompt(
        main_goal, plan_context, code_context, command_history, session_id
    )

    max_commands = 15
    command_count = 0
    objective_decomposition_done = False
    current_phase = "objectives"
    progress_made = False

    while command_count < max_commands:
        command_count += 1
        print(f"DEBUG: Requesting command {command_count} for objective {objective_id} (phase: {current_phase})")

        # Display plan every 10th command
        if command_count % 10 == 0:
            print(f"DEBUG: Plan state after {command_count} commands:")
            list_success, list_message = command_parser.parse_and_execute("LIST", plan, {'parent_id': objective_id, 'main_goal': main_goal})
            if list_success:
                print(list_message)

        # Get LLM response with memory context
        llm_response = chat_llm(prompt)
        print(f"DEBUG: LLM command response: '{llm_response}'")

        # Get memory-guided command suggestions
        suggestions = planning_memory_interface.get_context_aware_command_suggestions(
            plan_context, command_history, main_goal
        )

        # Parse and validate command
        command_text = llm_response.strip()
        import re
        command_match = re.match(r'(\w+)\s*(.*)', command_text, re.IGNORECASE)
        if not command_match:
            print(f"DEBUG: Invalid command format: '{command_text}' - trying memory suggestion")
            if suggestions:
                command_text = suggestions[0][0]  # Use top memory suggestion
                print(f"DEBUG: Using memory-suggested command: '{command_text}'")
            else:
                continue

        command_name = command_match.group(1).upper()
        print(f"DEBUG: Parsed command name: '{command_name}' (phase: {current_phase})")

        # Memory-guided phase enforcement
        if current_phase == "objectives":
            # Check if memory suggests DONE would be appropriate
            done_confidence = planning_memory_interface.should_attempt_done(plan_context, command_history)
            if done_confidence > 0.7 and command_name != "DONE":
                print(f"DEBUG: Memory suggests high confidence for DONE ({done_confidence:.2f}), but LLM chose {command_name}")
                # Could override here if confidence is very high

            valid_commands = ['ADD_OBJECTIVE', 'EDIT_OBJECTIVE', 'LIST', 'DONE']
            if command_name not in valid_commands:
                print(f"DEBUG: Invalid command '{command_name}' in objectives phase, allowed: {valid_commands}")
                # Try memory suggestion instead
                if suggestions:
                    memory_cmd = suggestions[0][0]
                    if memory_cmd.upper() in valid_commands:
                        command_text = memory_cmd
                        command_name = memory_cmd.upper()
                        print(f"DEBUG: Using memory-suggested valid command: '{command_text}'")
                    else:
                        continue
                else:
                    continue
        elif current_phase == "actions":
            pass  # All commands allowed in actions phase

        # Execute the command
        success, message = command_parser.parse_and_execute(
            command_text, plan,
            {'parent_id': objective_id, 'main_goal': main_goal}
        )

        # Record command attempt in memory
        planning_memory_interface.record_command_attempt(
            session_id, command_text, plan_context, success, False
        )

        command_history.append(command_text)
        print(f"DEBUG: Command execution result: {success} - {message}")

        if success:
            progress_made = True

            # Check for DONE command transition
            if command_name == 'DONE':
                objective_decomposition_done = True
                current_phase = "actions"
                print(f"DEBUG: Objective decomposition marked as DONE, transitioning to actions phase")

            # Check if we should continue based on phase and state
            if current_phase == "objectives":
                pending_objectives = [node_id for node_id, node in plan.nodes.items()
                                     if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children]
                if not pending_objectives or objective_decomposition_done:
                    print(f"DEBUG: Objectives phase complete")
                    current_phase = "actions"
                    objective_decomposition_done = True
            elif current_phase == "actions":
                leaf_objectives = [node_id for node_id, node in plan.nodes.items()
                                  if isinstance(node, ObjectiveNode) and not node.children]
                actions_exist = any(isinstance(node, ActionNode) and node.parent_id in leaf_objectives
                                   for node in plan.nodes.values())
                if actions_exist:
                    print(f"DEBUG: Actions added to leaf objectives, completing unfolding")
                    break

        elif not success:
            print(f"DEBUG: Command failed, trying fallback")
            # Enhanced fallback with memory guidance
            current_obj = plan.get_node(objective_id)
            if current_phase == "actions" or is_specific_objective(current_obj.description):
                fallback_obj = plan.add_objective("Implement required changes", objective_id)
                plan.add_action(fallback_obj.id, "code_editor",
                               {"description": "Analyze and implement the required changes"},
                               "Fallback action due to command parsing failure")
                progress_made = True
                break
            else:
                refined_descriptions = refine_objective(current_obj.description, parent_context_str, main_goal, code_context)
                if refined_descriptions:
                    new_obj = plan.add_objective(refined_descriptions[0], objective_id)
                    print(f"DEBUG: Added refined objective: '{new_obj.description}'")
                    progress_made = True
                    break

    # Mark objective as completed
    plan.update_node_status(objective_id, STATUS_COMPLETED)
    print(f"DEBUG: Completed memory-augmented unfolding of objective {objective_id}")

    return progress_made


def _generate_memory_enhanced_prompt(main_goal: str, plan_context: str, code_context: str,
                                   command_history: list, session_id: str) -> str:
    """
    Generate a memory-enhanced prompt that incorporates historical planning patterns
    and context-aware command suggestions.
    """
    # Get memory-guided suggestions
    suggestions = planning_memory_interface.get_context_aware_command_suggestions(
        plan_context, command_history, main_goal
    )

    # Format suggestions for prompt
    suggestions_text = ""
    if suggestions:
        suggestions_text = "\nMEMORY-GUIDED SUGGESTIONS (use if LLM gets stuck):\n"
        for i, (cmd, conf) in enumerate(suggestions[:3], 1):
            suggestions_text += f"{i}. {cmd} (confidence: {conf:.2f})\n"

    # Add loop detection warning if applicable
    loop_warning = ""
    if planning_memory_interface.detect_loop_pattern(command_history, plan_context):
        loop_warning = "\n⚠️ LOOP DETECTION: Recent commands show repetitive patterns. Prioritize DONE or ADD_ACTION to break the loop.\n"

    # Check DONE confidence
    done_confidence = planning_memory_interface.should_attempt_done(plan_context, command_history)
    done_guidance = ""
    if done_confidence > 0.6:
        done_guidance = f"\n💡 MEMORY INSIGHT: High confidence ({done_confidence:.2f}) that DONE would be appropriate now.\n"

    return f"""{config.PLANNER_COMMAND_PROMPT_TEMPLATE}

{suggestions_text}{loop_warning}{done_guidance}

RECENT COMMAND HISTORY (last 5):
{chr(10).join(command_history[-5:])}

What is the single most important command to execute next to progress toward the goal?
Respond with ONLY the command, no explanations.
"""


def _apply_memory_guided_intervention(plan: PlanGraph, objective_id: str, main_goal: str,
                                    backpack: list, context_prefix: str, command_history: list,
                                    session_id: str) -> bool:
    """
    Apply memory-guided intervention when planning gets stuck in loops.
    Returns True if intervention succeeded.
    """
    print(f"DEBUG: Applying memory-guided intervention for objective {objective_id}")

    # Get strong memory suggestions
    plan_context = _generate_plan_context(plan)
    suggestions = planning_memory_interface.get_context_aware_command_suggestions(
        plan_context, command_history, main_goal
    )

    # Try top 3 memory suggestions
    for suggested_cmd, confidence in suggestions[:3]:
        if confidence > 0.7:  # Only high-confidence suggestions
            print(f"DEBUG: Trying high-confidence memory suggestion: {suggested_cmd} (conf: {confidence:.2f})")

            success, message = command_parser.parse_and_execute(
                suggested_cmd, plan,
                {'parent_id': objective_id, 'main_goal': main_goal}
            )

            planning_memory_interface.record_command_attempt(
                session_id, suggested_cmd, plan_context, success, True  # Mark as loop intervention
            )

            if success:
                print(f"DEBUG: Memory-guided intervention succeeded with: {suggested_cmd}")
                return True

    # Last resort: force DONE if memory suggests high confidence
    done_confidence = planning_memory_interface.should_attempt_done(plan_context, command_history)
    if done_confidence > 0.8:
        print(f"DEBUG: Forcing DONE command based on high memory confidence ({done_confidence:.2f})")
        success, message = command_parser.parse_and_execute(
            "DONE", plan,
            {'parent_id': objective_id, 'main_goal': main_goal}
        )
        return success

    print(f"DEBUG: Memory-guided intervention failed")
    return False