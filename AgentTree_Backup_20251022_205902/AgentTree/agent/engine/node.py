#
# node.py (A Smaller Branch)
# This module defines the Node data structure, which is the fundamental
# building block of the Monte Carlo Search Tree.
#

class Node:
    """Represents a state in the MCTS tree."""
    def __init__(self, document_state, parent=None, plan="", backpack=[]):
        self.document_state = document_state  # Current code state
        self.parent = parent
        self.plan_that_led_here = plan  # The code that led to this state
        self.backpack = backpack  # List of dictionaries as returned by the Scout
        self.children = []
        self.visits = 0
        self.value = 0.0

        # Code-specific attributes
        self.execution_result = None  # Result from code execution (dict with success, output, error, time)
        self.test_results = None  # Test outcomes if applicable
        self.performance_metrics = {}  # Additional metrics like execution time, memory usage, etc.