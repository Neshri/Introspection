#
# main.py (The Root)
# This is the main entry point for the agent. Its only responsibility is to
# start the agent's primary process.
#
# It uses the following modules:
# - agent.agent: The main trunk of the application, containing the core run loop.
#

from agent import agent  # Import the main agent module containing the core run loop for the application

if __name__ == "__main__":
    agent.run()