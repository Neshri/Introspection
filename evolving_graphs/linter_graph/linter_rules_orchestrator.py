"""Rule for checking orchestrator pattern and linear data flow."""

import os  # filesystem operations
import ast  # abstract syntax tree for parsing Python code


def check_orchestrator_pattern(target_files=None):
    """Check for orchestrator pattern and linear data flow in graph files."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Default behavior: scan all .py files in evolving_graphs
        files_to_check = []
        for root, dirs, files in os.walk('evolving_graphs'):
            for file in files:
                if file.endswith('.py'):
                    files_to_check.append(os.path.join(root, file))
    else:
        # Single-file mode: only check specified files
        files_to_check = target_files

    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, filepath)
        except (SyntaxError, UnicodeDecodeError):
            continue

        # Check for orchestrator pattern - look for classes that might be orchestrators
        orchestrator_classes = []
        role_classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name.lower()
                if 'orchestrator' in class_name or 'runner' in class_name or 'pipeline' in class_name:
                    orchestrator_classes.append(node)
                elif any(role in class_name for role in ['scout', 'planner', 'executor', 'evaluator', 'critic']):
                    role_classes.append(node)

        # If we have orchestrator classes, check for linear data flow
        if orchestrator_classes:
            # Check that orchestrator holds state and manages roles
            has_state = False
            has_roles = False

            for orch_class in orchestrator_classes:
                for node in ast.walk(orch_class):
                    if isinstance(node, ast.Assign):
                        # Look for state attributes like main_goal, database, etc.
                        for target in node.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                                attr_name = target.attr
                                if attr_name in ['main_goal', 'database', 'backpack', 'state']:
                                    has_state = True
                                elif attr_name in ['scout', 'planner', 'executor', 'evaluator', 'critic']:
                                    has_roles = True
                            elif isinstance(target, ast.Name):
                                # Look for role attributes
                                if target.id in ['scout', 'planner', 'executor', 'evaluator', 'critic']:
                                    has_roles = True

                    # Check for role-to-role communication (violation of linear data flow)
                    # But allow orchestrator to call methods on role instances
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Attribute):
                            # Check for role.role_method() calls where role is not the orchestrator
                            if isinstance(node.func.value, ast.Attribute) and isinstance(node.func.value.value, ast.Name):
                                caller = node.func.value.value.id
                                caller_attr = node.func.value.attr
                                # If caller_attr is a role and caller is another role (not orchestrator), it's forbidden
                                if caller_attr in ['scout', 'planner', 'executor', 'evaluator', 'critic']:
                                    if caller != 'self':
                                        violations.append((
                                            filepath,
                                            f"{caller}.{caller_attr}.{node.func.attr}()",
                                            "Linear Data Flow: Roles must not directly access other sibling roles' state."
                                        ))
                                    # Allow orchestrator (self) to call methods on role instances

            if not has_state:
                violations.append((
                    filepath,
                    "Orchestrator class",
                    "Orchestrator Pattern: Orchestrator must hold primary state (main_goal, database connections)."
                ))

            if not has_roles:
                violations.append((
                    filepath,
                    "Orchestrator class",
                    "Orchestrator Pattern: Orchestrator must initialize and manage role instances."
                ))

        # Check for cross-role direct communication patterns
        # But allow orchestrator to access role attributes
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                # Look for patterns like role1.role2.attribute (cross-role access)
                if isinstance(node.value, ast.Attribute) and isinstance(node.value.value, ast.Name):
                    caller = node.value.value.id
                    first_attr = node.value.attr
                    second_attr = node.attr
                    # If first_attr is a role and caller is also a role (not orchestrator), it's forbidden
                    if first_attr in ['scout', 'planner', 'executor', 'evaluator', 'critic']:
                        if caller in ['scout', 'planner', 'executor', 'evaluator', 'critic']:
                            violations.append((
                                filepath,
                                f"{caller}.{first_attr}.{second_attr}",
                                "Linear Data Flow: Direct cross-role communication forbidden."
                            ))
                        # Allow orchestrator (self) to access role attributes

    return violations