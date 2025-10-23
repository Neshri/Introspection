#!/usr/bin/env python3
"""
Combined script to check all coding rules from the rules.md document.
Runs all validation checks with a single command.
"""

import sys  # system-specific parameters and functions

from .rules import (  # all rule checking functions
    check_import_comments,  # checks for explanatory comments on imports
    check_imports_compliance,  # validates import compliance with rules
    check_duplication,  # detects code duplication
    check_file_sizes,  # enforces file size limits
    analyze_lines_count,  # analyzes line counts in files
    check_shared_module_placement,  # checks placement of shared modules
    analyze_directory_structure,  # analyzes directory structure cohesion
)


def main():
    """Main function to run all rule checks."""
    print("Running all rule checks...\n")

    violations_found = False

    # Check import comments
    print("1. Checking import comments...")
    violations = check_import_comments()
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
    violations = check_imports_compliance()
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
    duplications = check_duplication()
    if duplications:
        violations_found = True
        print("Potential duplications found:")
        for line, files in duplications.items():
            print(f"\nLine: {line}")
            print("Files:")
            for file in sorted(set(files)):  # Use set to remove duplicates in case a file has the line multiple times
                print(f"  - {file}")
    else:
        print("No duplications found.")
    print()

    # Check file sizes
    print("4. Checking file sizes...")
    violations = check_file_sizes()
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

    # Analyze lines count
    print("5. Analyzing total line counts...")
    results = analyze_lines_count()
    print("Files sorted by total line count (descending):")
    for path, lines in results:
        print(f"{path}: {lines}")
    print()

    # Check shared module placement
    print("6. Checking shared module placement...")
    violations = check_shared_module_placement()
    if violations:
        violations_found = True
        print("Shared module placement violations:")
        for parent_dir, mod, files_using in violations:
            print(f"Module '{mod}' is shared by sibling files in {parent_dir} but not placed in parent directory.")
            print(f"Files using it: {files_using}")
            print()
    else:
        print("No shared module placement violations found.")
    print()

    # Analyze directory structure
    print("7. Analyzing directory structure...")
    directories = analyze_directory_structure()
    violations = {dir_path: data for dir_path, data in directories.items() if data["violation"]}
    if violations:
        violations_found = True
        print("Directory cohesion violations (>7 .py files):")
        for dir_path, data in violations.items():
            print(f"{dir_path}: {data['file_count']} files")
            print(f"Files: {data['files']}")
            print()
    else:
        print("All directories are within cohesion limits.")

    print("\nAll checks completed.")

    # Exit with code based on violations
    sys.exit(1 if violations_found else 0)


if __name__ == "__main__":
    main()