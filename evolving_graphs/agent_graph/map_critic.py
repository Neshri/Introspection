import re
from typing import List, Dict, Tuple, Optional
from .semantic_gatekeeper import SemanticGatekeeper

class MapCritic:
    """
    Analyzes the rendered PROJECT_MAP.md to identify gaps, ambiguities, and inconsistencies.
    Acts as a 'Scientist' reviewing the evidence.
    """
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def critique(self, project_map_content: str) -> List[Tuple[str, str]]:
        """
        Parses the map into individual modules and analyzes them sequentially.
        This prevents context overloading and ensures specific focus.
        """
        # 1. Parse the map into individual module chunks
        modules = self._parse_project_map(project_map_content)
        
        critiques = []
        
        # 2. Iterate through modules (One context at a time)
        # We can limit this loop or prioritize core modules if speed is a concern,
        # but for thoroughness, we check all found modules.
        for module_name, module_content in modules.items():
            
            # Stop if we have enough high-quality critiques (optional optimization)
            if len(critiques) >= 3:
                break

            instruction = self._analyze_single_module(module_name, module_content)
            
            if instruction:
                critiques.append((module_name, instruction))
                    
        return critiques

    def _parse_project_map(self, content: str) -> Dict[str, str]:
        """
        Splits the massive markdown string into a dictionary:
        { 'agent_core.py': '## 📦 Module: agent_core.py\n...' }
        """
        # Regex to split by the module header
        # Matches: ## 📦 Module: `some_name.py`
        pattern = r"(## 📦 Module: `(.*?)`)"
        
        parts = re.split(pattern, content)
        
        modules = {}
        current_name = None
        
        # re.split includes the capture groups. 
        # The list structure will be: [preamble, header_full, name_only, content, header_full, name_only, content...]
        # We skip the preamble (index 0).
        for i in range(1, len(parts), 3):
            if i + 2 < len(parts):
                header = parts[i]
                name = parts[i+1]
                body = parts[i+2]
                modules[name] = header + body
                
        return modules

    def _analyze_single_module(self, module_name: str, module_content: str) -> Optional[str]:
        """
        Sends a single module context to the LLM to check for specific quality issues.
        Returns an instruction string if a problem is found, or None.
        """
        prompt = f"""
### ROLE
You are a Code Documentation Auditor.

### INPUT
Documentation for specific module: **{module_name}**
{module_content}

### TASK
Analyze ONLY this module for specific description errors.
Ignore code snippets; focus on the English descriptions (Role, Logic, Impact).

Check for these specific flaws:
1. **Lazy Definitions**: Does it say "Does X" without saying *how*? (e.g., "Manages state" vs "Manages state using a stack").
2. **Missing Constants**: If it lists specific ALL_CAPS configuration variables in logic, are they described in the Interface section?
3. **Vague Dependencies**: Does "Impact Analysis" list files that aren't mentioned in "Used By" or imports?

### OUTPUT
If the documentation is acceptable, return valid JSON: {{"audit_result": "PASS"}}
If there is a flaw, return valid JSON with a **single, specific instruction** to fix it.

Example Fail: {{"audit_result": "Explicitly describe the data structure used for 'memory state'."}}
Example Pass: {{"audit_result": "PASS"}}
"""
        
        # We define a custom schema for the gatekeeper to extract just the instruction or status
        # Since gatekeeper extracts a specific field, we ask for "audit_result".
        
        result = self.gatekeeper.execute_with_feedback(
            prompt,
            json_key="audit_result",
            forbidden_terms=[], # We want the critic to be able to use any technical term necessary
            verification_source=module_content,
            log_context=f"MapCritic:{module_name}"
        )

        # Clean the result
        if not result or not isinstance(result, str):
            return None
            
        if "PASS" in result.upper() and len(result) < 10:
            return None
            
        return result