#!/usr/bin/env python3
"""
test_sandbox_fix.py
Simple test to verify the sandbox directory creation fix.
"""

import os
import shutil
import tempfile

# Import the SandboxManager directly
from evolving_graphs.agent_graph.sandbox_utils import SandboxManager


def test_sandbox_creation():
    """Test that sandbox creation works within evolving_graphs directory."""

    # Create a temporary directory structure to simulate the project
    with tempfile.TemporaryDirectory() as temp_root:
        # Create the evolving_graphs structure
        evolving_graphs_dir = os.path.join(temp_root, 'evolving_graphs')
        os.makedirs(evolving_graphs_dir)

        # Create agent_graph subdirectory
        agent_graph_dir = os.path.join(evolving_graphs_dir, 'agent_graph')
        os.makedirs(agent_graph_dir)

        # Change to agent_graph directory to simulate module execution
        original_cwd = os.getcwd()
        os.chdir(agent_graph_dir)

        try:
            # Create sandbox manager and test creation
            manager = SandboxManager()
            print(f"Base dir: {manager.base_dir}")

            # Try to create the sandbox
            manager.create_directory_sandbox()
            print(f"Candidate dir: {manager.candidate_dir}")

            # Check if candidate was created correctly
            candidate_exists = os.path.exists(manager.candidate_dir)
            print(f"Candidate exists: {candidate_exists}")

            if candidate_exists:
                # Check if it contains the expected structure
                candidate_agent = os.path.join(manager.candidate_dir, 'agent_graph')
                has_agent_graph = os.path.exists(candidate_agent)
                print(f"Has agent_graph in candidate: {has_agent_graph}")

                if has_agent_graph:
                    has_main = os.path.exists(os.path.join(candidate_agent, 'agent_graph_main.py'))
                    print(f"Has agent_graph_main.py in candidate: {has_main}")
                else:
                    has_main = False
            else:
                has_main = False

            # Clean up candidate
            manager.rollback_directory_sandbox()

            return candidate_exists and has_agent_graph and has_main

        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    success = test_sandbox_creation()
    print(f"Test result: {'PASSED' if success else 'FAILED'}")
    exit(0 if success else 1)