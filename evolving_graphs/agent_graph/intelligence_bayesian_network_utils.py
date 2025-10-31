# intelligence_bayesian_network_utils.py
# Bayesian Belief Network utilities for intelligent planning
# Provides probabilistic reasoning over plan structures with uncertainty modeling

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode


@dataclass
class Factor:
    """Represents a probabilistic factor with variables and their value assignments."""
    variables: List[str]
    values: Dict[Tuple[str, ...], float]

    def multiply(self, other: 'Factor') -> 'Factor':
        """Multiplies this factor with another factor."""
        common_vars = set(self.variables) & set(other.variables)
        self_only = [v for v in self.variables if v not in common_vars]
        other_only = [v for v in other.variables if v not in common_vars]
        all_vars = sorted(common_vars) + self_only + other_only

        new_values = defaultdict(float)
        for s_key, s_p in self.values.items():
            for o_key, o_p in other.values.items():
                if all(s_key[self.variables.index(v)] == o_key[other.variables.index(v)] for v in common_vars):
                    new_key = tuple(
                        s_key[self.variables.index(v)] if v in self.variables else o_key[other.variables.index(v)]
                        for v in all_vars
                    )
                    new_values[new_key] += s_p * o_p

        return Factor(all_vars, dict(new_values))

    def sum_out(self, var: str) -> 'Factor':
        """Sums out a variable from this factor."""
        if var not in self.variables:
            return self
        pos = self.variables.index(var)
        new_vars = self.variables[:pos] + self.variables[pos+1:]
        summed = defaultdict(float)
        for key, p in self.values.items():
            new_key = key[:pos] + key[pos+1:]
            summed[new_key] += p
        return Factor(new_vars, dict(summed))

    def reduce(self, var: str, value: str) -> 'Factor':
        """Reduces factor by setting variable to a specific value."""
        if var not in self.variables:
            return self
        pos = self.variables.index(var)
        new_vars = self.variables[:pos] + self.variables[pos+1:]
        new_values = {}
        for key, p in self.values.items():
            if key[pos] == value:
                new_key = key[:pos] + key[pos+1:]
                new_values[new_key] = p
        return Factor(new_vars, dict(new_values))

    def normalize(self) -> 'Factor':
        """Normalizes the factor values to sum to 1."""
        total = sum(self.values.values())
        if total == 0:
            return self
        self.values = {k: v / total for k, v in self.values.items()}
        return self


class BeliefNode:
    """Represents an individual belief variable in the Bayesian network."""
    def __init__(self, node_id: str, states: List[str], parents: List[str] = None):
        self.node_id = node_id
        self.states = states  # List of possible state values
        self.parents = parents or []  # List of parent node IDs
        self.cpt: Dict[Tuple[str, ...], Dict[str, float]] = {}  # Conditional probability table

    def set_cpt(self, cpt: Dict[Tuple[str, ...], Dict[str, float]]):
        """Sets the conditional probability table."""
        self.cpt = cpt

    def get_factor(self) -> Factor:
        """Converts the CPT into a factor for inference."""
        vars_list = self.parents + [self.node_id]
        values = {}
        for parent_combo, probs in self.cpt.items():
            for state, p in probs.items():
                key = parent_combo + (state,)
                values[key] = p
        return Factor(vars_list, values)


class BayesianBeliefNetwork:
    """Manages belief states and performs probabilistic inference using variable elimination."""
    def __init__(self):
        self.nodes: Dict[str, BeliefNode] = {}
        self.node_order: List[str] = []  # Topological order of nodes
        self.evidence: Dict[str, str] = {}

    def set_topology(self, node_order: List[str]):
        """Sets the topological ordering of nodes."""
        self.node_order = node_order
        for node in self.nodes.values():
            node.parents = sorted(node.parents, key=lambda x: self.node_order.index(x))

    def add_node(self, node: BeliefNode):
        """Adds a belief node to the network."""
        self.nodes[node.node_id] = node

    def add_evidence(self, node_id: str, value: str):
        """Adds evidence for a specific node."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found in network")
        if value not in self.nodes[node_id].states:
            raise ValueError(f"Invalid state {value} for node {node_id}")
        self.evidence[node_id] = value

    def remove_evidence(self, node_id: str):
        """Removes evidence for a specific node."""
        self.evidence.pop(node_id, None)

    def clear_evidence(self):
        """Clears all evidence."""
        self.evidence = {}

    def query(self, query_var: str) -> Dict[str, float]:
        """Performs probabilistic inference to compute P(query_var | evidence)."""
        # Get initial factors from all nodes
        factors = [node.get_factor() for node in self.nodes.values()]

        # Reduce factors by evidence
        for node_id, value in self.evidence.items():
            factors = [f.reduce(node_id, value) for f in factors]

        # Eliminate hidden variables
        hidden_vars = [nid for nid in self.node_order if nid != query_var and nid not in self.evidence]
        for var in hidden_vars:
            new_factors = []
            for f in factors:
                summed = f.sum_out(var)
                if summed.values:  # Only add non-empty factors
                    new_factors.append(summed)
            factors = new_factors

        # Multiply remaining factors
        if not factors:
            return {}
        result = factors[0]
        for f in factors[1:]:
            result = result.multiply(f)

        # Normalize and return
        result.normalize()
        return {key[0]: v for key, v in result.values.items()}


def create_planning_belief_network(plan_graph: PlanGraph) -> BayesianBeliefNetwork:
    """Factory function to create a Bayesian belief network from a PlanGraph."""
    network = BayesianBeliefNetwork()

    # Determine topological order
    node_order = []
    visited = set()
    to_visit = [plan_graph.root_id]

    while to_visit:
        current = to_visit.pop(0)
        if current in visited:
            continue
        visited.add(current)
        node_order.append(current)
        node = plan_graph.get_node(current)
        if isinstance(node, ObjectiveNode):
            to_visit.extend(node.children)

    network.node_order = node_order
    network.set_topology(node_order)

    # Create belief nodes
    for node_id in node_order:
        node = plan_graph.get_node(node_id)
        if isinstance(node, ObjectiveNode):
            states = ['pending', 'in_progress', 'completed', 'failed']
            parents = [node.parent_id] if node.parent_id else []
            belief_node = BeliefNode(node_id, states, parents)

            # Set CPT based on planning logic
            if parents:
                cpt = {}
                for p_state in states:
                    if p_state == 'completed':
                        cpt[(p_state,)] = {'pending': 0.1, 'in_progress': 0.2, 'completed': 0.6, 'failed': 0.1}
                    else:
                        cpt[(p_state,)] = {'pending': 0.4, 'in_progress': 0.3, 'completed': 0.2, 'failed': 0.1}
            else:
                # Root prior
                belief_node.set_cpt({(): {'pending': 0.5, 'in_progress': 0.3, 'completed': 0.2, 'failed': 0.0}})

            if parents:
                belief_node.set_cpt(cpt)
            network.add_node(belief_node)

        elif isinstance(node, ActionNode):
            states = ['pending', 'completed', 'failed']
            parents = [node.parent_id]
            belief_node = BeliefNode(node_id, states, parents)

            # Set CPT for actions
            cpt = {}
            for p_state in ['pending', 'in_progress', 'completed', 'failed']:
                if p_state == 'completed':
                    cpt[(p_state,)] = {'pending': 0.0, 'completed': 0.9, 'failed': 0.1}
                else:
                    cpt[(p_state,)] = {'pending': 0.8, 'completed': 0.1, 'failed': 0.1}
            belief_node.set_cpt(cpt)
            network.add_node(belief_node)

    return network


def get_confidence_scores(network: BayesianBeliefNetwork, plan_graph: PlanGraph) -> Dict[str, float]:
    """Computes confidence scores for PlanGraph nodes using Bayesian inference."""
    scores = {}
    for node_id in network.nodes:
        probs = network.query(node_id)
        scores[node_id] = probs.get('completed', 0.0)
    return scores