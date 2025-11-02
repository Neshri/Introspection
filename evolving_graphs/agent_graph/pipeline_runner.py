# pipeline_runner.py (Pipeline Runner Orchestrator)
# PipelineRunner class encapsulates the scout→planner→executor→verifier→commit logic.

import os
from .memory_interface import MemoryInterface  # External memory interface for feedback loop

from .task_planner_graph import PlanGraph # Data structure used for creating more complex planning in the pipeline
from .code_descriptor import HierarchicalCodeDescriptor  # Mandatory import for architecture analysis
from .intelligence_project_scout import Scout  # Intelligence components for scouting and planning
from .intelligence_plan_generator import Planner  # Intelligence components for scouting and planning
from .pipeline_executor import Executor  # Executor class for generating and applying code changes
from .editor_core import Editor  # Editor class for safe file modifications and code changes
from .pipeline_code_verifier import Verifier  # CodeValidator for verifying code changes
from .sandbox_utils import SandboxManager  # Unified sandboxing API for directory and execution isolation
from .code_context_analyzer import ASTAnalyzer  # AST analyzer for validator
from .dependency_graph_builder import DependencyGraph  # Dependency graph for validator
from .reality_validator import RealityValidator  # Reality validator for plan validation


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
        self.sandbox_manager = SandboxManager(self.root_dir)  # Unified sandbox manager
        # Create sandbox during initialization
        self.create_candidate()
        # Set root_dir to the sandbox location
        self.root_dir = self.sandbox_manager.directory_sandbox.candidate_dir
        # Initialize components with sandbox root_dir
        self.architect = CodeArchitect(self.root_dir)  # CodeArchitect for generating architecture summaries
        self.scout = Scout(self.memory, os.path.join(self.root_dir, 'agent_graph'))  # Scout for gathering context with memory
        self.planner = Planner(self.memory)  # Planner for creating strategy with memory
        self.executor = Executor(main_goal)  # Executor for code changes
        self.executor.set_working_directory(self.root_dir)  # Set executor working directory
        self.editor = Editor(self.root_dir)  # Editor for safe file modifications
        # Initialize validator components
        self.ast_analyzer = ASTAnalyzer()  # AST analyzer for validation
        self.dependency_graph = DependencyGraph(self.ast_analyzer)  # Dependency graph builder
        self.reality_validator = RealityValidator(self.ast_analyzer, self.dependency_graph)  # Reality validator
        self.code_validator = Verifier()  # CodeValidator for verifying code changes
        self.code_validator.set_working_directory(self.root_dir)  # Set validator working directory

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

            # Build dependency graph from backpack for validation
            self.dependency_graph.build_from_backpack(backpack)

            # 2. PLANNER PHASE: Create or update the plan
            print("Planner is updating the plan...")
            plan = PlanGraph(self.main_goal)
            planner_result = self.planner.update_plan(self.main_goal, backpack, plan, architecture_summary)
            plan, planner_memory_ids = planner_result
            used_memory_ids_this_turn.extend(planner_memory_ids)
            print("Plan updated successfully")
            plan.display()

            # Validate plan feasibility with reality validator
            objectives = [obj.description for obj in plan.nodes.values() if hasattr(obj, 'description')]
            validation_result = self.reality_validator.validate_plan_feasibility(objectives, backpack)
            if not validation_result['feasible']:
                print(f"Plan validation failed: {validation_result['issues']}")
                # Continue but with lower confidence

            # 3. EXECUTOR PHASE: Generate code changes based on plan
            print("Executor is generating code changes...")
            plan_json = plan.to_json()  # Convert plan to JSON for executor
            proposed_code_change = self.executor.execute_plan(plan_json, backpack)
            print("Code changes generated by executor")

            # 4. CODE VALIDATOR PHASE: Verify the proposed code changes
            print("CodeValidator is verifying the code changes...")
            verification_result = self.code_validator.verify_change(self.main_goal, proposed_code_change)
            if not verification_result['success']:
                print(f"Code verification failed: {verification_result['error']}")
                # Could implement retry logic here
                return {
                    'success': False,
                    'message': f'Code verification failed: {verification_result["error"]}'
                }

            # 5. EDITOR PHASE: Apply the verified code changes
            print("Editor is applying the code changes...")
            # Assuming proposed_code_change is a dict with file operations
            if isinstance(proposed_code_change, dict) and 'operations' in proposed_code_change:
                for operation in proposed_code_change['operations']:
                    success = self.editor.edit_file(operation['file_path'], [operation])
                    if not success:
                        print(f"Failed to apply operation to {operation['file_path']}")
                        return {
                            'success': False,
                            'message': f'Failed to edit file: {operation["file_path"]}'
                        }

            # 6. VERIFY WITH LINTER: Final linting check
            print("Running final linter verification...")
            linter_result = self.verify_with_linter(proposed_code_change)
            if not linter_result['success']:
                print(f"Linter verification failed: {linter_result['error']}")
                return {
                    'success': False,
                    'message': f'Linter verification failed: {linter_result["error"]}'
                }

            print("Pipeline completed successfully")
            # Update memory feedback for success
            for mem_id in used_memory_ids_this_turn:
                self.memory.update_memory_feedback(mem_id, 1.0, self.turn_counter)
            return {
                'success': True,
                'message': 'Pipeline executed successfully with all validations passed'
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