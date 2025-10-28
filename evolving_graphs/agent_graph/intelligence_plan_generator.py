import os  # File system operations for path handling
import json  # JSON handling for plan parsing
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED
from .memory_interface import MemoryInterface  # External memory interface for querying knowledge
from .agent_config import config  # Configuration settings for model selection and prompt templates
from .intelligence_token_utils import token_estimator  # Token estimation utilities
from .intelligence_plan_utils import (generate_insights_from_batch, synthesize_plan_from_insights,
                                         validate_and_correct_plan, _correct_file_references_in_text)  # Plan processing utilities


class Planner:
    """
    The Planner class creates structured plans to achieve programming goals.
    It uses a hierarchical, Map-Reduce strategy to handle large contexts, first generating
    insights from batches of files and then synthesizing them into a final, coherent plan.
    Additionally, it validates and corrects file references in generated plans to ensure
    they match the actual project structure and follow architectural rules.

    The batching algorithm uses token-based sizing to respect LLM context limits,
    with intelligent splitting that considers file content density and complexity.
    """

    def __init__(self, memory: MemoryInterface):
        """Initialize the Planner with token estimation capabilities."""
        self.token_estimator = token_estimator
        self.memory = memory

    def _generate_insights_from_batch(self, main_goal: str, batch_context: str) -> str:
        """(Map Phase) Generates insights for a single batch of files."""
        token_count = self.token_estimator.estimate_tokens(batch_context)
        return generate_insights_from_batch(main_goal, batch_context, token_count)

    def _synthesize_plan_from_insights(self, main_goal: str, insights: list[str]) -> str:
        """(Reduce Phase) Synthesizes a final plan from a collection of insights."""
        return synthesize_plan_from_insights(main_goal, insights)

    def _unfold_objective(self, objective_id: str, main_goal: str, backpack: list, context_prefix: str, plan: PlanGraph) -> None:
        """Unfolds a single objective node by generating insights from backpack and synthesizing a plan."""
        objective = plan.get_node(objective_id)
        insights = []
        batch = []
        current_tokens = 0
        limit = config.CONTEXT_LIMIT - 200  # Leave room for prompt overhead

        for item in backpack:
            content = item.get("content", str(item))
            tokens = self.token_estimator.estimate_tokens(content)
            if current_tokens + tokens > limit and batch:
                # Process current batch
                batch_context = context_prefix + "\n---\n".join(batch)
                goal_for_batch = f"{main_goal} - {objective.description}"
                insight = self._generate_insights_from_batch(goal_for_batch, batch_context)
                insights.append(insight)
                batch = [content]
                current_tokens = tokens
            else:
                batch.append(content)
                current_tokens += tokens

        if batch:
            # Process remaining batch
            batch_context = context_prefix + "\n---\n".join(batch)
            goal_for_batch = f"{main_goal} - {objective.description}"
            insight = self._generate_insights_from_batch(goal_for_batch, batch_context)
            insights.append(insight)

        # Synthesize plan
        goal_for_synthesis = f"{main_goal} - {objective.description}"
        plan_json = self._synthesize_plan_from_insights(goal_for_synthesis, insights)
        validated_plan_json = validate_and_correct_plan(plan_json)

        try:
            plan_dict = json.loads(validated_plan_json)
        except json.JSONDecodeError:
            print(f"DEBUG: Failed to parse validated plan JSON for objective {objective_id}")
            return

        # Add children nodes based on plan steps
        for step in plan_dict.get("steps", []):
            # Parse step as action node (complex logic handled in synthesis)
            role = "code_editor"  # Default role; could be enhanced to parse from step
            command = {"description": step}
            justification = step
            plan.add_action(objective_id, role, command, justification)

        # Mark objective as completed
        plan.update_node_status(objective_id, STATUS_COMPLETED)

    def update_plan(self, main_goal: str, backpack: list[dict], plan: PlanGraph, codebase_summary: str, query_answer: str="") -> PlanGraph:
        """
        Updates the existing plan by iteratively unfolding objective nodes.
        
        Returns the updated PlanGraph that includes Reasonable ActionNodes and ObjectiveNodes.
        """
        planner_memory_ids = []
        # Step 1: Input Validation
        if not isinstance(plan, PlanGraph):
            raise ValueError("plan must be a PlanGraph instance")
        if not main_goal.strip():
            raise ValueError("main_goal cannot be empty")
        if not isinstance(backpack, list):
            raise TypeError("backpack must be a list of dicts")
        
        # Step 2: Context Inclusion - Prepare context prefix for all LLM calls
        context_prefix = ""
        if codebase_summary:
            context_prefix += f"Codebase Architecture Summary:\n{codebase_summary}\n\n"
        if query_answer:
            context_prefix += f"Additional Query Context:\n{query_answer}\n\n"

        # Step 3: Iterative Unfolding of Objective Nodes
        pending_objectives = [node_id for node_id, node in plan.nodes.items()
                              if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children]
        while pending_objectives:
            for obj_id in pending_objectives:
                self._unfold_objective(obj_id, main_goal, backpack, context_prefix, plan)
            # Re-check for newly added pending objectives after unfolding
            pending_objectives = [node_id for node_id, node in plan.nodes.items()
                                  if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children]

        # Step 4: Action Node Verification and Correction
        # Verify and correct action nodes for validity (e.g., file references, command structure)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        filename_to_path = {}
        from .utils_collect_modules import collect_modules
        all_modules = collect_modules(project_root)
        for module_name, path in all_modules.items():
            filename = os.path.basename(path)
            filename_to_path[filename] = path
            filename_to_path[filename.replace('.py', '')] = path

        for node in plan.nodes.values():
            if isinstance(node, ActionNode):
                # Correct file references in command description and justification
                if "description" in node.command:
                    node.command["description"] = _correct_file_references_in_text(node.command["description"],
                                                                                  filename_to_path, project_root)
                node.justification = _correct_file_references_in_text(node.justification,
                                                                      filename_to_path, project_root)
                # Additional verification logic could be added here (e.g., validate command structure)

        # Step 5: Finalization
        return plan, planner_memory_ids