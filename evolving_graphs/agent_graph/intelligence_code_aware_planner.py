#
# intelligence_code_aware_planner.py (Code-Aware Planner)
# Core code-aware planning logic with structured phases and LLM integration.
#

from typing import Dict, List, Optional, Tuple, Any, Union, Literal
import ast
import os
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_COMPLETED  # Graph-based task planning structure
from .intelligence_plan_memory_interface import planning_memory_interface  # Memory integration for learning
from .intelligence_plan_command_utils import command_parser  # Command parsing and execution
from ._llm_service_utils import chat_llm  # Standardized LLM chat functionality
from .intelligence_plan_builder_graph_context_utils import _generate_plan_context  # Plan context generation
from .intelligence_plan_objective_utils import is_specific_objective  # Objective specificity checking
from .intelligence_plan_execution_utils import refine_objective  # Objective refinement logic
from .agent_config import config  # Configuration settings
from .code_context_analyzer import CodeContext, code_context, ast_analyzer  # AST analysis and code context management
from .dependency_graph_builder import DependencyGraph  # Dependency graph analysis
from .reality_validator import RealityValidator, PlanValidation  # Plan validation against reality


class CodeAwarePlanner:
    """
    Production-ready code-aware planner that integrates AST analysis, dependency graphs,
    and LLM-driven planning for intelligent code modification strategies.

    Features:
    - AST-integrated code understanding
    - Dependency-aware planning
    - LLM-driven objective refinement
    - Memory-augmented learning
    - Reality validation
    - Structured error handling and logging
    """

    def __init__(self):
        """Initialize the code-aware planner with required components."""
        import logging
        self.logger = logging.getLogger(__name__)

        # Initialize core analyzers
        self.code_context = code_context
        self.ast_analyzer = ast_analyzer
        self.dependency_graph = DependencyGraph(ast_analyzer)
        self.reality_validator = RealityValidator(ast_analyzer, self.dependency_graph)

        # Initialize memory interface for learning
        self.memory_interface = planning_memory_interface

        self.logger.info("CodeAwarePlanner initialized successfully")

    def plan_with_code_awareness(
        self,
        main_goal: str,
        backpack: List[Dict[str, Any]],
        plan: PlanGraph,
        codebase_summary: str
    ) -> Tuple[PlanGraph, List[Any]]:
        """
        Generate a code-aware plan using AST analysis and LLM integration.

        Args:
            main_goal: The primary programming objective
            backpack: List of context items providing additional information
            plan: The current PlanGraph to enhance with code awareness
            codebase_summary: Summary of the codebase architecture

        Returns:
            Tuple of (updated PlanGraph, list of planner insights/memory IDs)
        """
        try:
            self.logger.info(f"Starting code-aware planning for goal: {main_goal[:100]}...")

            # Phase 1: Validate inputs and initialize planning context
            self._validate_inputs(main_goal, backpack, plan, codebase_summary)

            # Phase 2: Analyze codebase structure and dependencies
            code_analysis = self._analyze_codebase_structure(codebase_summary, backpack)

            # Phase 3: Enhance plan with code-aware insights
            enhanced_plan = self._enhance_plan_with_code_awareness(
                plan, main_goal, code_analysis, backpack
            )

            # Phase 4: Validate plan against reality
            validation_result = self._validate_plan_against_reality(enhanced_plan, main_goal, backpack)
            if not validation_result.is_valid:
                self.logger.warning(f"Plan validation issues: {validation_result.issues}")
                enhanced_plan = self._repair_plan_validation_issues(
                    enhanced_plan, validation_result, main_goal, code_analysis
                )

            # Phase 5: Store learning insights for future planning
            insights = self._generate_planner_insights(
                main_goal, code_analysis, enhanced_plan, validation_result
            )

            # Phase 6: Final validation and return
            enhanced_plan.validate_consistency()
            self.logger.info(f"Code-aware planning completed. Plan has {len(enhanced_plan.nodes)} nodes")

            return enhanced_plan, insights

        except Exception as e:
            self.logger.error(f"Code-aware planning failed: {str(e)}", exc_info=True)
            # Return original plan as fallback
            return plan, []

    def _validate_inputs(
        self,
        main_goal: str,
        backpack: List[Dict[str, Any]],
        plan: PlanGraph,
        codebase_summary: str
    ) -> None:
        """Validate all input parameters for planning."""
        if not isinstance(main_goal, str) or not main_goal.strip():
            raise ValueError("main_goal must be a non-empty string")

        if not isinstance(backpack, list):
            raise TypeError("backpack must be a list")

        if not isinstance(plan, PlanGraph):
            raise TypeError("plan must be a PlanGraph instance")

        if not isinstance(codebase_summary, str):
            raise TypeError("codebase_summary must be a string")

        self.logger.debug("Input validation passed")

    def _analyze_codebase_structure(
        self,
        codebase_summary: str,
        backpack: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze the codebase structure using AST and dependency analysis.

        Returns:
            Dict containing analysis results including:
            - key_files: Important files identified
            - dependencies: Dependency relationships
            - code_patterns: Recurring patterns
            - risk_areas: Potential problem areas
        """
        self.logger.debug("Analyzing codebase structure")

        analysis = {
            "key_files": [],
            "dependencies": {},
            "code_patterns": [],
            "risk_areas": [],
            "ast_insights": {}
        }

        try:
            # Extract file information from backpack
            file_contexts = [item for item in backpack if isinstance(item, dict) and "file_path" in item]

            # Analyze key files for AST insights
            for file_item in file_contexts[:10]:  # Limit to first 10 files for performance
                file_path = file_item.get("file_path", "")
                content = file_item.get("content", "")
                if file_path.endswith(".py"):
                    try:
                        ast_insights = self.ast_analyzer.analyze_file(file_path, content)
                        if ast_insights:
                            analysis["ast_insights"][file_path] = ast_insights
                            analysis["key_files"].append(file_path)
                    except Exception as e:
                        self.logger.warning(f"AST analysis failed for {file_path}: {e}")

            # Build dependency graph
            try:
                analysis["dependencies"] = self.dependency_graph.build_from_files(
                    [f["file_path"] for f in file_contexts if f["file_path"].endswith(".py")]
                )
            except Exception as e:
                self.logger.warning(f"Dependency analysis failed: {e}")

            # Identify patterns and risk areas from codebase summary
            analysis["code_patterns"] = self._extract_code_patterns(codebase_summary)
            analysis["risk_areas"] = self._identify_risk_areas(codebase_summary, analysis)

        except Exception as e:
            self.logger.warning(f"Codebase analysis encountered issues: {e}")

        return analysis

    def _enhance_plan_with_code_awareness(
        self,
        plan: PlanGraph,
        main_goal: str,
        code_analysis: Dict[str, Any],
        backpack: List[Dict[str, Any]]
    ) -> PlanGraph:
        """Enhance the plan with code-aware insights and refined objectives."""

        self.logger.debug("Enhancing plan with code awareness")

        # Update root objective if needed
        root_node = plan.get_node(plan.root_id)
        if root_node.description != main_goal:
            root_node.description = main_goal

        # Find pending objectives to refine
        pending_objectives = plan.get_pending_objectives()

        for objective in pending_objectives:
            try:
                # Check if objective needs refinement
                if not is_specific_objective(objective.description):
                    self.logger.debug(f"Refining objective: {objective.description[:100]}...")
                    refined_descriptions = self._refine_objective_with_code_awareness(
                        objective, main_goal, code_analysis, backpack
                    )
                    self.logger.debug(f"Refined descriptions type: {type(refined_descriptions)}, value: {refined_descriptions}")

                    # Type checking: ensure refined_descriptions is a list
                    if not isinstance(refined_descriptions, list):
                        self.logger.error(f"refined_descriptions is not a list, type: {type(refined_descriptions)}, value: {refined_descriptions}. Using fallback.")
                        refined_descriptions = [objective.description]

                    if refined_descriptions:
                        self.logger.debug(f"Processing {len(refined_descriptions)} refined descriptions")
                        # Create sub-objectives for refined descriptions
                        for desc in refined_descriptions:
                            if isinstance(desc, str):
                                new_obj = plan.add_objective(desc, objective.id)
                                self.logger.debug(f"Added refined objective: {desc[:50]}...")
                            else:
                                self.logger.warning(f"Skipping non-string refined description: {desc} (type: {type(desc)})")

                        # Mark original objective as completed (broken down)
                        plan.update_node_status(objective.id, STATUS_COMPLETED)
                    else:
                        self.logger.debug("No refined descriptions generated")

                else:
                    # Objective is specific, add code-aware actions
                    self._add_code_aware_actions(plan, objective, code_analysis)

            except Exception as e:
                self.logger.warning(f"Failed to enhance objective {objective.id}: {e}")

        return plan

    def _refine_objective_with_code_awareness(
        self,
        objective: ObjectiveNode,
        main_goal: str,
        code_analysis: Dict[str, Any],
        backpack: List[Dict[str, Any]]
    ) -> List[str]:
        """Refine an objective using code awareness and LLM."""

        # Build context for refinement
        context_parts = []

        # Add codebase insights
        if code_analysis.get("ast_insights"):
            context_parts.append("Code Structure Analysis:")
            for file_path, insights in code_analysis["ast_insights"].items():
                context_parts.append(f"- {file_path}: {insights.get('summary', 'N/A')}")

        # Add dependency information
        if code_analysis.get("dependencies"):
            context_parts.append("Key Dependencies:")
            for dep_type, deps in code_analysis["dependencies"].items():
                if deps:
                    context_parts.append(f"- {dep_type}: {list(deps.keys())[:5]}...")  # Limit output

        # Add backpack context
        relevant_backpack = [item for item in backpack if isinstance(item, dict)]
        if relevant_backpack:
            context_parts.append("Available Context:")
            for item in relevant_backpack[:3]:  # Limit to first 3 items
                context_parts.append(f"- {item.get('type', 'Unknown')}: {item.get('description', 'N/A')[:100]}...")

        full_context = "\n".join(context_parts)

        # Use LLM to refine objective
        try:
            refined = refine_objective(
                objective.description,
                f"Main Goal: {main_goal}",
                main_goal,
                full_context
            )
            return refined if refined else [objective.description]
        except Exception as e:
            self.logger.warning(f"LLM refinement failed: {e}")
            return [objective.description]

    def _add_code_aware_actions(
        self,
        plan: PlanGraph,
        objective: ObjectiveNode,
        code_analysis: Dict[str, Any]
    ) -> None:
        """Add code-aware actions to a specific objective."""

        # Generate action based on objective and code analysis
        action_description = self._generate_code_aware_action_description(
            objective.description, code_analysis
        )

        if action_description:
            # Determine appropriate role based on action type
            role = self._determine_action_role(objective.description, code_analysis)

            command = {
                "description": action_description,
                "code_awareness": True,
                "analysis_used": list(code_analysis.keys())
            }

            plan.add_action(objective.id, role, command, f"Code-aware action for: {objective.description}")

    def _generate_code_aware_action_description(
        self,
        objective_desc: str,
        code_analysis: Dict[str, Any]
    ) -> str:
        """Generate a detailed action description with code awareness."""

        # Use LLM to generate detailed action with code context
        prompt = f"""Generate a specific, actionable description for the following programming objective:

Objective: {objective_desc}

Code Analysis Context:
- Key Files: {code_analysis.get('key_files', [])}
- Dependencies: {bool(code_analysis.get('dependencies'))}
- Risk Areas: {code_analysis.get('risk_areas', [])}

Provide a precise, technical description of what needs to be done, including:
- Specific files to modify
- Code elements to change
- Dependencies to consider
- Potential risks

Response should be a clear, actionable description."""

        try:
            response = chat_llm(prompt)
            return response.strip()
        except Exception as e:
            self.logger.warning(f"Failed to generate action description: {e}")
            return f"Implement {objective_desc} with code awareness"

    def _determine_action_role(
        self,
        objective_desc: str,
        code_analysis: Dict[str, Any]
    ) -> str:
        """Determine the most appropriate agent role for the action."""

        # Simple heuristic based on objective content
        desc_lower = objective_desc.lower()

        if any(word in desc_lower for word in ['analyze', 'explore', 'search', 'find']):
            return 'scout'
        elif any(word in desc_lower for word in ['edit', 'modify', 'update', 'change', 'implement']):
            return 'code_editor'
        else:
            # Default to code_editor for most programming tasks
            return 'code_editor'

    def _repair_plan_validation_issues(
        self,
        plan: PlanGraph,
        validation_result: PlanValidation,
        main_goal: str,
        code_analysis: Dict[str, Any]
    ) -> PlanGraph:
        """Attempt to repair plan validation issues."""

        self.logger.debug("Attempting to repair plan validation issues")

        # For now, log issues but return plan as-is
        # Future enhancement: implement specific repair strategies
        for issue in validation_result.issues:
            self.logger.warning(f"Plan validation issue: {issue}")

        return plan

    def _validate_plan_against_reality(self, plan: PlanGraph, main_goal: str, backpack: List[Dict[str, Any]]) -> PlanValidation:
        """Validate plan against reality using available validators."""
        from .reality_validator import PlanValidation

        # Get all objectives from the plan
        objectives = [node.description for node in plan.nodes.values()
                     if hasattr(node, 'description') and node.description != main_goal]

        if objectives:
            feasibility = self.reality_validator.validate_plan_feasibility(objectives, backpack)
            validation = PlanValidation()
            validation.is_valid = feasibility.get('feasible', True)
            # Create mock issues from feasibility results
            validation.issues = []
            if feasibility.get('issues', {}).get('missing_dependencies'):
                validation.issues.extend(f"Missing dependency: {dep}" for dep in feasibility['issues']['missing_dependencies'])
            if feasibility.get('issues', {}).get('architectural_issues'):
                validation.issues.extend(feasibility['issues']['architectural_issues'])
            return validation
        else:
            # No objectives to validate, assume valid
            validation = PlanValidation()
            validation.is_valid = True
            validation.issues = []
            return validation

    def _generate_planner_insights(
        self,
        main_goal: str,
        code_analysis: Dict[str, Any],
        plan: PlanGraph,
        validation_result: PlanValidation
    ) -> List[Any]:
        """Generate insights for the memory system."""

        insights = []

        try:
            # Store successful patterns in memory
            if validation_result.is_valid:
                self.logger.debug("Attempting to store planning pattern in memory...")
                try:
                    memory_id = self.memory_interface.store_planning_pattern(
                        goal_pattern=main_goal,
                        successful_approach={
                            "code_analysis_used": bool(code_analysis.get("ast_insights")),
                            "dependencies_analyzed": bool(code_analysis.get("dependencies")),
                            "plan_nodes_created": len(plan.nodes)
                        }
                    )
                    self.logger.debug(f"Successfully stored planning pattern with ID: {memory_id}")
                    if memory_id:
                        insights.append(memory_id)
                except AttributeError as e:
                    self.logger.warning(f"PlanningMemoryInterface missing store_planning_pattern method: {e}")
                    # Try alternative method if available
                    if hasattr(self.memory_interface, 'store_pattern'):
                        self.logger.debug("Trying alternative store_pattern method...")
                        alt_memory_id = self.memory_interface.store_pattern(
                            goal_pattern=main_goal,
                            successful_approach={
                                "code_analysis_used": bool(code_analysis.get("ast_insights")),
                                "dependencies_analyzed": bool(code_analysis.get("dependencies")),
                                "plan_nodes_created": len(plan.nodes)
                            }
                        )
                        if alt_memory_id:
                            insights.append(alt_memory_id)
                            self.logger.debug(f"Used alternative method to store pattern with ID: {alt_memory_id}")
                    else:
                        self.logger.warning("No alternative memory storage method available")
                except Exception as e:
                    self.logger.warning(f"Failed to store planning insights: {e}")
                    # Continue without memory storage - this should not break the planning process

        except Exception as e:
            self.logger.warning(f"Failed to store planning insights: {e}")

        return insights

    def _extract_code_patterns(self, codebase_summary: str) -> List[str]:
        """Extract recurring code patterns from codebase summary."""
        patterns = []

        # Simple pattern extraction - can be enhanced with more sophisticated analysis
        if "agent" in codebase_summary.lower():
            patterns.append("agent-based architecture")
        if "graph" in codebase_summary.lower():
            patterns.append("graph-based data structures")
        if "llm" in codebase_summary.lower():
            patterns.append("LLM integration patterns")

        return patterns

    def _identify_risk_areas(self, codebase_summary: str, analysis: Dict[str, Any]) -> List[str]:
        """Identify potential risk areas in the codebase."""
        risks = []

        # Check for complex dependencies
        deps = analysis.get("dependencies", {})
        if deps and len(deps) > 10:
            risks.append("High dependency complexity")

        # Check for many AST issues
        ast_insights = analysis.get("ast_insights", {})
        issue_count = sum(len(insights.get("issues", [])) for insights in ast_insights.values())
        if issue_count > 5:
            risks.append("Multiple AST analysis issues detected")

        return risks


# Create singleton instance for module-level access
code_aware_planner = CodeAwarePlanner()