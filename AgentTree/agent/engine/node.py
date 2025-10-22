#
# node.py (A Smaller Branch)
# This module defines the Node data structure, which is the fundamental
# building block of the Monte Carlo Search Tree.
#

class Node:
    """Represents a state in the MCTS tree."""
    def __init__(self, document_state, parent=None, plan=""):
        self.document_state = document_state
        self.parent = parent
        self.plan_that_led_here = plan
        self.children = []
        self.visits = 0
        self.value = 0.0