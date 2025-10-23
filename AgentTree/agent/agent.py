# agent.py (Modified for the Linear Pipeline with Agent Class Integration)
# Imports: Standard time library, config and state_manager utilities, node for tree structures,
# scout/planner/executor/verifier for pipeline components, Agent class for goal management.

import time  # Standard library for time-related functions, used for sleep in the main loop
from .utils import config, state_manager  # Utilities for agent settings and state management
from .engine.node import Node  # Node class for the tree structure in search algorithms
# from .engine import mcts # We are temporarily replacing MCTS with the pipeline
from .shared.core import Scout, Planner  # Intelligence components for scouting and planning
from .pipeline.executor import Executor  # Executor class for generating and applying code changes
from .pipeline.verifier import Verifier  # Verifier class for testing and validating code changes
from . import Agent  # Agent class for goal-setting and management

# Backward compatibility: keep run() function using direct state_manager calls
def run():
    """The main, continuous loop that drives the agent's behavior."""
    print("--- Initializing Agent ---")

    loaded_goal, current_code_state = state_manager.load_document_on_startup()
    
    # Initialize our specialist agents
    scout = Scout()
    planner = Planner()
    executor = Executor(loaded_goal, current_code_state)
    verifier = Verifier()

    turn_number = 1
    try:
        while True:
            print(f"\n--- Turn {turn_number} ---")

            # This is the new, linear pipeline. It replaces the single MCTS call.

            # 1. SCOUT PHASE: Gather context
            print("Scout is analyzing the project...")
            backpack = scout.scout_project(loaded_goal)
            print(f"Scout returned a backpack with {len(backpack)} relevant files.")

            # 2. PLANNER PHASE: Create a strategy
            print("Planner is creating a plan...")
            plan = planner.create_plan(loaded_goal, backpack)
            print(f"Planner created the following plan:\n{plan}")

            # 3. EXECUTOR PHASE: Write the new code
            print("Executor is generating the code change...")
            proposed_code_change = executor.execute_plan(plan, backpack)
            # For simplicity, let's assume it only modifies one file for now

            # 4. VERIFIER PHASE: Check the work
            print("Verifier is testing the new code...")
            verification_result = verifier.verify_change(loaded_goal, proposed_code_change)
            print(f"Verifier returned result: Success={verification_result['success']}")

            # 5. COMMIT PHASE: Decide whether to accept the change
            if verification_result['success']:
                print("Change VERIFIED. Committing to memory.")
                current_code_state = proposed_code_change # Update the state
                state_manager.save_document_state(current_code_state, loaded_goal)
            else:
                print("Change FAILED verification. Discarding change and trying again next turn.")
                # In the future, this failure reason would be fed back into the next loop

            turn_number += 1
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n--- User interrupted. Shutting down agent. ---")
    finally:
        print("--- Agent shutdown complete. ---")

