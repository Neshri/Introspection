#!/usr/bin/env python3
"""
Simple test script to run the Scout and observe its crawling behavior.
"""

from evolving_graphs.agent_graph.intelligence_project_scout import Scout

def test_scout():
    import time
    # Create a mock memory interface for testing
    class MockMemory:
        def query_memory(self, query, current_turn=0, n_results=5):
            return {'ids': [[]], 'documents': [[]]}

    memory = MockMemory()
    scout = Scout(memory, 'evolving_graphs/agent_graph')
    sample_goal = "Improve stability"
    print("Starting Scout with goal-directed traversal...")
    start_time = time.time()
    backpack, used_memory_ids = scout.scout_project(sample_goal, current_turn=0)
    end_time = time.time()
    time_taken = end_time - start_time

    print("\n=== TEST RESULTS ===")
    print(f"Sample Goal: {sample_goal}")
    print(f"Time taken: {time_taken:.2f} seconds")
    print(f"Backpack contains {len(backpack)} modules.")
    print("\nBackpack modules:")
    for i, module in enumerate(backpack):
        print(f"  {i+1}. {module['file_path']}: {module['justification'][:100]}...")

    # Check output format consistency
    print("\n=== OUTPUT FORMAT CHECK ===")
    expected_keys = {"file_path", "justification", "key_elements", "full_code"}
    for module in backpack:
        if set(module.keys()) == expected_keys:
            print(f"✓ {module['file_path']} - correct format")
        else:
            print(f"✗ {module['file_path']} - missing keys: {expected_keys - set(module.keys())}")

if __name__ == "__main__":
    test_scout()