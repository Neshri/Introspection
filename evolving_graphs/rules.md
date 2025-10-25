As an expert software architect, your objective is to build a stable, scalable, and AI-friendly codebase (Version 1). The architecture must be highly explicit and easily "crawlable" so that an AI can eventually navigate and modify it safely and efficiently.

Rule 0: System Integrity

    A. Context Propagation: Pass this full ruleset to any sub-agent assisting in development to ensure architectural consistency.

    B. Architectural Recovery: Before writing code, diagnose and resolve any contradictions in the existing architecture against these rules.

Architectural Rules

Core Structure:

    Component Architecture: All primary components, hereafter referred to as "graphs" (e.g., agent_graph, linter_graph), must reside as direct subdirectories within the /evolving_graphs/ directory. No Python modules are permitted in the project root or directly within /evolving_graphs/. All modules must belong to a specific graph.

    Semantic Naming: Module filenames must follow the domain_responsibility.py pattern (e.g., agent_core.py, memory_interface.py).

    Designated Entry Points: Each component subdirectory must have a single executable entry point named [context]_main.py.

    File Size: Modules shall not exceed 300 non-empty, non-comment lines to enforce modularity.

    DRY (Don't Repeat Yourself): Duplicated blocks of 5+ lines are forbidden. Extract them into a function within a relevant [component]_utils.py module.

Imports & API:

    Strictly Relative Imports: All intra-project imports must be relative. This ensures components are self-contained and prevents unintended coupling. Absolute imports are forbidden.

        Intra-Component: from .sibling_module import X

        Inter-Component Execution: A component may only execute another component as a subprocess via its entry point, never through a direct import. This creates a stability firewall.

    Mandatory Import Signposts: Every relative import must have a same-line comment explaining its purpose.

        from .agent_planner import Planner # To generate the next sequence of actions.

    Empty __init__.py: All __init__.py files must be empty to make every module dependency explicit in its import path.

State and Data Management:

    Bounded Context Object: To prevent passing excessive arguments, aggregate operational state and configuration into Context objects (e.g., AgentContext). These objects are created in the main entry point and passed down the call stack, making data dependencies explicit in function signatures.

    Memory Abstraction Layer: All interactions with the external memory store (e.g., ChromaDB) must be handled by a single, dedicated memory_interface.py module. This module is the sole gateway for memory operations and should be accessed via the Context object.

Final Compliance Check:

    Before completing a task, re-read and verify all changed files against these rules.