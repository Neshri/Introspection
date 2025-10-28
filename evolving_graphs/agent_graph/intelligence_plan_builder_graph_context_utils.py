from typing import Dict, List, Optional, Tuple, Any
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED


def _generate_plan_context(plan: PlanGraph) -> str:
    """Generate a textual representation of the current plan for LLM context."""
    lines = ["CURRENT PLAN STATE:"]
    objectives = [node for node in plan.nodes.values() if isinstance(node, ObjectiveNode)]
    actions = [node for node in plan.nodes.values() if isinstance(node, ActionNode)]

    if objectives:
        lines.append("OBJECTIVES:")
        for obj in objectives:
            status = "✓" if obj.status == STATUS_COMPLETED else "○" if obj.status == STATUS_PENDING else "●"
            lines.append(f"  {status} {obj.id}: {obj.description}")
            if obj.children:
                lines.append(f"    Children: {', '.join(obj.children)}")

    if actions:
        lines.append("ACTIONS:")
        for action in actions:
            lines.append(f"  {action.id} (parent: {action.parent_id}): {action.command.get('description', 'No description')}")

    return "\n".join(lines)