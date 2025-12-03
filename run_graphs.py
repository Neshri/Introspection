from evolving_graphs.agent_graph.agent_graph_main import main
from evolving_graphs.linter_graph.linter_graph_main import main as linter_main
from evolving_graphs.sandboxer_graph.sandboxer_graph_main import main as sandboxer_main
from evolving_graphs.loganalyzer_graph.loganalyzer_graph_main import main as loganalyzer_main
import logging
import time
import os

if __name__ == "__main__":
    sandbox_path = sandboxer_main("agent_graph")
    print(f"Created sandbox at {sandbox_path}")

    # 1. Define the variable for the log file
    log_file_path = os.path.join(sandbox_path, "run.log")

    # 2. Configure logging to write to that file AND the terminal
    # Force reconfiguration since agent_graph_main imports logging.basicConfig
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path), # This saves the data for the analyzer
            logging.StreamHandler()
        ]
    )

    start_time = time.time()
    agent_result = main("Improve accuracy, stability, and readability.", sandbox_path)
    print(agent_result)
    print(f"Time taken: {time.time() - start_time}")

    # 3. Send the log file variable to the analyzer
    log_response = loganalyzer_main(log_file_path)
    print(log_response)