from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Union, Literal
import uuid

# --- Define Custom Exceptions ---
class PlanGraphError(Exception):
    """Base exception for PlanGraph-related errors."""
    pass

class InvalidStatusTransition(PlanGraphError):
    """Raised when an invalid status transition is attempted."""
    pass

class NodeNotFound(PlanGraphError):
    """Raised when a requested node is not found."""
    pass

class ConsistencyError(PlanGraphError):
    """Raised when graph consistency validation fails."""
    pass

# --- Define Status Constants for consistency ---
STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

# --- Allowed Status Transitions ---
ALLOWED_TRANSITIONS_OBJ = {
    STATUS_PENDING: [STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_FAILED],
    STATUS_IN_PROGRESS: [STATUS_COMPLETED, STATUS_FAILED],
    STATUS_COMPLETED: [],
    STATUS_FAILED: [],
}

ALLOWED_TRANSITIONS_ACT = {
    STATUS_PENDING: [STATUS_COMPLETED, STATUS_FAILED],
    STATUS_COMPLETED: [],
    STATUS_FAILED: [],
}

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
            raise PlanGraphError(f"Node with ID {node.id} already exists.")
        self.nodes[node.id] = node

    def get_node(self, node_id: str) -> Union[ObjectiveNode, ActionNode]:
        """Retrieves a node by its ID."""
        if node_id not in self.nodes:
            raise NodeNotFound(f"Node with ID {node_id} not found.")
        return self.nodes[node_id]

    def add_objective(self, description: str, parent_id: str) -> ObjectiveNode:
        """Adds a new ObjectiveNode as a child of an existing node."""
        parent_node = self.get_node(parent_id)
        if not isinstance(parent_node, ObjectiveNode):
            raise PlanGraphError("Only ObjectiveNodes can have children.")

        new_node = ObjectiveNode(description=description, parent_id=parent_id)
        self._add_node_internal(new_node)
        parent_node.children.append(new_node.id)
        return new_node

    def add_action(self, parent_id: str, role: str, command: Dict, justification: str) -> ActionNode:
        """Adds a new ActionNode as a child of an ObjectiveNode."""
        parent_node = self.get_node(parent_id)
        if not isinstance(parent_node, ObjectiveNode):
            raise PlanGraphError("Only ObjectiveNodes can have children.")

        new_node = ActionNode(parent_id=parent_id, role=role, command=command, justification=justification)
        self._add_node_internal(new_node)
        parent_node.children.append(new_node.id)
        return new_node
        
    def update_node_status(self, node_id: str, status: str):
        """Updates the status of any node with transition validation."""
        node = self.get_node(node_id)
        if node.status == status:
            return  # No change needed

        # Validate transition
        allowed_transitions = ALLOWED_TRANSITIONS_OBJ if isinstance(node, ObjectiveNode) else ALLOWED_TRANSITIONS_ACT
        if status not in allowed_transitions.get(node.status, []):
            raise InvalidStatusTransition(f"Invalid status transition from '{node.status}' to '{status}' for node {node_id}")

        node.status = status

    def update_action_result(self, action_id: str, result: Any):
        """Updates the result of an ActionNode and sets its status to completed."""
        node = self.get_node(action_id)
        if not isinstance(node, ActionNode):
            raise PlanGraphError(f"Node {action_id} is not an ActionNode.")
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

    # --- Consistency Validation ---

    def validate_consistency(self):
        """Validates the graph's structural consistency."""
        self._validate_node_references()
        self._validate_status_consistency()
        self._validate_graph_acyclicity()

    def _validate_node_references(self):
        """Validates that all node references are valid."""
        for node in self.nodes.values():
            if isinstance(node, ObjectiveNode):
                for child_id in node.children:
                    if child_id not in self.nodes:
                        raise ConsistencyError(f"ObjectiveNode {node.id} references non-existent child {child_id}")
                    child = self.nodes[child_id]
                    if child.parent_id != node.id:
                        raise ConsistencyError(f"Node {child_id} has inconsistent parent reference")

    def _validate_status_consistency(self):
        """Validates that status values are consistent with node types."""
        for node in self.nodes.values():
            if isinstance(node, ObjectiveNode):
                if node.status not in ALLOWED_TRANSITIONS_OBJ:
                    raise ConsistencyError(f"ObjectiveNode {node.id} has invalid status '{node.status}'")
            elif isinstance(node, ActionNode):
                if node.status not in ALLOWED_TRANSITIONS_ACT:
                    raise ConsistencyError(f"ActionNode {node.id} has invalid status '{node.status}'")

    def _validate_graph_acyclicity(self):
        """Validates that the graph has no cycles."""
        visited = set()
        rec_stack = set()

        def has_cycle(node_id):
            visited.add(node_id)
            rec_stack.add(node_id)
            node = self.nodes[node_id]

            if isinstance(node, ObjectiveNode):
                for child_id in node.children:
                    if child_id not in visited:
                        if has_cycle(child_id):
                            return True
                    elif child_id in rec_stack:
                        return True

            rec_stack.remove(node_id)
            return False

        if has_cycle(self.root_id):
            raise ConsistencyError("Graph contains cycles")

    # --- Analysis Utilities ---

    def get_statistics(self) -> Dict[str, Any]:
        """Returns statistical information about the graph."""
        total_objectives = sum(1 for node in self.nodes.values() if isinstance(node, ObjectiveNode))
        total_actions = sum(1 for node in self.nodes.values() if isinstance(node, ActionNode))

        status_counts = {
            "objectives": {
                STATUS_PENDING: 0,
                STATUS_IN_PROGRESS: 0,
                STATUS_COMPLETED: 0,
                STATUS_FAILED: 0,
            },
            "actions": {
                STATUS_PENDING: 0,
                STATUS_COMPLETED: 0,
                STATUS_FAILED: 0,
            }
        }

        for node in self.nodes.values():
            if isinstance(node, ObjectiveNode):
                status_counts["objectives"][node.status] += 1
            elif isinstance(node, ActionNode):
                status_counts["actions"][node.status] += 1

        return {
            "total_nodes": len(self.nodes),
            "total_objectives": total_objectives,
            "total_actions": total_actions,
            "status_counts": status_counts,
            "completion_rate": (status_counts["objectives"][STATUS_COMPLETED] + status_counts["actions"][STATUS_COMPLETED]) / len(self.nodes) if self.nodes else 0,
        }

    def get_pending_objectives(self) -> List[ObjectiveNode]:
        """Returns all pending objective nodes."""
        return [node for node in self.nodes.values()
                if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING]

    def get_completed_actions(self) -> List[ActionNode]:
        """Returns all completed action nodes."""
        return [node for node in self.nodes.values()
                if isinstance(node, ActionNode) and node.status == STATUS_COMPLETED]

    def to_json(self) -> Dict[str, Any]:
        """Serializes the PlanGraph to a JSON-compatible dictionary for pipeline integration."""
        nodes_data = {}
        for node_id, node in self.nodes.items():
            node_dict = asdict(node)
            # Convert result to string if it's not JSON-serializable
            if isinstance(node, ActionNode) and node.result is not None:
                try:
                    import json
                    json.dumps(node.result)  # Test serialization
                    node_dict['result'] = node.result
                except (TypeError, ValueError):
                    node_dict['result'] = str(node.result)
            nodes_data[node_id] = node_dict

        return {
            "root_id": self.root_id,
            "nodes": nodes_data,
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'PlanGraph':
        """Deserializes a PlanGraph from a JSON-compatible dictionary."""
        graph = cls.__new__(cls)  # Create without __init__
        graph.nodes = {}
        graph.root_id = data["root_id"]

        for node_id, node_data in data["nodes"].items():
            node_type = node_data.pop("type", None)  # Assuming we add type info, but for now infer from keys
            if "children" in node_data:
                node = ObjectiveNode(**node_data)
            else:
                node = ActionNode(**node_data)
            graph.nodes[node_id] = node

        return graph

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

