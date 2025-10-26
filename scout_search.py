#!/usr/bin/env python
# A standalone debugging script to run the Scout on a specific goal.

import sys
import os
import argparse
import shutil
import logging

# --- Setup Project Path ---
# This is crucial for an external script to be able to import project modules.
# It adds the project's root directory to Python's import search path.
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# --- Project Imports ---
# These can now be imported because the path is set correctly.
from evolving_graphs.agent_graph.intelligence_project_scout import Scout
from evolving_graphs.agent_graph.memory_interface import MemoryInterface

# Configure basic logging for the script's output
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

def main():
    """
    Sets up the environment, runs the Scout with a command-line goal,
    and prints the results.
    """
    parser = argparse.ArgumentParser(description="Use the Scout to find relevant project modules for a specific goal.")
    parser.add_argument("goal", type=str, help="The search goal for the Scout to investigate.")
    args = parser.parse_args()

    # --- Configuration ---
    # Define the paths and settings needed to run the Scout.
    db_path = "debug_memory_db"  # Use a temporary, separate DB to not pollute the main one.
    agent_graph_path = os.path.join(project_root, "evolving_graphs", "agent_graph")

    # Ensure the environment is clean before starting.
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    try:
        print("--- Setting up Scout dependencies ---")
        # 1. Instantiate the MemoryInterface.
        memory = MemoryInterface(db_path=db_path)
        print(f"Temporary memory created at '{db_path}'")

        # 2. Instantiate the Scout, providing its required dependencies.
        scout = Scout(memory=memory, working_directory=agent_graph_path)
        print(f"Scout initialized for directory: '{agent_graph_path}'")

        print(f"\n--- Running Scout for goal: '{args.goal}' ---")
        # 3. Run the scout_project method. We use turn=1 as this is a one-shot run.
        backpack, _ = scout.scout_project(main_goal=args.goal, current_turn=1)

        # 4. Print the results in a readable format.
        print(f"\n--- Scout's Backpack ({len(backpack)} items found) ---")
        if not backpack:
            print("The Scout did not find any relevant modules for this goal.")
        else:
            for i, item in enumerate(backpack, 1):
                # Make the file path relative for cleaner output
                relative_path = os.path.relpath(item['file_path'], project_root)
                print(f"{i}. File: {relative_path}")
                print(f"   Justification: {item['justification']}")
                print("-" * 20)

    finally:
        # --- Cleanup ---
        # Ensure the temporary database is always removed.
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            print(f"\n--- Cleanup complete ---")
            print(f"Temporary memory at '{db_path}' has been removed.")

if __name__ == "__main__":
    main()