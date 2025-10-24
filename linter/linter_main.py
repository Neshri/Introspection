#!/usr/bin/env python3
"""
Combined script to check all coding rules for flat architecture.
Runs all validation checks with a single command.
Updated for simplified ruleset without hierarchical structure checks.
Supports optional single-file mode when a _main.py file is specified.
"""

import os  # filesystem operations
import sys  # system-specific parameters and functions

from .linter_rules_recovery import check_architectural_recovery  # To diagnose and resolve architectural contradictions.
from .linter_rules_importcomments import check_import_comments  # To validate explanatory comments on imports.
from .linter_rules_importcompliance import check_imports_compliance  # To ensure imports comply with flat architecture rules.
from .linter_rules_duplication import check_duplication  # To detect potential code duplication.
from .linter_rules_filesize import check_file_sizes  # To enforce file size limits.
from .linter_rules_compliance import check_final_compliance  # To perform final compliance check on modified files.


def validate_file_argument(file_path):
    """Validate that the provided file path is a valid _main.py file."""
    if not file_path.endswith('_main.py'):
        print(f"Error: File must end with '_main.py'. Provided: {file_path}")
        sys.exit(1)

    if not os.path.isfile(file_path):
        print(f"Error: File does not exist: {file_path}")
        sys.exit(1)

    return file_path


def get_target_files(file_path=None):
    """Get the list of files to check. If file_path is provided, return just that file; otherwise, return all Python files in agent_tree."""
    if file_path:
        return [os.path.abspath(file_path)]

    # Default behavior: scan all .py files in agent_tree
    target_files = []
    for root, dirs, files in os.walk('agent_tree'):
        for file in files:
            if file.endswith('.py'):
                target_files.append(os.path.abspath(os.path.join(root, file)))
    return target_files


def main():
    """Main function to run all rule checks."""
    # Parse command-line arguments
    target_file = None
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            print("Usage: python -m linter.linter_main [optional_file_path]")
            print("If file_path is provided, it must be a _main.py file.")
            sys.exit(1)
        target_file = validate_file_argument(sys.argv[1])

    target_files = get_target_files(target_file)

    if target_file:
        print(f"Running rule checks on single file: {target_file}\n")
    else:
        print("Running all rule checks on entire project...\n")

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