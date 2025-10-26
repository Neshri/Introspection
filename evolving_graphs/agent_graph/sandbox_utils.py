"""
sandbox_utils.py - Unified sandboxing utilities integrating safe execution, directory isolation, and verification.
"""

import os

from .sandbox_builtins import _setup_safe_builtins
from .sandbox_directory_sandbox import DirectorySandbox, create_candidate, promote_candidate, rollback_candidate
from .sandbox_execution import execute_safe_code
from .sandbox_verification import verify_with_linter_subprocess


class SandboxManager:
    """
    Unified sandbox manager integrating safe code execution, directory isolation, and verification.

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
        self.directory_sandbox = DirectorySandbox(self.base_dir)

    def create_directory_sandbox(self) -> None:
        """Create a deep copy of the evolving_graphs directory to a candidate directory."""
        self.directory_sandbox.create_directory_sandbox()

    def promote_directory_sandbox(self) -> None:
        """Promote the candidate to baseline and update evolving_graphs."""
        self.directory_sandbox.promote_directory_sandbox()

    def rollback_directory_sandbox(self) -> None:
        """Delete the candidate directory to discard changes."""
        self.directory_sandbox.rollback_directory_sandbox()

    def verify_with_linter_subprocess(self, proposed_code_change) -> dict:
        """
        Execute the linter graph as a subprocess to verify the code change.

        Args:
            proposed_code_change: The proposed code change to verify.

        Returns:
            dict: Verification result with 'success' and optional 'error'.
        """
        # Path to linter entry point relative to candidate
        linter_entry = os.path.join(self.directory_sandbox.candidate_dir, 'linter_graph', 'linter_graph_main.py')
        return verify_with_linter_subprocess(self.directory_sandbox.candidate_dir, linter_entry)

    def execute_safe_code(self, code: str) -> dict:
        """
        Executes Python code safely using multiprocessing.Process with resource limits.

        Args:
            code: Python code string to execute.

        Returns:
            dict: Result with success, output, error, execution_time.
        """
        return execute_safe_code(code)


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