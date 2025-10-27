# pipeline_runner.py (Pipeline Runner Orchestrator)
# PipelineRunner class encapsulates the scout→planner→executor→verifier→commit logic.

import os
from .memory_interface import MemoryInterface  # External memory interface for feedback loop

from .task_planner_graph import PlanGraph # Data structure used for creating more complex planning in the pipeline
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
            architecture_file = os.path.join(self.root_dir, "codebase_architecture.md")
            with open(architecture_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print("No previous codebase_architecture.md found")
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
        self.planner = Planner(self.memory)  # Planner for creating strategy with memory
        self.executor = Executor(main_goal)  # Executor for code changes
        self.sandbox_manager = SandboxManager(self.root_dir)  # Unified sandbox manager
        # Create sandbox during initialization
        self.create_candidate()
        # Set root_dir to the sandbox location
        self.root_dir = self.sandbox_manager.directory_sandbox.candidate_dir
        # Initialize components with sandbox root_dir
        self.architect = CodeArchitect(self.root_dir)  # CodeArchitect for generating architecture summaries
        self.scout = Scout(self.memory, os.path.join(self.root_dir, 'agent_graph'))  # Scout for gathering context with memory

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

            # 0.5. ARCHITECT PHASE: Generate architecture summary
            print("Architect is generating the architecture summary...")
            try:
                architecture_summary = self.architect.generate_architecture_summary()
                print("Architecture summary generated successfully.")
            except Exception as e:
                print(f"Architecture generation failed: {e}. Proceeding without architecture summary.")
                architecture_summary = None

            # 1. SCOUT PHASE: Gather context for brainstorming ideas
            print("Scout is analyzing the project...")
            scout_result = self.scout.scout_project(self.main_goal, self.turn_counter)
            backpack, scout_memory_ids = scout_result
            used_memory_ids_this_turn.extend(scout_memory_ids)
            print(f"Scout returned a backpack with {len(backpack)} relevant files.")
           
           #TODO scout <--> planner <--> executor
            
            plan = PlanGraph(self.main_goal)

            planner_result = self.planner.update_plan(self.main_goal, backpack, plan, architecture_summary)
            plan = planner_result
            plan.display()
            used_memory_ids_this_turn.extend(planner_memory_ids)
            while scout_query:
                backpack, scout_memory_ids, query_answer = self.scout.query(self.main_goal, scout_query)    
                planner_result = self.planner.update_plan(self.main_goal, backpack, plan, architecture_summary, query_answer)
                planner_memory_ids, scout_query = planner_result
                pass









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