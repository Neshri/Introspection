# intelligence_multihorizon_planner_utils.py
# Multi-horizon planning utilities for intelligent decision-making across time scales
# Provides layered planning with tactical, strategic, and visionary horizons

from typing import Dict, List, Optional, NamedTuple, Any, Enum
from collections import defaultdict
from enum import Enum as PyEnum
from .task_planner_graph import PlanGraph, ObjectiveNode, ActionNode
from .intelligence_bayesian_network_utils import BayesianBeliefNetwork, get_confidence_scores, create_planning_belief_network


class PlanningHorizon(PyEnum):
    """Enumeration for different planning time horizons."""
    TACTICAL = "tactical"  # Short-term, immediate actions (hours/days)
    STRATEGIC = "strategic"  # Medium-term, goal-oriented (weeks/months)
    VISIONARY = "visionary"  # Long-term, transformative (months/years)


class HorizonConstraint(NamedTuple):
    """Named tuple representing constraints between planning horizons."""
    from_horizon: PlanningHorizon
    to_horizon: PlanningHorizon
    constraint_type: str  # e.g., 'dependency', 'resource', 'temporal'
    description: str
    weight: float  # Importance weight for constraint evaluation


class MultiHorizonPlanner:
    """
    Manages multi-horizon planning with layered plan coordination and constraint propagation.
    Integrates belief networks for feasibility evaluation across horizons.
    """

    def __init__(self):
        self.plans: Dict[PlanningHorizon, PlanGraph] = {}  # Plans per horizon
        self.constraints: List[HorizonConstraint] = []  # Cross-horizon constraints
        self.belief_networks: Dict[PlanningHorizon, BayesianBeliefNetwork] = {}  # Belief networks per horizon
        self.horizon_dependencies: Dict[PlanningHorizon, List[PlanningHorizon]] = {
            PlanningHorizon.TACTICAL: [PlanningHorizon.STRATEGIC],
            PlanningHorizon.STRATEGIC: [PlanningHorizon.VISIONARY],
            PlanningHorizon.VISIONARY: []
        }

    def add_plan(self, horizon: PlanningHorizon, plan: PlanGraph) -> None:
        """Adds or updates a plan for a specific horizon."""
        self.plans[horizon] = plan
        self.belief_networks[horizon] = create_planning_belief_network(plan)

    def get_plan(self, horizon: PlanningHorizon) -> Optional[PlanGraph]:
        """Retrieves the plan for a specific horizon."""
        return self.plans.get(horizon)

    def add_constraint(self, constraint: HorizonConstraint) -> None:
        """Adds a cross-horizon constraint."""
        self.constraints.append(constraint)

    def propagate_constraints(self, from_horizon: PlanningHorizon) -> List[str]:
        """
        Propagates constraints from one horizon to dependent horizons.
        Returns list of affected horizon identifiers.
        """
        affected_horizons = []
        for constraint in self.constraints:
            if constraint.from_horizon == from_horizon:
                to_plan = self.plans.get(constraint.to_horizon)
                if to_plan:
                    # Apply constraint logic (simplified - could be more complex)
                    self._apply_constraint_to_plan(constraint, to_plan)
                    affected_horizons.append(constraint.to_horizon.value)

        # Recursively propagate to dependent horizons
        for dep_horizon in self.horizon_dependencies.get(from_horizon, []):
            affected_horizons.extend(self.propagate_constraints(dep_horizon))

        return list(set(affected_horizons))

    def coordinate_horizons(self, primary_horizon: PlanningHorizon) -> Dict[str, Any]:
        """
        Coordinates planning across horizons starting from primary horizon.
        Returns coordination status and conflicts.
        """
        coordination_result = {
            'status': 'success',
            'conflicts': [],
            'updates': []
        }

        primary_plan = self.plans.get(primary_horizon)
        if not primary_plan:
            coordination_result['status'] = 'error'
            coordination_result['conflicts'].append(f"No plan for {primary_horizon.value}")
            return coordination_result

        # Check constraints and dependencies
        for constraint in self.constraints:
            if constraint.from_horizon == primary_horizon:
                to_plan = self.plans.get(constraint.to_horizon)
                if to_plan and not self._check_constraint_satisfaction(constraint, primary_plan, to_plan):
                    coordination_result['conflicts'].append(f"Constraint violation: {constraint.description}")

        # Propagate successful changes
        if not coordination_result['conflicts']:
            affected = self.propagate_constraints(primary_horizon)
            coordination_result['updates'] = affected

        return coordination_result

    def update_plan_horizon(self, horizon: PlanningHorizon, node_id: str, updates: Dict[str, Any]) -> bool:
        """
        Updates a specific node in a horizon plan and propagates changes.
        Returns success status.
        """
        plan = self.plans.get(horizon)
        if not plan:
            return False

        try:
            node = plan.get_node(node_id)
            for key, value in updates.items():
                if hasattr(node, key):
                    setattr(node, key, value)

            # Update belief network
            self.belief_networks[horizon] = create_planning_belief_network(plan)

            # Propagate constraints
            self.propagate_constraints(horizon)
            return True
        except (KeyError, AttributeError):
            return False

    def evaluate_feasibility(self, horizon: PlanningHorizon, node_id: str) -> Dict[str, float]:
        """
        Evaluates feasibility of a plan node using integrated belief network.
        Returns confidence scores for different outcomes.
        """
        network = self.belief_networks.get(horizon)
        if not network:
            return {}

        plan = self.plans.get(horizon)
        if not plan:
            return {}

        # Add evidence from current plan state
        self._update_network_evidence(network, plan)

        # Query feasibility
        return network.query(node_id)

    def get_overall_feasibility(self, horizon: PlanningHorizon) -> float:
        """
        Computes overall feasibility score for a horizon plan.
        """
        network = self.belief_networks.get(horizon)
        plan = self.plans.get(horizon)
        if not network or not plan:
            return 0.0

        scores = get_confidence_scores(network, plan)
        return sum(scores.values()) / len(scores) if scores else 0.0

    def _apply_constraint_to_plan(self, constraint: HorizonConstraint, plan: PlanGraph) -> None:
        """Applies a constraint to a plan (internal method)."""
        # Simplified constraint application - in practice, this would be more sophisticated
        if constraint.constraint_type == 'dependency':
            # Ensure dependent objectives are marked appropriately
            pass  # Implementation depends on specific constraint logic

    def _check_constraint_satisfaction(self, constraint: HorizonConstraint,
                                     from_plan: PlanGraph, to_plan: PlanGraph) -> bool:
        """Checks if a constraint is satisfied between two plans (internal method)."""
        # Simplified check - real implementation would validate specific constraint rules
        return True  # Placeholder

    def _update_network_evidence(self, network: BayesianBeliefNetwork, plan: PlanGraph) -> None:
        """Updates belief network evidence from current plan state (internal method)."""
        for node_id, node in plan.nodes.items():
            if hasattr(node, 'status'):
                network.add_evidence(node_id, node.status)