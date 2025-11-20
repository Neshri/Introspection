import json
from typing import Tuple, Set, Optional, List

from .agent_config import DEFAULT_MODEL
from .llm_util import chat_llm

# --- Semantic Constraints ---

BANNED_ADJECTIVES: Set[str] = {
    "efficient", "efficiently",
    "optimal", "optimally",
    "seamless", "seamlessly",
    "robust", "robustly",
    "comprehensive", "comprehensively",
    "easy", "easily",
    "powerful", "advanced",
    "innovative", "cutting-edge",
    "streamlined",
    "facilitate"
}

class SemanticGatekeeper:
    """
    Manages LLM interactions with strict semantic enforcement.
    Acts as a firewall against 'slop', hallucinations, and format errors.
    """
    
    def execute_with_feedback(self, initial_prompt: str, json_key: str, forbidden_terms: List[str] = []) -> str:
        """
        Executes LLM with a feedback loop.
        """
        final_prompt = f"{initial_prompt}\n\nIMPORTANT: Return ONLY a valid JSON object with key '{json_key}'. Do not write explanations. Do not apologize. Just JSON."
        
        system_instruction = "System: Output valid JSON only. No Markdown."
        conversation_history = f"{system_instruction}\nUser: {final_prompt}"
        
        MAX_RETRIES = 2
        
        for attempt in range(MAX_RETRIES + 1):
            raw_response = chat_llm(DEFAULT_MODEL, conversation_history)
            
            # Debug Log
            print(f"\n[Gatekeeper Attempt {attempt}] History Len: {len(conversation_history)}")

            clean_val = self._parse_json_safe(raw_response, json_key)
            
            if clean_val:
                is_valid, critique = self._critique_content(clean_val, forbidden_terms)
                if is_valid:
                    return clean_val
                
                feedback = critique
                print(f"!! REJECTED (Content): '{clean_val}' -> {feedback}")
            else:
                feedback = f"Critique: Invalid JSON. I need a JSON object with key '{json_key}'."
                print(f"!! REJECTED (Format): '{raw_response[:100]}...'")

            conversation_history += f"\nAssistant: {raw_response}\nUser: {feedback}"
        
        print("!! FEEDBACK LOOP EXHAUSTED !!")
        return "performs specified logic"

    def _critique_content(self, text: str, forbidden_terms: List[str]) -> Tuple[bool, str]:
        text_lower = text.lower()
        
        # 1. Fluff Check
        found_words = [w for w in BANNED_ADJECTIVES if w in text_lower]
        if found_words:
            return False, f"Critique: You used marketing fluff words: {found_words}. Remove them. Be technical."
        
        # 2. Tense Check (Enforce Present Tense)
        first_word = text.split()[0].lower()
        if first_word in ["will", "shall", "must", "should", "can"]:
            return False, f"Critique: Do not use future/modal tense ('{first_word}'). Use present tense (e.g., 'calculates', 'renders')."
        if first_word == "to":
            return False, "Critique: Do not use infinitive ('to'). Use present tense (e.g., 'calculates')."

        # 3. Tautology Check
        for term in forbidden_terms:
            if term.lower() in text_lower:
                return False, f"Critique: You repeated the term '{term}'. Do not mention the subject name in the definition."

        # 4. Density Check
        words = text.split()
        if len(text) < 12 or len(words) < 2:
            return False, "Critique: Response is too vague. Use a 'Verb + Object' structure."
            
        return True, "Valid"

    def _parse_json_safe(self, raw: str, key: str) -> Optional[str]:
        try:
            if not raw: return None
            clean = raw.strip()
            
            if "```" in clean:
                lines = clean.splitlines()
                clean_lines = []
                in_block = False
                for line in lines:
                    if line.strip().startswith("```"):
                        in_block = not in_block
                        continue
                    if in_block or (not in_block and line.strip().startswith("{")):
                         clean_lines.append(line)
                if not clean_lines:
                    clean = clean.replace("```json", "").replace("```", "")
                else:
                    clean = "\n".join(clean_lines)
            
            clean = clean.strip()
            if not clean.startswith("{"): return None

            data = json.loads(clean)
            val = data.get(key, "").strip()
            
            if not val or val.lower() == key.lower(): return None
            return val
        except (json.JSONDecodeError, AttributeError):
            return None