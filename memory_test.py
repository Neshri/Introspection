# evolving_graphs/agent_graph/test_memory_interface.py

import os
import shutil
# 'time' is no longer needed for the logic
from evolving_graphs.agent_graph.memory_interface import MemoryInterface

def main():
    """A demonstration of the turn-based MemoryInterface class capabilities."""
    db_path = "test_db"
    
    # Ensure the test environment is clean before starting
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
        
    print(f"Creating a temporary database at './{db_path}/'")
    memory = MemoryInterface(db_path=db_path)
    
    # Initialize the master clock for the agent's lifecycle
    current_turn = 1

    try:
        # --- 1. Testing Memory Addition ---
        print("\n--- 1. ADDING MEMORIES (Turn 1) ---")
        core_mem_id = memory.add_memory("The agent's prime directive is to achieve its goal.", memory_type="core", creator_role="System", current_turn=current_turn)
        print(f"Added CORE memory with ID: {core_mem_id}")
        
        dyn_mem_1_id = memory.add_memory("Architectural patterns like Orchestrator are good.", memory_type="dynamic", creator_role="Architect", current_turn=current_turn)
        print(f"Added DYNAMIC memory with ID: {dyn_mem_1_id}")

        dyn_mem_2_id = memory.add_memory("Using pytest is a good way to verify code.", memory_type="dynamic", creator_role="Planner", current_turn=current_turn)
        print(f"Added DYNAMIC memory with ID: {dyn_mem_2_id}")

        # --- 2. Testing Memory Querying ---
        current_turn += 1
        print(f"\n--- 2. QUERYING MEMORIES (Turn {current_turn}) ---")
        query_text = "How should I structure the application workflow?"
        results = memory.query_memory(query_text, n_results=1, current_turn=current_turn)
        print(f"\nQuerying for: '{query_text}'")
        if results and results['documents'][0]:
            print(f"  Top result: '{results['documents'][0][0]}'")
            # Verify that the last_accessed_turn was updated
            retrieved_mem_id = results['ids'][0][0]
            updated_meta = memory.collection.get(ids=[retrieved_mem_id])['metadatas'][0]
            print(f"  Verified 'last_accessed_turn' is now: {updated_meta.get('last_accessed_turn')}")
        else:
            print("  No relevant results found.")

        # --- 3. Testing Feedback Mechanism ---
        current_turn += 1
        print(f"\n--- 3. APPLYING FEEDBACK (Turn {current_turn}) ---")
        print(f"Updating memory about 'pytest' (ID: {dyn_mem_2_id[:8]}...)")
        
        initial_score = memory.collection.get(ids=[dyn_mem_2_id])['metadatas'][0]['relevance_score']
        print(f"  Score before feedback: {initial_score:.2f}")

        memory.update_memory_feedback(dyn_mem_2_id, feedback_adjustment=+5.0, current_turn=current_turn)
        score_after_positive = memory.collection.get(ids=[dyn_mem_2_id])['metadatas'][0]['relevance_score']
        print(f"  Score after +5.0 feedback: {score_after_positive:.2f}")

        memory.update_memory_feedback(dyn_mem_2_id, feedback_adjustment=-15.0, current_turn=current_turn)
        score_after_negative = memory.collection.get(ids=[dyn_mem_2_id])['metadatas'][0]['relevance_score']
        print(f"  Score after -15.0 feedback: {score_after_negative:.2f}")

        # --- 4. Testing Self-Cleaning (Decay) ---
        print("\n--- 4. TESTING DECAY (SELF-CLEANING) ---")
        print("Simulating 3 turns passing without accessing the 'Orchestrator' memory...")
        
        # We know dyn_mem_1 was created and last accessed on turn 1
        score_before_decay = memory.collection.get(ids=[dyn_mem_1_id])['metadatas'][0]['relevance_score']
        core_score_before_decay = memory.collection.get(ids=[core_mem_id])['metadatas'][0]['relevance_score']

        print(f"  Dynamic memory score BEFORE maintenance: {score_before_decay:.2f}")
        print(f"  Core memory score BEFORE maintenance:    {core_score_before_decay:.2f}")

        # Advance the master clock by 3 turns
        current_turn += 3
        print(f"\nPerforming maintenance on Turn {current_turn}...")
        memory.perform_maintenance(current_turn=current_turn, decay_rate=10.0)
        print("  >> Maintenance complete <<\n")

        score_after_decay = memory.collection.get(ids=[dyn_mem_1_id])['metadatas'][0]['relevance_score']
        core_score_after_decay = memory.collection.get(ids=[core_mem_id])['metadatas'][0]['relevance_score']

        print(f"  Dynamic memory score AFTER maintenance: {score_after_decay:.2f} (Should be lower)")
        print(f"  Core memory score AFTER maintenance:    {core_score_after_decay:.2f} (Should be unchanged)")

        # --- 5. Testing Self-Cleaning (Pruning) ---
        print("\n--- 5. TESTING PRUNING (SELF-CLEANING) ---")
        print(f"Driving a memory's score below the prune threshold (e.g., < 1.0)...")
        # Give massive negative feedback on the same turn
        memory.update_memory_feedback(dyn_mem_2_id, feedback_adjustment=-100.0, current_turn=current_turn)
        
        # Run maintenance again on the same turn to trigger the prune
        memory.perform_maintenance(current_turn=current_turn, prune_threshold=1.0)

        result = memory.collection.get(ids=[dyn_mem_2_id])
        if not result['ids']:
            print(f"  SUCCESS: Memory {dyn_mem_2_id[:8]}... was correctly pruned.")
        else:
            print(f"  FAILURE: Memory {dyn_mem_2_id[:8]}... was not pruned.")

    finally:
        # --- Cleanup ---
        print(f"\n--- CLEANUP ---")
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            print(f"Successfully removed temporary database at './{db_path}/'")

if __name__ == "__main__":
    main()