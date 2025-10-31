import ollama
import sys
import ast
import re

# --- CONFIGURATION and PROBLEM DESCRIPTION ---
MODEL = 'gemma3:12b-it-qat' 
MAX_REFINEMENT_LOOPS = 5
problem_description = """
Write a Python function called `process_glimmer_string` that takes a string of
digits (e.g., "314159") and applies a one-step "Glimmer" transformation to it.

The function must return a new string of digits of the same length.

The transformation of each digit is determined by two arbitrary rules based on
the **index** of the digit in the string:

1.  **"Growth" Rule (for Prime Indices):** If a digit is at a **prime index** (2, 3, 5, 7, etc.),
    its new value is `(current_digit + value_of_left_neighbor) % 10`.

2.  **"Decay" Rule (for Non-Prime Indices):** If a digit is at a **non-prime index** (0, 1, 4, 6, etc.),
    its new value is `(current_digit - value_of_right_neighbor + 10) % 10`.

There are two critical constraints:

-   **Simultaneous Update:** The calculation for every new digit in the output string must be
    based on the digits in the **original, unmodified input string**.

-   **Boundary Condition:** For the digit at index 0 (which has no left neighbor) and the
    digit at the last index (which has no right neighbor), the "missing" neighbor's
    value is considered to be **0**.

Example of a full transformation:
- Input String: "1428"
- Expected Output String: "7260"
"""

def clean_code(response_content: str) -> str:
    start_fence = "```python"
    start_index = response_content.find(start_fence)
    if start_index == -1: start_fence = "```"; start_index = response_content.find(start_fence)
    if start_index != -1:
        code_start_index = response_content.find('\n', start_index) + 1
        if code_start_index == 0: code_start_index = start_index + len(start_fence)
        end_index = response_content.find("```", code_start_index)
        if end_index != -1: return response_content[code_start_index:end_index].strip()
    return response_content.strip()

def run_ollama_loop():
    """
    Implements a robust Architect -> Coder -> Auditor loop.
    """
    print(f"Using model: {MODEL}")
    print(f"Problem: {problem_description.strip()}")

    # --- STEP 1: THE ARCHITECT (Create the Plan) ---
    print("\n--- STEP 1: The Architect is creating a plan... ---")
    architect_prompt = f"""
    You are a meticulous software architect. Read the problem description and create a detailed, step-by-step pseudocode plan for the solution.
    The plan must explicitly handle all rules, constraints, and boundary conditions.

    Problem Description:
    {problem_description}
    """
    try:
        architect_response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': architect_prompt}])
        pseudocode_plan = architect_response['message']['content']
        print("ARCHITECT'S PLAN:\n" + pseudocode_plan)
    except ollama.ResponseError as e:
        print(f"Error communicating with Ollama: {e}", file=sys.stderr); sys.exit(1)

    # --- STEP 2: THE CODER (Initial Implementation) ---
    print("\n--- STEP 2: The Coder is implementing the plan... ---")
    coder_prompt = f"""
    You are a Python programmer. Your only job is to translate the following pseudocode plan into a working Python function.
    Adhere to the plan as closely as possible.

    Architect's Plan:
    {pseudocode_plan}
    """
    coder_response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': coder_prompt}])
    current_code = clean_code(coder_response['message']['content'])
    print("INITIAL CODE:\n" + current_code)

    # --- STEP 3: REFINEMENT LOOP ---
    for i in range(MAX_REFINEMENT_LOOPS):
        print(f"\n--- LOOP {i+1}/{MAX_REFINEMENT_LOOPS}: AUDIT AND REFINE ---")

        # --- STEP A: THE AUDITOR (Verify Implementation) ---
        print("\n--- Step A: The Auditor is verifying the code against the plan... ---")
        auditor_prompt = f"""
        You are a hyper-literal code auditor. Your only job is to verify if the Coder's Python code faithfully implements every step of the Architect's Plan.
        
        If the code is a perfect, line-for-line implementation of the plan, you MUST respond with the single word: PASS
        
        Otherwise, point out the *first specific step* in the plan that the code violates and explain the discrepancy.

        Architect's Plan:
        {pseudocode_plan}

        Coder's Code:
        ```python
        {current_code}
        ```
        """
        auditor_response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': auditor_prompt}])
        critique = auditor_response['message']['content']
        print(f"AUDITOR'S REPORT:\n{critique}")

        if critique.strip().upper() == "PASS":
            print("\n--- The Auditor has approved the implementation. Halting. ---")
            break
        
        # --- STEP B: THE CODER (Refinement) ---
        print("\n--- Step B: The Coder is fixing the implementation... ---")
        debug_prompt = f"""
        You are the Coder. The Auditor has found a discrepancy between your code and the Architect's Plan.
        Analyze their report and fix the bug to align your code with the plan. Provide the complete, corrected code.

        Auditor's Report:
        {critique}

        The plan you must follow:
        {pseudocode_plan}

        Your code with the bug:
        ```python
        {current_code}
        ```
        """
        debug_response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': debug_prompt}])
        current_code = clean_code(debug_response['message']['content'])
        print("REFINED CODE:\n" + current_code)

    # --- 4. FINAL RESULT ---
    print("\n--- FINAL RESULT ---")
    print(current_code)

if __name__ == "__main__":
    run_ollama_loop()