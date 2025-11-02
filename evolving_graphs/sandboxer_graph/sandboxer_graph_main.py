import argparse
import os
import shutil

def main(graph_folder: str) -> str:
    source_path = "../" + graph_folder
    candidates_dir = "../candidates"
    os.makedirs(candidates_dir, exist_ok=True)
    destination_path = os.path.join(candidates_dir, graph_folder)
    shutil.copytree(source_path, destination_path)
    return os.path.abspath(destination_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a copy of the specified graph and return its path.")
    parser.add_argument("--graph", required=True, help="The graph folder to copy into the sandbox.")
    args = parser.parse_args()
    
    path = main(args.graph)
    print(path)