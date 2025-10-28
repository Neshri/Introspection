import os  # File system operations for path handling
from typing import Dict, List, Optional, Tuple, Any
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED
from .intelligence_plan_validation_utils import validate_and_correct_plan, _correct_file_references_in_text


def refine_plan_with_validations(plan: PlanGraph, backpack: list[dict], project_root: str) -> PlanGraph:
    """
    Refines the plan with comprehensive validations and corrections.

    Args:
        plan (PlanGraph): The plan to refine
        backpack (list[dict]): The backpack context
        project_root (str): The project root directory

    Returns:
        PlanGraph: The refined plan
    """
    # Step 4: Action Node Verification and Correction
    # Verify and correct action nodes for validity (e.g., file references, command structure)
    filename_to_path = {}
    from .utils_collect_modules import collect_modules
    all_modules = collect_modules(project_root)
    for module_name, path in all_modules.items():
        filename = os.path.basename(path)
        filename_to_path[filename] = path
        filename_to_path[filename.replace('.py', '')] = path

    # Also include backpack file references for grounding
    backpack_files = set()
    for item in backpack:
        if "path" in item:
            backpack_files.add(item["path"])
        elif "file_path" in item:
            backpack_files.add(item["file_path"])

    print(f"DEBUG: Starting action node verification and correction for {len([n for n in plan.nodes.values() if isinstance(n, ActionNode)])} action nodes")
    verified_actions = 0
    corrected_actions = 0
    for node in plan.nodes.values():
        if isinstance(node, ActionNode):
            # Correct file references in command description and justification
            original_desc = node.command.get("description", "")
            if "description" in node.command:
                corrected_desc = _correct_file_references_in_text(original_desc, filename_to_path, project_root)
                node.command["description"] = corrected_desc
                if corrected_desc != original_desc:
                    print(f"DEBUG: Corrected file references in action {node.id}: '{original_desc[:100]}...' -> '{corrected_desc[:100]}...'")
                    corrected_actions += 1
                # Verify the description references actual codebase files
                from .intelligence_plan_command_utils import _verify_command_grounding, _refine_command_for_grounding
                if not _verify_command_grounding(node.command["description"], filename_to_path, backpack_files):
                    print(f"DEBUG: Action node {node.id} command not grounded in codebase, refining...")
                    refined_desc = _refine_command_for_grounding(original_desc, filename_to_path, backpack_files)
                    node.command["description"] = refined_desc
                    print(f"DEBUG: Refined ungrounded command to: '{refined_desc}'")
            original_justification = node.justification
            corrected_justification = _correct_file_references_in_text(node.justification, filename_to_path, project_root)
            node.justification = corrected_justification
            if corrected_justification != original_justification:
                print(f"DEBUG: Corrected file references in justification for action {node.id}")
                corrected_actions += 1
            verified_actions += 1
    print(f"DEBUG: Verified and corrected {verified_actions} action nodes, {corrected_actions} had reference corrections")

    # Step 5: Ensure PlanGraph has multiple nodes, is hierarchical, acyclic, and contains clear actionable commands
    total_nodes = len(plan.nodes)
    objective_nodes = sum(1 for node in plan.nodes.values() if isinstance(node, ObjectiveNode))
    action_nodes = sum(1 for node in plan.nodes.values() if isinstance(node, ActionNode))

    print(f"DEBUG: Final plan has {total_nodes} total nodes ({objective_nodes} objectives, {action_nodes} actions)")

    # Ensure minimum structure: at least 2 objectives and 2 actions for proper hierarchy
    if objective_nodes < 2 or action_nodes < 2:
        print("DEBUG: Plan lacks proper hierarchy, enhancing structure")
        if objective_nodes < 2:
            print("DEBUG: Adding minimum objectives for proper hierarchy")
            sub_obj1 = plan.add_objective("Analyze codebase and requirements", plan.root_id)
            sub_obj2 = plan.add_objective("Implement necessary changes", plan.root_id)
            print(f"DEBUG: Added objectives: '{sub_obj1.description}' and '{sub_obj2.description}'")
            # Add actions to each sub-objective
            if backpack:
                sample_file = backpack[0].get("path", backpack[0].get("file_path", "unknown_file.py"))
                plan.add_action(sub_obj1.id, "code_editor",
                               {"description": f"Review {sample_file} and understand current implementation"},
                               "Analysis action to ground understanding")
                print(f"DEBUG: Added analysis action for {sample_file}")
            plan.add_action(sub_obj2.id, "code_editor",
                           {"description": "Apply modifications to achieve the goal"},
                           "Implementation action for changes")
            print("DEBUG: Added implementation action")

    # Enhanced acyclicity check - verify no cycles in the graph
    print("DEBUG: Performing acyclicity verification")
    from .intelligence_plan_builder_core_utils import Planner  # Planner class moved from intelligence_plan_creation_utils (split for token limit)
    planner = Planner(None)  # We don't need memory for this check
    acyclic = planner._verify_graph_acyclicity(plan)
    if not acyclic:
        print("DEBUG: WARNING - Plan contains cycles, attempting to repair")
        # Simple repair: break any self-references
        for node in plan.nodes.values():
            if isinstance(node, ObjectiveNode) and node.id in node.children:
                node.children.remove(node.id)
                print(f"DEBUG: Removed self-reference from node {node.id}")
    else:
        print("DEBUG: Plan graph is acyclic")

    # Verify all ActionNode commands have clear, actionable descriptions
    print("DEBUG: Verifying action node command clarity")
    clear_commands = 0
    for node in plan.nodes.values():
        if isinstance(node, ActionNode):
            desc = node.command.get("description", "")
            if desc and len(desc.strip()) > 10 and "edit" in desc.lower():
                clear_commands += 1
            else:
                # Enhance unclear commands
                if not desc or len(desc.strip()) < 10:
                    original_justification = node.justification
                    node.command["description"] = f"Edit relevant codebase files to {node.justification.lower()}"
                    print(f"DEBUG: Enhanced unclear command for action {node.id}: '{original_justification[:100]}...' -> '{node.command['description']}'")
    print(f"DEBUG: Verified {clear_commands} action nodes have clear commands")

    return plan