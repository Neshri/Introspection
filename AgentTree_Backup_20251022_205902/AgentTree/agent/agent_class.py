# agent_class.py (Agent Class Implementation)
# This module defines the Agent class with goal-setting capabilities and run loop.
# Imports: Standard library for type hints, string operations, time, config, state_manager,
# intelligence modules (Scout, Planner), pipeline modules (Executor, Verifier).

import re
import time
from typing import Optional
from agent.utils import config, state_manager  # Utilities for agent settings and state management
from agent.intelligence.core import Scout, Planner  # Intelligence components for scouting and planning
from agent.pipeline.executor import Executor  # Executor class for generating and applying code changes
from agent.pipeline.verifier import Verifier  # Verifier class for testing and validating code changes


class Agent:
    """
    Agent class for managing goal-setting and persistence.
    Provides validation and immediate state saving for goals.
    """

    def __init__(self):
        """Initialize Agent with current goal loaded from state."""
        self.goal: Optional[str] = state_manager.load_goal()

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
            self.goal = new_goal
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
        return self.goal

    def run_with_agent(self):
        """Alternative run function using the new Agent class for goal management."""
        print("--- Initializing Agent with Goal Management ---")

        current_goal = self.get_goal()

        # Use goal from agent, fallback to config if None
        if current_goal is None:
            current_goal = config.INITIAL_GOAL
            self.set_goal(current_goal)

        loaded_goal, current_code_state = state_manager.load_document_on_startup()

        # Use agent's goal if document state goal is None
        if loaded_goal is None:
            loaded_goal = current_goal

        # Initialize our specialist agents
        scout = Scout()
        planner = Planner()
        executor = Executor(loaded_goal, current_code_state)
        verifier = Verifier()

        # Agent class integration for the new run_with_agent function
        turn_number = 1
        try:
            while True:
                print(f"\n--- Turn {turn_number} ---")

                # This is the new, linear pipeline. It replaces the single MCTS call.

                # 1. SCOUT PHASE: Gather context
                print("Scout is analyzing the project...")
                backpack = scout.scout_project(current_goal)
                print(f"Scout returned a backpack with {len(backpack)} relevant files.")

                # 2. PLANNER PHASE: Create a strategy
                print("Planner is creating a plan...")
                plan = planner.create_plan(current_goal, backpack)
                print(f"Planner created the following plan:\n{plan}")

                # 3. EXECUTOR PHASE: Write the new code
                print("Executor is generating the code change...")
                proposed_code_change = executor.execute_plan(plan, backpack)
                # For simplicity, let's assume it only modifies one file for now

                # 4. VERIFIER PHASE: Check the work
                print("Verifier is testing the new code...")
                verification_result = verifier.verify_change(proposed_code_change)
                print(f"Verifier returned result: Success={verification_result['success']}")

                # 5. COMMIT PHASE: Decide whether to accept the change
                if verification_result['success']:
                    print("Change VERIFIED. Committing to memory.")
                    current_code_state = proposed_code_change # Update the state
                    state_manager.save_document_state(current_code_state, current_goal)
                    # Update agent's goal if needed
                    if self.get_goal() != current_goal:
                        self.set_goal(current_goal)
                else:
                    print("Change FAILED verification. Discarding change and trying again next turn.")
                    # In the future, this failure reason would be fed back into the next loop

                turn_number += 1
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n--- User interrupted. Shutting down agent. ---")
        finally:
            print("--- Agent shutdown complete. ---")