from typing import Dict, List, Optional, Tuple, Any
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED


def _verify_graph_acyclicity(plan: PlanGraph) -> bool:
    """
    Performs a comprehensive acyclicity check on the plan graph.

    Args:
        plan (PlanGraph): The plan graph to verify

    Returns:
        bool: True if the graph is acyclic
    """
    def has_cycle(node_id: str, visited: set, rec_stack: set) -> bool:
        visited.add(node_id)
        rec_stack.add(node_id)

        node = plan.get_node(node_id)
        if isinstance(node, ObjectiveNode):
            for child_id in node.children:
                if child_id not in visited:
                    if has_cycle(child_id, visited, rec_stack):
                        return True
                elif child_id in rec_stack:
                    return True

        rec_stack.remove(node_id)
        return False

    visited = set()
    rec_stack = set()

    for node_id in plan.nodes:
        if node_id not in visited:
            if has_cycle(node_id, visited, rec_stack):
                return False
    return True