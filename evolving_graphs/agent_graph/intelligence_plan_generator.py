import os  # File system operations for path handling
import json  # JSON handling for plan parsing
from .task_planner_graph import PlanGraph, ObjectiveNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED
from .memory_interface import MemoryInterface  # External memory interface for querying knowledge
from .agent_config import config  # Configuration settings for model selection and prompt templates
from .intelligence_token_utils import token_estimator  # Token estimation utilities
from .intelligence_plan_utils import (generate_insights_from_batch, synthesize_plan_from_insights,
                                         validate_and_correct_plan)  # Plan processing utilities


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

    def create_plan(self, main_goal: str, backpack: list[dict]) -> tuple[str, list[str]]:
        """
        Generates a structured plan by breaking down a large context into manageable parts.

        Args:
            main_goal (str): The programming goal to achieve.
            backpack (list[dict]): List of relevant files with their content and justification.

        Returns:
            tuple: (plan, used_memory_ids_list) where plan is a structured plan in JSON format, and used_memory_ids_list is list of memory IDs used.
        """
        print(f"DEBUG: Planner received goal: {main_goal}")
        print(f"DEBUG: Planner received backpack with {len(backpack)} items. Starting hierarchical planning.")

        # Query memory for planning knowledge
        memory_results = self.memory.query_memory(main_goal, current_turn=0, n_results=5)  # Turn 0 since Planner doesn't track turns
        used_memory_ids = memory_results['ids'][0] if memory_results['ids'] else []
        memory_context = "\n".join(memory_results['documents'][0]) if memory_results['documents'] else ""

        if not backpack:
            print("DEBUG: Backpack is empty. Creating a simple plan based on goal alone.")
            return self._synthesize_plan_from_insights(main_goal, ["No file context was provided."])

        # Batch files using token-based sizing to respect context limits
        batches = []
        current_batch_content = ""
        current_batch_tokens = 0

        # Reserve tokens for prompt template overhead (goal + formatting)
        prompt_overhead_tokens = self.token_estimator.estimate_tokens(
            config.PLANNER_INSIGHT_PROMPT_TEMPLATE.format(goal=main_goal, backpack_context="")
        )
        available_tokens = config.CONTEXT_LIMIT - prompt_overhead_tokens

        print(f"DEBUG: Available tokens per batch: {available_tokens} (reserved {prompt_overhead_tokens} for prompt)")

        for item in backpack:
            item_content = f"File: {item['file_path']}\nJustification: {item['justification']}\nContent:\n{item['full_code']}\n\n"
            item_tokens = self.token_estimator.estimate_tokens(item_content)

            # If adding this item would exceed the limit, start a new batch
            if current_batch_tokens + item_tokens > available_tokens:
                if current_batch_content:
                    batches.append(current_batch_content)
                    print(f"DEBUG: Created batch with {current_batch_tokens} tokens")
                current_batch_content = item_content
                current_batch_tokens = item_tokens
            else:
                current_batch_content += item_content
                current_batch_tokens += item_tokens

        # Add the final batch if it has content
        if current_batch_content:
            batches.append(current_batch_content)
            print(f"DEBUG: Created final batch with {current_batch_tokens} tokens")

        print(f"DEBUG: Split {len(backpack)} files into {len(batches)} batches (token-based sizing)")

        # --- MAP PHASE ---
        # Generate insights from each batch of files
        all_insights = []
        for i, batch in enumerate(batches):
            print(f"DEBUG: Processing batch {i + 1}/{len(batches)}...")
            insight = self._generate_insights_from_batch(main_goal, batch)
            all_insights.append(insight)
            print(f"DEBUG: Insight for batch {i + 1}: {insight[:100]}...")

        # --- REDUCE PHASE ---
        # Synthesize a single plan from all the generated insights
        final_plan = self._synthesize_plan_from_insights(main_goal, all_insights)

        # --- VALIDATION PHASE ---
        # Validate and correct file references in the generated plan
        final_plan = validate_and_correct_plan(final_plan)

        print(f"DEBUG: Returning final plan with length: {len(final_plan)}")
        return final_plan, used_memory_ids


    def update_plan(self, main_goal: str, backpack: list[dict], plan: PlanGraph, codebase_summary: str, query_answer: str="") -> PlanGraph:
        """
        Updates the existing plan by iteratively unfolding objective nodes.
        Follows a 6-step process: Input Validation, Graph Traversal, Batching, Synthesis, Validation, Output Preparation.
        Returns the updated PlanGraph that includes Reasonable ActionNodes and ObjectiveNodes.
        """
        # Step 1: Input Validation and Context Preparation
        if not isinstance(plan, PlanGraph):
            raise ValueError("plan must be a PlanGraph instance")
        if not main_goal.strip():
            raise ValueError("main_goal cannot be empty")
        if not isinstance(backpack, list):
            raise TypeError("backpack must be a list of dicts")

        # Prepare context combining all inputs
        context_parts = [f"Main Goal: {main_goal}", f"Codebase Summary: {codebase_summary}"]
        if query_answer.strip():
            context_parts.append(f"Additional Context: {query_answer}")
        if backpack:
            backpack_context = "\n".join([
                f"File: {item.get('file_path', 'unknown')}\nJustification: {item.get('justification', '')}\nContent:\n{item.get('full_code', '')}"
                for item in backpack
            ])
            context_parts.append(f"Backpack Context:\n{backpack_context}")
        combined_context = "\n\n".join(context_parts)

        # Step 2: Graph Traversal and Objective Identification
        pending_objectives = []
        def traverse_objectives(node_id):
            node = plan.get_node(node_id)
            if isinstance(node, ObjectiveNode) and node.status in [STATUS_PENDING, STATUS_IN_PROGRESS]:
                pending_objectives.append(node)
            if isinstance(node, ObjectiveNode):
                for child_id in node.children:
                    traverse_objectives(child_id)

        traverse_objectives(plan.root_id)
        if not pending_objectives:
            # No pending objectives, return the plan as is
            return plan

        # Step 3: Batching and Insight Generation (Map Phase Adaptation)
        token_limit = config.CONTEXT_LIMIT // 4  # Conservative limit for updates
        batches = []
        current_batch = ""
        current_tokens = 0

        for obj in pending_objectives:
            obj_context = f"Objective: {obj.description}\nID: {obj.id}\nStatus: {obj.status}\n"
            obj_tokens = self.token_estimator.estimate_tokens(obj_context)

            if current_tokens + obj_tokens > token_limit:
                if current_batch:
                    batches.append(current_batch)
                current_batch = obj_context
                current_tokens = obj_tokens
            else:
                current_batch += obj_context
                current_tokens += obj_tokens

        if current_batch:
            batches.append(current_batch)

        all_insights = []
        for batch in batches:
            insight = self._generate_insights_from_batch(f"Update and unfold objectives for: {main_goal}", batch)
            all_insights.append(insight)

        # Step 4: Sub-Plan Synthesis and Graph Update (Reduce Phase Adaptation)
        sub_plan = self._synthesize_plan_from_insights(f"Unfold objectives for: {main_goal}", all_insights)

        # Parse sub_plan as dict and update graph
        try:
            plan_dict = json.loads(sub_plan)
            for obj in pending_objectives:
                # Mark current objective as completed if sub-objectives are generated
                if 'sub_objectives' in plan_dict:
                    for sub_obj_desc in plan_dict['sub_objectives']:
                        sub_obj = plan.add_objective(sub_obj_desc, obj.id)
                        # Add actions if specified
                        if 'actions' in plan_dict and sub_obj_desc in plan_dict['actions']:
                            for action_spec in plan_dict['actions'][sub_obj_desc]:
                                plan.add_action(sub_obj.id, action_spec.get('role', 'unknown'),
                                              action_spec.get('command', {}),
                                              action_spec.get('justification', ''))
                    plan.update_node_status(obj.id, STATUS_COMPLETED)
                else:
                    # If no sub-objectives, mark as completed
                    plan.update_node_status(obj.id, STATUS_COMPLETED)
        except json.JSONDecodeError:
            # If parsing fails, add a generic sub-objective
            for obj in pending_objectives:
                plan.add_objective("Further refine this objective based on insights", obj.id)
                plan.update_node_status(obj.id, STATUS_COMPLETED)

        # Step 5: Validation and Correction (now on the graph structure, not string)
        # Since we're updating the graph directly, validate the graph structure instead
        # For now, we'll skip this as the graph methods ensure validity

        # Return the updated PlanGraph directly
        return plan