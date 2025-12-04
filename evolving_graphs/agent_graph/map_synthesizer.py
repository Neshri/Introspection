import os
from typing import Dict, List
import logging
from .summary_models import ModuleContext
from .semantic_gatekeeper import SemanticGatekeeper
from .agent_config import DEFAULT_MODEL

class MapSynthesizer:
    """
    Synthesizes a high-level "System Architecture" overview using Hierarchical Synthesis.
    """
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def synthesize(self, contexts: Dict[str, ModuleContext], processing_order: List[str]) -> str:
        """
        Generates a cohesive system summary by grouping modules by Archetype and synthesizing layers first.
        """
        # 1. Group Modules by Archetype
        groups = {
            "Entry Point": [],
            "Service": [],
            "Utility": [],
            "Data Model": [],
            "Configuration": []
        }
        
        for path in processing_order:
            if path not in contexts: continue
            ctx = contexts[path]
            archetype = ctx.archetype if ctx.archetype else "Utility"
            
            # Map raw archetype strings to our groups
            if "Entry Point" in archetype: groups["Entry Point"].append(ctx)
            elif "Service" in archetype: groups["Service"].append(ctx)
            elif "Utility" in archetype: groups["Utility"].append(ctx)
            elif "Data" in archetype: groups["Data Model"].append(ctx)
            elif "Config" in archetype: groups["Configuration"].append(ctx)
            else: groups["Utility"].append(ctx)

        # 2. Synthesize Each Group (Layer)
        layer_summaries = {}
        for group_name, modules in groups.items():
            if not modules: continue
            logging.info(f"Synthesizing Group: {group_name} ({len(modules)} modules)")
            layer_summaries[group_name] = self._synthesize_group(group_name, modules)

        # 3. Synthesize Final System Overview
        return self._synthesize_system(layer_summaries)

    def _synthesize_group(self, group_name: str, modules: List[ModuleContext]) -> str:
        # Prepare context list
        module_list = []
        for m in modules:
            name = os.path.basename(m.file_path)
            role = m.module_role.text if m.module_role else "No role defined."
            module_list.append(f"- **{name}**: {role}")
        
        modules_text = "\n".join(module_list)
        
        prompt = f"""
        ### ROLE
        You are a Technical Documentation Specialist.

        ### INPUT DATA
        Group: {group_name}
        Modules:
        {modules_text}

        ### TASK
        Synthesize a concise technical summary of this {group_name} layer.
        - Describe what this group of modules collectively achieves.
        - Highlight key interactions between them if obvious.
        - Be strictly objective. No marketing fluff.

        ### REQUIREMENTS
        1. Output strictly valid JSON with key "summary".
        2. Do NOT use words like "seamless", "robust", "pivotal".
        3. Focus on technical responsibility.
        """
        
        return self.gatekeeper.execute_with_feedback(
            prompt, 
            "summary", 
            forbidden_terms=["seamless", "robust", "pivotal", "meticulous"],
            verification_source=modules_text,
            log_context=f"GroupSynth:{group_name}"
        )

    def _synthesize_system(self, layer_summaries: Dict[str, str]) -> str:
        layers_text = ""
        # Order matters for narrative
        order = ["Entry Point", "Service", "Utility", "Data Model", "Configuration"]
        
        for name in order:
            if name in layer_summaries:
                layers_text += f"### {name} Layer\n{layer_summaries[name]}\n\n"
        
        prompt = f"""
        ### ROLE
        You are a Technical Documentation Specialist.

        ### INPUT DATA
        System Layers:
        {layers_text}

        ### TASK
        Generate a High-Level System Overview.
        - Write a cohesive, text-based narrative (3-4 paragraphs).
        - Do NOT output a list or a dictionary.
        - Combine the layers into a story of how data flows through the system.

        ### REQUIREMENTS
        1. Output strictly valid JSON with key "overview".
        2. The value of "overview" must be a single MARKDOWN string.
        3. Do NOT use marketing adjectives.
        """
        
        return self.gatekeeper.execute_with_feedback(
            prompt, 
            "overview", 
            forbidden_terms=["seamless", "robust", "pivotal", "meticulous"], 
            verification_source=layers_text,
            log_context="SystemSynth"
        )
