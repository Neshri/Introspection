import os
from typing import Dict, List
import logging
from .summary_models import ModuleContext
from .semantic_gatekeeper import SemanticGatekeeper

class MapSynthesizer:
    """
    Synthesizes a high-level "System Architecture" overview using Flow-Based Synthesis.
    """
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def synthesize(self, contexts: Dict[str, ModuleContext], processing_order: List[str]) -> str:
        """
        Generates a cohesive system summary by analyzing the flow of data 
        through the archetypes.
        """
        # 1. Group Modules by Archetype
        groups = {
            "Entry Point": [],
            "Service": [],
            "Utility": [],
            "Data Model": [],
            "Configuration": []
        }
        
        # We need a quick lookup to see which layer a dependency belongs to
        module_to_layer = {}

        for path in processing_order:
            if path not in contexts: continue
            ctx = contexts[path]
            archetype = ctx.archetype if ctx.archetype else "Utility"
            
            # Map raw archetype strings to our groups
            target_group = "Utility"
            if "Entry Point" in archetype: target_group = "Entry Point"
            elif "Service" in archetype: target_group = "Service"
            elif "Utility" in archetype: target_group = "Utility"
            elif "Data" in archetype: target_group = "Data Model"
            elif "Config" in archetype: target_group = "Configuration"
            
            groups[target_group].append(ctx)
            module_to_layer[os.path.basename(path)] = target_group

        # 2. Synthesize Each Group (Layer) with Connectivity Context
        layer_summaries = {}
        for group_name, modules in groups.items():
            if not modules: continue
            logging.info(f"Synthesizing Group: {group_name} ({len(modules)} modules)")
            # We pass the module_to_layer map so the group summary knows 
            # if it's talking to the Data Layer or the Utility Layer
            layer_summaries[group_name] = self._synthesize_group(group_name, modules, module_to_layer)

        # 3. Synthesize Final System Overview (Merging logic)
        return self._synthesize_system(layer_summaries)

    def _synthesize_group(self, group_name: str, modules: List[ModuleContext], layer_map: Dict[str, str]) -> str:
        # Prepare context list with dependency hints
        module_details = []
        
        for m in modules:
            name = os.path.basename(m.file_path)
            role = m.module_role.text if m.module_role else "Role pending analysis."
            
            # Extract distinct external interactions
            interactions = set()
            if m.key_dependencies:
                for dep_path in m.key_dependencies.keys():
                    dep_name = os.path.basename(dep_path)
                    # If we know the layer of the dependency, note it
                    if dep_name in layer_map and layer_map[dep_name] != group_name:
                        target_layer = layer_map[dep_name]
                        interactions.add(f"calls {target_layer} ({dep_name})")
            
            interaction_str = f" -> Interactions: {', '.join(interactions)}" if interactions else ""
            module_details.append(f"- **{name}**: {role}{interaction_str}")
        
        modules_text = "\n".join(module_details)
        
        prompt = f"""
        ### ROLE
        You are a generic Systems Architect.

        ### INPUT DATA
        Layer: {group_name}
        Modules & Connectivity:
        {modules_text}

        ### TASK
        Synthesize a functional summary of the {group_name} layer.
        - Focus on **Responsibility**: What does this layer strictly own?
        - Focus on **Connectivity**: explicitly mention which *other* layers this layer interacts with based on the input.
        - Do not list modules one by one. Merge them into concepts (e.g., "The integration services handle...").

        ### REQUIREMENTS
        1. Output strictly valid JSON with key "summary".
        2. Keep it under 80 words.
        3. No marketing fluff ("seamless", "powerhouse").
        """
        
        return self.gatekeeper.execute_with_feedback(
            prompt, 
            "summary", 
            forbidden_terms=["seamless", "robust", "pivotal", "meticulous", "comprehensive"],
            verification_source=modules_text,
            log_context=f"GroupSynth:{group_name}"
        )

    def _synthesize_system(self, layer_summaries: Dict[str, str]) -> str:
        layers_text = ""
        # Logical flow for the prompt to read
        order = ["Configuration", "Data Model", "Utility", "Service", "Entry Point"]
        
        for name in order:
            if name in layer_summaries:
                layers_text += f"[{name} Layer]: {layer_summaries[name]}\n"
        
        prompt = f"""
        ### ROLE
        You are a Technical Documentation Specialist.

        ### INPUT DATA
        Architecture Components:
        {layers_text}

        ### TASK
        Write a cohesive **System Architecture Narrative**.
        Instead of describing layers in isolation, describe the **flow of data and control** through the system.

        ### WRITING STRATEGY (MERGE, DON'T LIST)
        1. Start with the **Foundation** (Config/Data) to establish what the system is built on.
        2. Move to the **Application Logic** (Service/Utility) to show how data is manipulated.
        3. End with the **Execution** (Entry Point) to show how the user triggers these flows.
        4. Use transition phrases like "This data structure is then utilized by...", "Supported by the utility layer...", "acting as the gateway..."

        ### REQUIREMENTS
        1. Output strictly valid JSON with key "overview".
        2. The value must be a single MARKDOWN string (3 paragraphs max).
        3. **CRITICAL**: Do not use headers (##). Just text paragraphs.
        4. Do NOT use marketing adjectives (seamless, robust, bespoke).
        """
        
        return self.gatekeeper.execute_with_feedback(
            prompt, 
            "overview", 
            forbidden_terms=["seamless", "robust", "pivotal", "meticulous", "bespoke", "symphony"], 
            verification_source=layers_text,
            log_context="SystemSynth"
        )