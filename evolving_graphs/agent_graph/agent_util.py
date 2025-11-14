import logging
import os
from collections import deque
from typing import Dict, List, Any

# Assuming local imports
from .graph_analyzer import GraphAnalyzer

# --- Type Aliases for Clarity ---

# Defines a clear type for the summary object, which is a dictionary.
SummaryObject = Dict[str, Any]
# Defines a clear type for the project graph data structure.
ProjectGraph = Dict[str, Any]

class ProjectSummarizer:
    """
    Orchestrates the analysis and iterative summarization of a Python project.

    This class encapsulates the project's dependency graph and the state of
    module summaries, managing the entire summarization workflow.
    """
    def __init__(self, graph: ProjectGraph, max_cycles: int = 3):
        """
        Initializes the ProjectSummarizer.

        Args:
            graph: The dependency graph of the project.
            max_cycles: The maximum number of refinement passes to perform.
        """
        self.graph = graph
        self.max_cycles = max_cycles
        # This dictionary will store the summary for each module path.
        self.summaries: Dict[str, SummaryObject] = {}
        # The processing order is computed once during initialization for efficiency.
        self._processing_order = self._compute_topological_order()

    def _compute_topological_order(self) -> List[str]:
        """
        Calculates the processing order of modules using a topological sort.

        This ensures that a module is always processed after the modules it
        depends on have been processed.
        """
        # This list will store the final, ordered list of module paths.
        order: List[str] = []
        # This dictionary tracks how many dependencies are left to be processed for each module.
        deps_count = {path: len(data.get("dependencies", [])) for path, data in self.graph.items()}
        # The queue is initialized with all modules that have zero dependencies (the "leaf" nodes).
        queue: deque[str] = deque([path for path, count in deps_count.items() if count == 0])

        # The loop continues as long as there are modules with all dependencies met.
        while queue:
            path = queue.popleft()
            order.append(path)
            
            # For each module that depends on the one just processed...
            for dependent in self.graph.get(path, {}).get("dependents", []):
                # ...decrement its count of remaining dependencies.
                deps_count[dependent] -= 1
                # If the count reaches zero, this module is now ready to be processed.
                if deps_count[dependent] == 0:
                    queue.append(dependent)

        # If the final order doesn't include all modules, a dependency cycle exists.
        if len(order) != len(self.graph):
            unprocessed = sorted(list(set(self.graph.keys()) - set(order)))
            logging.warning(f"Cycle detected. Unordered modules: {[os.path.basename(p) for p in unprocessed]}")
            order.extend(unprocessed)
        
        return order

    def summarize_project(self) -> Dict[str, SummaryObject]:
        """
        Runs the iterative summarization process and returns the final summaries.
        
        This method iterates over the modules in a stable order for a fixed number
        of cycles or until the summaries no longer change.
        """
        # The outer loop handles the refinement cycles.
        for cycle in range(1, self.max_cycles + 1):
            logging.info(f"--- Starting Refinement Cycle {cycle}/{self.max_cycles} ---")
            # This flag tracks if any summary has changed during the current cycle.
            has_changed = False

            # The inner loop processes each module in the pre-calculated topological order.
            for path in self._processing_order:
                # This gathers the most recent summaries of the current module's dependencies.
                dep_summaries = {
                    dep: self.summaries.get(dep)
                    for dep in self.graph.get(path, {}).get("dependencies", [])
                    if dep in self.summaries
                }
                
                old_summary = self.summaries.get(path)
                
                # This block calls the summarization logic.
                try:
                    new_summary = _create_module_summary(path, self.graph, dep_summaries)
                except NotImplementedError:
                    # A placeholder is used if the summarization function isn't implemented.
                    new_summary = {
                        "summary": f"Summary for {os.path.basename(path)} (Cycle {cycle})",
                        "claims": [],
                    }

                # If the summary has been updated, store it and set the flag.
                if new_summary != old_summary:
                    has_changed = True
                    self.summaries[path] = new_summary
            
            # If a full cycle completes with no changes, we can exit early.
            if not has_changed:
                logging.info(f"Summaries converged after cycle {cycle}. Stopping early.")
                break
        
        return self.summaries

def _create_module_summary(path: str, graph: ProjectGraph, dep_summaries: Dict[str, SummaryObject]) -> SummaryObject:
    """Placeholder for the complex, AI-driven summarization logic."""
    logging.info(f"Summarizing module: {os.path.basename(path)}")
    raise NotImplementedError("This function should be implemented with the actual summarization logic.")


def project_pulse(target_file_path: str) -> Dict[str, SummaryObject]:
    """
    Analyzes a Python project and generates summaries for each module.

    This function serves as the main entry point for the entire process.
    """
    # 1. Validate the input file path.
    if not os.path.isfile(target_file_path):
        logging.error(f"Error: Target path '{target_file_path}' is not a valid file.")
        return {}
    
    # 2. Build the project's dependency graph.
    logging.info(f"Starting project analysis from root: {target_file_path}")
    analyzer = GraphAnalyzer(target_file_path)
    project_graph = analyzer.analyze()
    
    # 3. Instantiate and run the summarizer to orchestrate the main logic.
    summarizer = ProjectSummarizer(project_graph)
    final_summaries = summarizer.summarize_project()
    
    logging.info("Project analysis and summarization complete.")
    return final_summaries