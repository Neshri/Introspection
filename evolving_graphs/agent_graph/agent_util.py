"""
This module provides the core functionality for analyzing and summarizing a Python project.

It defines the main entry point `project_pulse` and the primary orchestrator,
the `ProjectSummarizer` class, which manages the multi-pass process of
generating a detailed "Module Context Map" for an AI agent.
"""

import logging
import os
from collections import deque
from typing import Dict, List, Any

# --- Local Project Imports ---

# Connects to the static code analyzer.
from .graph_analyzer import GraphAnalyzer
# --- Corrected Import ---
# Imports the new, structured data model for the module context.
from .summary_models import ModuleContext, Claim
from .module_contextualizer import ModuleContextualizer

# --- Type Aliases for Readability ---

# A ProjectGraph is a dictionary mapping a module's file path to its analysis data.
ProjectGraph = Dict[str, Any]


class ProjectSummarizer:
    """
    Orchestrates the analysis and iterative generation of a ModuleContext for each file.

    This class encapsulates the project's dependency graph and the state of
    the module contexts, managing the entire workflow from start to finish.
    """
    def __init__(self, graph: ProjectGraph, max_cycles: int = 3):
        """
        Initializes the ProjectSummarizer.

        Args:
            graph: The dependency graph of the project from the GraphAnalyzer.
            max_cycles: The maximum number of refinement passes to perform.
        """
        self.graph = graph
        self.max_cycles = max_cycles
        # This dictionary stores the evolving ModuleContext for each module path.
        self.contexts: Dict[str, ModuleContext] = {}
        # The processing order is computed once during initialization for efficiency.
        self._processing_order = self._compute_topological_order()

    def _compute_topological_order(self) -> List[str]:
        """
        Calculates the module processing order using a topological sort.

        This ensures that a module is always processed after the modules it
        depends on, which is critical for building up contextual understanding.
        """
        order: List[str] = []
        deps_count = {path: len(data.get("dependencies", [])) for path, data in self.graph.items()}
        queue: deque[str] = deque([path for path, count in deps_count.items() if count == 0])

        while queue:
            path = queue.popleft()
            order.append(path)
            for dependent in self.graph.get(path, {}).get("dependents", []):
                deps_count[dependent] -= 1
                if deps_count[dependent] == 0:
                    queue.append(dependent)

        if len(order) != len(self.graph):
            unprocessed = sorted(list(set(self.graph.keys()) - set(order)))
            logging.warning(f"Cycle detected. Unordered modules: {[os.path.basename(p) for p in unprocessed]}")
            order.extend(unprocessed)
        
        return order

    def generate_contexts(self) -> Dict[str, ModuleContext]:
        """
        Runs the iterative process to generate and refine the ModuleContext for each file.
        
        This method iterates over the modules in a stable order for a fixed number
        of cycles or until the contexts no longer change (converge).
        """
        for cycle in range(1, self.max_cycles + 1):
            logging.info(f"--- Starting Refinement Cycle {cycle}/{self.max_cycles} ---")
            has_changed_in_cycle = False

            for path in self._processing_order:
                # Gather the most recent contexts of the current module's dependencies.
                dep_contexts = {
                    dep: self.contexts.get(dep)
                    for dep in self.graph.get(path, {}).get("dependencies", [])
                    if dep in self.contexts
                }
                
                old_context = self.contexts.get(path)
                
                try:
                    # Delegate the actual context generation to the placeholder function.
                    new_context = _create_module_context(path, self.graph, dep_contexts)
                except NotImplementedError:
                    # If the underlying logic is not implemented, create a default,
                    # empty ModuleContext object to allow the system to function.
                    new_context = ModuleContext(file_path=path)

                # If the context has been updated, store it and flag that a change occurred.
                if new_context != old_context:
                    has_changed_in_cycle = True
                    self.contexts[path] = new_context
            
            # If a full cycle completes with no changes, the contexts have stabilized.
            if not has_changed_in_cycle:
                logging.info(f"Module contexts converged after cycle {cycle}. Stopping early.")
                break
        
        return self.contexts

def _create_module_context(path: str, graph: ProjectGraph, dep_contexts: Dict[str, ModuleContext]) -> ModuleContext:
    
    """
    Generates a ModuleContext for a given module path using the provided graph and dependency contexts.

    This function serves as a wrapper for the actual context generation logic, which is delegated to the ModuleContextualizer class.
    It logs the start of context generation for the module and ensures that the resulting ModuleContext has a valid file path.
    """
    logging.info(f"Generating context for module: {os.path.basename(path)}")
    mc = ModuleContextualizer(path, graph, dep_contexts)
    context = mc.contextualize_module()
    # Ensure the ModuleContext has the file path for proper representation
    if hasattr(context, 'file_path') and context.file_path is None:
        context.file_path = path
    elif not hasattr(context, 'file_path'):
        # If the contextualizer returns a ModuleContext without file_path support
        context = ModuleContext(file_path=path)
    return context


def project_pulse(target_file_path: str) -> Dict[str, ModuleContext]:
    """
    Analyzes a Python project and generates a detailed context map for each module.

    This function serves as the main public entry point for the process.
    """
    if not os.path.isfile(target_file_path):
        logging.error(f"Error: Target path '{target_file_path}' is not a valid file.")
        return {}
    
    logging.info(f"Starting project analysis from root: {target_file_path}")
    analyzer = GraphAnalyzer(target_file_path)
    project_graph = analyzer.analyze()
    
    # Instantiate and run the summarizer to orchestrate the main logic.
    summarizer = ProjectSummarizer(project_graph)
    final_contexts = summarizer.generate_contexts()
    
    logging.info("Project context map generation complete.")
    return final_contexts