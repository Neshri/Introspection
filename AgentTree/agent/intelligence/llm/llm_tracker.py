#
# llm_tracker.py (A Leaf)
# This module tracks prompt performance for self-improvement.
#
# It uses the following modules:
# - agent.utils.config: For configuration settings like log file path.
#

import os  # File system operations for data persistence and temporary file management
import json  # JSON handling for prompt performance tracking and data serialization
from agent import config  # Configuration module for model, prompt templates, and system settings

def track_prompt_performance(prompt_variation, score, goal, execution_result):
    """
    Track prompt performance for self-improvement.

    Records which prompt variations lead to better code generation outcomes.
    """
    try:
        # Load existing performance data
        if os.path.exists(config.PROMPT_PERFORMANCE_LOG):
            with open(config.PROMPT_PERFORMANCE_LOG, 'r') as f:
                performance_data = json.load(f)
        else:
            performance_data = {}

        # Use full prompt as key for detailed tracking
        prompt_key = prompt_variation.replace('\n', ' ').strip()

        # Update performance tracking
        if prompt_key not in performance_data:
            performance_data[prompt_key] = {
                'scores': [],
                'success_count': 0,
                'total_attempts': 0,
                'avg_score': 0,
                'goal': goal
            }

        performance_data[prompt_key]['scores'].append(score)
        performance_data[prompt_key]['total_attempts'] += 1
        if execution_result and execution_result['success']:
            performance_data[prompt_key]['success_count'] += 1

        # Calculate new average
        performance_data[prompt_key]['avg_score'] = sum(performance_data[prompt_key]['scores']) / len(performance_data[prompt_key]['scores'])

        # Keep only last 50 scores to prevent file bloat
        if len(performance_data[prompt_key]['scores']) > 50:
            performance_data[prompt_key]['scores'] = performance_data[prompt_key]['scores'][-50:]

        # Save updated data
        with open(config.PROMPT_PERFORMANCE_LOG, 'w') as f:
            json.dump(performance_data, f, indent=2)

    except Exception as e:
        # Don't crash the main process if tracking fails
        pass

def get_best_prompt_variations(limit=5):
    """
    Retrieve the best performing prompt variations from historical data.
    """
    try:
        if os.path.exists(config.PROMPT_PERFORMANCE_LOG):
            with open(config.PROMPT_PERFORMANCE_LOG, 'r') as f:
                performance_data = json.load(f)

            # Sort by average score and success rate
            sorted_prompts = sorted(
                performance_data.items(),
                key=lambda x: (x[1]['avg_score'], x[1]['success_count'] / max(1, x[1]['total_attempts'])),
                reverse=True
            )

            return sorted_prompts[:limit]
        else:
            return []
    except Exception as e:
        return []