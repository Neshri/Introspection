# intelligence_error_pattern_recognition_utils.py
# Pattern recognition and analysis module for intelligent planning architecture
# Provides failure pattern identification, matching, discovery, and proactive adaptation

from typing import Dict, List, Optional, NamedTuple, Any, Tuple
from collections import defaultdict
import time
from .intelligence_feedback_processor_utils import ExecutionOutcome
from .intelligence_bayesian_network_utils import BayesianBeliefNetwork


class FailurePattern(NamedTuple):
    """Structured representation of recurring failure patterns in plan execution."""
    pattern_id: str
    error_type: str
    description: str
    frequency: int
    confidence: float  # Pattern confidence score (0.0 to 1.0)
    affected_nodes: List[str]  # Plan nodes commonly affected by this pattern
    temporal_context: str  # When the pattern typically occurs (e.g., 'execution', 'planning')
    last_occurrence: float  # Timestamp of last occurrence


class PatternRecognizer:
    """
    Recognizes and analyzes failure patterns in intelligent planning systems.
    Maintains pattern knowledge base and performs proactive adaptation.
    """

    def __init__(self, belief_network: BayesianBeliefNetwork):
        self.belief_network: BayesianBeliefNetwork = belief_network  # Belief network for uncertainty modeling

        # Pattern knowledge base
        self.failure_patterns: Dict[str, FailurePattern] = {}  # Known failure patterns
        self.pattern_history: List[Tuple[str, float]] = []  # Pattern occurrence history [(pattern_id, timestamp)]

        # Adaptive learning parameters
        self.pattern_threshold: float = 0.7  # Confidence threshold for pattern recognition
        self.min_pattern_frequency: int = 3  # Minimum occurrences to establish pattern
        self.learning_rate: float = 0.1  # Rate of adaptation for pattern confidence

    def identify_failure_patterns(self, outcome: ExecutionOutcome) -> List[FailurePattern]:
        """Identifies failure patterns from execution outcomes using belief network analysis."""
        identified_patterns = []

        # Query belief network for failure likelihood assessment
        failure_probs = self.belief_network.query(outcome.action_id)
        failure_confidence = 1.0 - failure_probs.get('completed', 0.0)

        # Check against known patterns
        for pattern in self.failure_patterns.values():
            if self._matches_pattern(outcome, pattern):
                # Update pattern frequency and confidence
                updated_pattern = FailurePattern(
                    pattern_id=pattern.pattern_id,
                    error_type=pattern.error_type,
                    description=pattern.description,
                    frequency=pattern.frequency + 1,
                    confidence=min(1.0, pattern.confidence + self.learning_rate * failure_confidence),
                    affected_nodes=pattern.affected_nodes,
                    temporal_context=pattern.temporal_context,
                    last_occurrence=time.time()
                )
                self.failure_patterns[pattern.pattern_id] = updated_pattern
                identified_patterns.append(updated_pattern)

        # Discover new patterns if confidence is high enough
        if failure_confidence >= self.pattern_threshold and not identified_patterns:
            new_pattern = self._discover_new_pattern(outcome, failure_confidence)
            if new_pattern:
                self.failure_patterns[new_pattern.pattern_id] = new_pattern
                identified_patterns.append(new_pattern)

        return identified_patterns

    def _matches_pattern(self, outcome: ExecutionOutcome, pattern: FailurePattern) -> bool:
        """Determines if an execution outcome matches a known failure pattern."""
        # Basic matching criteria
        if outcome.error and pattern.error_type.lower() in outcome.error.lower():
            return True

        # Check affected nodes
        if outcome.action_id in pattern.affected_nodes:
            return True

        # Belief network-based matching
        if pattern.confidence > self.pattern_threshold:
            # More sophisticated matching could use semantic similarity or Bayesian inference
            return len(pattern.affected_nodes) > 0

        return False

    def _discover_new_pattern(self, outcome: ExecutionOutcome, confidence: float) -> Optional[FailurePattern]:
        """Discovers new failure patterns from execution outcomes."""
        if not outcome.error:
            return None

        pattern_id = f"pattern_{len(self.failure_patterns)}_{int(time.time())}"
        error_type = outcome.error.split(':')[0] if ':' in outcome.error else outcome.error

        return FailurePattern(
            pattern_id=pattern_id,
            error_type=error_type,
            description=f"Automatically discovered pattern for {error_type} errors",
            frequency=1,
            confidence=confidence,
            affected_nodes=[outcome.action_id],
            temporal_context='execution',
            last_occurrence=time.time()
        )

    def update_pattern_knowledge(self, outcome: ExecutionOutcome, patterns: List[FailurePattern],
                                correction_success: bool):
        """Updates pattern knowledge base with new information."""
        for pattern in patterns:
            self.pattern_history.append((pattern.pattern_id, time.time()))

        # Propagate learning to belief network
        if correction_success:
            self.belief_network.add_evidence(outcome.action_id, 'completed')
        else:
            self.belief_network.add_evidence(outcome.action_id, 'failed')

    def generate_preventive_actions(self, patterns: List[FailurePattern]) -> List[Dict[str, Any]]:
        """Generates preventive actions based on identified patterns."""
        preventive_actions = []

        for pattern in patterns:
            if pattern.confidence > self.pattern_threshold:
                action = {
                    'pattern_id': pattern.pattern_id,
                    'action_type': 'monitor_and_alert',
                    'description': f"Monitor for {pattern.error_type} conditions",
                    'priority': 'high' if pattern.frequency > 5 else 'medium'
                }
                preventive_actions.append(action)

        return preventive_actions

    def adapt_plans_proactively(self) -> Dict[str, Any]:
        """
        Performs proactive plan adaptation based on learned patterns and belief network analysis.
        Returns adaptation results and recommendations.
        """
        adaptations = {
            'pattern_based_refinements': [],
            'belief_network_updates': [],
            'horizon_coordination': []
        }

        # Analyze patterns for proactive refinements
        for pattern in self.failure_patterns.values():
            if pattern.frequency >= self.min_pattern_frequency and pattern.confidence > self.pattern_threshold:
                refinement = self._generate_proactive_refinement(pattern)
                if refinement:
                    adaptations['pattern_based_refinements'].append(refinement)

        # Update belief network with preventive evidence
        for node_id in self.belief_network.nodes:
            risk_score = self._calculate_node_risk(node_id)
            if risk_score > 0.7:
                adaptations['belief_network_updates'].append({
                    'node_id': node_id,
                    'risk_score': risk_score,
                    'recommended_action': 'increase_monitoring'
                })

        return adaptations

    def _generate_proactive_refinement(self, pattern: FailurePattern) -> Optional[Dict[str, Any]]:
        """Generates proactive plan refinement for a failure pattern."""
        if pattern.frequency < self.min_pattern_frequency:
            return None

        return {
            'pattern_id': pattern.pattern_id,
            'refinement_type': 'resource_preallocation',
            'affected_nodes': pattern.affected_nodes,
            'confidence': pattern.confidence,
            'expected_impact': 'reduce_failure_rate_by_' + str(int(pattern.confidence * 20)) + '_percent'
        }

    def _calculate_node_risk(self, node_id: str) -> float:
        """Calculates risk score for a plan node based on pattern analysis."""
        risk_score = 0.0
        affected_count = 0

        for pattern in self.failure_patterns.values():
            if node_id in pattern.affected_nodes:
                risk_score += pattern.confidence * (pattern.frequency / 10.0)  # Normalize frequency
                affected_count += 1

        return min(1.0, risk_score / max(1, affected_count))

    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Returns statistics on pattern recognition performance."""
        return {
            'total_patterns': len(self.failure_patterns),
            'pattern_frequency_distribution': {pid: p.frequency for pid, p in self.failure_patterns.items()},
            'recent_pattern_history': self.pattern_history[-10:],  # Last 10 occurrences
        }