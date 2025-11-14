
from .memory_core import ChromaMemory
from .llm_util import chat_llm
from .agent_config import DEFAULT_MODEL, CONTEXT_LIMIT
from .agent_util import project_pulse

class CrawlerAgent:
    def __init__(self, goal: str, target_root: str):
        self.goal = goal
        self.target_root = target_root
        self.memory = ChromaMemory()
        print(f"Initializing CrawlerAgent with goal: {self.goal} and target root: {self.target_root}")

    def run(self) -> str:
        # TODO: Implement the agent's logic here
        print(f"Running CrawlerAgent for goal: {self.goal} and target root: {self.target_root}")
        project_map =  project_pulse(self.target_root)
        for key, value in project_map.items():
            print(f"File: {key}, Context data: {value}\n\n")
        current_turn = 0
        response = ""
        # Use for loop for now.
        for i in range(5):
            # Do stuff here like understand the codebase by navigating the graph.
            self.memory.cleanup_memories(current_turn)
            current_turn += 1

        return response