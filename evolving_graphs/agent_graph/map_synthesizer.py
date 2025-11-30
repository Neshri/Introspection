import os
from typing import Dict, List
import logging
from .summary_models import ModuleContext
from .semantic_gatekeeper import SemanticGatekeeper
from .agent_config import DEFAULT_MODEL
from .llm_util import chat_llm

class MapSynthesizer:
    """
    Synthesizes a high-level "System Architecture" overview from the detailed module contexts.
    """
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def synthesize(self, contexts: Dict[str, ModuleContext], processing_order: List[str]) -> str:
        """
        Generates a cohesive system summary using a Verified Rolling Synthesis approach.
        """
        current_summary = "The system is initialized."
        
        for module_path in processing_order:
            if module_path not in contexts: continue
            
            module = contexts[module_path]
            module_name = os.path.basename(module.file_path)
            module_role = module.module_role.text if module.module_role else "No role defined."
            
            logging.info(f"Synthesizing module: {module_name}")
            
            critique = None
            success = False
            
            for attempt in range(3): # Max 3 retries
                # 1. Synthesis Step
                new_summary = self._generate_summary(current_summary, module_name, module_role, critique)
                
                # 2. Atomic Verification Step (3 Calls)
                errors = []
                
                # Check 1: Presence
                if not self._check_presence(new_summary, module_name):
                    errors.append(f"Module '{module_name}' is missing from the summary.")
                
                # Check 2: Fidelity
                elif not self._check_fidelity(new_summary, module_name, module_role):
                    errors.append(f"Module '{module_name}' role is misrepresented. It must be described as: {module_role}")
                    
                # Check 3: Hallucination
                elif self._check_hallucination(new_summary, module_name, module_role):
                    errors.append(f"Module '{module_name}' has hallucinated capabilities not in its role.")
                
                if not errors:
                    current_summary = new_summary
                    success = True
                    break # Success, move to next module
                
                # 3. Regeneration Trigger
                critique = " ".join(errors)
                logging.warning(f"Verification Failed for {module_name} (Attempt {attempt+1}): {critique}")
            
            # Fallback: If retries exhausted, append simple string to avoid data loss
            if not success:
                 logging.error(f"Failed to synthesize {module_name} after 3 attempts. Appending raw role.")
                 current_summary += f"\n- **{module_name}**: {module_role} (Verification Failed)"

        return current_summary

    def _generate_summary(self, current_summary: str, name: str, role: str, critique: str = None) -> str:
        prompt = f"""
        Act as a Lead Software Architect.
        
        Current System Architecture:
        {current_summary}
        
        New Module to Integrate:
        - Name: {name}
        - Role: {role}
        
        Task:
        Rewrite the System Architecture to include the New Module.
        - Maintain the narrative flow.
        - Ensure {name} is described ACCURATELY according to its role.
        - Do NOT remove existing modules.
        """
        
        if critique:
            prompt += f"\n\nCRITIQUE (Previous Attempt Failed): {critique}\nFIX THIS ERROR."
            
        messages = [{"role": "user", "content": prompt}]
        return chat_llm(DEFAULT_MODEL, messages).strip()

    def _check_presence(self, summary: str, name: str) -> bool:
        prompt = f"""
        Summary:
        {summary}
        
        Task: Is the module `{name}` explicitly mentioned in the summary?
        Return ONLY JSON: {{ "present": boolean }}
        """
        val = self.gatekeeper.execute_with_feedback(prompt, "present", [])
        return str(val).lower() == "true"

    def _check_fidelity(self, summary: str, name: str, role: str) -> bool:
        prompt = f"""
        Summary:
        {summary}
        
        Module: {name}
        Defined Role: {role}
        
        Task: Does the summary describe `{name}` in a way that is consistent with its Defined Role?
        Return ONLY JSON: {{ "consistent": boolean }}
        """
        val = self.gatekeeper.execute_with_feedback(prompt, "consistent", [])
        return str(val).lower() == "true"

    def _check_hallucination(self, summary: str, name: str, role: str) -> bool:
        prompt = f"""
        Summary:
        {summary}
        
        Module: {name}
        Defined Role: {role}
        
        Task: Does the summary attribute any major actions/capabilities to `{name}` that are NOT present in its Defined Role?
        Return ONLY JSON: {{ "hallucination": boolean }}
        """
        val = self.gatekeeper.execute_with_feedback(prompt, "hallucination", [])
        return str(val).lower() == "true"
