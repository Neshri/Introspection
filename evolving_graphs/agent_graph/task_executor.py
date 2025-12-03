import ast
import json
import re
from typing import Optional, Any
from .semantic_gatekeeper import SemanticGatekeeper

class TaskExecutor:
    """
    Implements the 'Plan-and-Solve' pattern.
    VERIFIES high-level goals against ACTUAL code snippets to prevent hallucination.
    """
    def __init__(self, gatekeeper: SemanticGatekeeper):
        self.gatekeeper = gatekeeper

    def _clean_and_parse(self, gatekeeper_response: str) -> Any:
        """
        Utilities to handle SemanticGatekeeper's specific return format:
        1. Strips '(⚠️ ...)' and '(Unverified)' suffixes.
        2. Parses the remaining string (which might be a Python dict/list string).
        """
        if not gatekeeper_response: 
            return None
            
        # 1. Strip the Gatekeeper's confidence notes
        clean_text = re.sub(r'\s*\(⚠️.*?\)$', '', gatekeeper_response, flags=re.DOTALL)
        clean_text = clean_text.replace("(Unverified) ", "").strip()

        # 2. Parse. Expect JSON, fall back to Python literals.
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            try:
                return ast.literal_eval(clean_text)
            except Exception:
                return clean_text

    def solve_complex_task(self, main_goal: str, context_data: str, log_label: str) -> Optional[str]:
        # --- PHASE 1: THE PLANNER ---
        plan_prompt = f"""
        Goal: {main_goal}
        
        Context:
        \"\"\"
        {context_data}
        \"\"\"
        
        Task: Break this goal into 2-3 distinct, factual sub-questions.
        
        Constraints:
        1. Do NOT use marketing buzzwords (e.g. "facilitate", "streamline", "robust", "seamless").
        2. Questions must be technical and specific to the code.
        
        Output Format:
        Return valid JSON with a single key "plan". The value must be a list of strings.
        Example: {{ "plan": ["How is the class instantiated?", "What arguments are passed?"] }}
        """
        
        raw_plan = self.gatekeeper.execute_with_feedback(
            plan_prompt, "plan", verification_source=None, log_context=f"{log_label}:Plan"
        )
        
        parsed_plan = self._clean_and_parse(raw_plan)
        
        if isinstance(parsed_plan, dict):
            sub_questions = parsed_plan.get("plan", [])
        elif isinstance(parsed_plan, list):
            sub_questions = parsed_plan
        else:
            sub_questions = [str(raw_plan)]
            
        if not isinstance(sub_questions, list):
            sub_questions = [str(sub_questions)]

        # --- PHASE 2: THE EXECUTOR ---
        findings = []
        valid_evidence_found = False

        for i, question in enumerate(sub_questions):
            # UPDATED PROMPT: Request Python Dict format (Single Quotes) to avoid JSON escaping issues
            execution_prompt = f"""
            Context:
            \"\"\"
            {context_data}
            \"\"\"
            
            Question: {question}
            
            Task: Answer the question AND classify the evidence type.
            
            Constraints:
            1. Return a valid JSON object with key "result".
            2. The "result" object must contain "answer_text" and "status".
            3. CRITICAL: Use SINGLE QUOTES for the 'answer_text' value to avoid escaping issues (e.g. 'Code calls "foo"').
            
            Classifications:
            - ACTIVE: Logic execution, calls, instantiation.
            - PASSIVE: Imports, type hints, constants.
            - NONE: No evidence found.
            
            Return JSON: 
            {{ 
                "result": {{
                    "answer_text": 'Code calls "self.run()"',
                    "status": "ACTIVE"
                }} 
            }}
            """
            
            # Request "result" key specifically
            raw_response = self.gatekeeper.execute_with_feedback(
                execution_prompt, 
                "result", 
                verification_source=context_data, 
                log_context=f"{log_label}:Step{i+1}"
            )
            
            data = self._clean_and_parse(raw_response)
            
            # Defaults
            answer_text = "No detail provided."
            status = "NONE"
            
            # Robust Parsing Logic
            if isinstance(data, dict):
                # Check if we got the nested 'result' key despite asking Gatekeeper to extract it
                # (Gatekeeper sometimes returns the whole object key included)
                target = data.get("result", data)
                if isinstance(target, dict):
                     answer_text = target.get("answer_text", str(target))
                     status = target.get("status", "NONE").upper()
                else:
                     answer_text = str(target)
            elif isinstance(data, str):
                answer_text = data
                # Last resort heuristic
                if "import" in answer_text.lower(): status = "PASSIVE"
                elif "no evidence" not in answer_text.lower(): status = "ACTIVE"

            # Clean leakage: If answer_text is a string representation of a dict, clean it.
            if isinstance(answer_text, str) and answer_text.strip().startswith("{"):
                 try:
                     # Try to re-parse deeply nested stringified JSON
                     inner = self._clean_and_parse(answer_text)
                     if isinstance(inner, dict):
                         answer_text = inner.get("answer_text", str(inner))
                 except:
                     pass

            findings.append(f"Q: {question}\nA: {answer_text} [Status: {status}]")
            
            if status == "ACTIVE":
                valid_evidence_found = True

        # --- PHASE 3: THE SYNTHESIZER ---
        
        if not valid_evidence_found:
            return None

        findings_block = "\n".join(findings)
        
        final_prompt = f"""
        Goal: {main_goal}
        
        Context:
        \"\"\"
        {context_data}
        \"\"\"
        
        Verified Findings:
        {findings_block}
        
        Task: Synthesize these findings into a concise, accurate Intent description.
        
        Constraints:
        1. Start strictly with a specific ACTION VERB.
        2. Do NOT use generic verbs like "Uses", "Imports".
        3. The result must be a SINGLE string.
        
        Return JSON: {{ "result": "Configures the timeout settings." }}
        """
        
        # CHANGED: verification_source should be context_data (Source Code), not findings_block.
        # Validating against findings is circular. Validating against code is grounding.
        # Removed "imports" from forbidden_terms to allow valid noun usage
        result_raw = self.gatekeeper.execute_with_feedback(
            final_prompt, 
            "result", 
            forbidden_terms=["uses", "utilizes", "leverages"], 
            verification_source=context_data, 
            log_context=f"{log_label}:Synthesis"
        )

        final_intent = self._clean_and_parse(result_raw)
        
        # Unwrap if dict
        if isinstance(final_intent, dict):
            # Try likely keys
            final_intent = final_intent.get("result", final_intent.get("intent", str(final_intent)))

        if isinstance(final_intent, (list, set, tuple)):
             return ", ".join(str(x) for x in final_intent)
             
        return str(final_intent) if final_intent else None