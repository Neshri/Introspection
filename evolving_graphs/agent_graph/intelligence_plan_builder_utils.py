# Split intelligence_plan_builder_utils.py to reduce token count
# Core Planner class moved to intelligence_plan_builder_core_utils.py
# Graph-related functions split into multiple utils modules for token limit compliance

from .intelligence_plan_builder_core_utils import Planner as CorePlanner  # Core planner functionality
from .intelligence_plan_builder_graph_utils import update_plan  # Graph plan update functionality


class Planner(CorePlanner):

    def update_plan(self, main_goal: str, backpack: list[dict], plan, codebase_summary: str, query_answer: str = ""):
        """
        Updates the existing plan using command-based incremental building.
        Delegates to the graph utils module's update_plan function.

        Returns the updated PlanGraph and a list of planner memory IDs with full LLM response logging.
        """
        return update_plan(main_goal, backpack, plan, codebase_summary, query_answer)