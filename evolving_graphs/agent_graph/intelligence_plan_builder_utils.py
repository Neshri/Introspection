# Split intelligence_plan_builder_utils.py to reduce token count
# Core Planner class moved to intelligence_plan_builder_core_utils.py
# Graph-related functions split into multiple utils modules for token limit compliance

from .intelligence_plan_builder_core_utils import Planner as CorePlanner  # Core planner functionality
from .intelligence_plan_builder_graph_utils import update_plan  # Graph plan update functionality


class Planner(CorePlanner):

    def update_plan(self, main_goal: str, backpack: list[dict], plan, codebase_summary: str, query_answer: str = "", use_code_awareness: bool = True):
        """
        Updates the existing plan using advanced planning architectures.
        Defaults to code-aware planning for production-ready code agent architecture.

        Returns the updated PlanGraph and a list of planner insights.
        """
        return update_plan(main_goal, backpack, plan, codebase_summary, query_answer, use_code_awareness=use_code_awareness)