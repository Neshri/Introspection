from .agent_class import Agent  # Agent class for goal management and execution
from .agent import run  # Backward compatibility run function
from . import config, format_backpack_context  # Shared utilities moved to agent level
from .utils import state_manager  # State management utilities remain in utils
from .intelligence import (  # Intelligence components
    chat_llm,
    Planner,
    Scout,
    get_critic_score,
    evaluate_code_quality,
    get_executor_response,
    execute_code,
    track_prompt_performance,
    get_best_prompt_variations
)

# Backward compatibility aliases for intelligence components
# These can be removed once all consumers are updated to use direct imports

__all__ = [
    "Agent",
    "run",
    "config",
    "state_manager",
    "chat_llm",
    "format_backpack_context",
    "Planner",
    "Scout",
    "get_critic_score",
    "evaluate_code_quality",
    "get_executor_response",
    "execute_code",
    "track_prompt_performance",
    "get_best_prompt_variations"
]