import ollama
import time
import json

# --- CONFIGURATION ---
MODEL = "granite4:3b"
MAX_ROUNDS = 4

# --- THE PARLIAMENT (Organic Stress Test) ---
PERSONAS = {
    "ARCHITECT": """
        You are the ARCHITECT.
        Your job is to perform a DEEP ARCHITECTURAL ANALYSIS.
        Do NOT just classify the module.
        Explain the DESIGN INTENT.
        Explain the RESPONSIBILITIES.
        Explain the RELATIONSHIPS with other components.
        Identify key INVARIANTS and PATTERNS.
        
        CITATION RULES:
        1. You MUST cite specific lines for every claim.
        2. If you claim a dependency exists, cite the IMPORT line (e.g. "Imported on line 5").
        3. If you claim a feature exists, cite the METHOD definition.
        
        Avoid generic fluff. Be technical and specific.
    """,
    "SKEPTIC": """
        You are the SKEPTIC.
        Your job is to verify CITATIONS.
        
        PROTOCOL:
        1. FIRST, scan the REALITY_CODE and list ALL imports found at the top.
        2. SECOND, scan for the specific classes/functions cited by the Architect.
        3. THIRD, verify if the Architect's claims match the code.
        
        If the Architect claims "It imports json", check your list from Step 1.
        If the code is missing that import, you yell "CITATION ERROR".
        
        At the end of your analysis, you MUST output exactly one of these two lines:
        VERDICT: APPROVED
        VERDICT: REJECTED
    """,
    "SCRIBE": """
        You are the SCRIBE.
        Your job is to synthesize the final report.
        It must be concise, factual, and cite the evidence provided by the Architect.
        No fluff.
    """
}

# --- REALITY (The Shared Context) ---
TARGET_FILE = "/c/Introspection/evolving_graphs/agent_graph/module_contextualizer.py"

def read_target_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def reduce_code_to_skeleton(source_code):
    """
    Parses source code and strips function bodies to reduce context size.
    Keeps imports, class definitions, method signatures, and docstrings.
    """
    try:
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Keep docstring if present
                new_body = []
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                    new_body.append(node.body[0])
                
                # Add '...' to indicate body removal
                new_body.append(ast.Expr(value=ast.Constant(value=...)))
                node.body = new_body
        
        # Use ast.unparse (Python 3.9+)
        return ast.unparse(tree)
    except Exception as e:
        return f"# Error reducing code: {e}\n# Returning original source...\n{source_code}"

SHARED_GOAL = f"Analyze {TARGET_FILE}. Explain its Architectural Role, Design Patterns, and Key Responsibilities. Cite line numbers."

def chat(model, messages):
    try:
        response = ollama.chat(model=model, messages=messages)
        return response['message']['content']
    except Exception as e:
        return f"[Error: {e}]"

def main():
    # 1. Read Reality
    print(f"--- Reading Target File: {TARGET_FILE} ---")
    reality_code = read_target_file(TARGET_FILE)
    print(f"Code Length: {len(reality_code)} chars\n")

    # Initialize Histories
    histories = {name: [{'role': 'system', 'content': prompt + f"\nREALITY_CODE:\n{reality_code}\n\nGOAL: {SHARED_GOAL}"}] 
                 for name, prompt in PERSONAS.items()}
    
    # --- PARLIAMENT SESSION ---
    print("--- Starting Parliament Session ---")
    
    # Round 1: Architect Proposes
    print("[ARCHITECT] is analyzing...")
    arch_resp = chat(MODEL, histories["ARCHITECT"] + [{'role': 'user', 'content': "Analyze this code. Explain the WHY and HOW. Cite your evidence."}])
    print(f"ARCHITECT: {arch_resp}\n")
    histories["ARCHITECT"].append({'role': 'assistant', 'content': arch_resp})

    # Verification Loop (Max 2 Retries)
    for attempt in range(2):
        # Round 2: Skeptic Verifies
        print(f"--- Round 2 (Attempt {attempt+1}): Verification ---")
        print("[SKEPTIC] is verifying...")
        skeptic_prompt = f"The Architect said:\n{arch_resp}\n\nVerify these claims against the REALITY CODE. Are the citations correct? If NO, explain why."
        skeptic_resp = chat(MODEL, histories["SKEPTIC"] + [{'role': 'user', 'content': skeptic_prompt}])
        print(f"SKEPTIC: {skeptic_resp}\n")
        histories["SKEPTIC"].append({'role': 'assistant', 'content': skeptic_resp})

        if "VERDICT: REJECTED" in skeptic_resp:
            print("!!! SKEPTIC REJECTED. REQUESTING CORRECTION !!!")
            feedback = f"The Skeptic rejected your analysis:\n{skeptic_resp}\n\nReview the REALITY CODE again.\nIf the Skeptic is wrong (e.g. missed an import), POINT IT OUT.\nIf you were wrong, fix your citations."
            arch_resp = chat(MODEL, histories["ARCHITECT"] + [{'role': 'user', 'content': feedback}])
            print(f"ARCHITECT (Correction): {arch_resp}\n")
            histories["ARCHITECT"].append({'role': 'assistant', 'content': arch_resp})
        elif "VERDICT: APPROVED" in skeptic_resp:
            print("!!! SKEPTIC APPROVED !!!")
            break
        else:
            print("!!! SKEPTIC VERDICT UNCLEAR (Assuming Rejection) !!!")
            feedback = f"The Skeptic did not give a clear verdict. Please review the feedback:\n{skeptic_resp}"
            arch_resp = chat(MODEL, histories["ARCHITECT"] + [{'role': 'user', 'content': feedback}])
            print(f"ARCHITECT (Correction): {arch_resp}\n")
            histories["ARCHITECT"].append({'role': 'assistant', 'content': arch_resp})

    # Round 3: Scribe Synthesizes
    if "VERDICT: APPROVED" not in skeptic_resp:
        print("!!! FINAL REJECTION. UNABLE TO REACH CONSENSUS !!!")
    else:
        print("--- Round 3: Synthesis ---")
        print("[SCRIBE] is writing...")
        scribe_prompt = f"Based on the verified analysis:\n{arch_resp}\n\nWrite a concise summary."
        scribe_resp = chat(MODEL, histories["SCRIBE"] + [{'role': 'user', 'content': scribe_prompt}])
        print(f"SCRIBE: {scribe_resp}\n")

if __name__ == "__main__":
    main()
