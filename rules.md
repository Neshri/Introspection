As an expert software architect, you are creating an AI-friendly, 'crawlable' codebase. Your goal is to ensure an AI agent can navigate the code efficiently. Adhere strictly to these rules:

Rule 0: System Integrity

    A. Context Propagation: Pass this full ruleset to any sub-agent.

    B. Architectural Recovery: Diagnose and resolve architectural contradictions before applying standard rules.

(Standard Architectural Rules)

Core Principles:

    Shallow Architecture: Project modules must reside in the root directory or in a direct subdirectory of the root. No nested subdirectories are allowed.

    Directory Cohesion: Every subdirectory must have a single, clear responsibility. A directory with over 7 modules suggests a refactor is needed.

    Semantic Naming: Module filenames must clearly describe their responsibility using a domain_responsibility.py pattern (e.g., agent_executor.py).

    Designated Entry Points: Any executable function of the project (e.g., the main application, a test suite) must have a single entry point module in the root directory, named [context]_main.py.

    File Size: No file shall exceed 300 non-empty, non-comment lines.

    DRY (Don't Repeat Yourself): Duplicated blocks of 5+ contiguous lines of executable logic are forbidden.

        Extract the duplicated logic into a new, reusable function or class.

        Place this logic into a new module named utils_[description].py. This utility module should reside in the root directory.

        Replace the original duplicated blocks with an import and a call to the new utility module.

Import and API Rules:

    Consumption Logic: Imports must follow these strict locality rules:

        Within the same directory: Use simple relative imports (from .sibling_module import X).

        From a subdirectory into the root: Forbidden. Root modules cannot depend on subdirectories. Logic needed by the root must reside in the root.

        From the root into a subdirectory: Use relative imports (from ..root_module import X).

        Between two subdirectories: Use relative imports (from ..directory_name.module_name import X).

    Mandatory Import Signposts: Every intra-project import must have a same-line comment explaining its purpose (the "why"). The comment, excluding the preceding #, must not exceed 60 characters.

        Correct: from .agent_planner import Planner # To generate the next sequence of actions.

    No Public API (__init__.py): All __init__.py files must be empty. This enforces that every module is imported directly via its full path, making dependencies explicit.

Final Compliance Check:

    Before completing a task, re-read and verify all changed files against these rules.