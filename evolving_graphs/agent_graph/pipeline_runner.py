# pipeline_runner.py (Pipeline Runner Orchestrator)
# PipelineRunner class encapsulates the scout→planner→executor→verifier→commit logic.

import os
from .memory_interface import MemoryInterface  # External memory interface for feedback loop

from .code_descriptor import HierarchicalCodeDescriptor  # Mandatory import for architecture analysis
from .intelligence_project_scout import Scout  # Intelligence components for scouting and planning
from .intelligence_plan_generator import Planner  # Intelligence components for scouting and planning
from .pipeline_executor import Executor  # Executor class for generating and applying code changes
from .sandbox_utils import SandboxManager  # Unified sandboxing API for directory and execution isolation


class CodeArchitect:
    """
    CodeArchitect role: Generates hierarchical architecture summaries using HierarchicalCodeDescriptor.
    """

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.descriptor = HierarchicalCodeDescriptor(root_dir)

    def generate_architecture_summary(self) -> str:
        """
        Generates and returns the architecture summary as a string.
        """
        try:
            self.descriptor.generate_hierarchical_description()
            architecture_file = os.path.join(self.root_dir, "codebase_architecture.md")
            with open(architecture_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Architecture generation failed: {e}")


class PipelineRunner:
    """
    Encapsulates the linear pipeline logic: scout → planner → executor → verifier → commit.
    """

    def __init__(self, main_goal: str, root_dir: str):
        """
        Initialize the pipeline runner with goal and root directory.

        Args:
            main_goal: The main goal for the agent.
            root_dir: The root directory for the project.
        """
        self.main_goal = main_goal
        self.root_dir = root_dir
        self.turn_counter = 0  # Track pipeline turns for feedback
        self.memory = MemoryInterface(db_path="memory_db")  # Memory interface for feedback loop
        self.architect = CodeArchitect(self.root_dir)  # CodeArchitect for generating architecture summaries
        self.scout = Scout(self.memory, os.path.join(self.root_dir, 'agent_graph'))  # Scout for gathering context with memory
        self.planner = Planner(self.memory)  # Planner for creating strategy with memory
        self.executor = Executor(main_goal)  # Executor for code changes
        self.sandbox_manager = SandboxManager(self.root_dir)  # Unified sandbox manager

    def create_candidate(self) -> None:
        """Create candidate sandbox using unified sandbox manager."""
        self.sandbox_manager.create_directory_sandbox()

    def promote_candidate(self) -> None:
        """Promote candidate sandbox using unified sandbox manager."""
        self.sandbox_manager.promote_directory_sandbox()

    def rollback_candidate(self) -> None:
        """Rollback candidate sandbox using unified sandbox manager."""
        self.sandbox_manager.rollback_directory_sandbox()

    def run_pipeline(self) -> dict:
        """
        Run one iteration of the pipeline with sandbox management and memory feedback.

        Returns:
            dict: Result containing success status and any messages.
        """
        try:
            # Increment turn counter
            self.turn_counter += 1
            used_memory_ids_this_turn = []

            # 0. SANDBOX SETUP: Create candidate copy
            print("Creating candidate sandbox...")
            self.create_candidate()

            # 0.5. ARCHITECT PHASE: Generate architecture summary
            print("Architect is generating the architecture summary...")
            try:
                architecture_summary = self.architect.generate_architecture_summary()
                print("Architecture summary generated successfully.")
            except Exception as e:
                print(f"Architecture generation failed: {e}. Proceeding without architecture summary.")
                architecture_summary = None

            # 1. SCOUT PHASE: Gather context
            print("Scout is analyzing the project...")
            scout_result = self.scout.scout_project(self.main_goal, self.turn_counter)
            backpack, scout_memory_ids = scout_result
            used_memory_ids_this_turn.extend(scout_memory_ids)
            if architecture_summary:
                # Append architecture summary to the backpack
                backpack.append({
                    'file_path': 'codebase_architecture.md',
                    'content': architecture_summary,
                    'type': 'architecture_summary'
                })
            print(f"Scout returned a backpack with {len(backpack)} relevant files.")

            # 2. PLANNER PHASE: Create a strategy
            print("Planner is creating a plan...")
            planner_result = self.planner.create_plan(self.main_goal, backpack)
            plan, planner_memory_ids = planner_result
            used_memory_ids_this_turn.extend(planner_memory_ids)
            print(f"Planner created the following plan:\n{plan}")

            # 3. EXECUTOR PHASE: Write the new code
            print("Executor is generating the code change...")
            proposed_code_change = self.executor.execute_plan(plan, backpack)
            print(f"Executor returned proposed change (length: {len(proposed_code_change)})")

            # 4. VERIFIER PHASE: Check the work using subprocess execution of linter_graph_main.py
            print("Verifier is testing the new code...")
            verification_result = self.verify_with_linter(proposed_code_change)
            print(f"Verifier returned result: Success={verification_result['success']}")

            # 5. COMMIT PHASE: Decide whether to accept the change
            if verification_result['success']:
                print("Change VERIFIED. Promoting candidate to baseline.")
                self.promote_candidate()
                # Memory feedback: +1.0 for success
                for mem_id in used_memory_ids_this_turn:
                    self.memory.update_memory_feedback(mem_id, 1.0, self.turn_counter)
                return {
                    'success': True,
                    'message': 'Pipeline completed successfully and promoted.'
                }
            else:
                print("Change FAILED verification. Rolling back candidate.")
                self.rollback_candidate()
                # Memory feedback: -2.0 for failure
                for mem_id in used_memory_ids_this_turn:
                    self.memory.update_memory_feedback(mem_id, -2.0, self.turn_counter)
                return {
                    'success': False,
                    'message': 'Pipeline failed verification.'
                }

        except Exception as e:
            print(f"Error in pipeline: {e}")
            # Ensure candidate is rolled back on error
            self.rollback_candidate()
            # Memory feedback: -2.0 for failure
            for mem_id in used_memory_ids_this_turn:
                self.memory.update_memory_feedback(mem_id, -2.0, self.turn_counter)
            return {
                'success': False,
                'message': f'Pipeline error: {e}'
            }

    def verify_with_linter(self, proposed_code_change) -> dict:
        """
        Execute the linter graph as a subprocess to verify the code change.

        Args:
            proposed_code_change: The proposed code change to verify.

        Returns:
            dict: Verification result with 'success' and optional 'error'.
        """
        return self.sandbox_manager.verify_with_linter_subprocess(proposed_code_change)