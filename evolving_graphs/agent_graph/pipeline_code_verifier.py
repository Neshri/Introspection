import ast  # For parsing Python code to check syntax errors
import os  # For checking if directories like 'tests' exist
import subprocess  # For running pytest command if tests directory is present
import tempfile  # For creating temporary files if needed for testing


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

    def verify_change(self, main_goal, proposed_code_change) -> dict:
        """
        Verifies a proposed code change by checking for Python syntax errors
        and running tests if available.

        Args:
            main_goal: The main goal for the agent
            proposed_code_change: Either a dict with 'new_content' or a string of code content

        Returns:
            dict: A dictionary with 'success' (bool) indicating if verification passed,
                and if False, 'error' (str) with details of the failure.
        """
        print("Verifier is testing the new code...")

        # Extract the new content from the proposed change
        if isinstance(proposed_code_change, dict):
            new_content = proposed_code_change.get('new_content', '')
        else:
            new_content = proposed_code_change

        # Step 1: Check for Python syntax errors using ast.parse
        try:
            ast.parse(new_content)
        except SyntaxError as e:
            return {
                'success': False,
                'error': f'Syntax error in code: {str(e)}'
            }

        # Step 2: Check if tests directory exists in working_dir and run pytest if it does
        tests_dir = os.path.join(self.working_dir, 'tests') if self.working_dir else 'tests'
        if os.path.isdir(tests_dir):
            try:
                # Run pytest in the candidate directory context
                cwd_path = self.working_dir if self.working_dir else '.'
                result = subprocess.run(['pytest'], capture_output=True, text=True, cwd=cwd_path)
                if result.returncode != 0:
                    # Pytest failed, include stdout and stderr in error
                    error_details = result.stdout + '\n' + result.stderr
                    return {
                        'success': False,
                        'error': f'Tests failed: {error_details}'
                    }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Error running tests: {str(e)}'
                }

        # If all checks pass
        return {'success': True}