# evolving_graphs/agent_graph/agent_graph_main.py

import os
import ast
import sys
import networkx as nx
import ollama

# Add the project root to the Python path to allow for consistent module resolution.
sys.path.append(os.getcwd())

class HierarchicalCodeDescriptor:
    """
    Analyzes a Python codebase, building a dependency graph and generating a hierarchical,
    recursive summary of the entire system architecture using an LLM.
    """

    def __init__(self, root_dir, model="gemma3:4b-it-qat"):
        self.root_dir = root_dir
        self.model = model
        self.dependency_graph = nx.DiGraph()
        self.summaries = {}  # Cache for generated summaries (memoization)

    def _find_python_files(self):
        """Finds all Python files, ignoring common non-code directories."""
        excluded_dirs = {'.venv', '.git', '__pycache__', 'candidates', 'memory_db'}
        for root, dirs, files in os.walk(self.root_dir, topdown=True):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if file.endswith(".py"):
                    yield os.path.join(root, file)

    def _get_module_name(self, file_path):
        """Converts a file path to a Python module name."""
        rel_path = os.path.relpath(file_path, self.root_dir)
        return os.path.splitext(rel_path.replace(os.sep, '.'))[0]

    def _build_dependency_graph(self):
        """
        Builds a dependency graph by first creating all nodes, then adding edges.
        This prevents race conditions where nodes are created without attributes.
        """
        python_files = list(self._find_python_files())
        module_map = {self._get_module_name(fp): fp for fp in python_files}

        # PHASE 1: Create all nodes with their path attribute first.
        for module_name, file_path in module_map.items():
            self.dependency_graph.add_node(module_name, path=file_path)

        # PHASE 2: Parse files and add edges between the existing nodes.
        for module_name, file_path in module_map.items():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=file_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ImportFrom):
                            if node.level > 0:
                                parent_parts = module_name.split('.')[:-node.level]
                                base = ".".join(parent_parts)
                                imported_module = f"{base}.{node.module}" if node.module else base
                            else:
                                imported_module = node.module

                            if imported_module in module_map:
                                self.dependency_graph.add_edge(imported_module, module_name)
                        elif isinstance(node, ast.Import):
                            for alias in node.names:
                                if alias.name in module_map:
                                    self.dependency_graph.add_edge(alias.name, module_name)
            except Exception as e:
                print(f"Warning: Could not parse {file_path}: {e}")
        
        # Validate that the graph is a Directed Acyclic Graph (DAG)
        if not nx.is_directed_acyclic_graph(self.dependency_graph):
            print("Error: Circular dependencies detected! This will break the recursive summary.")
            cycles = list(nx.simple_cycles(self.dependency_graph))
            for i, cycle in enumerate(cycles):
                print(f"  Cycle {i+1}: {' -> '.join(cycle)} -> {cycle[0]}")
            sys.exit(1) # Exit because recursion will fail

    def _chat_llm(self, prompt):
        """Wrapper for the ollama chat LLM."""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content'].strip()
        except Exception as e:
            return f"Error: LLM chat failed: {e}"

    def _get_or_generate_summary(self, module_name):
        """
        Recursively gets or generates a summary for a module.
        This is the core of the hierarchical summarization.
        """
        if module_name in self.summaries:
            return self.summaries[module_name]

        print(f"  -> Synthesizing summary for: {module_name}")

        dependencies = list(self.dependency_graph.predecessors(module_name))
        dependency_summaries_text = ""
        if dependencies:
            print(f"     Found dependencies: {', '.join(dependencies)}")
            summaries = [self._get_or_generate_summary(dep) for dep in dependencies]
            dependency_summaries_text = "\n\n".join(
                [f"--- Dependency: `{dep}` ---\n{summary}" for dep, summary in zip(dependencies, summaries)]
            )
        else:
            print("     No internal dependencies found.")
            
        module_path = self.dependency_graph.nodes[module_name]['path']
        with open(module_path, "r", encoding="utf-8") as f:
            code = f.read()

        prompt = f"""
        As an expert software architect, create a concise, high-level summary of a Python module based on its code and the summaries of its dependencies.

        **CONTEXT: DEPENDENCY SUMMARIES**
        {dependency_summaries_text if dependency_summaries_text else "This module has no internal project dependencies."}
        
        **MODULE TO ANALYZE: `{module_name}`**
        ```python
        {code}
        ```

        **YOUR TASK:**
        Analyze the code for `{module_name}` and write a summary that explains:
        1.  **Purpose:** What is the single primary responsibility of this module?
        2.  **Key Exports:** What are the most important classes or functions this module provides for other modules to use (its public API)?
        3.  **Role & Interaction:** How does it use its dependencies (if any) to achieve its purpose? How does it contribute to the overall system?

        **Focus on the architectural significance and the connections between modules.**
        """
        
        print(f"     Querying LLM for {module_name}...")
        summary = self._chat_llm(prompt)
        
        self.summaries[module_name] = summary
        return summary

    def generate_hierarchical_description(self):
        """
        Generates a final, synthesized description of the entire codebase.
        """
        print("Step 1/3: Building and validating dependency graph...")
        self._build_dependency_graph()

        print("\nStep 2/3: Identifying architectural entry points (root nodes ending in '_main.py')...")
        root_nodes = [
            module_name
            for module_name in self.dependency_graph.nodes()
            if self.dependency_graph.nodes[module_name]['path'].endswith('_main.py')
        ]

        if not root_nodes:
            print("Error: Could not find any root nodes matching the '_main.py' convention.")
            return

        print(f"-> Found {len(root_nodes)} entry point(s): {', '.join(root_nodes)}")
        print("\nStep 3/3: Starting recursive summarization from entry point(s)...")
        
        root_summaries = [self._get_or_generate_summary(root) for root in root_nodes]

        print("\nStep 4/4: Synthesizing the final detailed and precise architectural analysis...")
        
        final_context = "\n\n".join(
            [f"--- High-Level Component Summary: `{root}` ---\n{summary}" for root, summary in zip(root_nodes, root_summaries)]
        )

        # --- MODIFIED SYNTHESIS PROMPT (FORBIDS BLACK BOXES) ---
        synthesis_prompt = f"""
        As a Chief Architect, you have been given high-level summaries for the main entry points of a software project. Your task is to synthesize these into a single, detailed, and practical architectural overview.

        **COMPONENT SUMMARIES:**
        {final_context}

        **YOUR TASK:**
        Write a final architectural overview of the entire system. Structure your response in Markdown with the following sections:

        ### 1. Overall System Purpose
        A brief, one-paragraph description of what the entire application is designed to do.

        ### 2. Architectural Entry Points
        A bulleted list of the main entry points (`{'`, `'.join(root_nodes)}`) and their primary responsibilities.

        ### 3. Detailed Workflow Analysis
        For **each** entry point listed above, provide a detailed, step-by-step description of its execution flow. 
        
        **CRITICAL RULE:** You MUST be specific. When mentioning a class or function, you MUST state the full module it comes from (e.g., "instantiates `PipelineRunner` from `pipeline_pipeline_runner`"). Do NOT use generic placeholders like "from a core module" or "from a helper function." Be precise.
        
        For example:
        - "Execution begins in `agent_graph_main`, which instantiates `PipelineRunner` from `pipeline_pipeline_runner`."
        - "`PipelineRunner.run_pipeline()` is called, which first invokes the `Scout` (from `intelligence_project_scout`) to gather files into a 'backpack'."
        - "This 'backpack' is then passed to the `Planner` (from `intelligence_plan_generator`) to create a strategic 'plan' object."

        ### 4. Key Data Structures & Concepts
        Based on the summaries, identify and describe the core data objects or concepts that are passed between the major components. For example:
        - **Backpack:** What is its purpose and what does it likely contain?
        - **Plan:** What kind of information is stored in the plan?
        - **Verification Result:** How is success or failure communicated between components?

        This document must be detailed and precise enough for a new developer to trace the code's execution path accurately.
        """
        
        final_description = self._chat_llm(synthesis_prompt)
        
        output_path = os.path.join(self.root_dir, "codebase_architecture.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Detailed Codebase Architecture\n\n{final_description}")
        
        print(f"\n✅ Detailed and precise hierarchical description successfully generated: {output_path}")

def main():
    """
    Main entry point for the hierarchical code descriptor script.
    """
    project_root = "." 
    print(f"Starting Hierarchical Code Descriptor for project at: {os.path.abspath(project_root)}")
    print("-" * 60)
    
    descriptor = HierarchicalCodeDescriptor(root_dir=project_root)
    descriptor.generate_hierarchical_description()
    print("-" * 60)

if __name__ == "__main__":
    main()