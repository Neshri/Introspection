import os
import json
import logging
from typing import Dict, List, Optional
from .summary_models import ModuleContext
from .task_executor import TaskExecutor

class MapSynthesizer:
    """
    Synthesizes a high-level "System Architecture" overview using a Generic Grounded approach.
    Identifies key architectural anchors dynamically and weaves them into a cohesive narrative.
    """
    def __init__(self, task_executor: TaskExecutor):
        self.executor = task_executor

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
            
            # Enrich with Public API to give the LLM concrete logic to describe
            api_points = []
            if ctx.public_api:
                # Sort and take top 5 methods to avoid bloating context
                sorted_api = sorted(ctx.public_api.items(), key=lambda x: x[0])[:5]
                for entity, g_text in sorted_api:
                    api_points.append(f"`{entity}`: {g_text.text}")
            
            api_str = f"\n  - Key Interfaces: {'; '.join(api_points)}" if api_points else ""
            
            # Include dependencies
            deps = [os.path.basename(d) for d in (ctx.key_dependencies or {}).keys()]
            dep_str = f"\n  - Interacts with: {', '.join(deps)}" if deps else ""
            
            anchor_details.append(f"### Component: {name} ({archetype})\n- **Role**: {role}{api_str}{dep_str}")

        # 3. List the "Supporting Cast" (everything else) for high-level context
        supporting_cast = []
        anchor_set = set(anchors)
        for path in processing_order:
            if path in anchor_set or path not in contexts: continue
            supporting_cast.append(os.path.basename(path))

        # 4. Perform Grounded Synthesis using TaskExecutor Pipeline
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
        An audited, multi-pass synthesis to build a technical story from anchor modules.
        """
        anchors_text = "\n\n".join(anchor_details)
        supporting_text = ", ".join(supporting_cast) if supporting_cast else "None"
        goal_text = f"Project Goal: {goal}\n" if goal else ""
        
        main_goal = """
        Synthesize a cohesive 3-paragraph System Architecture Narrative.
        
        Paragraph 1: THE ORCHESTRATION. Describe the primary entry points and the flow of control.
        Paragraph 2: THE ANALYSIS LOGIC. Explain how data flows through the system and what technical transformations occur.
        Paragraph 3: STABILITY & VERIFICATION. Describe how the system ensures accuracy and handles complexity or errors.

        STRICT REQUIREMENTS:
        - Use technical, objective language. No marketing fluff (e.g., 'powerful', 'seamless').
        - Focus on the COLLABORATION between components, not just a list.
        - Start directly with the technical explanation. Do NOT say "This project is..." or "The architecture is...".
        - Ensure the narrative is cohesive and flows naturally between paragraphs.
        """
        
        # We wrap the prompt in the context format expected by TaskExecutor
        context_data = f"""
ARCHITECTURAL DATA:
{anchors_text}

SUPPORTING COMPONENTS: 
{supporting_text}
"""

        # Using solve_complex_task gives us the Drafter-Auditor loop and grounding checks
        return self.executor.solve_complex_task(
            main_goal + " Use strictly technical language. No future-casting or marketing fluff.",
            context_data,
            log_label="GroundedSynthesis"
        )