# agent_runner.py (Legacy Runner)
# Imports: Standard time library; config; intelligence roles (Scout, Planner); pipeline roles (Executor, Verifier); Agent class for goal management.

import time  # Standard library for time-related functions, used for sleep in the main loop
from .agent_config import config  # Configuration settings
from .intelligence_project_scout import Scout  # Intelligence components for scouting and planning
from .intelligence_plan_generator import Planner  # Intelligence components for scouting and planning
from .pipeline_executor import Executor  # Executor class for generating and applying code changes
from .pipeline_code_verifier import Verifier  # Verifier class for testing and validating code changes
from .agent_core import Agent  # Agent class for goal-setting and management

# Backward compatibility: keep run() function for legacy execution
def run():
    """The main, continuous loop that drives the agent's behavior."""
    print("--- Initializing Agent ---")

    loaded_goal, current_code_state = None, None

    # Initialize our specialist agents
    scout = Scout()
    planner = Planner()
    executor = Executor(loaded_goal)
    verifier = Verifier()

    turn_number = 1
    try:
        while True:
            print(f"\n--- Turn {turn_number} ---")

            # This is the new, linear pipeline.

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
                # State persistence now handled by memory_interface
            else:
                print("Change FAILED verification. Discarding change and trying again next turn.")
                # In the future, this failure reason would be fed back into the next loop

            turn_number += 1
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n--- User interrupted. Shutting down agent. ---")
    finally:
        print("--- Agent shutdown complete. ---")

