"""
sandbox_utils.py - Unified sandboxing utilities for safe execution and directory isolation.
"""

import multiprocessing  # Process isolation for code execution
import os  # File system operations for directory sandboxing
import resource  # Resource limits for CPU and memory
import shutil  # Directory copying and management
import subprocess  # Subprocess execution for verification
import tempfile  # Temporary directory creation for safe execution
import time  # Performance timing for execution
from io import StringIO  # Output capture in child process
import sys  # System operations for output redirection


# Custom safe builtins - block dangerous modules and functions
SAFE_BUILTINS = {
    # Safe built-ins
    'print': print,
    'len': len,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
    'range': range,
    'enumerate': enumerate,
    'zip': zip,
    'sorted': sorted,
    'min': min,
    'max': max,
    'sum': sum,
    'abs': abs,
    'round': round,
    'type': type,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'repr': repr,
    'Exception': Exception,
    'ValueError': ValueError,
    'TypeError': TypeError,
    'IndexError': IndexError,
    'KeyError': KeyError,
    'AttributeError': AttributeError,
    'None': None,
    'True': True,
    'False': False,
    # Math operations
    '__import__': __import__,  # Will be restricted further
}


def _setup_safe_builtins():
    """Set up custom builtins that block dangerous modules."""
    def safe_import(name, *args, **kwargs):
        blocked_modules = {
            'os', 'sys', 'subprocess', 'importlib', 'builtins',
            'eval', 'exec', 'open', 'file', 'input'
        }
        if name in blocked_modules:
            raise ImportError(f"Import of '{name}' is blocked for security")
        return __import__(name, *args, **kwargs)

    SAFE_BUILTINS['__import__'] = safe_import
    return SAFE_BUILTINS


class SandboxManager:
    """
    Unified sandbox manager for safe code execution and directory isolation.

    Manages resource limits, module blocking, and directory sandboxing operations.
    """

    def __init__(self, root_dir: str = None):
        """
        Initialize sandbox manager with root directory for operations.

        Args:
            root_dir: Root directory for directory sandboxing (optional for execution-only).
        """
        self.root_dir = root_dir
        # Calculate evolving_graphs/ directory relative to this module's location
        module_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.dirname(module_dir)  # evolving_graphs/ directory
        self.version = 1
        self.candidate_version = None
        self.candidate_dir = None

    def create_directory_sandbox(self) -> None:
        """
        Create a deep copy of the evolving_graphs directory to a candidate directory with versioned subfolders.
        """
        def ignore_patterns(dir_name: str, contents: list) -> list:
            """Ignore function to exclude .git, .venv, and parent's candidates/."""
            ignore_list = ['.git', '.venv']
            if dir_name == 'evolving_graphs':
                ignore_list.append('candidates')
                ignore_list.append('temp_agent_baseline')
                ignore_list.append('temp_linter_baseline')
            return ignore_list

        # Set candidate version
        self.candidate_version = f"v{self.version}"
        self.version += 1

        # Candidate structure: evolving_graphs/candidates/candidate_vN/evolving_graphs/
        candidate_full_dir = os.path.join(self.base_dir, 'candidates', f'candidate_{self.candidate_version}', 'evolving_graphs')
        self.candidate_dir = candidate_full_dir

        # Remove existing candidate if it exists
        if os.path.exists(candidate_full_dir):
            shutil.rmtree(candidate_full_dir)

        # Ensure candidates directory exists
        candidates_dir = os.path.join(self.base_dir, 'candidates')
        os.makedirs(candidates_dir, exist_ok=True)

        # Copy evolving_graphs to candidate location (excludes parent's candidates/)
        evolving_graphs_src = self.base_dir

        # Use manual directory walking to avoid symlink depth issues
        def copy_tree_manual(src, dst, exclude_dirs=None):
            if exclude_dirs is None:
                exclude_dirs = set()
            os.makedirs(dst, exist_ok=True)
            for item in os.listdir(src):
                if item in exclude_dirs:
                    continue
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    copy_tree_manual(s, d, exclude_dirs)
                else:
                    shutil.copy2(s, d)

        # Copy with exclusions
        copy_tree_manual(evolving_graphs_src, candidate_full_dir, exclude_dirs={'candidates', 'temp_agent_baseline', 'temp_linter_baseline'})

    def promote_directory_sandbox(self) -> None:
        """Promote the candidate to baseline and update evolving_graphs."""
        # Candidate directories (relative paths)
        candidate_agent_dir = os.path.join(self.candidate_dir, 'agent_graph')
        candidate_linter_dir = os.path.join(self.candidate_dir, 'linter_graph')

        # Target directories (relative paths from current location)
        target_agent_dir = '.'
        target_linter_dir = os.path.join('..', 'linter_graph')

        # Backup current baseline
        temp_agent_dir = os.path.join(self.base_dir, 'temp_agent_baseline')
        temp_linter_dir = os.path.join(self.base_dir, 'temp_linter_baseline')
        if os.path.exists(temp_agent_dir):
            shutil.rmtree(temp_agent_dir)
        if os.path.exists(temp_linter_dir):
            shutil.rmtree(temp_linter_dir)
        if os.path.exists(target_agent_dir):
            shutil.move(target_agent_dir, temp_agent_dir)
        if os.path.exists(target_linter_dir):
            shutil.move(target_linter_dir, temp_linter_dir)

        # Move candidate to baseline
        shutil.move(candidate_agent_dir, target_agent_dir)
        shutil.move(candidate_linter_dir, target_linter_dir)

        # Clean up candidate and temp (relative paths)
        candidate_parent = os.path.join(self.base_dir, 'candidates', f'candidate_{self.candidate_version}')
        shutil.rmtree(candidate_parent)
        if os.path.exists(temp_agent_dir):
            shutil.rmtree(temp_agent_dir)
        if os.path.exists(temp_linter_dir):
            shutil.rmtree(temp_linter_dir)

    def rollback_directory_sandbox(self) -> None:
        """Delete the candidate directory to discard changes."""
        candidate_parent = os.path.join(self.base_dir, 'candidates', f'candidate_{self.candidate_version}')
        if os.path.exists(candidate_parent):
            shutil.rmtree(candidate_parent)

    def verify_with_linter_subprocess(self, proposed_code_change) -> dict:
        """
        Execute the linter graph as a subprocess to verify the code change.

        Args:
            proposed_code_change: The proposed code change to verify.

        Returns:
            dict: Verification result with 'success' and optional 'error'.
        """
        try:
            # Path to linter entry point relative to candidate
            linter_entry = os.path.join(self.candidate_dir, 'linter_graph', 'linter_graph_main.py')
            # Run linter on the candidate agent_graph
            candidate_agent_path = os.path.join(self.candidate_dir, 'agent_graph')
            result = subprocess.run(
                ['python3', linter_entry, '--folders', candidate_agent_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(linter_entry)  # Run from linter directory
            )
            # Linter exits with 0 on success, 1 on violations
            if result.returncode == 0:
                return {'success': True}
            else:
                error_msg = result.stdout + result.stderr
                return {'success': False, 'error': f'Linter violations: {error_msg}'}
        except Exception as e:
            return {'success': False, 'error': f'Error running linter: {str(e)}'}

    def execute_safe_code(self, code: str) -> dict:
        """
        Executes Python code safely using multiprocessing.Process with resource limits.

        Args:
            code: Python code string to execute.

        Returns:
            dict: Result with success, output, error, execution_time.
        """
        result = {
            'success': False,
            'output': '',
            'error': '',
            'execution_time': 0.0
        }

        # Create temporary directory for execution
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                start_time = time.time()

                # Create output queue for inter-process communication
                output_queue = multiprocessing.Queue()

                # Create and start the process
                process = multiprocessing.Process(
                    target=self._execute_in_process,
                    args=(code, output_queue, temp_dir)
                )
                process.start()

                # Wait for completion with timeout
                process.join(timeout=30)

                # Check if process is still alive (timeout)
                if process.is_alive():
                    process.terminate()
                    process.join(timeout=5)
                    if process.is_alive():
                        process.kill()
                    result['error'] = "Execution timed out after 30 seconds"
                    result['success'] = False
                else:
                    # Get results from queue
                    if not output_queue.empty():
                        exec_result = output_queue.get_nowait()
                        result.update(exec_result)
                    else:
                        result['error'] = "No output received from execution"
                        result['success'] = False

                end_time = time.time()
                result['execution_time'] = end_time - start_time

            except Exception as e:
                result['error'] = f"Execution failed: {str(e)}"
                result['success'] = False

        return result

    def _execute_in_process(self, code: str, output_queue, temp_dir: str):
        """Function to run in the child process with safe environment."""
        try:
            # Set resource limits
            resource.setrlimit(resource.RLIMIT_CPU, (30, 30))  # CPU time limit 30s
            resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))  # Memory limit 100MB

            # Change to temp directory
            os.chdir(temp_dir)

            # Capture stdout and stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            stdout_capture = StringIO()
            stderr_capture = StringIO()
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture

            # Set safe builtins
            safe_builtins = _setup_safe_builtins()
            exec_globals = {'__builtins__': safe_builtins}

            # Execute the code
            exec(code, exec_globals)

            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # Put results in queue
            try:
                output_queue.put({
                    'success': True,
                    'output': stdout_capture.getvalue(),
                    'error': stderr_capture.getvalue()
                }, timeout=1)
            except:
                pass  # If queue is full or broken, just continue

        except Exception as e:
            try:
                output_queue.put({
                    'success': False,
                    'output': '',
                    'error': str(e)
                }, timeout=1)
            except:
                pass  # If queue is full or broken, just continue


# Backward compatibility wrappers
def execute_code(code: str) -> dict:
    """Backward compatibility wrapper for safe code execution."""
    manager = SandboxManager()
    return manager.execute_safe_code(code)


def create_candidate() -> None:
    """Backward compatibility wrapper for directory sandbox creation."""
    manager = SandboxManager()
    manager.create_directory_sandbox()


def promote_candidate() -> None:
    """Backward compatibility wrapper for directory sandbox promotion."""
    manager = SandboxManager()
    manager.promote_directory_sandbox()


def rollback_candidate() -> None:
    """Backward compatibility wrapper for directory sandbox rollback."""
    manager = SandboxManager()
    manager.rollback_directory_sandbox()