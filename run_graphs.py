from evolving_graphs.agent_graph.agent_graph_main import main
from evolving_graphs.linter_graph.linter_graph_main import main as linter_main
from evolving_graphs.sandboxer_graph.sandboxer_graph_main import main as sandboxer_main
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
if __name__ == "__main__":
    # Create a copy of agent_graph
    sandbox_path = sandboxer_main("agent_graph")
    print(f"Created sandbox at {sandbox_path}")
    agent_result = main("Improve accuracy, stability, and readability.", sandbox_path)
    print(agent_result)
    