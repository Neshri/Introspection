import ollama
import time
import threading
import datetime
import re
import os
import shutil
import math # Needed for MCTS selection

# --- Configuration ---
MODEL = 'gemma3:12b-it-qat'
INITIAL_GOAL = "Write a short, engaging story about a robot who discovers music."
CURRENT_DOC_FILENAME = "agent_memory_current.txt"
PREVIOUS_DOC_FILENAME = "agent_memory_previous.txt"
MCTS_ITERATIONS_PER_STEP = 10 # How many "futures" to imagine before taking a step

# --- NEW: A simple class for our search tree nodes ---
class Node:
    def __init__(self, document_state, parent=None, plan=""):
        self.document_state = document_state
        self.parent = parent
        self.plan_that_led_here = plan # The action that created this node
        self.children = []
        self.visits = 0
        self.value = 0.0 # From 1-10, the average score of this path

# --- PROMPTS (Repurposed for MCTS) ---
# The Executor is now our "Expansion" operator
EXECUTOR_PROMPT_TEMPLATE = """
You are a creative Executor. Your job is to generate the *next logical paragraph or section* to continue the story.

**Main Goal:** {goal}
**Working Document (Current Story):**
---
{document}
---

**Task:**
Write the next single paragraph to continue the story. Be creative and build upon what is already there. Your output must be ONLY the new paragraph.
"""

# The Critic is now our "Simulation" (or evaluation) operator
CRITIC_PROMPT_TEMPLATE = """
You are a literary Critic. Your job is to evaluate the quality of a story-in-progress.

**Main Goal:** {goal}

**Story So Far:**
---
{document}
---

**Task:**
Read the story so far. On a scale of 1 to 10, how engaging, coherent, and promising is it?
- 1: A complete dead end, incoherent.
- 5: Has some potential but is flawed.
- 10: Brilliant, a compelling foundation for a great story.

Your output must be ONLY a single integer score from 1 to 10.
"""

# --- Shared State ---
agent_state = {'goal': INITIAL_GOAL, 'running': True}


def main_agent_loop():
    """The main loop, now structured around MCTS."""
    
    local_goal = agent_state['goal']
    
    print("--- 🚀 Initializing Agent ---")
    _, loaded_doc = load_document_on_startup(CURRENT_DOC_FILENAME) # Simplified loading
    
    if loaded_doc:
        print("✅ Previous session found. Loading state...")
        root_node = Node(document_state=loaded_doc)
    else:
        print("✨ Starting a new session.")
        root_node = Node(document_state="The story begins.")

    print(f"🎯 Main Goal: {local_goal}")
    print("Agent is now using MCTS. It will 'think' before each step.")
    
    turn_number = 1
    while agent_state['running']:
        print(f"\n--- Turn {turn_number} (Thinking for {MCTS_ITERATIONS_PER_STEP} iterations) ---")
        
        # This is the MCTS "thinking" loop
        for i in range(MCTS_ITERATIONS_PER_STEP):
            print(f"\r🤔 Thinking... [{i+1}/{MCTS_ITERATIONS_PER_STEP}]", end="")
            
            # 1. SELECTION: Find the most promising path to explore
            current_node = root_node
            while current_node.children:
                # Use UCB1 formula to balance exploration and exploitation
                current_node = max(current_node.children, key=lambda n: (n.value / n.visits) + math.sqrt(2 * math.log(current_node.visits) / n.visits) if n.visits > 0 else float('inf'))

            # 2. EXPANSION: If we've reached a leaf, create one new child node
            if current_node.visits > 0 or current_node == root_node:
                executor_prompt = EXECUTOR_PROMPT_TEMPLATE.format(goal=local_goal, document=current_node.document_state)
                response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': executor_prompt}])
                new_paragraph = response['message']['content'].strip()
                
                new_document_state = current_node.document_state + "\n\n" + new_paragraph
                new_node = Node(document_state=new_document_state, parent=current_node, plan=new_paragraph)
                current_node.children.append(new_node)
                current_node = new_node # Move to the new node for simulation

            # 3. SIMULATION: Get a quality score from the Critic for the new path
            critic_prompt = CRITIC_PROMPT_TEMPLATE.format(goal=local_goal, document=current_node.document_state)
            response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': critic_prompt}])
            try:
                score = int(response['message']['content'].strip())
            except ValueError:
                score = 1 # Penalize if the critic doesn't return a number

            # 4. BACKPROPAGATION: Update the stats all the way up the tree
            temp_node = current_node
            while temp_node is not None:
                temp_node.visits += 1
                temp_node.value += score
                temp_node = temp_node.parent
        
        print("\n💡 Thinking complete.")
        
        # After thinking, choose the best path to actually take
        if not root_node.children:
            print("Agent has no further ideas. Stopping.")
            break
            
        best_child = max(root_node.children, key=lambda n: n.visits) # The most explored path is the most robust
        
        print(f"✅ Agent commits to the next step:\n---")
        print(best_child.plan_that_led_here)
        print("---\n")
        
        # The chosen path becomes the new reality
        root_node = best_child
        root_node.parent = None # Detach from the old tree
        
        save_document_state(root_node.document_state, local_goal)
        turn_number += 1
        time.sleep(1)


# --- Helper Functions (load, save, input_thread, main) ---
# These functions remain largely the same, just ensure they are present.
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