#
# main.py (The Root)
# This is the main entry point for the agent. Its only responsibility is to
# start the agent's primary process.
#
# It uses the following modules:
# - agent.agent_class: Agent class for goal-setting and management with run loop.
#

import argparse  # Standard library for command-line argument parsing
from agent import Agent  # Agent class for goal management and run loop

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Agent with a specified goal.")
    parser.add_argument("--goal", required=True, help="The goal string for the agent to pursue.")
    args = parser.parse_args()

    agent = Agent(goal=args.goal)
    agent.run_with_agent()