#
# mcts.py (A Major Branch)
# This is the core "thinking" engine of the agent. It implements the Monte
# Carlo Tree Search algorithm to explore possible futures and decide on the best
# next action.
#
# It uses the following modules:
# - agent.engine.node: The data structure for the tree.
# - agent.utils.llm_handler: To call the LLM for expansion and simulation.
# - agent.utils.config: For MCTS-specific settings like iteration count.
#

import math
from agent.engine.node import Node
from agent.utils import llm_handler
from agent.utils import config

def run_mcts_cycle(root_node):
    """Performs one full "thinking" cycle and returns the best next node."""
    for i in range(config.MCTS_ITERATIONS_PER_STEP):
        current_node = root_node
        # 1. SELECTION: Find the most promising path to explore
        while current_node.children:
            if all(child.visits == 0 for child in current_node.children):
                current_node = current_node.children[0]
                break
            current_node = max(current_node.children, key=lambda n: (n.value / n.visits) + math.sqrt(2 * math.log(current_node.visits) / n.visits) if n.visits > 0 else float('inf'))

        # 2. EXPANSION: If we've reached a leaf, create one new child node
        if current_node.visits > 0 or current_node == root_node:
            expand_node(current_node)

        # 3. SIMULATION: Get a quality score from the Critic for the new path
        score = simulate_node(current_node)

        # 4. BACKPROPAGATION: Update the stats all the way up the tree
        backpropagate(current_node, score)

    # After thinking, choose the best path to actually take
    if not root_node.children:
        return None

    best_child = max(root_node.children, key=lambda n: n.visits)
    return best_child

def expand_node(node):
    """Creates one new child node for expansion."""
    goal = config.INITIAL_GOAL
    response = llm_handler.get_executor_response(goal, node.document_state)
    new_paragraph = response.strip()

    new_document_state = node.document_state + "\n\n" + new_paragraph
    new_node = Node(document_state=new_document_state, parent=node, plan=new_paragraph)
    node.children.append(new_node)

def simulate_node(node):
    """Gets a quality score for the node."""
    goal = config.INITIAL_GOAL
    response = llm_handler.get_critic_score(goal, node.document_state)
    try:
        score = int(response)
    except ValueError:
        score = 1
    return score

def backpropagate(node, score):
    """Updates the stats all the way up the tree."""
    temp_node = node
    while temp_node is not None:
        temp_node.visits += 1
        temp_node.value += score
        temp_node = temp_node.parent