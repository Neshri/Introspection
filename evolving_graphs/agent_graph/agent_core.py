
from .memory_core import ChromaMemory

class CrawlerAgent:
    def __init__(self, goal: str, target_root: str):
        self.goal = goal
        self.target_root = target_root
        self.memory = ChromaMemory()
        print(f"Initializing CrawlerAgent with goal: {self.goal} and target root: {self.target_root}")

    def run(self) -> str:
        # TODO: Implement the agent's logic here
        print(f"Running CrawlerAgent for goal: {self.goal} and target root: {self.target_root}")
        current_turn = 0
        
        self.memory.cleanup_memories(current_turn)
        

        response = ""
        return response