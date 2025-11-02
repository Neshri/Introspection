import ast  # For parsing Python code to check syntax errors
import os  # For checking if directories like 'tests' exist
import re  # For regex-based pre-validation checks
import subprocess  # For running pytest command if tests directory is present
import tempfile  # For creating temporary files if needed for testing
from collections import defaultdict  # For DRY violation detection


class Verifier:
    """
    Verifier class for validating proposed code changes.

    This class provides methods to verify code changes by checking for syntax errors
    and optionally running available tests using pytest.
    """

    def __init__(self):
        """
        Initialize the Verifier with no working directory set.
        """
        self.working_dir = None

    def set_working_directory(self, working_dir: str):
        """
        Set the working directory for the Verifier to the candidate path.

        Args:
            working_dir: The path to the candidate directory.
        """
        self.working_dir = working_dir

    def pre_validate_syntax(self, code: str) -> dict:
        """
        Performs basic syntax pre-validation checks before full AST parsing.
        Checks for common LLM errors like incorrect indentation, missing colons,
        and invalid import statements.

        Args:
            code: The Python code string to validate.

        Returns:
            dict: A dictionary with 'success' (bool) indicating if pre-validation passed,
                and if False, 'error' (str) with details of the failure.
        """
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Check for incorrect indentation (mixing tabs and spaces)
            if '\t' in line and ' ' in line[:len(line) - len(line.lstrip())]:
                return {
                    'success': False,
                    'error': f'Mixed tabs and spaces in indentation on line {i}: {line}'
                }

            # Check for missing colons in control structures
            if re.match(r'^\s*(if|elif|else|for|while|def|class|with|try|except|finally)\b', stripped):
                if not stripped.endswith(':'):
                    return {
                        'success': False,
                        'error': f'Missing colon after control structure on line {i}: {stripped}'
                    }

            # Check for invalid import statements
            if stripped.startswith('import ') or stripped.startswith('from '):
                # Basic check: ensure import statement has proper structure
                if 'import' not in stripped or (stripped.startswith('from ') and ' import ' not in stripped):
                    return {
                        'success': False,
                        'error': f'Invalid import statement on line {i}: {stripped}'
                    }
                # Check for common typos or invalid syntax
                if re.search(r'import\s+[^a-zA-Z_]', stripped) or re.search(r'from\s+[^a-zA-Z_.]', stripped):
                    return {
                        'success': False,
                        'error': f'Invalid characters in import statement on line {i}: {stripped}'
                    }

        return {'success': True}

    def check_architecture_rules(self, code: str) -> dict:
        """
        Checks the generated code against architectural rules defined in rules.md using regex and AST.

        Args:
            code: The Python code string to validate.

        Returns:
            dict: A dictionary with 'success' (bool) indicating if checks passed,
                and if False, 'error' (str) with details of the violations.
        """
        violations = []

        # Parse the code into AST for structural analysis
        try:
            tree = ast.parse(code)
        except SyntaxError:
            # Syntax errors are handled separately, so skip here
            return {'success': True}

        # 1. Check for relative import rules
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                # Check for forbidden absolute imports of project modules
                if node.level == 0 and node.module and (node.module.startswith('evolving_graphs.') or node.module.startswith('agent_graph.')):
                    violations.append(f"Forbidden absolute import: from {node.module} import ...")
                # Check for deep imports (.. or more)
                if node.level > 1:
                    dots = '.' * node.level
                    module_part = f"{dots}{node.module}" if node.module else dots
                    names = ', '.join(alias.name for alias in node.names)
                    violations.append(f"Forbidden deep import: from {module_part} import {names}")
                # Check for mandatory import comments on intra-project imports
                if node.module and (node.module.startswith('.') or node.module.startswith('evolving_graphs.') or node.module.startswith('agent_graph.')):
                    lines = code.splitlines()
                    if node.lineno - 1 < len(lines):
                        line = lines[node.lineno - 1]
                        if '#' not in line:
                            names = ', '.join(alias.name for alias in node.names)
                            import_stmt = f"from {'.' * node.level}{node.module} import {names}"
                            violations.append(f"Missing explanatory comment: {import_stmt}")

        # 2. Check component structure (no modules in root)
        # This is harder to check from code alone, but we can check for imports from root
        # Assuming the code is for a specific component
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                # If importing from evolving_graphs root without subdirectory, flag it
                if 'from evolving_graphs.' in stripped and stripped.count('.') == 1 and not stripped.split('.')[1].startswith('agent_graph') and not stripped.split('.')[1].startswith('linter_graph'):
                    violations.append(f"Import from root forbidden: {stripped} on line {i}")

        # 3. Semantic naming: Check file-level (but since we have the code, check class/function names using domain_responsibility pattern)
        # This is approximate since we don't have the filename here
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    violations.append(f"Non-semantic class name: {node.name}")
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z][a-zA-Z0-9_]*$', node.name) and not node.name.startswith('_'):
                    violations.append(f"Non-semantic function name: {node.name}")

        # 4. File size limits: Count non-empty, non-comment lines
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        if len(code_lines) > 300:
            violations.append(f"File too large: {len(code_lines)} lines (limit: 300)")

        # 5. DRY principles: Check for duplicated code blocks (simplified, looking for exact duplicates of 5+ lines)
        block_counts = defaultdict(int)
        current_block = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('import ') and not stripped.startswith('from '):
                current_block.append(stripped)
                if len(current_block) >= 5:
                    block_signature = tuple(current_block[-5:])
                    block_counts[block_signature] += 1
            else:
                current_block = []
        for sig, count in block_counts.items():
            if count > 1:
                violations.append("Potential code duplication detected (5+ line block repeated)")

        if violations:
            return {
                'success': False,
                'error': '; '.join(violations)
            }
        return {'success': True}

    def verify_change(self, main_goal, proposed_code_change) -> dict:
        """
        Verifies a proposed code change by checking for Python syntax errors,
        architectural rule compliance, and running tests if available.

        Args:
            main_goal: The main goal for the agent
            proposed_code_change: Either a dict with 'new_content' or a string of code content

        Returns:
            dict: A dictionary with 'success' (bool) indicating if verification passed,
                and if False, 'error' (str) with details of the failure.
        """
        print("Verifier is testing the new code...")
        print(f"DEBUG: Code length: {len(str(proposed_code_change))} characters")
        print(f"DEBUG: First 200 chars: {str(proposed_code_change)[:200]}")

        # Extract the new content from the proposed change
        if isinstance(proposed_code_change, dict):
            new_content = proposed_code_change.get('new_content', '')
        else:
            new_content = proposed_code_change

        print(f"DEBUG: Extracted content length: {len(new_content)} characters")
        print(f"DEBUG: Content preview: {new_content[:300]}")

        # Step 1: Pre-validate basic syntax issues
        print("DEBUG: Running pre-validation...")
        pre_validation_result = self.pre_validate_syntax(new_content)
        if not pre_validation_result['success']:
            print(f"DEBUG: Pre-validation failed: {pre_validation_result['error']}")
            return pre_validation_result

        # Step 2: Check for Python syntax errors using ast.parse
        print("DEBUG: Running AST syntax check...")
        try:
            ast.parse(new_content)
            print("DEBUG: AST syntax check passed")
        except SyntaxError as e:
            print(f"DEBUG: AST syntax error: {str(e)}")
            return {
                'success': False,
                'error': f'Syntax error in code: {str(e)}'
            }

        # Step 3: Check architectural rule compliance
        print("DEBUG: Checking architecture rules...")
        architecture_result = self.check_architecture_rules(new_content)
        if not architecture_result['success']:
            print(f"DEBUG: Architecture check failed: {architecture_result['error']}")
            return architecture_result

        # Step 4: Check if tests directory exists in working_dir and run pytest if it does
        tests_dir = os.path.join(self.working_dir, 'tests') if self.working_dir else 'tests'
        print(f"DEBUG: Tests directory: {tests_dir}, exists: {os.path.isdir(tests_dir)}")
        if os.path.isdir(tests_dir):
            try:
                # Run pytest in the candidate directory context
                cwd_path = self.working_dir if self.working_dir else '.'
                print(f"DEBUG: Running pytest in directory: {cwd_path}")
                result = subprocess.run(['pytest'], capture_output=True, text=True, cwd=cwd_path)
                print(f"DEBUG: Pytest return code: {result.returncode}")
                if result.returncode != 0:
                    # Pytest failed, include stdout and stderr in error
                    error_details = result.stdout + '\n' + result.stderr
                    print(f"DEBUG: Pytest failed with output length: {len(error_details)}")
                    print(f"DEBUG: First 500 chars of error: {error_details[:500]}")
                    return {
                        'success': False,
                        'error': f'Tests failed: {error_details}'
                    }
                else:
                    print("DEBUG: All tests passed")
            except Exception as e:
                print(f"DEBUG: Exception running tests: {str(e)}")
                return {
                    'success': False,
                    'error': f'Error running tests: {str(e)}'
                }
        else:
            print("DEBUG: No tests directory found, skipping test execution")

        # If all checks pass
        return {'success': True}