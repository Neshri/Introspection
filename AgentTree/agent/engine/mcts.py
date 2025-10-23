#
# mcts.py (A Major Branch)
# This is the core "thinking" engine of the agent. It implements the Monte
# Carlo Tree Search algorithm to explore possible futures and decide on the best
# next action.
#
# It uses the following modules:
# - agent.engine.node: The data structure for the tree.
# - agent.intelligence.llm_executor: For code generation and execution.
# - agent.intelligence.llm_evaluator: For code quality evaluation.
# - agent.intelligence.llm_critic: For LLM-based code criticism.
# - agent.intelligence.llm_tracker: For performance tracking.
# - agent.utils.config: For MCTS-specific settings like iteration count.
#

import math  # Standard library for mathematical operations, used in UCB1 formula
from .node import Node  # Node class for tree data structure in MCTS
from ..shared.llm import get_executor_response, execute_code, evaluate_code_quality, get_critic_score, track_prompt_performance  # Intelligence functions
from ..shared.utils import format_backpack_context  # Shared utility functions
from ..utils import config  # Configuration settings for MCTS parameters and goals

def run_mcts_cycle(root_node, main_goal):
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
            expand_node(current_node, main_goal)

        # 3. SIMULATION: Get a quality score from the Critic for the new path
        score = simulate_node(current_node, main_goal)

        # 4. BACKPROPAGATION: Update the stats all the way up the tree
        backpropagate(current_node, score)

    # After thinking, choose the best path to actually take
    if not root_node.children:
        return None

    best_child = max(root_node.children, key=lambda n: n.visits)
    return best_child

def expand_node(node, main_goal):
    """Creates one new child node for expansion."""
    response = get_executor_response(main_goal, node.document_state, node.backpack)
    new_code = response.strip()

    # Extract code from markdown if present (LLM might wrap in ```python blocks)
    if new_code.startswith('```python'):
        new_code = new_code.replace('```python', '').replace('```', '').strip()
    elif new_code.startswith('```'):
        new_code = new_code.replace('```', '').strip()

    # For code generation, we replace the entire code state with the new version
    # rather than appending like we did with stories
    new_node = Node(document_state=new_code, parent=node, plan=new_code, backpack=node.backpack)
    node.children.append(new_node)

def simulate_node(node, main_goal):
    """Gets a quality score for the node by executing and evaluating the code."""

    # First execute the code to get actual runtime results
    execution_result = execute_code(node.document_state)

    # Store execution results in the node for later analysis
    node.execution_result = execution_result

    # Calculate score using the general evaluation framework
    base_score = evaluate_code_quality(node.document_state, execution_result, main_goal)

    # Get LLM critic score as well and combine for robustness
    llm_score = get_critic_score(main_goal, node.document_state, node.backpack)
    combined_score = min(10, max(1, (base_score + llm_score) // 2))

    # Track this prompt/code combination for self-improvement
    # Extract the prompt that was used to generate this code
    backpack_context = format_backpack_context(node.backpack)

    prompt_used = config.EXECUTOR_PROMPT_TEMPLATE.format(goal=main_goal, document=node.parent.document_state if node.parent else node.document_state, backpack_context=backpack_context)
    track_prompt_performance(prompt_used, combined_score, main_goal, execution_result)

    return combined_score

def backpropagate(node, score):
    """Updates the stats all the way up the tree."""
    temp_node = node
    while temp_node is not None:
        temp_node.visits += 1
        temp_node.value += score
        temp_node = temp_node.parent