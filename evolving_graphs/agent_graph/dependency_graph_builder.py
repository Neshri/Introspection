#
# dependency_graph_builder.py (Dependency Graph Builder)
# Builds and analyzes codebase dependency graphs for better planning and validation.
#

from typing import Dict, List, Optional, Any
from .code_context_analyzer import ASTAnalyzer, CodeContext  # AST analysis for dependency extraction


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

    def get_file_dependencies(self, file_path: str) -> List[str]:
        """Get direct dependencies of a specific file."""
        return self.graph.get(file_path, [])

    def get_reverse_dependencies(self, file_path: str) -> List[str]:
        """Get files that depend on the specified file."""
        return self.reverse_graph.get(file_path, [])

    def has_circular_dependency(self) -> bool:
        """Check if the dependency graph has circular dependencies."""
        visited = set()
        rec_stack = set()

        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)

            if node in self.graph:
                for dep in self.graph[node]:
                    if dep not in visited:
                        if has_cycle(dep):
                            return True
                    elif dep in rec_stack:
                        return True

            rec_stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if has_cycle(node):
                    return True
        return False

    def get_dependency_stats(self) -> Dict[str, Any]:
        """Get statistics about the dependency graph."""
        stats = {
            'total_files': len(self.graph),
            'total_dependencies': sum(len(deps) for deps in self.graph.values()),
            'most_depended_on': max(self.reverse_graph.items(), key=lambda x: len(x[1]), default=('', [])),
            'circular_dependencies': self.has_circular_dependency()
        }
        return stats

    def build_from_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Build dependency graph from a list of file paths.

        This method provides compatibility with code that expects build_from_files
        to exist. It analyzes the files and builds a dependency graph, returning
        statistics about the dependencies found.

        Args:
            file_paths: List of file paths to analyze

        Returns:
            Dict containing dependency statistics and analysis
        """
        import os
        result = {
            'file_count': len(file_paths),
            'analyzed_files': [],
            'dependencies_found': {},
            'errors': []
        }

        self.graph.clear()
        self.reverse_graph.clear()

        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    analysis = self.ast_analyzer.analyze_file(file_path, content)
                    dependencies = self.ast_analyzer.find_dependencies(file_path)

                    self.graph[file_path] = dependencies
                    result['analyzed_files'].append(file_path)
                    result['dependencies_found'][file_path] = dependencies

                    # Build reverse graph
                    for dep in dependencies:
                        if dep not in self.reverse_graph:
                            self.reverse_graph[dep] = []
                        self.reverse_graph[dep].append(file_path)
                else:
                    result['errors'].append(f"File not found: {file_path}")
            except Exception as e:
                result['errors'].append(f"Error analyzing {file_path}: {str(e)}")

        # Add dependency statistics
        result.update(self.get_dependency_stats())

        return result