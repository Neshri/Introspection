#
# main.py (The Root)
# This is the main entry point for the agent. Its only responsibility is to
# start the agent's primary process.
#
# It uses the following modules:
# - agent.agent_class: Agent class for goal-setting and management with run loop.
#

from agent import Agent  # Import the Agent class for goal management and run loop

if __name__ == "__main__":
    agent = Agent()
    agent.run_with_agent()