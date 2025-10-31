import ollama
import sys
import ast
import re

# --- CONFIGURATION and PROBLEM DESCRIPTION ---
MODEL = 'gemma3:4b-it-qat' 
MAX_REFINEMENT_LOOPS = 10 # This loop should be more efficient
problem_description = """
Write a Python function called `simulate_gridbot` that simulates a simple robot 
on a 10x10 grid.

The robot's state is defined by its coordinate (x, y) and its direction ('N', 'E', 'S', 'W').
The grid boundaries are from (0, 0) at the bottom-left to (9, 9) at the top-right.

The function takes an initial state (a tuple like `(x, y, direction)`) and a string
of instructions. It must return the robot's final state as a tuple.

There are three instructions:
- 'R': Turn right 90 degrees. (e.g., 'N' becomes 'E').
- 'L': Turn left 90 degrees. (e.g., 'N' becomes 'W').
- 'F': Move one step forward in the current direction.

**Crucially, if a move instruction would take the robot off the grid, the move
is ignored, and the robot remains in its current position but continues with
the next instruction.**

Example simulation:
- Input: initial_state = (0, 0, 'N'), instructions = "RFF"
- Final Output: (2, 0, 'E')
"""

def clean_code(response_content: str) -> str:
    """
    Cleans the LLM's response to extract only the Python code.
    """
    start_fence = "```python"
    start_index = response_content.find(start_fence)
    if start_index == -1:
        start_fence = "```"
        start_index = response_content.find(start_fence)
    
    if start_index != -1:
        code_start_index = response_content.find('\n', start_index) + 1
        if code_start_index == 0:
             code_start_index = start_index + len(start_fence)
        
        end_fence = "```"
        end_index = response_content.find(end_fence, code_start_index)
        
        if end_index != -1:
            return response_content[code_start_index:end_index].strip()
            
    return response_content.strip()

def run_ollama_loop():
    """
    Implements a robust adversarial loop: Coder vs. Breaker.
    """
    print(f"Using model: {MODEL}")
    print(f"Problem: {problem_description.strip()}")

    # --- STEP 1: INITIAL CODE GENERATION (The Coder) ---
    print("\n--- STEP 1: INITIAL CODE GENERATION ---")
    try:
        initial_response = ollama.chat(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': 'You are a Python programmer. Your task is to write a function that correctly follows all rules in the problem description.'},
                {'role': 'user', 'content': problem_description},
            ]
        )
        current_code = clean_code(initial_response['message']['content'])
        print("INITIAL CODE:\n" + current_code)
    except ollama.ResponseError as e:
        print(f"Error communicating with Ollama: {e}", file=sys.stderr); sys.exit(1)

    # --- STEP 2: REFINEMENT LOOP ---
    for i in range(MAX_REFINEMENT_LOOPS):
        print(f"\n--- LOOP {i+1}/{MAX_REFINEMENT_LOOPS}: RED TEAM REVIEW ---")

        # --- STEP A: FIND A FLAW (The Breaker) ---
        print("\n--- Step A: The Breaker is searching for a flaw... ---")
        breaker_prompt = f"""
        You are a QA Adversary. Your only goal is to find a single, concrete flaw in the Coder's work.
        1. Carefully read the original Problem Rules.
        2. Carefully read the Coder's Code.
        3. Find a specific, simple input where the code's logic will violate the rules.
        4. Describe the flaw by providing the input, the wrong output the code would produce, and the correct output required by the rules.

        If you have reviewed the code against all rules and cannot find a flaw, you MUST respond with the single word: PASS

        Problem Rules:
        {problem_description}

        Coder's Code:
        ```python
        {current_code}
        ```
        """
        breaker_response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': breaker_prompt}])
        critique = breaker_response['message']['content']
        print(f"BREAKER'S REPORT:\n{critique}")

        if critique.strip().upper() == "PASS":
            print("\n--- The Breaker could not find a flaw. Halting. ---")
            break
        
        # --- STEP B: FIX THE FLAW (The Coder) ---
        print("\n--- Step B: The Coder is fixing the bug... ---")
        debug_prompt = f"""
        You are the Coder. The Breaker has found a verifiable bug in your code.
        Analyze their report and fix the bug. Provide the complete, corrected code.

        Breaker's Bug Report:
        {critique}

        Your code with the bug:
        ```python
        {current_code}
        ```
        """
        debug_response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': debug_prompt}])
        current_code = clean_code(debug_response['message']['content'])
        print("REFINED CODE:\n" + current_code)

    # --- 3. FINAL RESULT ---
    print("\n--- FINAL RESULT ---")
    print(current_code)

if __name__ == "__main__":
    run_ollama_loop()