import chromadb
import uuid

class MemoryInterface:
    def query_memory(self, query, current_turn=0, n_results=5):
        raise NotImplementedError

class ChromaMemory(MemoryInterface):
    def __init__(self):
        # Initialize ChromaDB persistent client with local storage
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # Create or get existing collection for storing memories
        self.collection = self.client.get_or_create_collection(name="memories")

    def add_memory(self, memory_text, embedding, turn_added, helpfulness, metadata=None):
        """
        Add a memory with its embedding and metadata.
        """
        memory_id = str(uuid.uuid4())
        combined_metadata = {
            "turn_added": turn_added,
            "helpfulness": helpfulness,
            "last_used_turn": turn_added  # Initialize last_used_turn to turn_added
        }
        if metadata:
            combined_metadata.update(metadata)
        self.collection.add(
            ids=[memory_id],
            documents=[memory_text],
            embeddings=[embedding],
            metadatas=[combined_metadata]
        )

    def query_memory(self, query, current_turn=0, n_results=5):
        """
        Query memories and return top n results based on similarity.
        Updates last_used_turn for retrieved memories.
        """
        # Perform similarity search
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        # Update last_used_turn for retrieved memories
        if results['ids']:
            for memory_id in results['ids'][0]:
                # Get current metadata
                current_metadata = self.collection.get(ids=[memory_id], include=["metadatas"])['metadatas'][0]
                # Update last_used_turn
                updated_metadata = current_metadata.copy()
                updated_metadata['last_used_turn'] = current_turn
                # Update the metadata in the collection
                self.collection.update(
                    ids=[memory_id],
                    metadatas=[updated_metadata]
                )

        return results

    def update_helpfulness(self, memory_id, new_helpfulness):
        """
        Update the helpfulness score of a specific memory.
        """
        # Get current metadata
        current_metadata = self.collection.get(ids=[memory_id], include=["metadatas"])['metadatas'][0]
        # Update helpfulness
        updated_metadata = current_metadata.copy()
        updated_metadata['helpfulness'] = new_helpfulness
        # Update the metadata in the collection
        self.collection.update(
            ids=[memory_id],
            metadatas=[updated_metadata]
        )

    def cleanup_memories(self, current_turn):
        """
        Remove memories that are unhelpful or unused for many turns.
        Criteria: helpfulness < 0.3 or current_turn - last_used_turn > 50
        """
        # Get all memories
        all_memories = self.collection.get(include=["metadatas"])
        ids_to_delete = []
        for memory_id, metadata in zip(all_memories['ids'], all_memories['metadatas']):
            helpfulness = float(metadata.get('helpfulness', 0))
            last_used_turn = int(metadata.get('last_used_turn', 0))
            if helpfulness < 0.3 or (current_turn - last_used_turn) > 50:
                ids_to_delete.append(memory_id)
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)