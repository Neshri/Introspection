#!/usr/bin/env python3
"""
Combined script to check all coding rules for flat architecture.
Runs all validation checks with a single command.
Updated for simplified ruleset without hierarchical structure checks.
Supports optional single-file mode when a _main.py file is specified.
"""

import os  # filesystem operations
import sys  # system-specific parameters and functions
import argparse  # command-line argument parsing

# Handle imports for both package and standalone execution
try:
    from .linter_rules_recovery import check_architectural_recovery
    from .linter_rules_importcomments import check_import_comments
    from .linter_rules_importcompliance import check_imports_compliance
    from .linter_rules_duplication import check_duplication
    from .linter_rules_filesize import check_file_sizes
    from .linter_rules_compliance import check_final_compliance
except ImportError:
    # Fallback for standalone execution
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from linter_rules_recovery import check_architectural_recovery  # To diagnose and resolve architectural contradictions.
    from linter_rules_importcomments import check_import_comments  # To validate explanatory comments on imports.
    from linter_rules_importcompliance import check_imports_compliance  # To ensure imports comply with flat architecture rules.
    from linter_rules_duplication import check_duplication  # To detect potential code duplication.
    from linter_rules_filesize import check_file_sizes  # To enforce file size limits.
    from linter_rules_compliance import check_final_compliance  # To perform final compliance check on modified files.


def find_project_root():
    """Find the project root directory containing the evolving_graphs folder."""
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, 'evolving_graphs')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    # Fallback to current directory if not found
    return os.getcwd()


def resolve_path(path_str):
    """Resolve a path relative to the project root if relative, or absolute if already absolute."""
    if os.path.isabs(path_str):
        return path_str
    project_root = find_project_root()
    return os.path.abspath(os.path.join(project_root, path_str))


def validate_file(file_path):
    """Validate that the provided file path exists and is a Python file."""
    if not file_path.endswith('.py'):
        raise ValueError(f"File must end with '.py'. Provided: {file_path}")
    if not os.path.isfile(file_path):
        raise ValueError(f"File does not exist: {file_path}")
    return file_path


def validate_directories(dirs):
    """Validate that provided directory paths exist."""
    for dir_path in dirs:
        if not os.path.isdir(dir_path):
            raise ValueError(f"Directory does not exist: {dir_path}")
    return dirs


def collect_target_files(folders=None, file_path=None):
    """Collect target files to lint based on folders or single file."""
    target_files = []
    if file_path:
        target_files = [resolve_path(file_path)]
    elif folders:
        resolved_folders = [resolve_path(f) for f in folders]
        for folder in resolved_folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith('.py'):
                        target_files.append(os.path.abspath(os.path.join(root, file)))
    else:
        # Default: scan evolving_graphs
        for root, dirs, files in os.walk(resolve_path('evolving_graphs')):
            for file in files:
                if file.endswith('.py'):
                    target_files.append(os.path.abspath(os.path.join(root, file)))
    return target_files


def parse_arguments():
    """Parse command-line arguments using argparse."""
    parser = argparse.ArgumentParser(
        description="Combined script to check all coding rules for flat architecture.",
        epilog="Examples:\n"
               "  %(prog)s\n"
               "  %(prog)s --file evolving_graphs/linter_graph/linter_main.py\n"
               "  %(prog)s --folders evolving_graphs/agent_graph evolving_graphs/linter_graph"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--file', '-f',
        type=str,
        help='Specify a single Python file to lint'
    )
    group.add_argument(
        '--folders', '-d',
        nargs='+',
        help='Specify one or more directories to scan for Python files'
    )
    return parser.parse_args()


def main():
    """Main function to run all rule checks."""
    args = parse_arguments()

    try:
        if args.file:
            validate_file(resolve_path(args.file))
            target_files = collect_target_files(file_path=args.file)
            print(f"Running rule checks on single file: {resolve_path(args.file)}\n")
        elif args.folders:
            validate_directories([resolve_path(f) for f in args.folders])
            target_files = collect_target_files(folders=args.folders)
            print(f"Running rule checks on specified folders: {', '.join(args.folders)}\n")
        else:
            target_files = collect_target_files()
            print("Running all rule checks on entire project...\n")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    violations_found = False

    # Check architectural recovery (Rule 0B) - must be done first
    print("0. Checking architectural recovery (Rule 0B)...")
    violations = check_architectural_recovery(target_files)
    if violations:
        violations_found = True
        print("Architectural recovery violations found:")
        for file, imp, reason in violations:
            print(f"File: {file}")
            print(f"Import: {imp}")
            print(f"Reason: {reason}")
            print()
    else:
        print("No architectural recovery violations found.")
    print()

    # Check import comments
    print("1. Checking import comments...")
    violations = check_import_comments(target_files)
    if violations:
        violations_found = True
        print("Found custom imports without explanatory comments:")
        for filepath, import_str in violations:
            print(f"- {filepath}: {import_str}")
    else:
        print("All custom imports have explanatory comments.")
    print()

    # Check imports compliance
    print("2. Checking imports compliance...")
    violations = check_imports_compliance(target_files)
    if violations:
        violations_found = True
        print("Import compliance violations found:")
        for file, imp, reason in violations:
            print(f"File: {file}")
            print(f"Import: {imp}")
            print(f"Reason: {reason}")
            print()
    else:
        print("No import compliance violations found.")
    print()

    # Check duplication
    print("3. Checking for code duplication...")
    duplications = check_duplication(target_files)
    if duplications:
        violations_found = True
        print("Potential duplications found:")
        for violation in duplications:
            print(f"\nFile: {violation['file']}")
            print(f"Line: {violation['line']}")
            print(f"Message: {violation['message']}")
    else:
        print("No duplications found.")
    print()

    # Check file sizes
    print("4. Checking file sizes...")
    violations = check_file_sizes(target_files)
    if violations:
        violations_found = True
        print("File size violations:")
        for filepath, count, status in violations:
            if isinstance(count, int):
                print(f"{filepath}: {count} lines {status}")
            else:
                print(f"{filepath}: {count} {status}")
    else:
        print("All files are within size limits.")
    print()

    # Analyze lines count - REMOVED: Not applicable in flat architecture

    # Analyze lines count - REMOVED: Not applicable in flat architecture

    print("\nAll checks completed.")

    # Final Compliance Check - verify changed files
    print("\n6. Performing Final Compliance Check on all files...")
    final_violations = check_final_compliance(target_files)
    if final_violations:
        violations_found = True
        print("Final compliance violations found:")
        for file, imp, reason in final_violations:
            print(f"File: {file}")
            print(f"Import: {imp}")
            print(f"Reason: {reason}")
            print()
    else:
        print("All files pass final compliance check.")

    # Exit with code based on violations
    sys.exit(1 if violations_found else 0)


if __name__ == "__main__":
    main()