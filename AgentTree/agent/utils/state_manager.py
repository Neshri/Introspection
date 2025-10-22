#
# state_manager.py (A Leaf)
# This module handles the agent's long-term memory by saving and loading
# the working document to and from files.
#
# It uses the following modules:
# - agent.utils.config: To get the filenames for the memory files.
#

import os  # File system operations for checking file existence and paths
import shutil  # File copying and moving for state persistence
import re  # Regular expressions for parsing file content
import datetime  # Timestamp generation for state files
from agent.utils import config  # Configuration module for memory file paths

def load_document_on_startup():
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
        goal_match = re.search(r"Goal: (.*?)\n\n--- Document Content ---", content, re.DOTALL)
        doc_match = re.search(r"--- Document Content ---\n(.*)", content, re.DOTALL)
        if goal_match and doc_match:
            goal_from_file = goal_match.group(1).strip()
            document_from_file = doc_match.group(1).strip()
            return goal_from_file, document_from_file
        else:
            return None, None
    except Exception as e:
        print(f"\n[!] Error loading document state: {e}")
        return None, None

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