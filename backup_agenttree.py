#!/usr/bin/env python3
"""
agent_tree Backup Script

This script creates a timestamped backup of the agent_tree folder and important data files.
It copies the entire agent_tree directory to a new backup folder in the project root.
Includes any existing agent_memory_current.txt file.

Usage: python backup_agent_tree.py
"""

import os
import shutil
import datetime

def main():
    # Get the project root directory (where this script is located)
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Generate timestamp for backup folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder_name = f"agent_tree_Backup_{timestamp}"
    backup_path = os.path.join(project_root, backup_folder_name)

    print("Starting agent_tree backup...")

    try:
        # Create backup directory
        os.makedirs(backup_path, exist_ok=False)
        print(f"Created backup directory: {backup_folder_name}")

        # Source paths
        agent_tree_src = os.path.join(project_root, "agent_tree")
        memory_file_src = os.path.join(project_root, "agent_memory_current.txt")

        # Copy agent_tree folder
        if os.path.exists(agent_tree_src):
            agent_tree_dst = os.path.join(backup_path, "agent_tree")
            shutil.copytree(agent_tree_src, agent_tree_dst)
            print("Copied agent_tree folder successfully.")
        else:
            raise FileNotFoundError("agent_tree folder not found in project root.")

        # Copy agent_memory_current.txt if it exists
        if os.path.exists(memory_file_src):
            memory_file_dst = os.path.join(backup_path, "agent_memory_current.txt")
            shutil.copy2(memory_file_src, memory_file_dst)
            print("Copied agent_memory_current.txt successfully.")
        else:
            print("agent_memory_current.txt not found - skipping this file.")

        print(f"Backup completed successfully in: {backup_path}")

    except Exception as e:
        print(f"Error during backup: {str(e)}")
        # Clean up partial backup if it exists
        if os.path.exists(backup_path):
            shutil.rmtree(backup_path)
            print("Cleaned up partial backup due to error.")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())