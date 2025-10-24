#
# main.py (The Root)
# This is the main entry point for the agent. Its only responsibility is to
# start the agent's primary process.
#
# It uses the following modules:
# - agent_core: Agent class for goal-setting and management with run loop.
#

import argparse  # Standard library for command-line argument parsing
import sys  # Standard library for system-specific parameters and functions
import os  # Standard library for operating system interfaces

# Add the parent directory to the Python path to enable absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import agent_core  # Import the module to make Agent accessible via dot notation

# Use the imported module's Agent class
Agent = agent_core.Agent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Agent with a specified goal.")
    parser.add_argument("--goal", required=True, help="The goal string for the agent to pursue.")
    args = parser.parse_args()

    agent = Agent(goal_string=args.goal)
    agent.run_with_agent()