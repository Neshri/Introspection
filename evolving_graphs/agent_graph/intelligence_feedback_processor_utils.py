# intelligence_feedback_processor_utils.py
# Feedback Integration module for intelligent planning architecture
# Processes execution outcomes, detects environmental changes, and updates belief networks

from typing import Dict, List, Optional, Tuple, Any, NamedTuple
from collections import defaultdict
import time
from .intelligence_bayesian_network_utils import BayesianBeliefNetwork  # Bayesian belief network utilities for probabilistic reasoning


class ExecutionOutcome(NamedTuple):
    """Structured representation of action execution results."""
    action_id: str
    success: bool
    output: Any
    error: Optional[str]
    timestamp: float


class EnvironmentalChange(NamedTuple):
    """Representation of detected environmental changes affecting plan execution."""
    change_type: str  # e.g., 'resource_unavailable', 'constraint_added'
    affected_nodes: List[str]  # PlanGraph node IDs affected by change
    confidence: float  # Confidence score (0.0 to 1.0)
    timestamp: float


class PerformanceMetrics:
    """Tracks execution statistics for performance monitoring and analysis."""
    def __init__(self):
        self.execution_count: int = 0
        self.success_count: int = 0
        self.failure_count: int = 0
        self.average_latency: float = 0.0
        self.execution_times: List[float] = []
        self.error_types: Dict[str, int] = defaultdict(int)

    def record_execution(self, outcome: ExecutionOutcome, latency: float):
        """Records an execution outcome and updates performance metrics."""
        self.execution_count += 1
        if outcome.success:
            self.success_count += 1
        else:
            self.failure_count += 1
            if outcome.error:
                self.error_types[outcome.error] += 1

        self.execution_times.append(latency)
        total_time = sum(self.execution_times)
        self.average_latency = total_time / len(self.execution_times)

    def get_success_rate(self) -> float:
        """Returns the current success rate as a percentage."""
        if self.execution_count == 0:
            return 0.0
        return (self.success_count / self.execution_count) * 100.0

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Provides a summary of current performance metrics."""
        return {
            'total_executions': self.execution_count,
            'success_rate': self.get_success_rate(),
            'average_latency': self.average_latency,
            'common_errors': dict(self.error_types.most_common(3)) if self.error_types else {}
        }


class FeedbackProcessor:
    """Processes execution feedback, detects changes, and updates belief networks for adaptive planning."""
    def __init__(self, belief_network: BayesianBeliefNetwork):
        self.belief_network: BayesianBeliefNetwork = belief_network  # Bayesian network for belief state management
        self.performance_metrics: PerformanceMetrics = PerformanceMetrics()  # Performance tracking instance
        self.changes_log: List[EnvironmentalChange] = []  # Log of detected environmental changes
        self.outcome_history: List[ExecutionOutcome] = []  # History of execution outcomes

    def process_outcome(self, outcome: ExecutionOutcome) -> List[EnvironmentalChange]:
        """
        Processes an execution outcome and returns any detected environmental changes.
        Updates performance metrics and belief network based on outcome.
        """
        start_time = time.time()
        self.outcome_history.append(outcome)

        # Update performance metrics
        latency = outcome.timestamp - start_time
        self.performance_metrics.record_execution(outcome, latency)

        # Detect environmental changes based on outcome
        changes = self._detect_changes(outcome)

        # Update belief network with new evidence
        self._update_beliefs(outcome, changes)

        return changes

    def _detect_changes(self, outcome: ExecutionOutcome) -> List[EnvironmentalChange]:
        """Detects environmental changes from execution outcomes using pattern analysis."""
        changes = []

        if not outcome.success and outcome.error:
            # Analyze error patterns for potential environmental changes
            change_confidence = self._calculate_change_confidence(outcome.error)

            if change_confidence > 0.7:  # High confidence threshold
                change = EnvironmentalChange(
                    change_type='execution_failure',
                    affected_nodes=[outcome.action_id],
                    confidence=change_confidence,
                    timestamp=time.time()
                )
                changes.append(change)
                self.changes_log.append(change)

        return changes

    def _calculate_change_confidence(self, error: str) -> float:
        """Calculates confidence score for potential environmental changes based on error patterns."""
        # Simple pattern-based confidence calculation
        error_patterns = {
            'resource': 0.8,
            'constraint': 0.7,
            'permission': 0.9,
            'timeout': 0.6
        }

        for pattern, confidence in error_patterns.items():
            if pattern.lower() in error.lower():
                return confidence
        return 0.3  # Default low confidence

    def _update_beliefs(self, outcome: ExecutionOutcome, changes: List[EnvironmentalChange]):
        """Updates the Bayesian belief network with new evidence from outcomes and changes."""
        # Add evidence based on execution outcome
        if outcome.success:
            self.belief_network.add_evidence(outcome.action_id, 'completed')
        else:
            self.belief_network.add_evidence(outcome.action_id, 'failed')

        # Add evidence from detected changes
        for change in changes:
            # For each affected node, reduce belief in current state
            for node_id in change.affected_nodes:
                if node_id in self.belief_network.nodes:
                    # Force belief update for affected nodes (simplified adaptive planning)
                    self.belief_network.remove_evidence(node_id)

    def get_adaptive_suggestions(self) -> Dict[str, Any]:
        """Provides suggestions for adaptive planning based on current state."""
        metrics = self.performance_metrics.get_metrics_summary()
        recent_changes = [c for c in self.changes_log if time.time() - c.timestamp < 3600]  # Last hour

        return {
            'performance_metrics': metrics,
            'recent_changes': recent_changes,
            'belief_confidence': self._get_overall_confidence(),
            'suggestions': self._generate_suggestions(metrics, recent_changes)
        }

    def _get_overall_confidence(self) -> float:
        """Calculates overall confidence in current plan based on belief network."""
        # Simplified: average completion probability across all nodes
        if not self.belief_network.nodes:
            return 0.0

        total_confidence = 0.0
        for node_id in self.belief_network.nodes:
            probs = self.belief_network.query(node_id)
            total_confidence += probs.get('completed', 0.0)

        return total_confidence / len(self.belief_network.nodes)

    def _generate_suggestions(self, metrics: Dict[str, Any], changes: List[EnvironmentalChange]) -> List[str]:
        """Generates adaptive planning suggestions based on metrics and changes."""
        suggestions = []

        if metrics['success_rate'] < 70.0:
            suggestions.append("Consider revising action implementations due to low success rate")
        if changes:
            suggestions.append(f"Address {len(changes)} recent environmental changes affecting plan execution")
        if metrics['average_latency'] > 10.0:
            suggestions.append("Optimize execution latency through parallel processing or resource allocation")

        return suggestions