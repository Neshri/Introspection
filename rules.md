As an expert software architect, your objective is to build a stable, scalable, and AI-friendly codebase (Version 1). The architecture must be highly explicit and easily "crawlable" so that an AI can eventually navigate and modify it safely and efficiently.

Rule 0: System Integrity

    A. Context Propagation: Pass this full ruleset to any sub-agent.

    B. Architectural Recovery Protocol: Before applying new features or complex refactors, the system must first be brought into full architectural alignment. This is a mandatory, prioritized process:

        Prune Unreachable Code: First, identify and delete any deprecated or unreachable modules. A module is considered deprecated if it is not imported and used by an active Orchestrator, a designated entry point, or another referenced module.

        Enforce Structural Conformance: Second, correct any violations of structural rules. This includes renaming files (Semantic Naming), ensuring correct entry points (Designated Entry Points), and verifying directory layouts (Graph Definition).

        Refactor Module Internals: Third, with the structure now correct, refactor the content of all active modules to comply with internal quality rules, primarily Module Token Limit and DRY.

        Validate Dependencies: Finally, verify the integrity of the import graph across the entire aligned system, checking for Acyclic Dependencies and proper Graph Decoupling.

Architectural Rules

Core Structure & The Genome:

    The Genome: The /evolving_graphs/ directory is a self-contained "Genome."

    Graph Definition: A direct subdirectory within a Genome is defined as a "Graph" if and only if it contains a designated entry point file. Directories without an entry point (e.g., __pycache__) are not Graphs.

    Semantic Naming: Module filenames must be domain_responsibility.py.

    Designated Entry Points: Each Graph must have one [graph_name]_main.py entry point.

    Module Token Limit: Modules must not exceed 3,000 tokens (tiktoken).

    DRY (Don't Repeat Yourself): Extract duplicated 5+ line blocks into _utils.py modules.

Recursive Evolution & Execution:

    Recursive Evolution Protocol: To create a child MCTS node, the executing Genome must create a candidates/ directory inside its own evolving_graphs/ directory. The complete, new child Genome must then be placed in a uniquely named subdirectory within that candidates/ directory.

        Example Path: If the parent is at .../parent/evolving_graphs/, the child must be created at .../parent/evolving_graphs/candidates/child_01/evolving_graphs/.

        Crucial Exclusion: The copy operation must explicitly ignore the parent's own candidates/ directory.

    Strictly Relative Paths: All file access and execution paths must be relative to the module's location. A Genome must not traverse upwards (../) beyond its own evolving_graphs/ directory.

    Graph Decoupling: A Graph is forbidden from importing modules from a sibling or child Graph. Interaction is only permitted by executing another Graph's entry point as a separate process.

Imports & API:

    Intra-Graph Imports: Within a single Graph, all Python imports must be relative.

    Mandatory Import Signposts: Every relative import requires a same-line comment explaining its purpose.

    Empty __init__.py: All __init__.py files must be empty.

State & Role Integrity:

    Acyclic Dependencies: Circular dependencies between any modules within a Graph are strictly forbidden. The import graph must be a Directed Acyclic Graph (DAG).

    Orchestrator Privilege: Within a Graph, a single orchestrator class (e.g., PipelineRunner) is the only entity permitted to hold instances of and directly call methods on multiple, distinct roles (e.g., Scout, Planner).

    Role Isolation: Roles are defined as classes that encapsulate a specific step of a workflow. A Role is forbidden from importing, instantiating, or directly calling another sibling Role. All data must be passed to it by the Orchestrator.

Final Compliance Check:

    Before completing a task, verify all changes against these rules.