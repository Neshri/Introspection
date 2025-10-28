from typing import List
from .intelligence_plan_execution_utils import (generate_insights_from_batch, synthesize_plan_from_insights)  # Execution and plan synthesis utilities
from .intelligence_token_utils import token_estimator  # Token estimation utilities


def generate_insights_from_batch_wrapper(main_goal: str, batch_context: str) -> str:
    """(Map Phase) Generates insights for a single batch of files."""
    token_count = token_estimator.estimate_tokens(batch_context)
    return generate_insights_from_batch(main_goal, batch_context, token_count)


def synthesize_plan_from_insights_wrapper(main_goal: str, insights: List[str]) -> str:
    """(Reduce Phase) Synthesizes a final plan from a collection of insights."""
    return synthesize_plan_from_insights(main_goal, insights)