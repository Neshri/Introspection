import ast
import json
import re
import logging
from typing import Optional, Any
from .semantic_gatekeeper import SemanticGatekeeper

class TaskExecutor:
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper
        self.max_retries = 3

    def _clean_and_parse(self, response: str, log_context: str = "Parse") -> Any:
        if not response: return None
        # Forensic logging
        logging.info(f"[{log_context}] [RAW_RESPONSE]:\n{response}")
        
        clean = re.sub(r'\s*\(⚠️.*?\)$', '', response, flags=re.DOTALL)
        clean = clean.replace("(Unverified) ", "").strip()
        clean = clean.strip("`'\"")
        
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[1] if "\n" in clean else clean
            if clean.endswith("```"): clean = clean[:-3]
        
        if clean.startswith("json"): clean = clean[4:].strip()

        try: return json.loads(clean, strict=False)
        except: pass
        try: return ast.literal_eval(clean)
        except: pass
        try: return json.loads(clean.replace('\n', ' '))
        except: return clean

    def _unwrap_text(self, data: Any) -> str:
        if isinstance(data, str): return data.strip()
        if isinstance(data, dict):
            for k in ["answer", "critique", "feedback", "result"]:
                if k in data: return self._unwrap_text(data[k])
            return " ".join(str(v) for v in data.values())
        return str(data)

    def solve_complex_task(self, main_goal: str, context_data: str, log_label: str) -> Optional[str]:
        try:
            logging.info(f"[{log_label}] STARTING TASK. Goal: {main_goal}")
            return self._run_goal_loop(main_goal, context_data, log_label)
        except Exception as e:
            logging.error(f"[{log_label}] CRASH: {e}", exc_info=True)
            return "Analysis failed."

    def _run_goal_loop(self, goal: str, context_data: str, log_label: str) -> str:
        feedback = ""
        current_answer = ""
        
        # Recency Bias Fix: Reference Top, Target Bottom
        if "### TARGET CODE" not in context_data:
            context_block = f"### TARGET CODE\n{context_data}"
        else:
            context_block = context_data

        for attempt in range(1, self.max_retries + 1):
            iteration_label = f"{log_label}:Iter{attempt}"
            
            # --- 1. DRAFTER PHASE ---
            if feedback:
                instruction_block = f"""
                <critical_instruction>
                PREVIOUS ATTEMPT REJECTED: {feedback}
                You MUST fix this specific error in your new answer.
                </critical_instruction>
                """
            else:
                instruction_block = "Analyze the code above."

            drafter_prompt = f"""
            You are a Technical Documentation Expert.
            
            {context_block}
            
            ### TASK
            Goal: {goal}
            
            {instruction_block}
            
            ### RESPONSE REQUIREMENTS
            1. Be concise and factual.
            2. Ignore guard clauses (do not describe logic that is skipped/unreachable).
            3. Return VALID JSON.
            
            ### EXAMPLE OUTPUT
            {{ "answer": "The function calculates X using Y." }}
            
            ### YOUR RESPONSE
            """
            
            logging.info(f"[{iteration_label}] [DRAFTER_PROMPT_SENT]")
            current_answer_raw = self.gatekeeper.execute_with_feedback(
                drafter_prompt, "answer", verification_source=None, log_context=f"{iteration_label}:Drafter", expect_json=True
            )
            
            parsed = self._clean_and_parse(current_answer_raw, log_context=f"{iteration_label}:Drafter")
            current_answer = self._unwrap_text(parsed)

            # --- 2. CRITIC PHASE ---
            # Improvement: Goal is center stage, Checklist is robust.
            critic_prompt = f"""
            You are a Code Auditor.
            
            {context_block}

            ### THE GOAL (Question asked)
            "{goal}"

            ### PROPOSED ANSWER (To Verify)
            "{current_answer}"

            ### AUDIT CHECKLIST
            1. **Responsiveness:** Does the Answer actually address the GOAL? (If asked for 'inputs', does it list inputs?)
            2. **Truthfulness:** Is every claim in the Answer supported by the code?
            3. **Completeness:** Did the Answer miss a critical side-effect (e.g. raising an exception, modifying a global)?
            4. **Guard Clauses:** Does the Answer claim logic happens that is actually inside a dead `if` block?

            ### OUTPUT FORMAT
            Return a JSON object.
            
            If Valid (Accurate AND Responsive):
            {{ "critique": "VERIFIED_PASS" }}
            
            If Invalid:
            {{ "critique": "FAIL", "feedback": "Explain specifically why it failed the checklist." }}
            """
            
            logging.info(f"[{iteration_label}] [CRITIC_PROMPT_SENT]")
            critique_raw = self.gatekeeper.execute_with_feedback(
                critic_prompt, "critique", verification_source=None, log_context=f"{iteration_label}:Critic", expect_json=True
            )
            
            critique_data = self._clean_and_parse(critique_raw, log_context=f"{iteration_label}:Critic")
            
            # --- 3. STATUS LOGIC ---
            status = "FAIL"
            feedback_msg = "Unknown Logic Error"
            
            raw_upper = str(critique_raw).upper()
            parsed_upper = str(critique_data).upper()
            success_markers = ["VERIFIED_PASS", "PASS", "VALID", "NO ERROR", "CORRECT"]

            if isinstance(critique_data, dict):
                val = str(critique_data.get("critique", "FAIL")).upper()
                if any(m in val for m in success_markers):
                    status = "PASS"
                else:
                    feedback_msg = critique_data.get("feedback", val)
            
            elif any(m in parsed_upper for m in success_markers):
                status = "PASS"
            elif any(m in raw_upper for m in success_markers):
                status = "PASS"

            if status == "PASS":
                logging.info(f"[{log_label}] Converged on Iteration {attempt}.")
                return current_answer
            else:
                logging.warning(f"[{log_label}] Iteration {attempt} Failed. Feedback: {feedback_msg}")
                feedback = feedback_msg
        
        logging.warning(f"[{log_label}] Loop Exhausted. Returning best effort.")
        return current_answer