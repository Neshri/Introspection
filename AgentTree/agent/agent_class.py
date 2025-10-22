# agent_class.py (Agent Class Implementation)
# This module defines the Agent class with goal-setting capabilities and run loop.
# Imports: Standard library for type hints, string operations, time, config, state_manager,
# intelligence modules (Scout, Planner), pipeline modules (Executor, Verifier).

import re
import time
from typing import Optional
from AgentTree.agent.utils import config, state_manager  # Utilities for agent settings and state management
from AgentTree.agent.intelligence.core import Scout, Planner  # Intelligence components for scouting and planning
from AgentTree.agent.pipeline.executor import Executor  # Executor class for generating and applying code changes
from AgentTree.agent.pipeline.verifier import Verifier  # Verifier class for testing and validating code changes


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

        print("Starting run_with_agent...")
    def run_with_agent(self):
        print("Initializing agent with goal management...")
        """Alternative run function using the new Agent class for goal management."""
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

        # Initialize our specialist agents
        print("DEBUG: Initializing Scout, Planner, Executor, Verifier")
        scout = Scout()
        planner = Planner()
        executor = Executor(loaded_goal, current_code_state)
        verifier = Verifier()

        # Agent class integration for the new run_with_agent function
        turn_number = 1
        max_turns = 10  # Add safety limit to prevent infinite loops
        goal_achieved = False
        try:
            while turn_number <= max_turns and not goal_achieved:
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
                print(f"DEBUG: Executor returned proposed change (length: {len(proposed_code_change)})")
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
                    # Check for goal completion after successful commit
                    goal_achieved = True
                else:
                    print("Change FAILED verification. Discarding change and trying again next turn.")
                    # In the future, this failure reason would be fed back into the next loop

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