import argparse
import os
import logging
from .agent_core import CrawlerAgent

# --- Logging Setup ---
# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Silence noisy HTTP libraries used by Ollama
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

def main(goal: str, target_folder: str) -> str:
    target_root = None
    # Find the root of the graph
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.endswith("_main.py"):
                target_root = os.path.join(root, file)
    if not target_root:
        raise FileNotFoundError(f"No file ending with _main.py found in {target_folder}")
    
    # Initialize the agent
    agent = CrawlerAgent(goal, target_root)
    # Run the agent
    agent.run()
    # TODO: Implement the rest of the function
    # just send back goal for now.
    return f"Agent run completed for goal: {goal}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--goal", required=True, help="The objective string.")
    parser.add_argument("--target_folder", required=True, help="The absolute path to the target folder.")
    args = parser.parse_args()
    goal = args.goal
    target_folder = args.target_folder

    result = main(goal, target_folder)
    print(result)