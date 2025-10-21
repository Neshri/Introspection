import ollama
import time
import threading
import datetime
import re
import os
import shutil

# --- Configuration ---
MODEL = 'gemma3:12b-it-qat'
INITIAL_GOAL = "Write a short, engaging story about a robot who discovers music."
CURRENT_DOC_FILENAME = "agent_memory_current.txt"
PREVIOUS_DOC_FILENAME = "agent_memory_previous.txt"

# --- PROMPTS (MOVED TO GLOBAL SCOPE) ---
EXECUTOR_PROMPT_TEMPLATE = """
You are the Executor. You have two modes: PLANNING and EXECUTING.

**Current Time:** {timestamp}
**Main Goal:** {goal}

**Working Document (Current Project State):**
---
{document}
---

**Previous Plan:** "{plan}"
**Critique of Plan:** "{critique}"

**Task:**
{task}
"""

CRITIC_PROMPT_TEMPLATE = """
You are the Critic. Your job is to evaluate the Executor's plan for alignment with the goal and the working document.

**Current Time:** {timestamp}
**Main Goal:** {goal}

**Working Document (Current Project State):**
---
{document}
---

**Proposed Step by Executor:**
"{plan}"

**Task:**
Critique the proposed step. Check for flaws and ensure it builds upon the Working Document.
- If the plan is a good *next step in planning*, critique it and suggest refinements.
- If the plan is solid and ready to be *acted upon*, respond with the keyword "[EXECUTE]" followed by your approval. For example: "[EXECUTE] The plan is sound. This is the logical next action to build the story."
"""

# --- Shared State for Threads ---
agent_state = {
    'goal': INITIAL_GOAL,
    'running': True
}

# (The rest of the functions are correct and do not need changes)

def load_document_on_startup(filename):
    """
    Tries to load the last saved state from the memory file.
    Returns the goal and document content if successful, otherwise None.
    """
    if not os.path.exists(filename):
        return None, None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        goal_match = re.search(r"Goal: (.*?)\n\n--- Document Content ---", content, re.DOTALL)
        doc_match = re.search(r"--- Document Content ---\n(.*)", content, re.DOTALL)
        if goal_match and doc_match:
            goal_from_file = goal_match.group(1).strip()
            document_from_file = doc_match.group(1).strip()
            return goal_from_file, document_from_file
        else:
            return None, None
    except Exception as e:
        print(f"\n[!] Error loading document state: {e}")
        return None, None

def save_document_state(document_content, current_goal):
    """Saves the current working document and goal, and rotates the previous version."""
    try:
        if os.path.exists(CURRENT_DOC_FILENAME):
            shutil.move(CURRENT_DOC_FILENAME, PREVIOUS_DOC_FILENAME)
        with open(CURRENT_DOC_FILENAME, "w", encoding="utf-8") as f:
            f.write(f"--- Agent Memory State ---\n")
            f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Goal: {current_goal}\n\n")
            f.write(f"--- Document Content ---\n")
            f.write(document_content)
    except Exception as e:
        print(f"\n[!] Error saving document state: {e}")

def user_input_thread():
    """Listens for user input in the background."""
    while agent_state['running']:
        try:
            user_input = input()
            if user_input.strip():
                print(f"\n--- 🎯 New Goal Received! Updating on next cycle. ---")
                print(f"    New Goal: {user_input.strip()}\n")
                agent_state['goal'] = user_input.strip()
        except EOFError:
            time.sleep(0.5)

def main_agent_loop():
    """The main loop for our agent's thought process."""
    local_goal = agent_state['goal']
    iteration = 1
    
    print("--- 🚀 Initializing Agent ---")
    loaded_goal, loaded_doc = load_document_on_startup(CURRENT_DOC_FILENAME)
    
    if loaded_goal == local_goal and loaded_doc is not None:
        print("✅ Previous session for the same goal found. Loading state...")
        working_document = loaded_doc
        current_plan = "Review the loaded working document and determine the next logical step to continue the project."
    else:
        print("✨ Starting a new session.")
        working_document = "The story is currently empty. The first step is to establish a basic outline."
        current_plan = "Brainstorm core concepts for the story (robot's purpose, setting, emotional arc)."

    critique = "No critique yet. This is the first step."

    print(f"🎯 Main Goal: {local_goal}")
    print("Agent is now running automatically. Type a new goal and press Enter to interrupt.")
    print("Press Ctrl+C to stop the agent.\n")

    while agent_state['running']:
        try:
            if local_goal != agent_state['goal']:
                local_goal = agent_state['goal']
                working_document = "The project is empty. The first step is to establish a basic outline."
                current_plan = "Brainstorm core concepts for the new goal."
                critique = "The goal has changed. Starting fresh."
                iteration = 1
                print(f"--- 🔄 Agent Resetting for New Goal ---")
                print(f"🎯 Main Goal: {local_goal}\n")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            is_execution_step = bool(re.search(r'\[EXECUTE\]', critique, re.IGNORECASE))
            
            print(f"--- Iteration {iteration} (Time: {timestamp}) ---")
            
            if is_execution_step:
                print("⚡ Executor is EXECUTING the plan...")
                task = f"Execute the approved plan: '{current_plan}'. Update the Working Document with the results. Your output should be ONLY the new, updated Working Document."
            else:
                print("💡 Executor is PLANNING the next step...")
                task = "Based on the critique, formulate the *next single, simple step*. Your output must be ONLY the description of this new step."

            executor_prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                timestamp=timestamp, goal=local_goal, document=working_document,
                plan=current_plan, critique=critique, task=task
            )

            response = ollama.chat(
                model=MODEL, messages=[{'role': 'user', 'content': executor_prompt}]
            )
            
            if is_execution_step:
                new_content = response['message']['content'].strip()
                HEADER_TO_CLEAN = "**Working Document (Current Project State):**"
                working_document = new_content.replace(HEADER_TO_CLEAN, "").strip()
                print("✅ Document Updated. Now planning the next step.\n")
                current_plan = "Review the updated document and determine the next logical step."
            else:
                current_plan = response['message']['content'].strip()
                print(f"✅ Executor's New Plan: {current_plan}\n")

            print("🤔 Critic is evaluating...")
            critic_prompt = CRITIC_PROMPT_TEMPLATE.format(
                timestamp=timestamp, goal=local_goal, document=working_document, plan=current_plan
            )
            
            response = ollama.chat(
                model=MODEL, messages=[{'role': 'user', 'content': critic_prompt}]
            )
            critique = response['message']['content'].strip()
            print(f"🧐 Critic's Feedback: {critique}\n")

            save_document_state(working_document, local_goal)
            iteration += 1
            time.sleep(5)

        except NameError as e:
            print(f"\n[!] A critical error occurred: {e}")
            print("[!] This is likely a bug in the script. Please check variable scopes.")
            agent_state['running'] = False
            break
        except Exception as e:
            print(f"\nAn error occurred in the main loop: {e}")
            agent_state['running'] = False
            break

def main():
    """Main entry point of the script."""
    input_handler = threading.Thread(target=user_input_thread, daemon=True)
    input_handler.start()
    try:
        main_agent_loop()
    except KeyboardInterrupt:
        print("\n--- 🛑 User interrupted. Shutting down agent. ---")
    finally:
        agent_state['running'] = False

if __name__ == "__main__":
    main()