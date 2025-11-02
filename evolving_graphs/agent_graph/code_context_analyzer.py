#
# code_context_analyzer.py (Code Context Analyzer)
# Analyzes Python code using AST to build comprehensive code context and understanding.
#

from typing import Dict, List, Optional, Any, Union
import ast
from dataclasses import dataclass, field

from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode, STATUS_PENDING, STATUS_COMPLETED
from .intelligence_plan_memory_interface import planning_memory_interface
from .intelligence_plan_command_utils import command_parser
from .agent_config import config


@dataclass
class CodeContext:
    """Enhanced code context with AST and dependency information."""
    ast_nodes: Dict[str, ast.AST] = field(default_factory=dict)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    import_map: Dict[str, str] = field(default_factory=dict)
    function_definitions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    class_definitions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    file_sizes: Dict[str, int] = field(default_factory=dict)


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


# Global instances for reuse
code_context = CodeContext()
ast_analyzer = ASTAnalyzer()