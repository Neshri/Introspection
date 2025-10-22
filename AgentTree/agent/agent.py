#
# agent.py (The Main Trunk)
# This module contains the primary orchestrating loop for the agent. It initializes
# the agent's state and then repeatedly calls the MCTS engine to "think" and
# decide on the next action to take.
#
# It uses the following modules:
# - agent.utils.config: To get the initial goal.
# - agent.utils.state_manager: To load and save its memory.
# - agent.engine.node: To create the root of the search tree.
# - agent.engine.mcts: To run the core "thinking" process.
#

import time
from agent.utils import config
from agent.utils import state_manager
from agent.engine.node import Node
from agent.engine import mcts

def run():
    """The main, continuous loop that drives the agent's behavior."""
    print("--- Initializing Agent ---")
    
    loaded_goal, loaded_doc = state_manager.load_document_on_startup()
    
    if loaded_goal == config.INITIAL_GOAL and loaded_doc is not None:
        print("Previous session found. Loading state...")
        root_node = Node(document_state=loaded_doc)
    else:
        print("Starting a new session.")
        root_node = Node(document_state="""def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test cases will be validated automatically""")

    print(f"Main Goal: {config.INITIAL_GOAL}")
    
    turn_number = 1
    try:
        while True:
            print(f"\n--- Turn {turn_number} ---")
            
            best_next_node = mcts.run_mcts_cycle(root_node)
            
            if best_next_node is None:
                print("Agent has concluded its work.")
                break

            print(f"Agent commits to the next step:\n---")
            print(best_next_node.plan_that_led_here)
            print("---\n")
            
            root_node = best_next_node
            root_node.parent = None
            
            state_manager.save_document_state(root_node.document_state, config.INITIAL_GOAL)
            turn_number += 1
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n--- User interrupted. Shutting down agent. ---")
    finally:
        print("--- Agent shutdown complete. ---")