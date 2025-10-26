"""
sandbox_execution.py - Safe code execution utilities using multiprocessing.
"""

import multiprocessing
import os
import resource
import tempfile
import time
from io import StringIO
import sys

from .sandbox_builtins import _setup_safe_builtins


def execute_safe_code(code: str) -> dict:
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
                target=_execute_in_process,
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


def _execute_in_process(code: str, output_queue, temp_dir: str):
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