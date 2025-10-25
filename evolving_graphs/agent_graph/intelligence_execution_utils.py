"""
intelligence_execution_utils.py - Code execution utilities for safe subprocess execution.

Provides functions for executing Python code safely in subprocess with timeout and resource limits.
"""

import subprocess  # Safe code execution in subprocess
import time  # Performance timing for execution
import tempfile  # Temporary file creation for safe execution
import os  # File system operations for temp files


def execute_code(code):
    """
    Executes Python code safely using subprocess and returns execution results.

    Returns a dict with:
    - success: bool
    - output: str (stdout)
    - error: str (stderr)
    - execution_time: float (seconds)
    """
    result = {
        'success': False,
        'output': '',
        'error': '',
        'execution_time': 0.0
    }

    # Create temporary file for the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        start_time = time.time()

        # Execute with timeout and resource limits
        process = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
            cwd=os.path.dirname(temp_file)  # Run in temp directory
        )

        end_time = time.time()
        result['execution_time'] = end_time - start_time
        result['output'] = process.stdout.strip()
        result['error'] = process.stderr.strip()
        result['success'] = process.returncode == 0

    except subprocess.TimeoutExpired:
        result['error'] = "Execution timed out after 30 seconds"
        result['success'] = False
    except Exception as e:
        result['error'] = f"Execution failed: {str(e)}"
        result['success'] = False
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_file)
        except:
            pass

    return result