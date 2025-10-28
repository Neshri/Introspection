from typing import Dict, List, Optional, Tuple, Any
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED
from .memory_interface import MemoryInterface  # External memory interface for querying knowledge
from .agent_config import config  # Configuration settings for model selection and prompt templates
from .intelligence_plan_prompt_utils import generate_insights_from_batch_wrapper, synthesize_plan_from_insights_wrapper
from .intelligence_plan_objective_utils import is_specific_objective  # Objective specificity utilities
from .intelligence_llm_service import chat_llm  # LLM service for command interactions
from .intelligence_plan_command_utils import command_parser  # Command parser for plan modification
from .intelligence_plan_execution_utils import refine_objective


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
        self.memory = memory

    def _generate_insights_from_batch(self, main_goal: str, batch_context: str) -> str:
        """(Map Phase) Generates insights for a single batch of files."""
        return generate_insights_from_batch_wrapper(main_goal, batch_context)

    def _synthesize_plan_from_insights(self, main_goal: str, insights: list[str]) -> str:
        """(Reduce Phase) Synthesizes a final plan from a collection of insights."""
        return synthesize_plan_from_insights_wrapper(main_goal, insights)