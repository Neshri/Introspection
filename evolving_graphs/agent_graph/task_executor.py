import ast
import json
import re
import logging
from typing import Optional, Any
from .semantic_gatekeeper import SemanticGatekeeper

class TaskExecutor:
    """
    Implements the 'Plan-Solve-Refine' pattern.
    STRICT COMPLIANCE: No context truncation allowed.
    Uses structured prompts ("The Sandwich Method") to reduce 3B model confusion.
    """
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def _clean_and_parse(self, gatekeeper_response: str) -> Any:
        if not gatekeeper_response: return None
        clean_text = re.sub(r'\s*\(⚠️.*?\)$', '', gatekeeper_response, flags=re.DOTALL)
        clean_text = clean_text.replace("(Unverified) ", "").strip()
        
        # 3B Model specific fix: Remove unescaped newlines inside strings if possible
        # or just strip strictly for common json wrapping
        clean_text = clean_text.strip('`').strip()
        if clean_text.startswith("json"): clean_text = clean_text[4:].strip()
        
        # Basic cleanup for common failures
        try:
             # Strict JSON Load
            return json.loads(clean_text, strict=False)
        except:
             pass

        if clean_text.startswith("[") and clean_text.endswith("]"):
            try:
                return ast.literal_eval(clean_text)
            except:
                pass

        try:
            return json.loads(clean_text)
        except:
            try:
                # Fallback to loose eval
                return ast.literal_eval(clean_text)
            except:
                # LAST RESORT: Flatten newlines. 
                # 3B model often puts literal \n in strings which breaks json.loads.
                # Since newlines are whitespace in JSON structure, flattening normally works 
                # unless the content strictly needs multiline (which our task doesn't).
                flat_text = clean_text.replace('\n', ' ').replace('\r', '')
                try:
                    return json.loads(flat_text)
                except:
                    try:
                        return ast.literal_eval(flat_text)
                    except:
                        return clean_text

    def _unwrap_text(self, data: Any) -> str:
        """
        Recursively extracts the first meaningful string from a dict/list wrapper.
        """
        if isinstance(data, str):
            clean = data.strip()
            if clean.startswith("{"):
                # Try interpreting string as a dict (JSON or Python Literal)
                try:
                    inner = json.loads(clean, strict=False)
                    if isinstance(inner, dict):
                        return self._unwrap_text(inner)
                except:
                    pass
                
                try:
                    inner = ast.literal_eval(clean)
                    if isinstance(inner, dict):
                        return self._unwrap_text(inner)
                except:
                    pass
            return data
            
        if isinstance(data, dict):
            for key in ["result", "description", "role", "answer", "answer_text", "sentence"]:
                if key in data:
                    return self._unwrap_text(data[key])
            for v in data.values():
                if isinstance(v, str):
                    return self._unwrap_text(v)
            return " ".join(str(v) for v in data.values())
            
        if isinstance(data, (list, tuple, set)):
            return " ".join(self._unwrap_text(x) for x in data)
            
        return str(data)

    def _refine_synthesis(self, draft_text: str, context_data: str, log_label: str) -> str:
        clean_draft = self._unwrap_text(draft_text)
        logging.info(f"[{log_label}] Refiner triggered for: '{clean_draft}'")
        
        # IMPROVEMENT: "Polisher" Prompt, not "Rewriter"
        # We give the code context ONLY for reference, but strictly forbid adding new facts.
        refine_prompt = f"""
        ### CODE CONTEXT (For Reference Only)
        \"\"\"
        {context_data}
        \"\"\"

        ### GOAL
        Format the Input Text into a single, cohesive sentence.

        ### INPUT TEXT
        "{clean_draft}"

        ### INSTRUCTIONS
        1. Combine the input statements into one smooth sentence.
        2. Fix "Lazy Lists" (e.g. "Uses A, B, C" -> "Uses A and B to support C").
        3. Do NOT add new information not present in the Input Text.
        4. Do NOT use marketing adjectives.

        ### OUTPUT FORMAT
        Return a single JSON object (no nesting): {{ "result": "The formatted sentence." }}
        """
        
        raw_refined = self.gatekeeper.execute_with_feedback(
            refine_prompt, "result", forbidden_terms=["comprehensive", "various", "seamless"], 
            verification_source=context_data, log_context=f"{log_label}:Refine"
        )
        
        parsed = self._clean_and_parse(raw_refined)
        return self._unwrap_text(parsed)



    def solve_complex_task(self, main_goal: str, context_data: str, log_label: str) -> Optional[str]:
        try:
            logging.info(f"[{log_label}] Starting Consensus Pipeline. Context Size: {len(context_data)} chars.")
            
            # --- PHASE 1: PROPOSER (Observation) ---
            # Role: Naive Observer. Lists everything they see.
            proposer_prompt = f"""
            ### CODE CONTEXT
            \"\"\"
            {context_data}
            \"\"\"
            
            ### TASK
            List ALL factual technical actions performed by this code (e.g. 'Calls function X', 'Instantiates class Y', 'Updates attribute Z').
            
            ### RULES
            1. Return a simple bulleted list.
            2. Do NOT infer intent. Just state the action.
            3. If the code is passive, say "No active logic."
            
            ### OUTPUT FORMAT
            Plain text list.
            """
            
            raw_proposal = self.gatekeeper.execute_with_feedback(
                proposer_prompt, "result", verification_source=None, log_context=f"{log_label}:Proposer", expect_json=False
            )
            
            # --- PHASE 2: CRITIC (Review) ---
            # Role: Skeptic. Finds mistakes in the proposal.
            critic_prompt = f"""
            ### CODE CONTEXT
            \"\"\"
            {context_data}
            \"\"\"
            
            ### PROPOSAL
            {raw_proposal}
            
            ### TASK
            Review the Proposal against the Code Context.
            
            ### CHECKLIST
            1. Hallucinations: Is there an action listed that is NOT in the code?
            2. Misinterpretations: Did it say "Instantiates" when it only "Types"?
            3. Omissions: Did it miss a key function call?
            
            ### OUTPUT FORMAT
            List the ERRORS found. If the proposal is perfect, say "No errors."
            """
            
            critique = self.gatekeeper.execute_with_feedback(
                critic_prompt, "result", verification_source=None, log_context=f"{log_label}:Critic", expect_json=False
            )
            
            # --- PHASE 3: JUDGE (Decision) ---
            # Role: Authority. Decides the final facts.
            judge_prompt = f"""
            ### PROPOSAL
            {raw_proposal}
            
            ### CRITIQUE
            {critique}
            
            ### CODE CONTEXT
            \"\"\"
            {context_data}
            \"\"\"
            
            ### TASK
            Based on the Proposal and Critique, generate the FINAL LIST of verified facts.
            - Exclude hallucinated items.
            - Write in plain text (bullet points).
            - NO JSON.
            
            ### OUTPUT FORMAT
            Plain text list.
            """
            
            approved_facts = self.gatekeeper.execute_with_feedback(
                judge_prompt, "result", verification_source=context_data, log_context=f"{log_label}:Judge", expect_json=False
            )
            
            # Fix: The 3B model sometimes outputs JSON even when asked for a list.
            # We must normalize this to text before passing it to the Synthesizer,
            # otherwise the Synthesizer sees JSON in the prompt and gets confused (causing Format Fails).
            if approved_facts and approved_facts.strip().startswith("{"):
                try:
                    parsed = json.loads(approved_facts)
                    if isinstance(parsed, dict):
                        # Extract the first list we find
                        for val in parsed.values():
                            if isinstance(val, list):
                                approved_facts = "\\n".join([f"- {x}" for x in val])
                                break
                except:
                    pass # Keep original text if parse fails
            
            if "No active logic" in approved_facts or not approved_facts.strip():
                return "Defines data structures or configuration."

            # --- PHASE 4: SYNTHESIS (Final Output) ---
            # Role: Scribe. Formats the result.
            synthesis_prompt = f"""
            ### APPROVED FACTS
            {approved_facts}
            
            ### GOAL
            {main_goal}
            
            ### INSTRUCTIONS
            Write a single sentence summary based on the facts above.
            Start with a verb.
            Do not use marketing words.
            
            ### OUTPUT
            Return JSON: {{ "result": "The summary string." }}
            """
            
            result_raw = self.gatekeeper.execute_with_feedback(
                synthesis_prompt, "result", forbidden_terms=["uses", "utilizes", "leverages", "comprehensive"], 
                verification_source=context_data, log_context=f"{log_label}:Synthesize"
            )

            final_intent = self._clean_and_parse(result_raw)
            unwrapped = self._unwrap_text(final_intent)

            # Safety Guard: If the result looks like a raw JSON list of facts (from Proposer phase leakage), 
            # force a fallback summary.
            if isinstance(unwrapped, str) and (unwrapped.startswith('[{"fact":') or "{\"fact\":" in unwrapped):
                logging.warning(f"[{log_label}] Leaked JSON detected in synthesis. Fallback triggered.")
                return "Performs logic as defined in the source code."

            return unwrapped

        except Exception as e:
            logging.error(f"[{log_label}] CRASH in TaskExecutor: {e}", exc_info=True)
            return "Analysis failed due to internal error."