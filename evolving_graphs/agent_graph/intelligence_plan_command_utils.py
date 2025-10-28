import os  # File system operations for path handling
import re  # Regular expressions for command parsing
from typing import Dict, List, Optional, Tuple, Any
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED
from .intelligence_plan_objective_utils import is_specific_objective  # Objective specificity utilities


def _verify_command_grounding(command_desc: str, filename_to_path: dict, backpack_files: set) -> bool:
    """
    Verifies that the command description references actual files from the codebase.

    Args:
        command_desc (str): The command description to verify
        filename_to_path (dict): Mapping of filenames to paths
        backpack_files (set): Set of files available in the backpack context

    Returns:
        bool: True if the command is grounded in actual codebase files
    """
    import re
    # Look for file references in the command description
    file_refs = re.findall(r'evolving_graphs/\S+\.py', command_desc)
    if not file_refs:
        # Try broader pattern
        file_refs = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_/]*\.py\b', command_desc)

    for file_ref in file_refs:
        # Check if file exists in all_modules or backpack
        filename = os.path.basename(file_ref)
        if filename not in filename_to_path and file_ref not in backpack_files:
            return False
    return True


def _refine_command_for_grounding(original_desc: str, filename_to_path: dict, backpack_files: set) -> str:
    """
    Refines a command description to ensure it references actual codebase files.

    Args:
        original_desc (str): The original command description
        filename_to_path (dict): Mapping of filenames to paths
        backpack_files (set): Set of files available in the backpack context

    Returns:
        str: A refined command description grounded in actual files
    """
    # Find a relevant file from backpack or all_modules
    available_files = list(backpack_files) + list(filename_to_path.keys())
    if available_files:
        # Use the first available file as a fallback
        fallback_file = available_files[0]
        return f"Edit {fallback_file} to implement changes as described in: {original_desc}"
    return original_desc


class CommandParser:
    """
    Parses and executes commands from LLM responses for incremental plan building.
    Supports commands: ADD_OBJECTIVE, ADD_ACTION, EDIT_OBJECTIVE, EDIT_ACTION, LIST
    """

    def __init__(self):
        self.commands = {
            'ADD_OBJECTIVE': self._add_objective,
            'ADD_ACTION': self._add_action,
            'EDIT_OBJECTIVE': self._edit_objective,
            'EDIT_ACTION': self._edit_action,
            'LIST': self._list_plan,
            'DONE': self._done
        }

    def parse_and_execute(self, command_text: str, plan: PlanGraph, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Parses a command from LLM response and executes it on the plan.

        Args:
            command_text (str): The raw command text from LLM
            plan (PlanGraph): The plan graph to modify
            context (Dict[str, Any]): Context containing parent_id, main_goal, etc.

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Extract command and parameters using regex
            command_match = re.match(r'(\w+)\s*(.*)', command_text.strip(), re.IGNORECASE)
            if not command_match:
                return False, f"Invalid command format: {command_text}"

            command_name = command_match.group(1).upper()
            params_str = command_match.group(2).strip()

            if command_name not in self.commands:
                return False, f"Unknown command: {command_name}"

            # Execute the command
            return self.commands[command_name](params_str, plan, context)

        except Exception as e:
            return False, f"Command execution failed: {str(e)}"

    def _add_objective(self, params: str, plan: PlanGraph, context: Dict[str, Any]) -> Tuple[bool, str]:
        """ADD_OBJECTIVE <description> [-> <parent_id>]"""
        # Parse description and optional parent
        match = re.match(r'(.+?)(?:\s*->\s*(.+))?$', params)
        if not match:
            return False, "ADD_OBJECTIVE requires a description"

        description = match.group(1).strip()
        parent_id = match.group(2).strip() if match.group(2) else context.get('parent_id', plan.root_id)

        if parent_id not in plan.nodes:
            return False, f"Parent objective {parent_id} not found"

        # Check node children limit (max 4 children per node)
        parent_node = plan.nodes[parent_id]
        if hasattr(parent_node, 'children') and len(parent_node.children) >= 4:
            return False, f"Parent objective {parent_id} already has 4 children (maximum allowed). Cannot add more children."

        new_obj = plan.add_objective(description, parent_id)
        return True, f"Added objective '{description}' with ID {new_obj.id}"

    def _add_action(self, params: str, plan: PlanGraph, context: Dict[str, Any]) -> Tuple[bool, str]:
        """ADD_ACTION <objective_id> <role> <description> [justification]"""
        parts = params.split(' ', 3)
        if len(parts) < 3:
            return False, "ADD_ACTION requires objective_id, role, and description"

        obj_id = parts[0].strip()
        role = parts[1].strip()
        description = parts[2].strip()
        justification = parts[3].strip() if len(parts) > 3 else "Action added via command interface"

        if obj_id not in plan.nodes:
            return False, f"Objective {obj_id} not found"

        node = plan.nodes[obj_id]
        if not isinstance(node, ObjectiveNode):
            return False, f"Node {obj_id} is not an objective"

        # Enforce that actions are only added at leaf nodes with specific objectives
        if node.children:
            return False, f"Cannot add action to objective {obj_id} - it has child objectives. Actions only allowed at leaf nodes."

        # Check if the objective is specific enough for actions
        if not is_specific_objective(node.description):
            return False, f"Cannot add action to objective {obj_id} - objective must be specific (targeting particular functions/files) before allowing actions."

        action = plan.add_action(obj_id, role, {"description": description}, justification)
        return True, f"Added action '{description}' to objective {obj_id}"

    def _edit_objective(self, params: str, plan: PlanGraph, context: Dict[str, Any]) -> Tuple[bool, str]:
        """EDIT_OBJECTIVE <objective_id> <new_description>"""
        parts = params.split(' ', 1)
        if len(parts) < 2:
            return False, "EDIT_OBJECTIVE requires objective_id and new description"

        obj_id = parts[0].strip()
        new_desc = parts[1].strip()

        if obj_id not in plan.nodes:
            return False, f"Objective {obj_id} not found"

        node = plan.nodes[obj_id]
        if not isinstance(node, ObjectiveNode):
            return False, f"Node {obj_id} is not an objective"

        old_desc = node.description
        node.description = new_desc
        return True, f"Edited objective {obj_id}: '{old_desc}' -> '{new_desc}'"

    def _edit_action(self, params: str, plan: PlanGraph, context: Dict[str, Any]) -> Tuple[bool, str]:
        """EDIT_ACTION <action_id> <new_description> [new_justification]"""
        parts = params.split(' ', 2)
        if len(parts) < 2:
            return False, "EDIT_ACTION requires action_id and new description"

        action_id = parts[0].strip()
        new_desc = parts[1].strip()
        new_just = parts[2].strip() if len(parts) > 2 else None

        if action_id not in plan.nodes:
            return False, f"Action {action_id} not found"

        node = plan.nodes[action_id]
        if not isinstance(node, ActionNode):
            return False, f"Node {action_id} is not an action"

        old_desc = node.command.get("description", "")
        node.command["description"] = new_desc
        if new_just:
            node.justification = new_just

        return True, f"Edited action {action_id}: '{old_desc}' -> '{new_desc}'"

    def _list_plan(self, params: str, plan: PlanGraph, context: Dict[str, Any]) -> Tuple[bool, str]:
        """LIST [objectives|actions|all]"""
        filter_type = params.strip().lower() if params.strip() else "all"

        result = []
        if filter_type in ["objectives", "all"]:
            objectives = [node for node in plan.nodes.values() if isinstance(node, ObjectiveNode)]
            if objectives:
                result.append("OBJECTIVES:")
                for obj in objectives:
                    status = "✓" if obj.status == STATUS_COMPLETED else "○" if obj.status == STATUS_PENDING else "●"
                    result.append(f"  {status} {obj.id}: {obj.description}")
                    if obj.children:
                        result.append(f"    Children: {', '.join(obj.children)}")

        if filter_type in ["actions", "all"]:
            actions = [node for node in plan.nodes.values() if isinstance(node, ActionNode)]
            if actions:
                result.append("ACTIONS:")
                for action in actions:
                    result.append(f"  {action.id}: {action.command.get('description', 'No description')}")

        if not result:
            return True, "Plan is empty"

        return True, "\n".join(result)

    def _done(self, params: str, plan: PlanGraph, context: Dict[str, Any]) -> Tuple[bool, str]:
        """DONE: Signal completion of objective decomposition"""
        return True, "DONE"


# Global command parser instance
command_parser = CommandParser()