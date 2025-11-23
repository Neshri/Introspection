import json
import re
import logging
from typing import Tuple, Set, Optional, List

from .agent_config import DEFAULT_MODEL
from .llm_util import chat_llm

# --- Semantic Constraints ---

# REMOVED: "functionality", "solution" (Too restrictive for code)
BANNED_ADJECTIVES: Set[str] = {
    "efficient", "efficiently", "optimal", "optimally", "seamless", "seamlessly",
    "robust", "robustly", "comprehensive", "comprehensively", "easy", "easily",
    "powerful", "advanced", "innovative", "cutting-edge", "streamlined", "facilitate"
}

class SemanticGatekeeper:
    """
    Manages LLM interactions with strict semantic enforcement.
    """
    
    def execute_with_feedback(self, initial_prompt: str, json_key: str, forbidden_terms: List[str] = [], verification_source: str = None, log_context: str = "General") -> str:
        final_prompt = f"{initial_prompt}\n\nIMPORTANT: Return ONLY a valid JSON object with key '{json_key}'. No Markdown."
        
        conversation_history = f"System: Output valid JSON only.\nUser: {final_prompt}"
        
        MAX_RETRIES = 2
        last_attempt_content = "[Analysis Failed]"
        
        for attempt in range(MAX_RETRIES + 1):
            raw_response = chat_llm(DEFAULT_MODEL, conversation_history)
            
            # 1. Parse JSON
            clean_val = self._parse_json_safe(raw_response, json_key)
            
            if not clean_val:
                logging.warning(f"[{log_context}] [Attempt {attempt}] FORMAT FAIL: {raw_response[:50]}...")
                conversation_history += f"\nAssistant: {raw_response}\nUser: Critique: Invalid JSON. Return strictly JSON with key '{json_key}'."
                continue

            last_attempt_content = clean_val # Save for fallback

            # 2. Check Style (The "Editor")
            is_valid_style, style_critique = self._critique_content(clean_val, forbidden_terms)
            if not is_valid_style:
                logging.warning(f"[{log_context}] [Attempt {attempt}] STYLE FAIL: '{clean_val}' -> {style_critique}")
                conversation_history += f"\nAssistant: {raw_response}\nUser: {style_critique}"
                continue

            # 3. Check Grounding (The "Auditor")
            if verification_source:
                confidence, reason = self._verify_grounding(clean_val, verification_source)
                
                if confidence == 0:
                    logging.warning(f"[{log_context}] [Attempt {attempt}] TRUTH FAIL (0/5): '{clean_val}' -> {reason}")
                    conversation_history += f"\nAssistant: {raw_response}\nUser: Critique: Factually unsupported. {reason}"
                    continue
                
                if confidence < 3:
                    logging.info(f"[{log_context}] [Attempt {attempt}] LOW CONFIDENCE ({confidence}/5): '{clean_val}' -> {reason}")
                    return f"{clean_val} (⚠️ {reason})"

            return clean_val
        
        logging.error(f"[{log_context}] FAIL: Exhausted retries. Returning last attempt.")
        return f"(Unverified) {last_attempt_content}"

    def _verify_grounding(self, claim: str, source_code: str) -> Tuple[int, str]:
        # ... (Keep existing logic)
        context_window = source_code[:2500]
        verify_prompt = f"""
        Act as a Code Auditor.
        Reference Code:
        ```python
        {context_window}
        ```
        Claim: "{claim}"
        Task: Rate confidence (0-5) that the Code supports the Claim.
        Return JSON: {{ "score": int, "reason": "short explanation" }}
        """
        response = chat_llm(DEFAULT_MODEL, verify_prompt)
        try:
            val = self._parse_whole_json(response)
            score = int(val.get("score", 3))
            reason = val.get("reason", "No reason provided")
            return score, reason
        except:
            return 3, "Verification Error"

    def _critique_content(self, text: str, forbidden_terms: List[str]) -> Tuple[bool, str]:
        text_lower = text.lower()
        
        # 1. Fluff Check
        found_words = [w for w in BANNED_ADJECTIVES if w in text_lower]
        if found_words:
            return False, f"Critique: Remove marketing words: {found_words}. Use technical terms."
        
        # 2. Tautology Check
        for term in forbidden_terms:
            if len(term) < 3: continue 
            pattern = r'\b' + re.escape(term.lower()) + r'\b'
            if re.search(pattern, text_lower):
                return False, f"Critique: Do not use the word '{term}' in the definition."

        # 3. Density Check (RELAXED)
        # Allow 2 words if it's technically dense (e.g. "Parses arguments")
        if len(text.split()) < 2:
            return False, "Critique: Too short. Explain the mechanism (Verb + Object)."
            
        return True, "Valid"

    def _parse_json_safe(self, raw: str, key: str) -> Optional[str]:
        try:
            if not raw: return None
            clean = raw.strip()
            if "```" in clean:
                clean = clean.split("```")[1].replace("json", "")
            start = clean.find("{")
            end = clean.rfind("}") + 1
            if start == -1: return None
            clean = clean[start:end]
            data = json.loads(clean)
            val = data.get(key, "")
            if isinstance(val, str): return val.strip()
            return str(val)
        except:
            return None

    def _parse_whole_json(self, raw: str) -> dict:
        try:
            clean = raw.strip()
            if "```" in clean:
                clean = clean.split("```")[1].replace("json", "")
            start = clean.find("{")
            end = clean.rfind("}") + 1
            if start == -1: return {}
            return json.loads(clean[start:end])
        except:
            return {}