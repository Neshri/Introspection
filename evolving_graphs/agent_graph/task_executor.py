import ast
import json
import re
import logging
from typing import Optional, Any, Tuple
from .semantic_gatekeeper import SemanticGatekeeper

class TaskExecutor:
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper
        self.max_retries = 5

    def _clean_and_parse(self, response: str, log_context: str = "Parse") -> Any:
        if not response: return None
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
            for k in ["answer", "result", "summary", "description", "text"]:
                if k in data and isinstance(data[k], str):
                    return data[k].strip()
            string_values = [str(v).strip() for v in data.values() if isinstance(v, str)]
            if string_values: return " ".join(string_values)
            return "\n".join([self._unwrap_text(v) for v in data.values()])
        if isinstance(data, list):
            return "\n".join([f"- {self._unwrap_text(x)}" for x in data])
        return str(data)

    def _verify_grounding_hard(self, answer: str, source_code: str) -> Optional[str]:
        claimed_entities = re.findall(r'`([^`]+)`', answer)
        if not claimed_entities: return None

        missing_entities = []
        for entity in claimed_entities:
            clean_entity = entity.replace("()", "").strip()
            if not clean_entity: continue

            if re.search(r'[\\#\*\?\[\]\(\)\{\}]', clean_entity):
                continue

            if re.match(r'^\w+$', clean_entity):
                pattern = r'\b' + re.escape(clean_entity) + r'\b'
                if not re.search(pattern, source_code):
                    missing_entities.append(entity)
            else:
                if clean_entity not in source_code:
                    missing_entities.append(entity)

        if missing_entities:
            return f"GUARDRAIL FAILURE: You cited {missing_entities}, but these identifiers do not exist in the source code."
        return None

    def _heuristic_audit(self, answer: str) -> Optional[str]:
        """
        DETERMINISTIC FILTER:
        Catches known prompt leaks and meta-commentary that LLMs often miss.
        """
        lower_ans = answer.lower()
        
        # 1. Prompt Leakage (The "Without Repeating" bug)
        # These are phrases common in system prompts but rare in actual documentation
        leaks = [
            "without repeating",
            "repeating the instruction",
            "ignoring guard clauses",
            "return valid json",
            "concise and factual",
            "as an ai language model",
            "do not mention",
            "following the instructions"
        ]
        for leak in leaks:
            if leak in lower_ans:
                return f"FAIL: Instruction Leak detected. You included the prompt phrase '{leak}' in the output."

        # 2. Meta-Description (The "Describes this class" bug)
        # We want functional descriptions, not structural ones.
        if "describes this class" in lower_ans or "describes the method" in lower_ans:
            return "FAIL: Meta-commentary detected. Do not say what the code *describes*; say what the code *does* (e.g., 'Calculates...', 'Initializes...')."

        return None

    def _audit_relevance(self, goal: str, answer: str, context_data: str, log_label: str) -> Tuple[str, str]:
        # --- 0. HEURISTIC CHECK (Fast & Strict) ---
        heuristic_error = self._heuristic_audit(answer)
        if heuristic_error:
            return "FAIL", heuristic_error

        # --- 1. LLM CHECK (Nuance) ---
        prompt = f"""
        You are a Quality Control Supervisor.
        
        CONTEXT (CODE):
        {context_data}
        
        GOAL: "{goal}"
        PROPOSED ANSWER: "{answer}"
        
        TASK: Determine if the PROPOSED ANSWER is acceptable.
        
        FAIL CONDITIONS:
        1. **Irrelevant:** Does not answer the GOAL based on the CONTEXT.
        2. **Meta-Commentary:** Says "The method describes..." instead of "The method calculates...".
        3. **Vague:** Uses generic words ("manages", "handles") without naming specific code elements.
        
        OUTPUT FORMAT:
        Return JSON.
        {{ "status": "PASS" }}
        OR
        {{ "status": "VAGUE", "reason": "Answer is too generic." }}
        OR
        {{ "status": "FAIL", "reason": "Explanation." }}
        """
        
        raw = self.gatekeeper.execute_with_feedback(
            prompt, "status", verification_source=None, log_context=f"{log_label}:Audit:Relevance", expect_json=True
        )
        data = self._clean_and_parse(raw, log_context=f"{log_label}:Audit:Relevance")
        
        status = "FAIL"
        reason = "Unknown error"
        
        if isinstance(data, dict):
            status = str(data.get("status", "FAIL")).upper()
            reason = data.get("reason", "Relevance check failed.")
        elif isinstance(data, str):
            clean_str = data.strip().upper()
            if "PASS" in clean_str:
                status = "PASS"
                reason = "Verified (String fallback)"
            elif "VAGUE" in clean_str:
                status = "VAGUE"
                reason = "Vague (String fallback)"
            else:
                status = "FAIL"
                reason = f"Invalid output format. Received: {clean_str}"
        elif data is None:
            status = "FAIL"
            reason = "Empty response from model."
        
        return status, reason

    def _audit_accuracy(self, answer: str, context_data: str, log_label: str) -> Tuple[str, str]:
        prompt = f"""
        You are a Code Auditor.
        
        SOURCE CODE:
        {context_data}
        
        CLAIM: "{answer}"
        
        TASK: Verify strictly against the SOURCE CODE.
        1. Are the described logic/variables actually present?
        2. Did it hallucinate functionality?
        
        Return JSON: {{ "status": "PASS" }} or {{ "status": "FAIL", "reason": "Correction needed." }}
        """
        
        raw = self.gatekeeper.execute_with_feedback(
            prompt, "status", verification_source=None, log_context=f"{log_label}:Audit:Accuracy", expect_json=True
        )
        data = self._clean_and_parse(raw, log_context=f"{log_label}:Audit:Accuracy")
        
        status = "FAIL"
        reason = "Fact verification failed."

        if isinstance(data, dict):
            status = str(data.get("status", "FAIL")).upper()
            reason = data.get("reason", "Fact verification failed.")
        elif isinstance(data, str):
            clean_str = data.strip().upper()
            if "PASS" in clean_str:
                status = "PASS"
                reason = "Verified (String fallback)"
            else:
                status = "FAIL"
                reason = f"Invalid output format. Received: {clean_str}"
        elif data is None:
            status = "FAIL"
            reason = "Empty response from model."
        
        if "FAIL" in status:
            return "FAIL", reason
            
        return "PASS", "Verified"

    def _refine_vague_answer(self, current_answer: str, context_data: str, log_label: str) -> str:
        logging.info(f"[{log_label}] Triggering VAGUE refinement.")
        
        evidence_prompt = f"""
        You wrote: "{current_answer}"
        
        This is too vague. Look at the SOURCE CODE.
        Identify the SPECIFIC function name, class, or variable that performs this action.
        
        SOURCE CODE:
        {context_data}
        
        Return JSON: {{ "evidence": "name_of_function_or_variable" }}
        """
        
        ev_raw = self.gatekeeper.execute_with_feedback(
            evidence_prompt, "evidence", verification_source=None, log_context=f"{log_label}:Refine:Evidence", expect_json=True
        )
        
        ev_data = self._clean_and_parse(ev_raw)
        evidence = ""
        if isinstance(ev_data, dict):
            evidence = ev_data.get("evidence", "")
        elif isinstance(ev_data, str):
            evidence = ev_data
        
        if not evidence: return current_answer
        
        rewrite_prompt = f"""
        ORIGINAL: "{current_answer}"
        EVIDENCE: `{evidence}`
        
        Rewrite the ORIGINAL sentence to be concrete.
        You MUST explicitly mention the EVIDENCE (using backticks).
        
        Return JSON: {{ "answer": "The module uses `{evidence}` to..." }}
        """
        
        rew_raw = self.gatekeeper.execute_with_feedback(
            rewrite_prompt, "answer", verification_source=None, log_context=f"{log_label}:Refine:Rewrite", expect_json=True
        )
        parsed = self._clean_and_parse(rew_raw)
        return self._unwrap_text(parsed)

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
        
        for attempt in range(1, self.max_retries + 1):
            iteration_label = f"{log_label}:Iter{attempt}"
            
            # --- 1. DRAFTER PHASE ---
            if feedback:
                instruction_block = f"""
                <critical_instruction>
                PREVIOUS ATTEMPT REJECTED: {feedback}
                You MUST fix this specific error.
                </critical_instruction>
                """
            else:
                instruction_block = "Analyze the code above."

            drafter_prompt = f"""
            You are a Technical Documentation Expert.
            
            {context_data}
            
            ### TASK
            Goal: {goal}
            
            {instruction_block}
            
            ### REQUIREMENTS
            1. Be concise and factual.
            2. Ignore guard clauses.
            3. Use backticks for code elements (e.g., `process()`).
            4. Do NOT mention instructions in the output (e.g. "without repeating").
            5. Return VALID JSON.
            
            ### EXAMPLE OUTPUT
            {{ "answer": "The function uses `process_data` to filter input." }}
            
            ### YOUR RESPONSE
            """
            
            logging.info(f"[{iteration_label}] [DRAFTER_PROMPT_SENT]")
            current_answer_raw = self.gatekeeper.execute_with_feedback(
                drafter_prompt, "answer", verification_source=None, log_context=f"{iteration_label}:Drafter", expect_json=True
            )
            parsed = self._clean_and_parse(current_answer_raw, log_context=f"{iteration_label}:Drafter")
            current_answer = self._unwrap_text(parsed)

            # --- 2. RELEVANCE AUDIT (Includes Heuristic Check) ---
            status, reason = self._audit_relevance(goal, current_answer, context_data, iteration_label)
            
            # Special Handling for VAGUE (Marketing Fluff)
            if status == "VAGUE":
                current_answer = self._refine_vague_answer(current_answer, context_data, iteration_label)
                status, reason = self._audit_relevance(goal, current_answer, context_data, f"{iteration_label}:ReAudit")

            if status == "FAIL":
                logging.warning(f"[{log_label}] Relevance Audit Failed: {reason}")
                feedback = reason
                continue

            # --- 3. ACCURACY AUDIT ---
            status, reason = self._audit_accuracy(current_answer, context_data, iteration_label)
            
            if status == "FAIL":
                logging.warning(f"[{log_label}] Accuracy Audit Failed: {reason}")
                feedback = reason
                continue

            # --- 4. GROUNDING GUARDRAIL ---
            guard_error = self._verify_grounding_hard(current_answer, context_data)
            if guard_error:
                logging.warning(f"[{log_label}] Guardrail Tripped: {guard_error}")
                feedback = guard_error
                continue

            # Success
            logging.info(f"[{log_label}] Converged on Iteration {attempt}.")
            return current_answer
        
        logging.warning(f"[{log_label}] Loop Exhausted. Returning best effort.")
        return current_answer