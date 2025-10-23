# agent_class.py (Agent Class Implementation)
# This module defines the Agent class with goal-setting capabilities and run loop.
# Imports: Standard library for type hints, string operations, time, config, state_manager,
# intelligence modules (Scout, Planner), pipeline modules (Executor, Verifier).

import re
import time
from typing import Optional
from agent import config  # Configuration settings
from .utils import state_manager  # State management utilities
from .intelligence.core import Scout, Planner  # Intelligence components for scouting and planning
from .pipeline.executor import Executor  # Executor class for generating and applying code changes
from .pipeline.verifier import Verifier  # Verifier class for testing and validating code changes


class Agent:
    """
    Agent class for managing goal-setting and persistence.
    Provides validation and immediate state saving for goals.
    """

    def __init__(self, goal_string: str):
        """Initialize Agent with the provided goal string."""
        self.main_goal = goal_string

    def set_goal(self, new_goal: str) -> bool:
        """
        Set a new goal with validation and immediate persistence.

        Args:
            new_goal: The new goal string to set (10-500 chars, no dangerous content)

        Returns:
            bool: True if goal was set successfully, False otherwise
        """
        if not self._validate_goal(new_goal):
            return False

        try:
            state_manager.save_goal_only(new_goal)
            self.main_goal = new_goal
            return True
        except Exception:
            return False

    def _validate_goal(self, goal: str) -> bool:
        """
        Validate goal string according to requirements.

        Args:
            goal: Goal string to validate

        Returns:
            bool: True if valid, False otherwise
        """
        # Non-empty string check
        if not goal or not isinstance(goal, str) or goal.strip() == "":
            return False

        # Length validation (10-500 characters)
        if len(goal) < 10 or len(goal) > 500:
            return False

        # Dangerous content check - block common harmful patterns
        dangerous_patterns = [
            r'\bscript\b', r'\beval\b', r'\bexec\b', r'\bimport\s+os\b',
            r'\bsystem\b', r'\brm\s', r'\bdel\s', r'\bformat\b.*\{.*\}',
            r'\b__import__\b', r'\bopen\b.*\bw\b', r'\bshutil\b',
            r'\bsubprocess\b', r'\bos\.', r'\bsys\.'
        ]

        goal_lower = goal.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, goal_lower):
                return False

        return True

    def get_goal(self) -> Optional[str]:
        """
        Get the current goal.

        Returns:
            Optional[str]: Current goal or None if not set
        """
        return self.main_goal

    def run_with_agent(self):
        """Run the agent using the new PipelineRunner class for goal management."""
        print("--- Initializing Agent with Goal Management ---")

        current_goal = self.get_goal()
        print(f"DEBUG: Initial agent goal: {current_goal}")

        # Use goal from agent, fallback to config if None
        if current_goal is None:
            current_goal = config.INITIAL_GOAL
            print(f"DEBUG: Using config fallback goal: {current_goal}")

        print("Loading document state...")
        loaded_goal, current_code_state = state_manager.load_document_on_startup()
        print(f"DEBUG: Loaded goal from state: {loaded_goal}")
        print(f"DEBUG: Current code state length: {len(current_code_state) if current_code_state else 0}")

        # Use agent's goal if document state goal is None
        if loaded_goal is None:
            loaded_goal = current_goal
            print(f"DEBUG: Using agent goal since loaded goal was None: {loaded_goal}")
        else:
            print(f"DEBUG: Using loaded goal from state: {loaded_goal}")

        # Set the goal if not already set
        if self.get_goal() is None:
            print(f"DEBUG: Setting agent goal to: {loaded_goal}")
            self.set_goal(loaded_goal)
            current_goal = loaded_goal

        # Initialize the pipeline runner
        from .pipeline.runner import PipelineRunner  # PipelineRunner class for encapsulated pipeline logic
        pipeline_runner = PipelineRunner(self.main_goal, current_code_state)

        # Agent class integration for the new run_with_agent function
        turn_number = 1
        max_turns = 10  # Add safety limit to prevent infinite loops
        goal_achieved = False
        try:
            while turn_number <= max_turns and not goal_achieved:
                print(f"\n--- Turn {turn_number} ---")

                # Run one pipeline iteration
                result = pipeline_runner.run_pipeline()

                if result['success']:
                    # Update agent's goal if needed
                    if self.get_goal() != current_goal:
                        self.set_goal(current_goal)
                    # Check for goal completion after successful commit
                    goal_achieved = True
                else:
                    print("Pipeline failed, will retry next turn.")

                if goal_achieved or turn_number > max_turns:
                    break
                turn_number += 1
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n--- User interrupted. Shutting down agent. ---")
        except Exception as e:
            print(f"\n--- Unexpected error occurred: {e} ---")
            print("--- Agent shutdown complete. ---")
        finally:
            print("--- Agent shutdown complete. ---")