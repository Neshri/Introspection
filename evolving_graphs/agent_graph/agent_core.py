from .memory_core import ChromaMemory
from .llm_util import chat_llm
from .agent_config import DEFAULT_MODEL, CONTEXT_LIMIT
from .agent_util import project_pulse
from .summary_models import ModuleContext
# ADDED: Import the renderer
from .report_renderer import ReportRenderer
from .map_synthesizer import MapSynthesizer
from .semantic_gatekeeper import SemanticGatekeeper

class CrawlerAgent:
    def __init__(self, goal: str, target_root: str):
        self.goal = goal
        self.target_root = target_root
        self.memory = ChromaMemory()
        print(f"Initializing CrawlerAgent with goal: {self.goal} and target root: {self.target_root}")

    def run(self) -> str:
        # TODO: Implement the agent's logic here
        print(f"Running CrawlerAgent for goal: {self.goal} and target root: {self.target_root}")
        
        # 1. Analyze the target graph
        project_map, processing_order = project_pulse(self.target_root)
        
        # 2. Synthesize System Architecture
        gatekeeper = SemanticGatekeeper()
        synthesizer = MapSynthesizer(gatekeeper)
        system_summary = synthesizer.synthesize(project_map, processing_order)
        
        # 3. Render the report instead of printing raw objects
        renderer = ReportRenderer(project_map, system_summary=system_summary)
        renderer.render()
        
        current_turn = 0
        response = "Analysis Complete. Check PROJECT_MAP.md."
        
        # Use for loop for now.
        for i in range(5):
            # Do stuff here like understand the codebase by navigating the graph. Will require a new module.
            self.memory.cleanup_memories(current_turn)
            current_turn += 1


        # For now just return the rendered map.
        return response