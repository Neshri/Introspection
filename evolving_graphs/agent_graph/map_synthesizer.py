import os
import json
import logging
from typing import Dict, List, Optional
from .summary_models import ModuleContext
from .semantic_gatekeeper import SemanticGatekeeper

class MapSynthesizer:
    """
    Synthesizes a high-level "System Architecture" overview using a Generic Grounded approach.
    Identifies key architectural anchors dynamically and weaves them into a cohesive narrative.
    """
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def synthesize(self, contexts: Dict[str, ModuleContext], processing_order: List[str], goal: Optional[str] = None) -> str:
        """
        Main entry point for architecture synthesis.
        """
        if not contexts:
            return "No module contexts available for synthesis."

        # 1. Identify Architectural Anchors dynamically
        anchors = self._identify_anchors(contexts)
        
        # 2. Extract context for the anchors
        anchor_details = []
        for path in anchors:
            ctx = contexts[path]
            name = os.path.basename(path)
            role = ctx.module_role.text if ctx.module_role else "Core component."
            archetype = ctx.archetype or "Utility"
            # Include dependencies to help the LLM see the relationships
            deps = [os.path.basename(d) for d in (ctx.key_dependencies or {}).keys()]
            dep_str = f" interacts with {', '.join(deps)}" if deps else ""
            anchor_details.append(f"- **{name}** ({archetype}): {role}{dep_str}")

        # 3. List the "Supporting Cast" (everything else) for high-level context
        supporting_cast = []
        anchor_set = set(anchors)
        for path in processing_order:
            if path in anchor_set or path not in contexts: continue
            supporting_cast.append(os.path.basename(path))

        # 4. Perform Single-Pass Grounded Synthesis
        return self._run_grounded_synthesis(anchor_details, supporting_cast, goal)

    def _identify_anchors(self, contexts: Dict[str, ModuleContext]) -> List[str]:
        """
        Dynamically identifies the 5-7 most significant modules to anchor the narrative.
        Prioritizes Entry Points and high-gravity Orchestrators.
        """
        scores = {}
        for path, ctx in contexts.items():
            score = 0
            archetype = (ctx.archetype or "").lower()
            name = os.path.basename(path).lower()
            
            # Entry Points get highest weight
            if "entry" in archetype or "main" in name:
                score += 100
            # Orchestrators/Services get high weight
            elif "service" in archetype or "core" in name or "orchestrator" in name:
                score += 50
            # Contextualizers/Analyzers
            elif "analyst" in name or "context" in name or "analyzer" in name:
                score += 30
            
            # Plus dependency gravity (how much it's used or uses)
            score += len(ctx.key_dependencies or {}) * 2
            
            scores[path] = score
            
        # Select top 7 anchors
        sorted_anchors = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return sorted_anchors[:7]

    def _run_grounded_synthesis(self, anchor_details: List[str], supporting_cast: List[str], goal: Optional[str]) -> str:
        """
        A single-pass, focused prompt to build a technical story from anchor modules.
        """
        anchors_text = "\n".join(anchor_details)
        supporting_text = ", ".join(supporting_cast) if supporting_cast else "None"
        goal_text = f"Project Goal: {goal}\n" if goal else ""
        
        prompt = f"""
        ### ROLE
        You are a Staff Software Architect.

        ### CONTEXT
        {goal_text}
        
        ### PRIMARY COMPONENTS (The Engine Room)
        {anchors_text}

        ### SECONDARY COMPONENTS
        {supporting_text}

        ### TASK
        Synthesize a **System Architecture Narrative** (2-3 paragraphs).
        Explain how these specific components collaborate to fulfill the Project Goal.

        ### WRITING GUIDELINES (TECHNICAL & CONCRETE)
        1. **Directness**: Start by defining exactly what the system is based on its core components.
        2. **Technical Grounding**: Use the provided module names and their specific roles. Focus on functional outcomes and architectural logic rather than simple data passing.
        3. **Style**: Use professional, technical language. Avoid adjectives (e.g., "wonderful", "robust", "powerful") and marketing buzzwords. 
        4. **Cohesion**: Ensure the narrative flows logically from input/orchestration to analysis and output. Do NOT use transition fillers like "Moreover", "Furthermore", or "Additionally".
        5. **Format**: Use clean Markdown paragraphs. No headers, no lists.

        ### OUTPUT REQUIREMENT
        Output strictly valid JSON with key "architecture_overview". The value should be the Markdown narrative.
        """
        
        return self.gatekeeper.execute_with_feedback(
            prompt, 
            "architecture_overview", 
            forbidden_terms=["moreover", "furthermore", "additionally", "robust", "seamless", "pivotal", "meticulous", "insight", "unfolds", "journey"],
            log_context="GroundedSynthesis"
        )