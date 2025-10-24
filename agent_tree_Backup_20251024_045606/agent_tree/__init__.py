# AgentTree root package
# Exposes the main Agent class for external use

from .agent.agent import Agent  # Agent class exposed by the agent package for goal management and execution

__all__ = ['Agent']