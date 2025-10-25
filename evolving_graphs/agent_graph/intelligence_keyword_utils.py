"""
intelligence_keyword_utils.py - Keyword extraction and processing utilities for project scouting.

Provides functions for extracting meaningful keywords from goals, expanding with synonyms,
generating case variations, and computing context bonuses for relevance scoring.
"""

import re  # Regular expressions for text processing


def extract_keywords_from_goal(goal: str) -> set:
    """
    Extract meaningful keywords from goal, including action words and reducing stop word filtering.

    Args:
        goal (str): The goal text to extract keywords from

    Returns:
        set: Set of extracted keywords
    """
    if not goal:
        return set()

    # Reduced stop words - keep action words and important connectors
    stop_words = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'in', 'on', 'at', 'to', 'from', 'by', 'with', 'as', 'for', 'of'
    }

    # Action words to prioritize
    action_words = {
        'improve', 'enhance', 'fix', 'add', 'remove', 'update', 'optimize',
        'refactor', 'implement', 'create', 'build', 'test', 'debug', 'analyze',
        'design', 'plan', 'execute', 'run', 'start', 'stop', 'load', 'save',
        'process', 'handle', 'manage', 'monitor', 'validate', 'check'
    }

    # Split and clean words
    words = goal.lower().split()
    keywords = set()

    for word in words:
        # Remove punctuation
        clean_word = ''.join(c for c in word if c.isalnum())
        if len(clean_word) > 1 and clean_word not in stop_words:
            keywords.add(clean_word)

    # Add synonyms if enabled (placeholder for configuration)
    # if config.ENABLE_SYNONYM_EXPANSION:
    keywords.update(expand_synonyms(keywords))

    return keywords


def expand_synonyms(keywords: set) -> set:
    """
    Expand keywords with synonyms for goal terms.

    Args:
        keywords (set): Original set of keywords

    Returns:
        set: Expanded set including synonyms
    """
    synonyms = {
        'stability': ['reliability', 'robustness', 'resilience', 'durability'],
        'performance': ['speed', 'efficiency', 'optimization'],
        'security': ['protection', 'safety', 'encryption'],
        'reliability': ['stability', 'robustness', 'dependability'],
        'efficiency': ['performance', 'optimization', 'speed'],
        'robustness': ['stability', 'reliability', 'resilience'],
        'logging': ['log', 'trace', 'monitor', 'track'],
        'error': ['exception', 'failure', 'bug', 'issue'],
        'test': ['testing', 'validation', 'verification'],
        'code': ['implementation', 'logic', 'algorithm'],
        'execution': ['run', 'execute', 'process', 'handle']
    }

    expanded = set()
    for keyword in keywords:
        expanded.add(keyword)
        if keyword in synonyms:
            expanded.update(synonyms[keyword])
    return expanded


def generate_case_variations(keyword: str) -> list:
    """
    Generate camelCase and snake_case variations of a keyword.

    Args:
        keyword (str): The keyword to generate variations for

    Returns:
        list: List of case variations
    """
    variations = []

    # Convert to snake_case: stability -> stability, improve_stability -> improve_stability
    snake_case = keyword.replace('-', '_').lower()
    variations.append(snake_case)

    # Convert to camelCase: stability -> stability, improve_stability -> improveStability
    if '_' in keyword:
        parts = keyword.split('_')
        camel = parts[0] + ''.join(word.capitalize() for word in parts[1:])
        variations.append(camel)
    else:
        variations.append(keyword)  # Already might be camelCase

    # Convert from camelCase to snake_case
    # stability -> stability
    # improveStability -> improve_stability
    snake_from_camel = re.sub(r'(?<!^)(?=[A-Z])', '_', keyword).lower()
    if snake_from_camel != keyword.lower():
        variations.append(snake_from_camel)

    return variations


def compute_context_bonus(keyword: str, code: str) -> int:
    """
    Compute context bonus based on keyword surroundings in code.

    Args:
        keyword (str): The keyword to check for context
        code (str): The code content to analyze

    Returns:
        int: Context bonus score (0-5)
    """
    bonus = 0
    code_lower = code.lower()
    keyword_lower = keyword.lower()

    # Look for keyword in function/class names, comments, docstrings
    lines = code.split('\n')
    for line in lines:
        line_lower = line.lower().strip()
        if keyword_lower in line_lower:
            # Bonus for comments/docstrings
            if line_lower.startswith('#') or '"""' in line_lower or "'''" in line_lower:
                bonus += 2
            # Bonus for function/class definitions
            elif 'def ' in line_lower or 'class ' in line_lower:
                bonus += 3
            # Bonus for variable names
            elif '=' in line and keyword_lower in line_lower.split('=')[0]:
                bonus += 1

    return min(bonus, 5)  # Cap context bonus