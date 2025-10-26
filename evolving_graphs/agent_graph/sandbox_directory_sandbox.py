"""
sandbox_directory_sandbox.py - Directory sandboxing utilities for safe file operations.
"""

import os
import shutil


class DirectorySandbox:
    """
    Handles directory sandboxing operations: creation, promotion, and rollback.
    """

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
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


def create_candidate(base_dir: str) -> DirectorySandbox:
    """Create a new directory sandbox."""
    sandbox = DirectorySandbox(base_dir)
    sandbox.create_directory_sandbox()
    return sandbox


def promote_candidate(sandbox: DirectorySandbox) -> None:
    """Promote the directory sandbox."""
    sandbox.promote_directory_sandbox()


def rollback_candidate(sandbox: DirectorySandbox) -> None:
    """Rollback the directory sandbox."""
    sandbox.rollback_directory_sandbox()