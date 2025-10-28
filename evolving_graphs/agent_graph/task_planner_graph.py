from dataclasses import dataclass, field
from typing import List, Dict, Any, Union, Literal
import uuid

# --- Define Status Constants for consistency ---
STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

# --- Define the Node Structures ---

@dataclass
class ActionNode:
    """Represents a single, concrete task for a specific role."""
    id: str = field(default_factory=lambda: f"act_{uuid.uuid4().hex[:8]}")
    parent_id: str = ""
    status: Literal["pending", "completed", "failed"] = STATUS_PENDING
    role: str = ""  # The role responsible, e.g., 'scout', 'code_editor'
    command: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    justification: str = ""

@dataclass
class ObjectiveNode:
    """Represents an abstract goal or sub-goal."""
    id: str = field(default_factory=lambda: f"obj_{uuid.uuid4().hex[:8]}")
    parent_id: str | None = None
    status: Literal["pending", "in_progress", "completed", "failed"] = STATUS_PENDING
    description: str = ""
    children: List[str] = field(default_factory=list)

# --- The Main Graph Implementation ---

class PlanGraph:
    """
    A stateful, acyclic graph representing the agent's strategy and progress.
    It is passed between roles to provide context and track the mission.
    """

    def __init__(self, root_objective: str):
        """Initializes the graph with a root objective."""
        self.nodes: Dict[str, Union[ObjectiveNode, ActionNode]] = {}
        root_node = ObjectiveNode(description=root_objective, status=STATUS_PENDING)
        self.root_id = root_node.id
        self._add_node_internal(root_node)

    def _add_node_internal(self, node: Union[ObjectiveNode, ActionNode]):
        """Internal method to add a node to the graph's dictionary."""
        if node.id in self.nodes:
            raise ValueError(f"Node with ID {node.id} already exists.")
        self.nodes[node.id] = node

    def get_node(self, node_id: str) -> Union[ObjectiveNode, ActionNode]:
        """Retrieves a node by its ID."""
        if node_id not in self.nodes:
            raise KeyError(f"Node with ID {node_id} not found.")
        return self.nodes[node_id]

    def add_objective(self, description: str, parent_id: str) -> ObjectiveNode:
        """Adds a new ObjectiveNode as a child of an existing node."""
        parent_node = self.get_node(parent_id)
        if not isinstance(parent_node, ObjectiveNode):
            raise TypeError("Only ObjectiveNodes can have children.")
        
        new_node = ObjectiveNode(description=description, parent_id=parent_id)
        self._add_node_internal(new_node)
        parent_node.children.append(new_node.id)
        return new_node

    def add_action(self, parent_id: str, role: str, command: Dict, justification: str) -> ActionNode:
        """Adds a new ActionNode as a child of an ObjectiveNode."""
        parent_node = self.get_node(parent_id)
        if not isinstance(parent_node, ObjectiveNode):
            raise TypeError("Only ObjectiveNodes can have children.")
            
        new_node = ActionNode(parent_id=parent_id, role=role, command=command, justification=justification)
        self._add_node_internal(new_node)
        parent_node.children.append(new_node.id)
        return new_node
        
    def update_node_status(self, node_id: str, status: str):
        """Updates the status of any node."""
        node = self.get_node(node_id)
        node.status = status

    def update_action_result(self, action_id: str, result: Any):
        """Updates the result of an ActionNode and sets its status to completed."""
        node = self.get_node(action_id)
        if not isinstance(node, ActionNode):
            raise TypeError(f"Node {action_id} is not an ActionNode.")
        node.result = result
        self.update_node_status(action_id, STATUS_COMPLETED)

    # --- Methods for the Orchestrator ---

    def contains_task_for_role(self, role: str) -> bool:
        """
        Checks if there are any pending actions for a specific role.
        """
        for node in self.nodes.values():
            if isinstance(node, ActionNode) and node.role == role and node.status == STATUS_PENDING:
                return True
        return False

    def get_pending_actions_for_role(self, role: str) -> List[ActionNode]:
        """
        Returns a list of all pending ActionNodes for a given role.
        """
        tasks = []
        for node in self.nodes.values():
            if isinstance(node, ActionNode) and node.role == role and node.status == STATUS_PENDING:
                tasks.append(node)
        return tasks

    def display(self):
        """Prints a human-readable representation of the graph."""
        print("--- Plan Graph ---")
        self._display_recursive(self.root_id, 0)
        print("------------------")

    def _display_recursive(self, node_id: str, indent: int):
        """Helper for recursively printing the graph structure."""
        node = self.get_node(node_id)
        prefix = "  " * indent
        
        if isinstance(node, ObjectiveNode):
            print(f"{prefix}🎯 [Objective] {node.description} (ID: {node.id}, Status: {node.status})")
            for child_id in node.children:
                self._display_recursive(child_id, indent + 1)
        elif isinstance(node, ActionNode):
            print(f"{prefix}⚡️ [Action] Role: {node.role}, Justification: {node.justification} (ID: {node.id}, Status: {node.status})")

