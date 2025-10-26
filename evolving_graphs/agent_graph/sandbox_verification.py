"""
sandbox_verification.py - Linter verification utilities for sandbox operations.
"""

import os
import subprocess


def verify_with_linter_subprocess(candidate_dir: str, linter_entry: str) -> dict:
    """
    Execute the linter graph as a subprocess to verify the code change.

    Args:
        candidate_dir: Path to the candidate directory.
        linter_entry: Path to the linter entry point.

    Returns:
        dict: Verification result with 'success' and optional 'error'.
    """
    try:
        # Run linter on the candidate agent_graph
        candidate_agent_path = os.path.join(candidate_dir, 'agent_graph')
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