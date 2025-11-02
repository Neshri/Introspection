# editor_core.py (Editor Role)
# This module defines the Editor class responsible for safe file modifications and code changes.

import os
from typing import Optional


class Editor:
    """
    The Editor class encapsulates the step of handling file modifications and code changes.
    It provides safe editing operations with validation and isolation.
    """

    def __init__(self, root_dir: str):
        """
        Initialize the Editor with the root directory for file operations.

        Args:
            root_dir: The root directory where file editing occurs.
        """
        self.root_dir = root_dir

    def read_file(self, file_path: str) -> Optional[str]:
        """
        Safely read the contents of a file relative to root_dir.

        Args:
            file_path: Relative path to the file from root_dir.

        Returns:
            The file contents as a string, or None if file not found or error.
        """
        full_path = os.path.join(self.root_dir, file_path)
        if not os.path.exists(full_path):
            return None
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None

    def write_file(self, file_path: str, content: str) -> bool:
        """
        Safely write content to a file relative to root_dir.

        Args:
            file_path: Relative path to the file from root_dir.
            content: The content to write.

        Returns:
            True if successful, False otherwise.
        """
        full_path = os.path.join(self.root_dir, file_path)
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False

    def apply_diff(self, file_path: str, old_content: str, new_content: str) -> bool:
        """
        Apply a diff by replacing old_content with new_content in the file.

        Args:
            file_path: Relative path to the file from root_dir.
            old_content: The content to replace.
            new_content: The replacement content.

        Returns:
            True if successful, False otherwise.
        """
        current_content = self.read_file(file_path)
        if current_content is None or old_content not in current_content:
            return False
        updated_content = current_content.replace(old_content, new_content, 1)
        return self.write_file(file_path, updated_content)

    def edit_file(self, file_path: str, changes: list[dict]) -> bool:
        """
        Apply multiple changes to a file. Each change is a dict with 'old' and 'new'.

        Args:
            file_path: Relative path to the file.
            changes: List of changes, each {'old': str, 'new': str}.

        Returns:
            True if all changes applied successfully.
        """
        content = self.read_file(file_path)
        if content is None:
            return False
        for change in changes:
            old = change.get('old', '')
            new = change.get('new', '')
            if old in content:
                content = content.replace(old, new, 1)
            else:
                return False
        return self.write_file(file_path, content)