import json
import re
import logging
from typing import Tuple, Set, Optional, List, Any

from .agent_config import DEFAULT_MODEL
from .llm_util import chat_llm

# --- Semantic Constraints ---
BANNED_ADJECTIVES: Set[str] = {
    "efficient", "efficiently", "optimal", "optimally", "seamless", "seamlessly",
    "robust", "robustly", "comprehensive", "comprehensively", "easy", "easily",
    "powerful", "advanced", "innovative", "cutting-edge", "streamlined", "facilitate"
}

class SemanticGatekeeper:
    """
    Manages LLM interactions with strict semantic enforcement.
    Updated to LOG PROMPTS on Style Failures.
    """
    
    def execute_with_feedback(self, initial_prompt: str, json_key: str, forbidden_terms: List[str] = [], verification_source: str = None, log_context: str = "General") -> str:
        final_prompt = f"{initial_prompt}\n\nIMPORTANT: Return ONLY a valid JSON object with key '{json_key}'. No Markdown. Escape all double quotes inside strings."
        
        messages = [
            {"role": "system", "content": "You are a strict technical analyst. Output valid JSON only."},
            {"role": "user", "content": final_prompt}
        ]
        
        MAX_RETRIES = 3 
        last_attempt_content = "[Analysis Failed]"
        last_warning = ""
        
        for attempt in range(MAX_RETRIES + 1):
            raw_response = chat_llm(DEFAULT_MODEL, messages)
            
            # --- PHASE 1: PARSE ---
            clean_val, json_error = self._parse_json_safe(raw_response, json_key)
            
            if clean_val is None:
                logging.warning(f"[{log_context}] [Attempt {attempt}] FORMAT FAIL.\nPROMPT: {final_prompt}\nRESPONSE: {raw_response}\nERROR: {json_error}")
                messages.append({"role": "assistant", "content": raw_response})
                messages.append({"role": "user", "content": f"System Alert: Invalid JSON format. Error: {json_error}. \nEnsure you escape double quotes inside the text (e.g. \\\"text\\\"). Return ONLY the object with key '{json_key}'."})
                continue

            last_attempt_content = clean_val 

            # --- PHASE 2: STYLE CHECK ---
            is_valid_style, style_critique = self._critique_content(clean_val, forbidden_terms)
            if not is_valid_style:
                # FIX: Log the PROMPT here so we can see why it chose those words
                logging.warning(f"[{log_context}] [Attempt {attempt}] STYLE FAIL.\nPROMPT: {final_prompt}\nRESPONSE: {raw_response}\nCRITIQUE: {style_critique}")
                messages.append({"role": "assistant", "content": raw_response})
                messages.append({"role": "user", "content": style_critique})
                continue

            # --- PHASE 3: TRUTH CHECK (The Auditor) ---
            if verification_source:
                confidence, reason = self._verify_grounding(clean_val, verification_source)
                
                if confidence < 3:
                    logging.warning(f"[{log_context}] [Attempt {attempt}] LOGIC REJECTION ({confidence}/5).\nCLAIM: {clean_val}\nREASON: {reason}")
                    last_warning = f" (⚠️ Verified as inaccurate: {reason})"
                    messages.append({"role": "assistant", "content": raw_response})
                    
                    guidance = ""
                    if "active" in reason.lower() and "passive" in reason.lower():
                        guidance = " HINT: If the code only imports the module but doesn't call its functions, explicitly state 'Passive usage only'."
                    elif "implement" in reason.lower() or "abstract" in reason.lower():
                        guidance = " HINT: If the code is an Abstract Class/Interface, describe it as 'Defining an interface'."

                    messages.append({"role": "user", "content": f"Auditor Critique: The code does NOT support that statement. \nAuditor Finding: {reason}\n\nTask: Rewrite the '{json_key}' value to be strictly accurate to the code snippet provided.{guidance}"})
                    continue

            return clean_val
        
        logging.error(f"[{log_context}] FAIL: Exhausted retries. Returning last attempt with warning.")
        return f"{last_attempt_content}{last_warning}"

    def _verify_grounding(self, claim: str, source_code: str) -> Tuple[int, str]:
        verify_prompt = f"""
        Act as a Code Auditor.
        Reference Code:
        \"\"\"
        {source_code}
        \"\"\"
        Claim to Verify: "{claim}"
        Task: Rate confidence (0-5) that the CLAIM is ACCURATE given the CODE.
        
        CRITICAL: 
        - Reject "Marketing Fluff": Claims about "business value", "insights", "efficiency", "real-time", or "user experience" are FALSE unless the code explicitly calculates them.
        - Reject "Implied Intent": Do not credit the module with the *intent* of its consumers. Only what it *actually does*.
        
        Scoring Rubric:
        5 (Accurate): Claim describes the Code perfectly (including accurately identifying passivity/abstractions).
        3 (Plausible): Claim is technically true but uses slightly flowery language.
        1 (False): Claim contradicts the Code OR contains unverifiable marketing fluff (e.g. "actionable insights").
        
        Return JSON: {{ "score": <int>, "reason": "<concise explanation>" }}
        """
        response = chat_llm(DEFAULT_MODEL, verify_prompt)
        try:
            val = self._parse_whole_json(response)
            return int(val.get("score", 3)), val.get("reason", "No reason provided")
        except:
            return 3, "Verification Error"

    def _critique_content(self, text_raw: str, forbidden_terms: List[str]) -> Tuple[bool, str]:
        text_lower = text_raw.lower()
        found_words = [w for w in BANNED_ADJECTIVES if w in text_lower]
        if found_words: return False, f"Critique: Remove marketing words: {found_words}."
        for term in forbidden_terms:
            if len(term) < 3: continue 
            if re.search(r'\b' + re.escape(term.lower()) + r'\b', text_lower):
                return False, f"Critique: Forbidden generic verb found: '{term}'. Be more specific."
        if len(text_raw) < 5: return False, "Critique: Response too short."
        return True, "Valid"

    def _extract_balanced_json(self, text: str) -> Optional[str]:
        start = text.find("{")
        if start == -1: return None
        balance = 0
        found_start = False
        for i in range(start, len(text)):
            char = text[i]
            if char == "{":
                balance += 1
                found_start = True
            elif char == "}":
                balance -= 1
            if found_start and balance == 0:
                return text[start:i+1]
        return None

    def _parse_json_safe(self, raw: str, key: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            if not raw: return None, "Empty response"
            clean = raw.strip()
            balanced_json = self._extract_balanced_json(clean)
            if balanced_json: clean = balanced_json
            else:
                if "```" in clean:
                    match = re.search(r"```(?:json)?(.*?)```", clean, re.DOTALL)
                    if match: clean = match.group(1).strip()
                if not clean.startswith("{"):
                    start = clean.find("{")
                    end = clean.rfind("}") + 1
                    if start != -1 and end != 0: clean = clean[start:end]

            try:
                data = json.loads(clean)
            except json.JSONDecodeError:
                try:
                    pattern = f'"{key}"\\s*:\\s*"(.*)"'
                    match = re.search(pattern, clean, re.DOTALL)
                    if match:
                        raw_val = match.group(1)
                        if '", "status"' in raw_val: raw_val = raw_val.split('", "status"')[0]
                        safe_val = raw_val.replace('"', "'")
                        data = {key: safe_val}
                    else:
                        raise ValueError("Regex repair failed")
                except:
                     return None, "JSON Decode Error"

            if "error" in data and len(data.keys()) == 1:
                return None, f"Model returned error object: {data['error']}"

            if key and key not in data:
                 if isinstance(data, dict) and "answer_text" in data and key == "result":
                     data = {"result": data}
                 else:
                    return None, f"Missing key '{key}'."

            val = data[key]
            if isinstance(val, (dict, list, bool, int, float)):
                return json.dumps(val), None
            return str(val).strip(), None

        except Exception as e:
            return None, str(e)

    def _parse_whole_json(self, raw: str) -> dict:
        try:
            balanced = self._extract_balanced_json(raw)
            if balanced: return json.loads(balanced)
            clean = raw.strip()
            if "```" in clean:
                match = re.search(r"```(?:json)?(.*?)```", clean, re.DOTALL)
                if match: clean = match.group(1).strip()
            start = clean.find("{")
            end = clean.rfind("}") + 1
            if start == -1: return {}
            return json.loads(clean[start:end])
        except:
            return {}