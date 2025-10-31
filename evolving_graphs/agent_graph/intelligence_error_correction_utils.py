# intelligence_error_correction_utils.py
# Continuous Error Correction module for intelligent planning architecture
# Provides failure pattern recognition, corrective actions, and adaptive plan refinement
# Refactored to use split modules for token limit compliance

from typing import Dict, List, Optional, Any
from .intelligence_feedback_processor_utils import ExecutionOutcome, FeedbackProcessor  # Feedback processing integration
from .intelligence_bayesian_network_utils import BayesianBeliefNetwork  # Belief network for probabilistic reasoning
from .intelligence_error_pattern_recognition_utils import PatternRecognizer, FailurePattern  # Pattern recognition
from .intelligence_error_correction_engine_utils import CorrectionEngine, CorrectionStrategy  # Correction strategies


class ErrorCorrectionEngine:
    """
    Engine for continuous error correction in intelligent planning systems.
    Recognizes failure patterns, applies corrective strategies, and adapts plans proactively.
    Refactored to use split modules: PatternRecognizer and CorrectionEngine.
    """

    def __init__(self, feedback_processor: FeedbackProcessor, belief_network: BayesianBeliefNetwork):
        self.feedback_processor: FeedbackProcessor = feedback_processor  # Integration with feedback processing
        self.belief_network: BayesianBeliefNetwork = belief_network  # Belief network for uncertainty modeling

        # Initialize split components
        self.pattern_recognizer = PatternRecognizer(belief_network)
        self.correction_engine = CorrectionEngine(belief_network)

        # Shared adaptive learning parameters
        self.pattern_threshold: float = 0.7  # Confidence threshold for pattern recognition
        self.min_pattern_frequency: int = 3  # Minimum occurrences to establish pattern
        self.learning_rate: float = 0.1  # Rate of adaptation for strategy effectiveness

    def process_execution_failure(self, outcome: ExecutionOutcome) -> Dict[str, Any]:
        """
        Processes an execution failure, identifies patterns, and applies corrective actions.
        Returns correction results including applied strategies and plan updates.
        """
        # Analyze failure for pattern recognition using PatternRecognizer
        identified_patterns = self.pattern_recognizer.identify_failure_patterns(outcome)
        correction_results = {}

        if identified_patterns:
            # Select and apply optimal correction strategy using CorrectionEngine
            best_strategy = self.correction_engine.select_correction_strategy(identified_patterns, outcome)
            if best_strategy:
                correction_results = self.correction_engine.apply_correction_strategy(best_strategy, outcome, identified_patterns)

                # Update pattern knowledge base
                correction_success = correction_results.get('success', False)
                self.pattern_recognizer.update_pattern_knowledge(outcome, identified_patterns, correction_success)

        return {
            'identified_patterns': [p.pattern_id for p in identified_patterns],
            'applied_strategy': correction_results.get('strategy_id'),
            'success': correction_results.get('success', False),
            'plan_updates': correction_results.get('plan_updates', []),
            'preventive_actions': self.pattern_recognizer.generate_preventive_actions(identified_patterns)
        }

    def adapt_plans_proactively(self) -> Dict[str, Any]:
        """
        Performs proactive plan adaptation based on learned patterns and belief network analysis.
        Returns adaptation results and recommendations.
        """
        return self.pattern_recognizer.adapt_plans_proactively()

    def add_correction_strategy(self, strategy: CorrectionStrategy):
        """Adds a new correction strategy to the knowledge base."""
        self.correction_engine.add_correction_strategy(strategy)

    def get_correction_statistics(self) -> Dict[str, Any]:
        """Returns comprehensive statistics on error correction performance."""
        pattern_stats = self.pattern_recognizer.get_pattern_statistics()
        correction_stats = self.correction_engine.get_correction_statistics()

        return {
            **pattern_stats,
            **correction_stats,
            'overall_correction_effectiveness': correction_stats.get('overall_correction_effectiveness', 0.0)
        }

    # Backward compatibility methods - delegate to appropriate components
    def _identify_failure_patterns(self, outcome: ExecutionOutcome) -> List[FailurePattern]:
        """Legacy method - delegates to PatternRecognizer.identify_failure_patterns"""
        return self.pattern_recognizer.identify_failure_patterns(outcome)

    def _select_correction_strategy(self, patterns: List[FailurePattern], outcome: ExecutionOutcome) -> Optional[CorrectionStrategy]:
        """Legacy method - delegates to CorrectionEngine.select_correction_strategy"""
        return self.correction_engine.select_correction_strategy(patterns, outcome)

    def _apply_correction_strategy(self, strategy: CorrectionStrategy, outcome: ExecutionOutcome,
                                  patterns: List[FailurePattern]) -> Dict[str, Any]:
        """Legacy method - delegates to CorrectionEngine.apply_correction_strategy"""
        return self.correction_engine.apply_correction_strategy(strategy, outcome, patterns)

    def _update_pattern_knowledge(self, outcome: ExecutionOutcome, patterns: List[FailurePattern],
                                correction_results: Dict[str, Any]):
        """Legacy method - delegates to PatternRecognizer.update_pattern_knowledge"""
        correction_success = correction_results.get('success', False)
        self.pattern_recognizer.update_pattern_knowledge(outcome, patterns, correction_success)

    def _generate_preventive_actions(self, patterns: List[FailurePattern]) -> List[Dict[str, Any]]:
        """Legacy method - delegates to PatternRecognizer.generate_preventive_actions"""
        return self.pattern_recognizer.generate_preventive_actions(patterns)