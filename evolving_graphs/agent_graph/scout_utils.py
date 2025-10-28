"""
scout_utils.py - Scout-related utility functions.

Provides common functionality for memory querying, keyword extraction,
relevance scoring, and scout operations.
"""

import logging
from .memory_interface import MemoryInterface  # External memory interface for querying knowledge
from .agent_config import config  # Configuration settings for model selection and parameters
from .intelligence_keyword_utils import extract_keywords_from_goal  # Keyword extraction utilities
from .intelligence_relevance_utils import (compute_keyword_score, compute_combined_relevance_score,
                                           should_enqueue_dependency, is_dependency_critical)  # Relevance scoring utilities


def query_memory_for_goal(memory: MemoryInterface, goal: str, current_turn: int, n_results: int = 5) -> tuple[list, str]:
    """
    Query memory for relevant knowledge based on a goal.

    Args:
        memory: MemoryInterface instance
        goal: The goal to query memory for
        current_turn: Current turn number
        n_results: Number of results to retrieve

    Returns:
        tuple: (used_memory_ids, memory_context)
    """
    memory_results = memory.query_memory(goal, current_turn=current_turn, n_results=n_results)
    used_memory_ids = memory_results['ids'][0] if memory_results['ids'] else []
    memory_context = "\n".join(memory_results['documents'][0]) if memory_results['documents'] else ""
    return used_memory_ids, memory_context


def extract_keywords_and_compute_relevance(keywords: list, code: str, depth: int, llm_response: dict = None) -> tuple[float, float]:
    """
    Extract keywords and compute relevance scores for code content.

    Args:
        keywords: List of keywords to check against
        code: The code content to analyze
        depth: Current depth in the search tree
        llm_response: Optional LLM response for relevance

    Returns:
        tuple: (keyword_score, combined_score)
    """
    keyword_score = compute_keyword_score(keywords, code)
    llm_rel = llm_response.get('relevant', False) if llm_response else False
    comb_score = compute_combined_relevance_score(keyword_score, llm_rel, depth)
    return keyword_score, comb_score


def evaluate_file_relevance(code: str, keywords: list, depth: int) -> tuple[float, dict]:
    """
    Evaluate file relevance based on keywords and optional LLM analysis.

    Args:
        code: The file content to evaluate
        keywords: Keywords extracted from the goal
        depth: Current depth in exploration

    Returns:
        tuple: (combined_relevance_score, llm_response_dict)
    """
    keyword_score = compute_keyword_score(keywords, code)
    should_llm = keyword_score >= config.RELEVANCE_THRESHOLD // 2 or depth == 0

    if should_llm:
        # This would call LLM - placeholder for now, would be implemented per specific use case
        llm_resp = {}  # get_scout_response would be called here
    else:
        llm_resp = {}

    llm_rel = llm_resp.get('relevant', False)
    comb_score = compute_combined_relevance_score(keyword_score, llm_rel, depth)

    return comb_score, llm_resp


def create_backpack_item(file_path: str, justification: str, llm_response: dict, code: str) -> dict:
    """
    Create a standardized backpack item dictionary.

    Args:
        file_path: Path to the file
        justification: Justification for inclusion
        llm_response: LLM response dictionary
        code: Full code content

    Returns:
        dict: Backpack item
    """
    return {
        "file_path": file_path,
        "justification": justification,
        "key_elements": llm_response.get('key_elements', []),
        "full_code": code
    }


def log_scout_progress(message: str, level: str = "info"):
    """
    Log scout progress with consistent formatting.

    Args:
        message: Message to log
        level: Logging level ('info', 'debug', 'warning', 'error')
    """
    if level == "info":
        logging.info(message)
    elif level == "debug":
        logging.debug(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)