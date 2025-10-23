# AgentTree/agent/pipeline/runner.py
# PipelineRunner class encapsulates the scout→planner→executor→verifier→commit logic.

from ..shared.core import Scout, Planner  # Intelligence components for scouting and planning
from .executor import Executor  # Executor class for generating and applying code changes
from .verifier import Verifier  # Verifier class for testing and validating code changes
from ..utils import state_manager  # Utility for saving document state


class PipelineRunner:
    """
    Encapsulates the linear pipeline logic: scout → planner → executor → verifier → commit.
    """

    def __init__(self, main_goal: str, initial_code_state: str):
        """
        Initialize the pipeline runner with goal and initial code state.

        Args:
            main_goal: The main goal for the agent.
            initial_code_state: The initial code state.
        """
        self.main_goal = main_goal
        self.current_code_state = initial_code_state
        self.scout = Scout()  # Scout for gathering context
        self.planner = Planner()  # Planner for creating strategy
        self.executor = Executor(main_goal, initial_code_state)  # Executor for code changes
        self.verifier = Verifier()  # Verifier for validation

    def run_pipeline(self) -> dict:
        """
        Run one iteration of the pipeline.

        Returns:
            dict: Result containing success status, updated code state, and any messages.
        """
        try:
            # 1. SCOUT PHASE: Gather context
            print("Scout is analyzing the project...")
            backpack = self.scout.scout_project(self.main_goal)
            print(f"Scout returned a backpack with {len(backpack)} relevant files.")

            # 2. PLANNER PHASE: Create a strategy
            print("Planner is creating a plan...")
            plan = self.planner.create_plan(self.main_goal, backpack)
            print(f"Planner created the following plan:\n{plan}")

            # 3. EXECUTOR PHASE: Write the new code
            print("Executor is generating the code change...")
            proposed_code_change = self.executor.execute_plan(plan, backpack)
            print(f"Executor returned proposed change (length: {len(proposed_code_change)})")

            # 4. VERIFIER PHASE: Check the work
            print("Verifier is testing the new code...")
            verification_result = self.verifier.verify_change(self.main_goal, proposed_code_change)
            print(f"Verifier returned result: Success={verification_result['success']}")

            # 5. COMMIT PHASE: Decide whether to accept the change
            if verification_result['success']:
                print("Change VERIFIED. Committing to memory.")
                self.current_code_state = proposed_code_change  # Update the state
                state_manager.save_document_state(self.current_code_state, self.main_goal)
                return {
                    'success': True,
                    'code_state': self.current_code_state,
                    'message': 'Pipeline completed successfully and committed.'
                }
            else:
                print("Change FAILED verification. Discarding change.")
                return {
                    'success': False,
                    'code_state': self.current_code_state,
                    'message': 'Pipeline failed verification.'
                }

        except Exception as e:
            print(f"Error in pipeline: {e}")
            return {
                'success': False,
                'code_state': self.current_code_state,
                'message': f'Pipeline error: {e}'
            }