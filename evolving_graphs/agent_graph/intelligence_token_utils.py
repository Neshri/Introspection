"""
intelligence_token_utils.py - Token estimation utilities for LLM context management.

Provides functions for estimating token counts and managing context limits.
"""

import tiktoken  # Token estimation for better context management


class TokenEstimator:
    """
    A class to handle token estimation with fallback support.
    """

    def __init__(self):
        """Initialize the token estimator with tiktoken or fallback."""
        # Use GPT-3.5-turbo tokenizer as fallback for Gemma3 (similar English tokenization)
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")  # GPT-3.5/4 tokenizer
        except Exception:
            # Fallback to basic character-based estimation if tiktoken fails
            self.tokenizer = None
            print("WARNING: tiktoken not available, falling back to character-based estimation")

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in text using tiktoken.

        Args:
            text (str): The text to estimate tokens for

        Returns:
            int: Estimated token count
        """
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Rough fallback: ~4 characters per token for English text
            return len(text) // 4


# Global instance for convenience
token_estimator = TokenEstimator()


def estimate_tokens(text: str) -> int:
    """
    Convenience function to estimate tokens using the global estimator.

    Args:
        text (str): The text to estimate tokens for

    Returns:
        int: Estimated token count
    """
    return token_estimator.estimate_tokens(text)