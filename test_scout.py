#!/usr/bin/env python3
"""
Simple test script to run the Scout and observe its crawling behavior.
"""

from evolving_graphs.agent_graph.intelligence_project_scout import Scout

def test_scout():
    scout = Scout()
    scout.set_working_directory('evolving_graphs/agent_graph')
    mock_goal = "Add a comment to agent_config.py"
    print("Starting Scout...")
    backpack = scout.scout_project(mock_goal)
    print(f"Backpack contains {len(backpack)} modules.")
    for module in backpack:
        print(f"  - {module['file_path']}: {module['justification'][:100]}...")

if __name__ == "__main__":
    test_scout()