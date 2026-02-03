"""
This module provides the core functionality for analyzing and summarizing a Python project.

It defines the main entry point `project_pulse` and the primary orchestrator,
the `ProjectSummarizer` class, which manages the multi-pass process of
generating a detailed "Module Context Map" for an AI agent.
"""

import logging
import os
from collections import deque
from typing import Dict, List, Any, Tuple

# --- Local Project Imports ---

# Connects to the static code analyzer.
from .graph_analyzer import GraphAnalyzer
# --- Corrected Import ---
# Imports the new, structured data model for the module context.
from .summary_models import ModuleContext, Claim
from .module_contextualizer import ModuleContextualizer
from .map_critic import MapCritic
from .report_renderer import ReportRenderer
from .semantic_gatekeeper import SemanticGatekeeper

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



    def generate_contexts(self) -> Tuple[Dict[str, ModuleContext], List[str]]:
        """
        Runs the iterative process to generate and refine the ModuleContext for each file.
        Now includes a Critic-Driven Refinement phase.
        """
        # Cache to store the input hash for each module from the previous cycle.
        self.context_hashes: Dict[str, str] = {}
        
        # Initialize Critic components
        gatekeeper = SemanticGatekeeper()
        critic = MapCritic(gatekeeper)

        for cycle in range(1, self.max_cycles + 1):
            logging.info(f"--- Starting Refinement Cycle {cycle}/{self.max_cycles} ---")
            has_changed_in_cycle = False
            processed_count = 0
            skipped_count = 0
            
            # Dictionary to store specific critique instructions for this cycle
            # Key: module_path, Value: instruction string
            critique_map = {}
            
            # --- CRITIC PHASE (Start of Cycle 2+) ---
            if cycle > 1:
                logging.info("Invoking MapCritic...")
                # 1. Render current state to a temporary string/file for the critic
                # We can use the ReportRenderer to generate the string in memory if we refactor it,
                # or just write to a temp file and read it back.
                temp_map_path = "TEMP_PROJECT_MAP.md"
                renderer = ReportRenderer(self.contexts, output_file=temp_map_path, verification_file=os.devnull)
                renderer.render() # Writes to file
                
                with open(temp_map_path, "r", encoding="utf-8") as f:
                    current_map_content = f.read()
                
                # 2. Get Critiques
                critiques = critic.critique(current_map_content)
                
                if not critiques:
                    logging.info("Critic found no issues. Stopping early.")
                    break
                
                logging.info(f"Critic found {len(critiques)} issues.")
                
                # 3. Map critiques to file paths
                # The critic returns module names (e.g. "agent_core.py"), we need full paths.
                for mod_name, instruction in critiques:
                    # Find path by basename
                    for path in self.graph.keys():
                        if os.path.basename(path) == mod_name:
                            critique_map[path] = instruction
                            # Force re-analysis by clearing hash
                            if path in self.context_hashes:
                                del self.context_hashes[path]
                            break

            for path in self._processing_order:
                # Gather the most recent contexts of the current module's dependencies.
                dep_contexts = {
                    dep: self.contexts.get(dep)
                    for dep in self.graph.get(path, {}).get("dependencies", [])
                    if dep in self.contexts
                }
                
                # --- Smart Caching Logic ---
                # 1. Calculate Input Hash
                upstream_state_str = ""
                upstream_logic_str = ""
                
                upstream_signature = []
                for dep_ctx in dep_contexts.values():
                    if dep_ctx:
                        for text in dep_ctx.public_api.values():
                            upstream_signature.append(text.text)
                
                upstream_hash_input = "".join(sorted(upstream_signature))
                source_code = self.graph.get(path, {}).get("source_code", "")
                
                # Include critique in the hash! If critique changes, we must re-run.
                critique_instruction = critique_map.get(path)
                critique_hash = str(critique_instruction) if critique_instruction else ""
                
                # Final Input Hash
                current_input_hash = str(hash(source_code + upstream_hash_input + critique_hash))
                
                # 2. Check Cache
                if path in self.context_hashes and self.context_hashes[path] == current_input_hash:
                    skipped_count += 1
                    continue

                # 3. Process Module
                old_context = self.contexts.get(path)
                
                try:
                    # Delegate the actual context generation to the placeholder function.
                    # Pass the critique instruction if it exists
                    new_context = _create_module_context(path, self.graph, dep_contexts, critique_instruction)
                except NotImplementedError:
                    new_context = ModuleContext(file_path=path)

                # 4. Update Cache & State
                self.context_hashes[path] = current_input_hash
                processed_count += 1

                if new_context != old_context:
                    has_changed_in_cycle = True
                    self.contexts[path] = new_context
            
            logging.info(f"Cycle {cycle} Stats: Processed {processed_count}, Skipped {skipped_count} (Cached)")

            if not has_changed_in_cycle and not critique_map:
                logging.info(f"Module contexts converged after cycle {cycle}. Stopping early.")
                break
        
        return self.contexts, self._processing_order

def _create_module_context(path: str, graph: ProjectGraph, dep_contexts: Dict[str, ModuleContext], critique_instruction: str = None) -> ModuleContext:
    """
    Generates a ModuleContext for a given module path using the provided graph and dependency contexts.
    """
    logging.info(f"Generating context for module: {os.path.basename(path)}")
    mc = ModuleContextualizer(path, graph, dep_contexts)
    context = mc.contextualize_module(critique_instruction)
    # Ensure the ModuleContext has the file path for proper representation
    if hasattr(context, 'file_path') and context.file_path is None:
        context.file_path = path
    elif not hasattr(context, 'file_path'):
        context = ModuleContext(file_path=path)
    logging.info(f"Generated context for module: {context}")
    return context





def project_pulse(target_file_path: str) -> Tuple[Dict[str, ModuleContext], List[str]]:
    """
    Analyzes a Python project and generates a detailed context map for each module.

    This function serves as the main public entry point for the process.
    """
    if not os.path.isfile(target_file_path):
        logging.error(f"Error: Target path '{target_file_path}' is not a valid file.")
        return {}, []
    
    logging.info(f"Starting project analysis from root: {target_file_path}")
    analyzer = GraphAnalyzer(target_file_path)
    project_graph = analyzer.analyze()
    
    # Instantiate and run the summarizer to orchestrate the main logic.
    summarizer = ProjectSummarizer(project_graph)
    final_contexts, processing_order = summarizer.generate_contexts()
    
    return final_contexts, processing_order