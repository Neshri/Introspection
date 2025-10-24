# AgentTree/agent/pipeline/runner.py
# PipelineRunner class encapsulates the scout→planner→executor→verifier→commit logic.

from .intelligence_project_scout import Scout  # Intelligence components for scouting and planning
from .intelligence_plan_generator import Planner  # Intelligence components for scouting and planning
from .utils_state_persistence import save_document_state as state_manager  # Utility for saving document state
from .pipeline_pipeline_executor import Executor  # Executor class for generating and applying code changes
from .pipeline_code_verifier import Verifier  # Verifier class for testing and validating code changes

import os  # For directory operations and changing working directory
import shutil  # For copying and managing directories


class PipelineRunner:
    """
    Encapsulates the linear pipeline logic: scout → planner → executor → verifier → commit.
    """

    def __init__(self, main_goal: str, initial_code_state: str, root_dir: str):
        """
        Initialize the pipeline runner with goal, initial code state, and root directory.

        Args:
            main_goal: The main goal for the agent.
            initial_code_state: The initial code state.
            root_dir: The root directory for the project.
        """
        self.main_goal = main_goal
        self.current_code_state = initial_code_state
        self.root_dir = root_dir
        self.version = 1  # Version tracker for candidate naming
        self.candidate_version = None  # Current candidate version
        self.scout = Scout()  # Scout for gathering context
        self.scout.set_working_directory(self.root_dir)
        self.planner = Planner()  # Planner for creating strategy
        self.executor = Executor(main_goal, initial_code_state)  # Executor for code changes
        self.candidate_dir = os.path.join(self.root_dir, 'candidate')  # Directory for sandbox copy
        self.baseline_dir = os.path.join(self.root_dir, 'evolving_graphs', 'agent_graph')  # Baseline is the agent code directory
        self.verifier = Verifier()  # Verifier for validation

    def create_candidate(self) -> None:
        """
        Create a deep copy of the evolving_graphs directory to a candidate directory with versioned subfolders for sandbox operations.
        """
        def ignore_patterns(dir_name: str, contents: list) -> list:
            """
            Ignore function for shutil.copytree to exclude .git and .venv directories.
            """
            return ['.git', '.venv']

        # Set candidate version
        self.candidate_version = f"v{self.version}"
        self.version += 1

        # Candidate structure: evolving_graphs/agent_graph_vN and evolving_graphs/linter_graph_vN
        candidate_agent_dir = os.path.join(self.candidate_dir, 'evolving_graphs', f'agent_graph_{self.candidate_version}')
        candidate_linter_dir = os.path.join(self.candidate_dir, 'evolving_graphs', f'linter_graph_{self.candidate_version}')

        # Remove existing candidate if it exists
        if os.path.exists(self.candidate_dir):
            shutil.rmtree(self.candidate_dir)

        # Copy only evolving_graphs folder from root
        evolving_graphs_src = os.path.join(self.root_dir, 'evolving_graphs')
        candidate_evolving_dir = os.path.join(self.candidate_dir, 'evolving_graphs')
        shutil.copytree(evolving_graphs_src, candidate_evolving_dir, ignore=ignore_patterns)

        # Rename subfolders to versioned names
        os.rename(os.path.join(candidate_evolving_dir, 'agent_graph'), candidate_agent_dir)
        os.rename(os.path.join(candidate_evolving_dir, 'linter_graph'), candidate_linter_dir)

    def promote_candidate(self) -> None:
        """
        Promote the candidate versioned agent_graph to the baseline and update evolving_graphs.
        """
        # Candidate versioned directories
        candidate_agent_dir = os.path.join(self.candidate_dir, 'evolving_graphs', f'agent_graph_{self.candidate_version}')
        candidate_linter_dir = os.path.join(self.candidate_dir, 'evolving_graphs', f'linter_graph_{self.candidate_version}')

        # Target directories in root evolving_graphs
        target_agent_dir = os.path.join(self.root_dir, 'evolving_graphs', 'agent_graph')
        target_linter_dir = os.path.join(self.root_dir, 'evolving_graphs', 'linter_graph')

        # Backup current baseline
        temp_agent_dir = os.path.join(self.root_dir, 'temp_agent_baseline')
        temp_linter_dir = os.path.join(self.root_dir, 'temp_linter_baseline')
        if os.path.exists(temp_agent_dir):
            shutil.rmtree(temp_agent_dir)
        if os.path.exists(temp_linter_dir):
            shutil.rmtree(temp_linter_dir)
        if os.path.exists(target_agent_dir):
            shutil.move(target_agent_dir, temp_agent_dir)
        if os.path.exists(target_linter_dir):
            shutil.move(target_linter_dir, temp_linter_dir)

        # Move candidate versioned to baseline
        shutil.move(candidate_agent_dir, target_agent_dir)
        shutil.move(candidate_linter_dir, target_linter_dir)

        # Clean up candidate and temp
        shutil.rmtree(self.candidate_dir)
        if os.path.exists(temp_agent_dir):
            shutil.rmtree(temp_agent_dir)
        if os.path.exists(temp_linter_dir):
            shutil.rmtree(temp_linter_dir)

    def rollback_candidate(self) -> None:
        """
        Delete the candidate directory to discard changes.
        """
        if os.path.exists(self.candidate_dir):
            shutil.rmtree(self.candidate_dir)

    def run_pipeline(self) -> dict:
        """
        Run one iteration of the pipeline with sandbox management.

        Returns:
            dict: Result containing success status, updated code state, and any messages.
        """
        try:
            # 0. SANDBOX SETUP: Create candidate copy
            print("Creating candidate sandbox...")
            self.create_candidate()
            original_cwd = os.getcwd()  # Save original working directory

            try:
                # Change to candidate agent directory for Scout, Executor, Verifier
                candidate_agent_dir = os.path.join(self.candidate_dir, 'evolving_graphs', f'agent_graph_{self.candidate_version}')
                os.chdir(candidate_agent_dir)
                self.verifier.set_working_directory(candidate_agent_dir)

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
                    print("Change VERIFIED. Promoting candidate to baseline.")
                    self.current_code_state = proposed_code_change  # Update the state
                    state_manager(self.current_code_state, self.main_goal)
                    self.promote_candidate()
                    return {
                        'success': True,
                        'code_state': self.current_code_state,
                        'message': 'Pipeline completed successfully and promoted.'
                    }
                else:
                    print("Change FAILED verification. Rolling back candidate.")
                    self.rollback_candidate()
                    return {
                        'success': False,
                        'code_state': self.current_code_state,
                        'message': 'Pipeline failed verification.'
                    }

            finally:
                # Always restore original working directory
                os.chdir(original_cwd)

        except Exception as e:
            print(f"Error in pipeline: {e}")
            # Ensure candidate is rolled back on error
            self.rollback_candidate()
            return {
                'success': False,
                'code_state': self.current_code_state,
                'message': f'Pipeline error: {e}'
            }