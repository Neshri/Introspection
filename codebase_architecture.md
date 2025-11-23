# Detailed Codebase Architecture

### 1. Overall System Purpose

The entire application is designed to provide robust, modifiable software architecture for managing complex systems through modular and flexible component interactions. It focuses on executing specific goals within defined project directories by integrating core components like `CrawlerAgent` from the `agent_core` module, enforcing comprehensive code quality checks via linting rules, and allowing safe experimentation with graph data through sandboxing operations.

### 2. Architectural Entry Points

- **`evolving_graphs.agent_graph.agent_graph_main`:** Acts as the main entry point for executing specific goals within a given project directory. It orchestrates the process by locating the root file, instantiating `CrawlerAgent`, and running its lifecycle using the `run()` method.
  
- **`evolving_graphs.linter_graph.linter_main.py`:** Serves as the primary script to run an exhaustive suite of linting rules across the codebase. It orchestrates all predefined coding-style checks and reports any violations, ensuring high standards for code quality and consistency.

- **`evolving_graphs.sandboxer_graph.sandboxer_graph_main`:** Provides a mechanism to create a copy of specified graph directories within the project's structure, enabling safe experimentation without affecting original data.

### 3. Detailed Workflow Analysis

#### `evolving_graphs.agent_graph.agent_graph_main`

1. **Import Necessary Libraries:** Uses Python's built-in libraries such as `argparse`, `os.walk` for parsing command-line arguments and traversing directories.
   
2. **Parse Command-Line Arguments:** Utilizes `argparse.ArgumentParser` to accept parameters like `--goal` and `--target_folder`.

3. **Locate Root File:** Implements a directory traversal mechanism using `os.walk` starting from the provided `target_folder`, searching for files ending with `_main.py`.

4. **Instantiate CrawlerAgent:** Upon identifying the target root, instantiates an instance of `CrawlerAgent` from `agent_core`, passing along the execution goal.

5. **Execute Agent Lifecycle:** Calls the `run()` method on the `CrawlerAgent` instance to execute the lifecycle of the agent based on the provided goal.

6. **Return Confirmation Message:** After successful execution, returns a message confirming completion.

#### `evolving_graphs.linter_graph.linter_main.py`

1. **Main Function Invocation:** Executes `main()`, which orchestrates the entire linting workflow by accepting either a single file or multiple directories as input via command-line arguments.

2. **Argument Parsing and Path Resolution:** Uses `argparse` to handle user inputs, validating paths with `resolve_path()` ensuring they are relative to or absolute within the project root (`evolving_graphs`).

3. **File/Directory Traversal:** Iterates through the provided files or directories using `os.walk`.

4. **Rule Execution Sequence:** Sequentially executes each linting rule:
   - Checks architectural recovery considerations.
   - Validates import comments and imports compliance.
   - Detects duplication, file sizes, initialization consistency.
   - Ensures orchestrator pattern adherence.
   - Verifies cross-graph imports.
   - Confirms final token compliance.

5. **Collect and Report Violations:** Accumulates violations per rule category, reporting them after all checks complete.

6. **Exit Code Communication:** Returns `1` for any violations or `0` for successful linting across the project.

#### `evolving_graphs.sandboxer_graph.sandboxer_graph_main`

1. **Main Function Invocation:** Executes with a single argument (`graph_folder`) representing the directory to be copied.

2. **Copy Operation Using shutil:** Utilizes `shutil.deepcopy()` to create an exact copy of the specified graph directory within the project's structure, returning its absolute path.

### 4. Key Data Structures & Concepts

- **Backpack:** In the context of `agent_graph`, it likely refers to a temporary storage mechanism for gathered files or data structures that are passed between components like Scout and Planner.
  
- **Plan:** Likely contains detailed information on tasks or strategies derived from the original codebase, possibly including execution paths, dependencies, or configurations required for running specific goals.

- **Verification Result:** Represents the outcome of linting operations, which could be a structured object containing lists of violations categorized by rule type and any associated messages. This result is crucial for communicating success or failure between components, often used to determine next steps in development workflows such as CI/CD pipelines.