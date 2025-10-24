#
# state_manager.py (A Leaf)
# This module handles the agent's long-term memory by saving and loading
# the working document to and from files.
#
# It uses the following modules:
# - agent.utils.config: To get the filenames for the memory files.
#

import os  # File system operations for checking file existence and managing file paths
import shutil  # File operations for renaming and backing up state files
import re  # Regular expressions for extracting goal and document content from saved files
import datetime  # Date and time utilities for timestamping saved state files
from .agent_config import config  # Configuration module for memory file paths and settings
from typing import Optional, Tuple  # Type hints for function signatures

def load_goal() -> Optional[str]:
    """
    Load only the goal from the dedicated goal file.
    Falls back to document state if goal file doesn't exist.

    Returns:
        Optional[str]: The goal string if found, None otherwise
    """
    goal_filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "agent_goal.txt")
    if os.path.exists(goal_filename):
        try:
            with open(goal_filename, "r", encoding="utf-8") as f:
                content = f.read()
            goal_match = re.search(r"Goal: (.*?)\n--- End Goal ---", content, re.DOTALL)
            if goal_match:
                return goal_match.group(1).strip()
        except Exception as e:
            print(f"\n[!] Error loading goal file: {e}")

    # Fallback to document state
    goal, _ = load_document_on_startup()
    return goal


def load_document_on_startup() -> Tuple[Optional[str], Optional[str]]:
    """
    Tries to load the last saved state from the memory file.
    Returns the goal and document content if successful, otherwise None.
    """
    filename = config.CURRENT_DOC_FILENAME
    if not os.path.exists(filename):
        return None, None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        goal_match = re.search(r"Goal: (.*?)\n\n--- Code Content ---", content, re.DOTALL)
        doc_match = re.search(r"--- Code Content ---\n(.*?)\n\n--- End of Code ---", content, re.DOTALL)
        if goal_match and doc_match:
            goal_from_file = goal_match.group(1).strip()
            document_from_file = doc_match.group(1).strip()
            return goal_from_file, document_from_file
        else:
            return None, None
    except Exception as e:
        print(f"\n[!] Error loading document state: {e}")
        return None, None

def save_goal_only(goal: str) -> None:
    """
    Saves only the goal to a dedicated goal file.
    Creates backup of previous goal if exists.

    Args:
        goal: The goal string to save
    """
    try:
        goal_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "agent_goal.txt"))
        backup_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "agent_goal_previous.txt"))

        if os.path.exists(goal_filename):
            shutil.move(goal_filename, backup_filename)

        with open(goal_filename, "w", encoding="utf-8") as f:
            f.write(f"--- Agent Goal ---\n")
            f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Goal: {goal}\n")
            f.write("--- End Goal ---\n")
    except Exception as e:
        print(f"\n[!] Error saving goal: {e}")


def save_document_state(document_content, current_goal):
    """Saves the current working code project and goal, and rotates the previous version."""
    try:
        if os.path.exists(config.CURRENT_DOC_FILENAME):
            shutil.move(config.CURRENT_DOC_FILENAME, config.PREVIOUS_DOC_FILENAME)
        with open(config.CURRENT_DOC_FILENAME, "w", encoding="utf-8") as f:
            f.write(f"--- Agent Code Generation State ---\n")
            f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Goal: {current_goal}\n\n")
            f.write(f"--- Code Content ---\n")
            f.write(document_content)
            f.write("\n\n--- End of Code ---\n")
    except Exception as e:
        print(f"\n[!] Error saving code state: {e}")