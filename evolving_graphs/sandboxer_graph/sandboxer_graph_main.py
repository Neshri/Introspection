import argparse
import os
import shutil

def main(graph_folder: str) -> str:
    """
    Create a copy of the specified graph and return its path.

    Args:
        graph_folder (str): The graph folder to copy.

    Returns:
        str: The absolute path of the copied graph folder.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    evolving_graphs_dir = os.path.dirname(script_dir)
    source_path = os.path.join(evolving_graphs_dir, graph_folder)
    candidates_dir = os.path.join(evolving_graphs_dir, "candidates")
    os.makedirs(candidates_dir, exist_ok=True)
    destination_path = os.path.join(candidates_dir, graph_folder)
    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    return os.path.abspath(destination_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a copy of the specified graph and return its path.")
    parser.add_argument("--graph", required=True, help="The graph folder to copy into the sandbox.")
    args = parser.parse_args()
    
    path = main(args.graph)
    print(path)