from typing import Dict, List, Optional, Tuple, Any
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED
from .intelligence_plan_objective_utils import is_specific_objective  # Objective specificity utilities
from .intelligence_llm_service import chat_llm  # LLM service for command interactions
from .intelligence_plan_command_utils import command_parser  # Command parser for plan modification
from .intelligence_plan_execution_utils import refine_objective
from .agent_config import config  # Configuration settings for model selection and prompt templates
from .intelligence_plan_builder_graph_context_utils import _generate_plan_context


def _unfold_objective_command_based(objective_id: str, main_goal: str, backpack: list, context_prefix: str, plan: PlanGraph) -> None:
    """Unfolds a single objective node using command-based LLM interaction for incremental plan building with enforced hierarchical decomposition."""
    objective = plan.get_node(objective_id)
    print(f"DEBUG: Starting command-based unfolding of objective {objective_id}: '{objective.description}'")

    # Build parent context by traversing up the hierarchy
    parent_context = []
    current_id = objective_id
    while current_id != plan.root_id:
        current_node = plan.get_node(current_id)
        parent_context.insert(0, current_node.description)
        current_id = current_node.parent_id
    parent_context_str = " -> ".join(parent_context) if parent_context else "Root Goal"

    # Build code context from backpack
    code_context_parts = []
    for item in backpack[:5]:  # Limit to first 5 items for context
        content = item.get("content", str(item))[:1000]  # Limit content length
        code_context_parts.append(content)
    code_context = "\n---\n".join(code_context_parts)

    # Generate plan context for LLM
    plan_context = _generate_plan_context(plan)

    # Use command-based prompt to get next step
    prompt = config.PLANNER_COMMAND_PROMPT_TEMPLATE.format(
        goal=main_goal,
        plan_context=plan_context,
        code_context=code_context
    )

    max_commands = 15  # Increased limit for more complex hierarchical decomposition
    command_count = 0
    objective_decomposition_done = False

    # State tracking for hierarchical enforcement
    current_phase = "objectives"  # Start with objective building phase

    while command_count < max_commands:
        command_count += 1
        print(f"DEBUG: Requesting command {command_count} for objective {objective_id} (phase: {current_phase})")

        # Display plan every 10th command
        if command_count % 10 == 0:
            print(f"DEBUG: Plan state after {command_count} commands:")
            list_success, list_message = command_parser.parse_and_execute("LIST", plan, {'parent_id': objective_id, 'main_goal': main_goal})
            if list_success:
                print(list_message)
            else:
                print(f"DEBUG: Failed to list plan: {list_message}")

        llm_response = chat_llm(prompt)
        print(f"DEBUG: LLM command response: '{llm_response}'")

        # Parse the command to check validity before execution
        command_text = llm_response.strip()
        import re
        command_match = re.match(r'(\w+)\s*(.*)', command_text, re.IGNORECASE)
        if not command_match:
            print(f"DEBUG: Invalid command format, skipping")
            continue

        command_name = command_match.group(1).upper()

        # Enforce hierarchical decomposition rules
        if current_phase == "objectives":
            # Only allow ADD_OBJECTIVE, EDIT_OBJECTIVE, LIST, DONE in objectives phase
            if command_name not in ['ADD_OBJECTIVE', 'EDIT_OBJECTIVE', 'LIST', 'DONE']:
                print(f"DEBUG: Invalid command '{command_name}' in objectives phase, only ADD_OBJECTIVE, EDIT_OBJECTIVE, LIST, DONE allowed")
                continue
            # Check if objective is specific enough for actions
            if command_name == 'ADD_ACTION':
                current_obj = plan.get_node(objective_id)
                if not is_specific_objective(current_obj.description):
                    print(f"DEBUG: Objective '{current_obj.description}' not specific enough for actions, adding ADD_OBJECTIVE instead")
                    # Force ADD_OBJECTIVE by refining the current objective
                    refined_descriptions = refine_objective(current_obj.description, parent_context_str, main_goal, code_context)
                    if refined_descriptions:
                        new_obj = plan.add_objective(refined_descriptions[0], objective_id)
                        print(f"DEBUG: Added refined objective: '{new_obj.description}'")
                        continue
                    else:
                        continue
                else:
                    # Objective is specific, allow ADD_ACTION
                    current_phase = "actions"
        elif current_phase == "actions":
            # In actions phase, allow all commands
            pass

        # Execute the command
        success, message = command_parser.parse_and_execute(command_text, plan, {
            'parent_id': objective_id,
            'main_goal': main_goal
        })

        print(f"DEBUG: Command execution result: {success} - {message}")

        # Check for DONE command to transition to actions phase
        if command_name == 'DONE' and success:
            objective_decomposition_done = True
            current_phase = "actions"
            print(f"DEBUG: Objective decomposition marked as DONE, transitioning to actions phase")

        if not success:
            print(f"DEBUG: Command failed, trying fallback approach")
            # Fallback: add a basic sub-objective and action (only if in actions phase or objective is specific)
            current_obj = plan.get_node(objective_id)
            if current_phase == "actions" or is_specific_objective(current_obj.description):
                fallback_obj = plan.add_objective("Implement required changes", objective_id)
                plan.add_action(fallback_obj.id, "code_editor",
                               {"description": "Analyze and implement the required changes"},
                               "Fallback action due to command parsing failure")
                break
            else:
                # Still in objectives phase, try to refine objective
                refined_descriptions = refine_objective(current_obj.description, parent_context_str, main_goal, code_context)
                if refined_descriptions:
                    new_obj = plan.add_objective(refined_descriptions[0], objective_id)
                    print(f"DEBUG: Added refined objective: '{new_obj.description}'")
                break

        # Check if we should continue based on current phase and pending objectives
        if current_phase == "objectives":
            # In objectives phase, continue until DONE or no more pending objectives
            pending_objectives = [node_id for node_id, node in plan.nodes.items()
                                 if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children]
            if not pending_objectives or objective_decomposition_done:
                print(f"DEBUG: Objectives phase complete (DONE received or no pending objectives)")
                current_phase = "actions"
                objective_decomposition_done = True  # Ensure we transition
        elif current_phase == "actions":
            # In actions phase, continue until specific conditions met
            # Check if leaf objectives now have actions or are specific enough
            leaf_objectives = [node_id for node_id, node in plan.nodes.items()
                              if isinstance(node, ObjectiveNode) and not node.children]
            actions_exist = any(isinstance(node, ActionNode) and node.parent_id in leaf_objectives for node in plan.nodes.values())
            if actions_exist:
                print(f"DEBUG: Actions added to leaf objectives, completing unfolding")
                break

    # Mark objective as completed
    plan.update_node_status(objective_id, STATUS_COMPLETED)
    print(f"DEBUG: Completed command-based unfolding of objective {objective_id} with hierarchical enforcement")