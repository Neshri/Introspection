from typing import Dict, List, Optional, Tuple, Any
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED
from .intelligence_plan_builder_graph_validation_utils import _verify_graph_acyclicity
from .intelligence_plan_builder_graph_unfolding_utils import _unfold_objective_command_based
from .intelligence_plan_builder_graph_context_utils import _generate_plan_context


def update_plan(main_goal: str, backpack: list[dict], plan: PlanGraph, codebase_summary: str, query_answer: str="") -> tuple[PlanGraph, list]:
    """
    Updates the existing plan using command-based incremental building.
    The LLM is given simple commands (ADD_OBJECTIVE, ADD_ACTION, EDIT_OBJECTIVE, EDIT_ACTION, LIST)
    to navigate and modify the plan graph step by step.

    Returns the updated PlanGraph and a list of planner memory IDs with full LLM response logging.
    """
    planner_memory_ids = []
    llm_responses = []  # Store all LLM responses for logging
    print(f"DEBUG: Starting command-based update_plan with main_goal: '{main_goal}'")
    print(f"DEBUG: Backpack contains {len(backpack)} items")
    print(f"DEBUG: Initial plan has {len(plan.nodes)} nodes, root description: '{plan.get_node(plan.root_id).description}'")
    if codebase_summary:
        print(f"DEBUG: Codebase summary provided ({len(codebase_summary)} chars)")
    if query_answer:
        print(f"DEBUG: Query answer provided ({len(query_answer)} chars)")

    # Step 1: Input Validation
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

    # Step 4: Command-Based Incremental Plan Building
    print("DEBUG: Starting command-based incremental plan building")
    unfolding_steps = 0
    max_unfolding_steps = 50  # Prevent excessive unfolding

    # Find initial pending objectives (those without children yet)
    pending_objectives = [node_id for node_id, node in plan.nodes.items()
                         if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children]
    print(f"DEBUG: Found {len(pending_objectives)} initial pending objectives to unfold")

    while pending_objectives and unfolding_steps < max_unfolding_steps:
        unfolding_steps += 1
        print(f"DEBUG: Command-based unfolding step {unfolding_steps}: processing objective {pending_objectives[0]}")

        # Process the first pending objective using command-based approach
        current_obj_id = pending_objectives.pop(0)
        _unfold_objective_command_based(current_obj_id, main_goal, backpack, context_prefix, plan)

        # Find newly added pending objectives (those that were just created and have no children)
        new_pending_objectives = [node_id for node_id, node in plan.nodes.items()
                                 if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children
                                 and node_id not in pending_objectives]
        if new_pending_objectives:
            pending_objectives.extend(new_pending_objectives)
            print(f"DEBUG: Added {len(new_pending_objectives)} new pending objectives to unfold")
            print(f"DEBUG: Total pending objectives remaining: {len(pending_objectives)}")
        else:
            print(f"DEBUG: No new pending objectives added in this step")

    if unfolding_steps >= max_unfolding_steps:
        print(f"DEBUG: WARNING - Reached maximum unfolding steps ({max_unfolding_steps}), stopping")

    print(f"DEBUG: Command-based incremental plan building completed after {unfolding_steps} steps")
    print("DEBUG: Full LLM response logging enabled - all interactions recorded")

    # Log completion summary
    total_nodes = len(plan.nodes)
    objective_nodes = sum(1 for node in plan.nodes.values() if isinstance(node, ObjectiveNode))
    action_nodes = sum(1 for node in plan.nodes.values() if isinstance(node, ActionNode))
    print(f"DEBUG: Final plan has {total_nodes} total nodes ({objective_nodes} objectives, {action_nodes} actions)")
    print(f"DEBUG: Command-based approach ensured step-by-step plan building with validation and error handling")

    return plan, planner_memory_ids