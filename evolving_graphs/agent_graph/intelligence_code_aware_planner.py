#
# intelligence_code_aware_planner.py (Code-Aware Planner with AST Integration)
# This module implements a production-ready code agent architecture with structured
# planning phases, AST analysis, dependency graphs, and reality validation.
#

from typing import Dict, List, Optional, Tuple, Any, Union, Literal
import ast
import os
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_COMPLETED
from .intelligence_plan_memory_interface import planning_memory_interface
from .intelligence_plan_command_utils import command_parser
from .intelligence_llm_service import chat_llm
from .intelligence_plan_builder_graph_context_utils import _generate_plan_context
from .intelligence_plan_objective_utils import is_specific_objective
from .intelligence_plan_execution_utils import refine_objective
from .agent_config import config


class HierarchicalDecompositionPreventer:
    """Prevents excessive hierarchical decomposition in planning."""

    def __init__(self):
        self.decomposition_depth: Dict[str, int] = {}
        self.specificity_scores: Dict[str, float] = {}

    def should_decompose_further(self, objective_description: str, current_depth: int = 0) -> bool:
        """Determine if an objective should be decomposed further."""
        # Calculate specificity score
        specificity = self._calculate_specificity(objective_description)

        # Check depth limits
        max_depth = 3  # Prevent going too deep
        if current_depth >= max_depth:
            return False

        # Check if objective is specific enough
        min_specificity = 0.7
        return specificity < min_specificity

    def _calculate_specificity(self, description: str) -> float:
        """Calculate how specific an objective description is."""
        score = 0.0

        # Specific file references
        if any(ext in description.lower() for ext in ['.py', '.json', '.md', '.txt']):
            score += 0.3

        # Function/class references
        if any(keyword in description.lower() for keyword in ['function', 'class', 'method', 'def ', 'class ']):
            score += 0.2

        # Specific action verbs
        if any(verb in description.lower() for verb in ['update', 'modify', 'add', 'remove', 'change', 'implement']):
            score += 0.2

        # Concrete details
        if len(description.split()) > 5:  # Longer descriptions tend to be more specific
            score += 0.2

        # AST-level specificity (functions, imports, etc.)
        if any(term in description.lower() for term in ['import', 'from ', 'def ', 'class ', 'return', 'self.']):
            score += 0.1

        return min(1.0, score)

    def track_objective(self, objective_id: str, description: str, depth: int):
        """Track an objective for decomposition analysis."""
        self.decomposition_depth[objective_id] = depth
        self.specificity_scores[objective_id] = self._calculate_specificity(description)


class PlanningPhase(Enum):
    """Structured planning phases for code-aware planning."""
    ANALYSIS = "analysis"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"


@dataclass
class CodeContext:
    """Enhanced code context with AST and dependency information."""
    ast_nodes: Dict[str, ast.AST] = field(default_factory=dict)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    import_map: Dict[str, str] = field(default_factory=dict)
    function_definitions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    class_definitions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    file_sizes: Dict[str, int] = field(default_factory=dict)


@dataclass
class PlanValidation:
    """Reality validation results for plan components."""
    is_grounded: bool = False
    missing_dependencies: List[str] = field(default_factory=list)
    syntax_errors: List[str] = field(default_factory=list)
    architectural_issues: List[str] = field(default_factory=list)
    confidence_score: float = 0.0


class ASTAnalyzer:
    """Analyzes Python code using AST for code understanding."""

    def __init__(self):
        self.analyzed_files: Dict[str, ast.Module] = {}

    def analyze_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        Analyze a Python file using AST and extract structural information.
        """
        try:
            tree = ast.parse(content, filename=file_path)
            self.analyzed_files[file_path] = tree

            analysis = {
                'functions': {},
                'classes': {},
                'imports': [],
                'globals': [],
                'complexity': self._calculate_complexity(tree)
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'][node.name] = {
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node)
                    }
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'][node.name] = {
                        'line': node.lineno,
                        'bases': [base.id if hasattr(base, 'id') else str(base) for base in node.bases],
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        'docstring': ast.get_docstring(node)
                    }
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        analysis['imports'].extend(n.name for n in node.names)
                    else:
                        module = node.module or ''
                        analysis['imports'].extend(f"{module}.{n.name}" if module else n.name for n in node.names)

            return analysis
        except SyntaxError as e:
            return {'syntax_error': str(e), 'functions': {}, 'classes': {}, 'imports': []}

    def _calculate_complexity(self, tree: ast.Module) -> int:
        """Calculate cyclomatic complexity approximation."""
        complexity = 1  # Base complexity
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
                complexity += len(node.values) - 1
        return complexity

    def find_dependencies(self, file_path: str) -> List[str]:
        """Extract file dependencies from imports."""
        if file_path not in self.analyzed_files:
            return []

        dependencies = []
        for node in ast.walk(self.analyzed_files[file_path]):
            if isinstance(node, ast.Import):
                for name in node.names:
                    dependencies.append(name.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    dependencies.append(node.module.split('.')[0])

        return list(set(dependencies))

    def validate_code_structure(self, code: str) -> Dict[str, Any]:
        """Validate code structure and return issues."""
        try:
            tree = ast.parse(code)
            return {'valid': True, 'issues': []}
        except SyntaxError as e:
            return {'valid': False, 'issues': [f"Syntax error: {e}"]}


class DependencyGraph:
    """Analyzes codebase dependencies for better planning."""

    def __init__(self, ast_analyzer: ASTAnalyzer):
        self.ast_analyzer = ast_analyzer
        self.graph: Dict[str, List[str]] = {}
        self.reverse_graph: Dict[str, List[str]] = {}

    def build_from_backpack(self, backpack: List[Dict[str, Any]]) -> None:
        """Build dependency graph from backpack files."""
        self.graph.clear()
        self.reverse_graph.clear()

        for item in backpack:
            file_path = item.get('file_path', '')
            content = item.get('content', '')

            if file_path.endswith('.py'):
                analysis = self.ast_analyzer.analyze_file(file_path, content)
                dependencies = self.ast_analyzer.find_dependencies(file_path)

                self.graph[file_path] = dependencies

                # Build reverse graph
                for dep in dependencies:
                    if dep not in self.reverse_graph:
                        self.reverse_graph[dep] = []
                    self.reverse_graph[dep].append(file_path)

    def get_affected_files(self, target_file: str) -> List[str]:
        """Get files that would be affected by changes to target_file."""
        affected = set()

        # Files that depend on target_file
        if target_file in self.reverse_graph:
            affected.update(self.reverse_graph[target_file])

        # Recursive dependencies
        to_check = list(affected)
        checked = set([target_file])

        while to_check:
            current = to_check.pop()
            if current in checked:
                continue
            checked.add(current)

            if current in self.reverse_graph:
                new_affected = set(self.reverse_graph[current]) - checked
                affected.update(new_affected)
                to_check.extend(new_affected)

        return list(affected)

    def get_dependency_order(self) -> List[str]:
        """Get files in dependency order (leaves first)."""
        # Simple topological sort
        visited = set()
        order = []

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            if node in self.graph:
                for dep in self.graph[node]:
                    visit(dep)
            order.append(node)

        for node in self.graph:
            visit(node)

        return order


class RealityValidator:
    """Validates plans against actual codebase reality."""

    def __init__(self, ast_analyzer: ASTAnalyzer, dependency_graph: DependencyGraph):
        self.ast_analyzer = ast_analyzer
        self.dependency_graph = dependency_graph

    def validate_objective(self, objective: str, backpack: List[Dict[str, Any]]) -> PlanValidation:
        """Validate an objective against codebase reality."""
        validation = PlanValidation()

        # Check if objective mentions specific files/functions that exist
        mentioned_files = self._extract_file_references(objective)
        validation.is_grounded = self._validate_file_references(mentioned_files, backpack)

        # Check for missing dependencies
        required_deps = self._extract_dependencies_from_objective(objective)
        validation.missing_dependencies = self._find_missing_dependencies(required_deps, backpack)

        # Calculate confidence score
        validation.confidence_score = self._calculate_confidence(validation)

        return validation

    def _extract_file_references(self, text: str) -> List[str]:
        """Extract file references from text."""
        import re
        # Match patterns like file.py, path/to/file.py, etc.
        file_pattern = r'\b[\w/\\]+\.py\b'
        return re.findall(file_pattern, text)

    def _validate_file_references(self, files: List[str], backpack: List[Dict[str, Any]]) -> bool:
        """Check if referenced files exist in backpack."""
        backpack_files = {item.get('file_path', '').split('/')[-1] for item in backpack}
        return all(file.split('/')[-1] in backpack_files for file in files)

    def _extract_dependencies_from_objective(self, objective: str) -> List[str]:
        """Extract potential dependencies from objective description."""
        # Simple keyword extraction for common libraries
        common_libs = ['os', 'sys', 'json', 'ast', 'typing', 'dataclasses', 'enum']
        found = []
        for lib in common_libs:
            if lib in objective.lower():
                found.append(lib)
        return found

    def _find_missing_dependencies(self, required_deps: List[str], backpack: List[Dict[str, Any]]) -> List[str]:
        """Find dependencies not available in current context."""
        # For now, assume all dependencies are missing if not in backpack
        # In a real implementation, this would check import statements
        return required_deps

    def _calculate_confidence(self, validation: PlanValidation) -> float:
        """Calculate overall confidence score."""
        score = 1.0
        if not validation.is_grounded:
            score *= 0.5
        if validation.missing_dependencies:
            score *= 0.7
        return max(0.0, min(1.0, score))


class CodeAwarePlanner:
    """Production-ready code agent with structured planning and AST integration."""

    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()
        self.dependency_graph = DependencyGraph(self.ast_analyzer)
        self.reality_validator = RealityValidator(self.ast_analyzer, self.dependency_graph)
        self.decomposition_preventer = HierarchicalDecompositionPreventer()
        self.current_phase = PlanningPhase.ANALYSIS
        self.code_context = CodeContext()

    def plan_with_code_awareness(self, main_goal: str, backpack: List[Dict[str, Any]],
                               plan: PlanGraph, codebase_summary: str = "") -> Tuple[PlanGraph, List[str]]:
        """
        Main planning method with code-aware structured phases.

        Returns updated PlanGraph and list of planning insights.
        """
        insights = []

        # Phase 1: Analysis - Build code understanding
        insights.extend(self._analysis_phase(main_goal, backpack, plan, codebase_summary))

        # Phase 2: Design - Create high-level architecture
        insights.extend(self._design_phase(main_goal, backpack, plan))

        # Phase 3: Implementation - Generate specific implementation steps
        insights.extend(self._implementation_phase(main_goal, backpack, plan))

        # Phase 4: Testing - Add validation and testing steps
        insights.extend(self._testing_phase(main_goal, backpack, plan))

        return plan, insights

    def _analysis_phase(self, main_goal: str, backpack: List[Dict[str, Any]],
                       plan: PlanGraph, codebase_summary: str) -> List[str]:
        """Analysis phase: Build comprehensive code understanding."""
        insights = ["=== ANALYSIS PHASE ==="]

        # Build dependency graph and analyze code structure
        self.dependency_graph.build_from_backpack(backpack)

        # Analyze each file in backpack
        for item in backpack:
            file_path = item.get('file_path', '')
            content = item.get('content', '')

            if file_path.endswith('.py'):
                analysis = self.ast_analyzer.analyze_file(file_path, content)
                file_size = len(content.split('\n'))

                # Store in code context
                self.code_context.ast_nodes[file_path] = self.ast_analyzer.analyzed_files.get(file_path)
                self.code_context.function_definitions[file_path] = analysis.get('functions', {})
                self.code_context.class_definitions[file_path] = analysis.get('classes', {})
                self.code_context.file_sizes[file_path] = file_size

                insights.append(f"Analyzed {file_path}: {len(analysis.get('functions', {}))} functions, "
                              f"{len(analysis.get('classes', {}))} classes, {file_size} lines")

        self.current_phase = PlanningPhase.DESIGN
        insights.append("Analysis phase completed - code structure understood")
        return insights

    def _design_phase(self, main_goal: str, backpack: List[Dict[str, Any]], plan: PlanGraph) -> List[str]:
        """Design phase: Create high-level architecture and objectives."""
        insights = ["=== DESIGN PHASE ==="]

        # Use LLM to generate design objectives based on code analysis
        design_prompt = self._generate_design_phase_prompt(main_goal, backpack)

        # Generate initial design objectives
        response = chat_llm(design_prompt)
        design_objectives = self._parse_design_objectives(response)

        # Add design objectives to plan
        for obj_desc in design_objectives:
            validation = self.reality_validator.validate_objective(obj_desc, backpack)
            if validation.confidence_score > 0.6:
                new_obj = plan.add_objective(obj_desc, plan.root_id)
                insights.append(f"Added validated design objective: {obj_desc} (confidence: {validation.confidence_score:.2f})")
            else:
                insights.append(f"Rejected low-confidence objective: {obj_desc} (confidence: {validation.confidence_score:.2f})")

        self.current_phase = PlanningPhase.IMPLEMENTATION
        insights.append("Design phase completed - high-level objectives established")
        return insights

    def _implementation_phase(self, main_goal: str, backpack: List[Dict[str, Any]], plan: PlanGraph) -> List[str]:
        """Implementation phase: Generate specific implementation steps."""
        insights = ["=== IMPLEMENTATION PHASE ==="]

        # Process pending objectives with code-aware unfolding
        pending_objectives = [node_id for node_id, node in plan.nodes.items()
                            if isinstance(node, ObjectiveNode) and node.status == STATUS_PENDING and not node.children]

        for obj_id in pending_objectives:
            self._unfold_objective_code_aware(obj_id, main_goal, backpack, plan, insights)

        self.current_phase = PlanningPhase.TESTING
        insights.append("Implementation phase completed - specific actions generated")
        return insights

    def _testing_phase(self, main_goal: str, backpack: List[Dict[str, Any]], plan: PlanGraph) -> List[str]:
        """Testing phase: Add validation and testing steps."""
        insights = ["=== TESTING PHASE ==="]

        # Add testing objectives for major components
        testing_objectives = [
            "Add syntax validation for all modified files",
            "Verify import dependencies are satisfied",
            "Test core functionality with unit tests",
            "Validate architectural compliance"
        ]

        for test_obj in testing_objectives:
            validation = self.reality_validator.validate_objective(test_obj, backpack)
            if validation.confidence_score > 0.7:
                test_node = plan.add_objective(test_obj, plan.root_id)
                # Add specific testing actions
                plan.add_action(test_node.id, "code_validator",
                              {"validation_type": "syntax", "target_files": "all_modified"},
                              "Validate syntax of all changes")
                insights.append(f"Added testing objective: {test_obj}")

        insights.append("Testing phase completed - validation steps added")
        return insights

    def _unfold_objective_code_aware(self, objective_id: str, main_goal: str,
                                   backpack: List[Dict[str, Any]], plan: PlanGraph,
                                   insights: List[str], current_depth: int = 0) -> bool:
        """Unfold objective with code-aware intelligence and decomposition prevention."""
        objective = plan.get_node(objective_id)

        # Check if we should decompose further
        if not self.decomposition_preventer.should_decompose_further(objective.description, current_depth):
            insights.append(f"Prevented over-decomposition of objective: {objective.description}")
            # Add direct action instead of decomposing further
            plan.add_action(objective_id, "code_editor",
                          {"description": f"Implement: {objective.description}"},
                          "Direct implementation due to sufficient specificity")
            plan.update_node_status(objective_id, STATUS_COMPLETED)
            return True

        # Track this objective
        self.decomposition_preventer.track_objective(objective_id, objective.description, current_depth)

        # Generate code-aware prompt
        prompt = self._generate_code_aware_prompt(main_goal, plan, backpack, objective)

        # Get LLM response
        response = chat_llm(prompt)

        # Parse and execute commands with validation
        success = self._execute_validated_commands(response, plan, objective_id, main_goal, insights)

        plan.update_node_status(objective_id, STATUS_COMPLETED)
        return success

    def _generate_design_phase_prompt(self, main_goal: str, backpack: List[Dict[str, Any]]) -> str:
        """Generate prompt for design phase."""
        # Summarize code structure
        code_summary = []
        total_files = len([f for f in self.code_context.ast_nodes.keys()])
        total_functions = sum(len(funcs) for funcs in self.code_context.function_definitions.values())
        total_classes = sum(len(classes) for classes in self.code_context.class_definitions.values())

        code_summary.append(f"Codebase contains {total_files} Python files, {total_functions} functions, {total_classes} classes")

        return f"""{config.PLANNER_COMMAND_PROMPT_TEMPLATE}

CODE-AWARE DESIGN PHASE:
Current codebase structure: {chr(10).join(code_summary)}

PRIMARY GOAL: {main_goal}

INSTRUCTIONS:
Generate 3-5 high-level design objectives that will guide the implementation.
Each objective should be specific to the codebase structure and reference actual files/classes where possible.
Focus on architectural decisions and major implementation steps.

Respond with design objectives, one per line.
"""

    def _generate_code_aware_prompt(self, main_goal: str, plan: PlanGraph,
                                  backpack: List[Dict[str, Any]], objective: ObjectiveNode) -> str:
        """Generate code-aware prompt for objective unfolding."""
        plan_context = _generate_plan_context(plan)

        # Build comprehensive code context with AST integration
        function_list = []
        for file_path, functions in self.code_context.function_definitions.items():
            function_list.extend([f"{file_path}::{func}" for func in functions.keys()])

        class_list = []
        for file_path, classes in self.code_context.class_definitions.items():
            class_list.extend([f"{file_path}::{cls}" for cls in classes.keys()])

        # Dependency context
        dep_context = []
        for file_path, deps in self.dependency_graph.graph.items():
            if deps:
                dep_context.append(f"{file_path} depends on: {', '.join(deps[:3])}")

        # Build the structured prompt
        code_context_parts = [
            f"Functions: {', '.join(function_list[:15])}",
            f"Classes: {', '.join(class_list[:10])}",
            f"Dependencies: {', '.join(dep_context[:5])}",
        ]
        code_context = "\n".join(code_context_parts)

        return f"""{config.CODE_AWARE_PLANNER_PROMPT_TEMPLATE}

CURRENT OBJECTIVE: {objective.description}

CODE CONTEXT (AST-ENRICHED):
{code_context}

PLAN CONTEXT:
{plan_context}

PRIMARY GOAL: {main_goal}
"""

    def _parse_design_objectives(self, response: str) -> List[str]:
        """Parse design objectives from LLM response."""
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        return [line for line in lines if len(line) > 10][:5]  # Filter and limit

    def _execute_validated_commands(self, response: str, plan: PlanGraph,
                                  objective_id: str, main_goal: str, insights: List[str]) -> bool:
        """Execute commands with reality validation."""
        import re
        command_match = re.match(r'(\w+)\s*(.*)', response.strip(), re.IGNORECASE)
        if not command_match:
            return False

        command_name = command_match.group(1).upper()
        command_params = command_match.group(2)

        # Validate command against reality
        if command_name == 'ADD_OBJECTIVE':
            # Validate objective description
            validation = self.reality_validator.validate_objective(command_params, [])
            if validation.confidence_score < 0.5:
                insights.append(f"Rejected ADD_OBJECTIVE due to low confidence: {validation.confidence_score}")
                return False

        success, message = command_parser.parse_and_execute(
            response.strip(), plan, {'parent_id': objective_id, 'main_goal': main_goal}
        )

        if success:
            insights.append(f"Executed validated command: {command_name}")

        return success


# Global instance for pipeline integration
code_aware_planner = CodeAwarePlanner()


def code_aware_update_plan(main_goal: str, backpack: list[dict], plan: PlanGraph,
                          codebase_summary: str = "") -> tuple[PlanGraph, list]:
    """
    Convenience function for code-aware planning integration.
    Returns updated PlanGraph and list of planning insights.
    """
    return code_aware_planner.plan_with_code_awareness(main_goal, backpack, plan, codebase_summary)