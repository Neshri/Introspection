#
# reality_validator.py (Reality Validator)
# Validates plans against actual codebase reality using code analysis and dependency checking.
#

from typing import Dict, List, Optional, Any
import re
from dataclasses import dataclass, field

from .code_context_analyzer import ASTAnalyzer, CodeContext  # AST analysis for validation
from .dependency_graph_builder import DependencyGraph  # Dependency analysis for validation


@dataclass
class PlanValidation:
    """Reality validation results for plan components."""
    is_grounded: bool = False
    missing_dependencies: List[str] = field(default_factory=list)
    syntax_errors: List[str] = field(default_factory=list)
    architectural_issues: List[str] = field(default_factory=list)
    confidence_score: float = 0.0


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

        # Check for syntax issues in objective description
        validation.syntax_errors = self._validate_objective_syntax(objective)

        # Check architectural compliance
        validation.architectural_issues = self._check_architectural_compliance(objective, backpack)

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

    def _validate_objective_syntax(self, objective: str) -> List[str]:
        """Check for syntax-related issues in objective description."""
        issues = []

        # Check for very long objectives that might be poorly formed
        if len(objective.split()) > 50:
            issues.append("Objective description is very long - consider breaking it down")

        # Check for common malformed patterns
        if objective.strip().startswith('and ') or objective.strip().startswith('or '):
            issues.append("Objective starts with conjunction - may be incomplete")

        return issues

    def _check_architectural_compliance(self, objective: str, backpack: List[Dict[str, Any]]) -> List[str]:
        """Check if objective complies with architectural rules."""
        issues = []

        # Check for references to forbidden patterns
        if 'import evolving_graphs.' in objective and 'from .' not in objective:
            issues.append("Objective suggests forbidden absolute import")

        # Check for module size concerns
        if 'large module' in objective.lower() or 'big file' in objective.lower():
            issues.append("Consider splitting large modules rather than just mentioning size")

        return issues

    def _calculate_confidence(self, validation: PlanValidation) -> float:
        """Calculate overall confidence score."""
        score = 1.0
        if not validation.is_grounded:
            score *= 0.5
        if validation.missing_dependencies:
            score *= 0.7
        if validation.syntax_errors:
            score *= 0.8
        if validation.architectural_issues:
            score *= 0.9
        return max(0.0, min(1.0, score))

    def validate_plan_feasibility(self, objectives: List[str], backpack: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate overall plan feasibility."""
        validations = [self.validate_objective(obj, backpack) for obj in objectives]

        overall_score = sum(v.confidence_score for v in validations) / len(validations) if validations else 0.0
        all_issues = {
            'missing_dependencies': list(set(dep for v in validations for dep in v.missing_dependencies)),
            'syntax_errors': list(set(err for v in validations for err in v.syntax_errors)),
            'architectural_issues': list(set(issue for v in validations for issue in v.architectural_issues))
        }

        return {
            'overall_confidence': overall_score,
            'issues': all_issues,
            'feasible': overall_score > 0.6
        }