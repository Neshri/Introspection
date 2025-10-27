# Detailed Codebase Architecture

### 1. Overall System Purpose

The application is designed to iteratively explore and refine a codebase within an evolving graphs project, ensuring code quality, architectural adherence, and strategic planning. It employs an agent to achieve a defined goal, coupled with a linter that continuously monitors the codebase for violations of architectural principles and best practices. The system prioritizes a flat architecture and provides a mechanism for verification and ongoing improvement.

### 2. Architectural Entry Points

*   `evolving_graphs.agent_graph.agent_graph_main`: Responsible for initiating the agent’s execution by instantiating an `Agent` object and triggering the agent's goal-oriented workflow.
*   `evolving_graphs.linter_graph.linter_graph_main`: Responsible for continuously monitoring the project's codebase using a suite of linters and checks, ensuring architectural compliance and code quality.

### 3. Detailed Workflow Analysis

**A. `evolving_graphs.agent_graph.agent_graph_main` Workflow:**

1.  **Command-Line Argument Parsing:** The `agent_graph_main` module receives a command-line argument, which represents the agent's goal string.
2.  **Agent Instantiation:**  The module then instantiates an `Agent` object from the `evolving_graphs.agent_graph.agent_core` module.
3.  **Agent Activation:** The `Agent` object then calls its `run_with_agent()` method.
4.  **Pipeline Runner Instantiation:** Inside `run_with_agent()`, the `Agent` instantiates a `PipelineRunner` from `pipeline_pipeline_runner`.
5.  **Backpack Creation:** The `PipelineRunner` instantiates a `Scout` from `intelligence_project_scout` to gather files into a "backpack" object.
6.  **Plan Generation:** The `PipelineRunner` passes the 'backpack' containing the discovered files to a `Planner` from `intelligence_plan_generator` to construct a strategic plan object.
7.  **Pipeline Execution:** The `Planner` determines the order of execution and, based on the plan, instructs the `PipelineRunner` to execute the identified pipeline stages.  Each stage could involve file processing, data manipulation, or other specific actions defined in the project.
8.  **Verification:** After each pipeline stage (or at a defined interval), the `PipelineRunner` invokes a `Verifier` (potentially from `verification_project_verifier`) to evaluate the outcome of the stage. The verifier reports on the stage’s success or failure and any specific issues detected.

**B. `evolving_graphs.linter_graph.linter_graph_main` Workflow:**

1.  **File Collection:** The `linter_graph_main` module receives a set of target files or directories from the command line or configuration. It utilizes the `collect_target_files()` function to determine the files to analyze. The `resolve_path` function within this module ensures all paths are absolute, relative to the project root.
2.  **Linter Initialization:** The `linter_graph_main` module initializes a series of linters and checks, potentially using a configuration file or other mechanism to specify which rules to apply. This includes linters for architectural recovery, import compliance, and more.
3.  **Rule Execution:** For each target file, the module invokes the appropriate linters.  Each linter performs its specified checks against the file’s content.
4.  **Violation Reporting:** Each linter generates a report detailing any violations it finds.  The report includes the file name, line number, and the nature of the issue.
5.  **Violation Aggregation:** The `linter_graph_main` module collects all the reported violations from the different linters into a single aggregated report.
6. **Verification Report Generation:** Finally, the module generates a comprehensive report of all violations detected across all files, which can then be consumed by other components of the system (potentially for triggering manual review or automated remediation).

### 4. Key Data Structures & Concepts

*   **Backpack:**  The "backpack" is a data structure used by the `Scout` (from `intelligence_project_scout`) to temporarily hold the files discovered during a specific exploration phase. It’s a dynamically updated list of file paths that the `Planner` later uses to determine the order of execution.
*   **Plan:** The `Plan` object, created by the `Planner` (from `intelligence_plan_generator`), represents the strategic order of execution for the pipeline.  It contains a sequence of steps or actions, along with dependencies between those actions. It might incorporate information about file dependencies, stage priorities, or other relevant constraints.
*   **Verification Result:** The `Verifier` (from potentially `verification_project_verifier`) produces a `VerificationResult` object. This object signifies the success or failure of a specific pipeline stage. If the stage fails, the `VerificationResult` will include details about the nature of the failure. The format of this result enables the system to track progress and trigger corrective actions.  A single `VerificationResult` is returned after each action.