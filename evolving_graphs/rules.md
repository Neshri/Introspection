As an expert software architect, your objective is to build a stable, scalable, and AI-friendly codebase (Version 1). The architecture must be highly explicit and easily "crawlable" so that an AI can eventually navigate and modify it safely and efficiently.

Rule 0: System Integrity

    A. Context Propagation: Pass this full ruleset to any sub-agent.

    B. Architectural Recovery: Before writing code, resolve architectural contradictions.

Architectural Rules

Core Structure & The Genome:

    The Genome: The /evolving_graphs/ directory is a self-contained "Genome."

    Component Architecture: A Genome consists of "graphs" (direct subdirectories). All modules must belong to a specific graph.

    Semantic Naming: Module filenames must be domain_responsibility.py.

    Designated Entry Points: Each graph must have a [context]_main.py entry point.

    Module Token Limit: Modules must not exceed 3,000 tokens (tiktoken).

    DRY (Don't Repeat Yourself): Extract duplicated 5+ line blocks into _utils.py modules.

Recursive Evolution & Execution:

    Recursive Evolution Protocol: To create a child MCTS node, a complete copy of the parent Genome must be placed in a candidates/[candidate_id]/ subdirectory at the parent's root.

        Crucial Exclusion: The copy operation must explicitly ignore the parent's candidates/ directory. This ensures the new child is a clean clone of the parent's current logic, not its entire evolutionary history.

    Strictly Relative Paths: All file access and execution paths must be relative. A Genome must not traverse upwards (../).

    Inter-Component Execution: Graphs are executed as subprocesses via their entry points. Direct cross-graph imports are forbidden.

Imports & API:

    Strictly Relative Imports: All Python imports within a Genome must be relative.

    Mandatory Import Signposts: Every relative import requires a same-line comment explaining its purpose.

    Empty __init__.py: All __init__.py files must be empty.

State & Pipeline Integrity:

    Orchestrator Pattern: A single orchestrator class (e.g., PipelineRunner) must manage the operational sequence. It is responsible for initializing all roles (Scout, Planner, etc.) and holding the primary state (main_goal, database connections).

    Linear Data Flow: The orchestrator must explicitly pass data between roles, with the output of one role becoming the input for the next (e.g., plan = self.planner.create_plan(..., backpack)). Roles are forbidden from directly accessing the state of other sibling roles; all communication must be managed by the orchestrator.

Final Compliance Check:

    Before completing a task, verify all changes against these rules.