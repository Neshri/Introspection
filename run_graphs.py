from evolving_graphs.agent_graph.agent_graph_main import main
from evolving_graphs.linter_graph.linter_graph_main import main as linter_main
from evolving_graphs.sandboxer_graph.sandboxer_graph_main import main as sandboxer_main

if __name__ == "__main__":
    sandbox_path = sandboxer_main("agent_graph")
    agent_result = main("Improve accuracy, stability, and readability.", sandbox_path)
    print(agent_result)
    