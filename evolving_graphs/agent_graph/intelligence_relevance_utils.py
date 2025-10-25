"""
intelligence_relevance_utils.py - Relevance scoring utilities for project scouting.

Provides functions for computing keyword-based relevance scores, combining scores,
and determining enqueue priorities for project exploration.
"""

from .intelligence_keyword_utils import compute_context_bonus  # Context bonus calculation
from .agent_config import config  # Configuration settings


def compute_keyword_score(keywords: set, code: str) -> int:
    """
    Compute multi-level keyword-based relevance score with exact, partial matches, and context bonuses.

    Args:
        keywords (set): Set of keywords to match against
        code (str): The code content to analyze

    Returns:
        int: Keyword relevance score
    """
    score = 0
    code_lower = code.lower()

    for keyword in keywords:
        keyword_lower = keyword.lower()
        exact_match = keyword_lower in code_lower

        if exact_match:
            score += 10  # Higher base score for exact matches
            # Additional points for multiple occurrences
            occurrences = code_lower.count(keyword_lower)
            score += min(occurrences - 1, 5)
        else:
            # Check for partial matches (substrings)
            partial_found = False
            for i in range(len(keyword_lower) - 2):  # At least 3 chars
                substring = keyword_lower[i:i+3]
                if substring in code_lower:
                    score += 3  # Partial match bonus
                    partial_found = True
                    break
            if not partial_found:
                # Check camelCase/snake_case variations if enabled
                if config.ENABLE_CASE_VARIATIONS:
                    from .intelligence_keyword_utils import generate_case_variations  # Case variation generation
                    variations = generate_case_variations(keyword)
                    for variation in variations:
                        if variation in code:
                            score += 8  # Case variation bonus
                            break

        # Context pattern matching bonus if enabled
        if config.ENABLE_CONTEXT_PATTERN_MATCHING and exact_match:
            context_bonus = compute_context_bonus(keyword, code)
            score += context_bonus

    return score


def compute_combined_relevance_score(keyword_score: int, llm_relevance: bool, depth: int) -> int:
    """
    Compute combined relevance score using keyword score, LLM relevance, and depth.

    Args:
        keyword_score (int): Keyword-based relevance score
        llm_relevance (bool): Whether LLM considers it relevant
        depth (int): Current exploration depth

    Returns:
        int: Combined relevance score
    """
    base_score = keyword_score * 1.5  # Weight keyword scores higher
    if llm_relevance:
        base_score += config.RELEVANCE_THRESHOLD * 2
    base_score -= depth * 1  # Reduce depth penalty for early exploration
    return max(0, base_score)


def should_enqueue_dependency(score: int, depth: int) -> bool:
    """
    Determine if a dependency should be enqueued based on score and depth.

    Args:
        score (int): Relevance score of the dependency
        depth (int): Current exploration depth

    Returns:
        bool: Whether to enqueue the dependency
    """
    # Allow exploration even with lower scores, but prioritize higher ones
    return (score >= config.RELEVANCE_THRESHOLD // 2 or depth <= 1) and depth < config.MAX_SCOUT_DEPTH


def is_dependency_critical(score: int) -> bool:
    """
    Determine if a dependency is critical based on its relevance score.

    Args:
        score (int): Relevance score

    Returns:
        bool: Whether the dependency is critical
    """
    return score > config.RELEVANCE_THRESHOLD * 1.5