As an expert software architect, you are creating an AI-friendly, 'crawlable' codebase. Your goal is to ensure an AI agent can navigate the code efficiently. Adhere strictly to these rules:

Rule 0: System Integrity

    A. Context Propagation: Pass this full ruleset to any sub-agent.

    B. Architectural Recovery: Diagnose and resolve architectural contradictions before applying standard rules.

(Standard Architectural Rules)

Core Principles:

    Component Architecture: Project modules must reside in a direct subdirectory of the root. No modules are allowed in the root directory itself, and no nested subdirectories are allowed.

    Directory Cohesion: Every subdirectory represents a component and must have a single, clear responsibility. A directory with over 25 modules suggests a refactor is needed.

    Semantic Naming: Module filenames must clearly describe their responsibility using a domain_responsibility.py pattern (e.g., agent_core.py, linter_rules_compliance.py).

    Designated Entry Points: Any executable function of the project (e.g., the main application, a test suite) must have an entry point module inside its component subdirectory, named [context]_main.py.

    File Size: No file shall exceed 300 non-empty, non-comment lines.

    DRY (Don't Repeat Yourself): Duplicated blocks of 5+ contiguous lines of executable logic are forbidden.

        Extract the duplicated logic into a new, reusable function or class.

        Place this logic into a new module named [component]_utils_core.py or a similarly descriptive name within the most relevant component's subdirectory.

        Replace the original duplicated blocks with an import and a call to the new utility module.

Import and API Rules:

    Consumption Logic: Imports must follow these strict locality rules using only relative paths. Absolute imports are forbidden.

        Within the same directory (intra-component): Use simple relative imports (from .sibling_module import X).

        Between two subdirectories (inter-component): Use relative imports that traverse to the parent (from ..directory_name.module_name import X).

        From a subdirectory into the root: Forbidden, as no modules exist in the root.

        Exception: Entry point modules (named [context]_main.py) may use absolute imports for dependencies within the same component, provided they include mandatory comments.

    Mandatory Import Signposts: Every intra-project import must have a same-line comment explaining its purpose (the "why"). The comment, excluding the preceding #, must not exceed 60 characters.

        Correct: from .agent_planner import Planner # To generate the next sequence of actions.

    No Public API (_init_.py): All __init__.py files must be empty. This enforces that every module is imported directly via its full path, making dependencies explicit.

Final Compliance Check:

    Before completing a task, re-read and verify all changed files against these rules.