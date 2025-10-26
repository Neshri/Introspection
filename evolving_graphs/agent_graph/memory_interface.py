import chromadb
import uuid
import time
import tiktoken

class MemoryInterface:
    """
    A dedicated interface to handle all interactions with the ChromaDB knowledge base.
    This class encapsulates all database logic, acting as a firewall.
    """

    def __init__(self, db_path: str = "memory_db", max_memory_tokens: int = 1000):
        """
        Initializes the connection to the persistent ChromaDB client.
        """
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="agent_knowledge")
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = max_memory_tokens

    def add_memory(self, content: str, current_turn: int, memory_type: str = "dynamic", creator_role: str = "unknown", initial_score: float = 100.0) -> str:
        """
        Adds a new memory to the database, enforcing a token limit.
        """
        token_count = len(self.tokenizer.encode(content))
        if token_count > self.max_tokens:
            raise ValueError(f"Memory content exceeds token limit ({token_count}/{self.max_tokens})")

        memory_id = str(uuid.uuid4())
        metadata = {
            "relevance_score": initial_score,
            "memory_type": memory_type,
            "creator_role": creator_role,
            "created_turn": current_turn,
            "last_accessed_turn": current_turn,
            "access_count": 0,       # NEW: Track how often this memory is retrieved
            "feedback_count": 0      # NEW: Track how often feedback is given
        }

        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[memory_id]
        )
        return memory_id

    def query_memory(self, query_text: str, current_turn: int, n_results: int = 5, min_score: float = 10.0) -> list:
        """
        Queries for relevant memories and updates their access metadata.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"relevance_score": {"$gte": min_score}},
            include=["metadatas", "documents"]
        )
        
        retrieved_ids = results['ids'][0]
        if retrieved_ids:
            metadatas_to_update = results['metadatas'][0]
            for meta in metadatas_to_update:
                meta['last_accessed_turn'] = current_turn
                meta['access_count'] = meta.get('access_count', 0) + 1 # NEW: Increment access count
            
            self.collection.update(ids=retrieved_ids, metadatas=metadatas_to_update)
            
        return results

    def update_memory_feedback(self, memory_id: str, feedback_adjustment: float, current_turn: int):
        """
        Updates a memory's score and its feedback/access metadata.
        """
        memory = self.collection.get(ids=[memory_id])
        if not memory['ids']:
            return

        metadata = memory['metadatas'][0]
        metadata['feedback_score'] = metadata.get('feedback_score', 0) + feedback_adjustment
        metadata['relevance_score'] += feedback_adjustment
        metadata['last_accessed_turn'] = current_turn
        metadata['feedback_count'] = metadata.get('feedback_count', 0) + 1 # NEW: Increment feedback count

        self.collection.update(ids=[memory_id], metadatas=[metadata])


    def perform_maintenance(self, current_turn: int, decay_rate: float = 0.1, prune_threshold: float = 1.0):
        """
        Performs self-cleaning based on turns, not wall-clock time.
        1. Decays the score of old, unused dynamic memories.
        2. Prunes memories whose scores have fallen below a threshold.
        """
        # --- 1. Decay Step ---
        all_dynamic_memories = self.collection.get(where={"memory_type": "dynamic"})
        
        ids_to_update = []
        metadatas_to_update = []

        for i, metadata in enumerate(all_dynamic_memories['metadatas']):
            # Use .get() for safety with potentially old data schemas
            last_accessed = metadata.get('last_accessed_turn', current_turn)
            turns_since_access = current_turn - last_accessed
            
            # Only apply decay to memories that haven't been accessed for more than one turn
            if turns_since_access > 1:
                # The decay is proportional to how many turns have passed
                decay = turns_since_access * decay_rate
                metadata['relevance_score'] -= decay
                
                ids_to_update.append(all_dynamic_memories['ids'][i])
                metadatas_to_update.append(metadata)

        if ids_to_update:
            self.collection.update(ids=ids_to_update, metadatas=metadatas_to_update)

        # --- 2. Prune Step ---
        # This logic is based on the decayed relevance_score and is already correct.
        ids_to_delete = self.collection.get(
            where={
                "$and": [
                    {"relevance_score": {"$lt": prune_threshold}},
                    {"memory_type": "dynamic"}
                ]
            }
        )['ids']
        
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
            print(f"Pruned {len(ids_to_delete)} decayed memories.")