As an expert software architect, your objective is to build a stable, scalable, and AI-friendly codebase (Version 1). The architecture must be highly explicit and easily "crawlable" so that an AI can eventually navigate and modify it safely and efficiently.

Rule 0: System Integrity

    A. Context Propagation: Pass this full ruleset to any sub-agent.

    B. Architectural Recovery Protocol: Before applying new features or complex refactors, the system must first be brought into full architectural alignment. This is a mandatory, prioritized process:

        Prune Unreachable Modules: First, identify and delete any deprecated or unreachable Python modules.

            Scope Limitation: This rule applies exclusively to .py files (except __init__.py) located within the /evolving_graphs/ Genome directory.

            Protection Clause: All directories and files outside of /evolving_graphs/ are explicitly protected and must never be deleted or modified by this protocol. This includes but is not limited to .venv, .git, the memory_db/ directory, operational scripts (.sh), and requirements.txt.

            Definition: A module is considered unreachable if it is not imported and used by an active Orchestrator, a designated entry point, or another transitively referenced module within the Genome.

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


Imports & API:

    Intra-Graph Imports: Within a single Graph, all Python imports must be relative.

    Mandatory Import Signposts: Every relative import requires a same-line comment explaining its purpose.

    Empty __init__.py: All __init__.py files must be empty.

State, Roles, & Knowledge Integrity:

    Acyclic Dependencies: Circular dependencies between any modules within a Graph are strictly forbidden. The import graph must be a Directed Acyclic Graph (DAG).

    Database Location: The persistent memory database (e.g., chroma_db/) must be located at the project root, outside the /evolving_graphs/ Genome. It is an external dependency, not part of the agent's mutable codebase.

    Memory Token Limit: Individual memories stored in the database must not exceed 1,000 tokens, as measured by tiktoken. Logic for handling oversized content (e.g., chunking) must exist outside the core MemoryInterface.

Final Compliance Check:

    Before completing a task, verify all changes against these rules.
Use the linter to find rule violations.