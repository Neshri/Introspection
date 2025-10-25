#
# utils.py (A Leaf)
# This module contains shared utility functions for formatting and common operations.
#

def format_backpack_context(backpack, chunk_index=None, total_chunks=None):
    """
    Formats backpack items into a consistent context string for LLM prompts.

    Args:
        backpack: List of dict items with 'file_path', 'justification', and 'full_code' keys
        chunk_index: Optional int, index of current chunk (0-based)
        total_chunks: Optional int, total number of chunks

    Returns:
        str: Formatted context string
    """
    if not backpack:
        return ""

    backpack_context = ""
    for i, item in enumerate(backpack):
        backpack_context += f"**File {i+1}: {item.get('file_path', 'Unknown')}**\n"
        backpack_context += f"Justification: {item.get('justification', 'N/A')}\n"
        backpack_context += f"Code:\n{item.get('full_code', '')}\n\n"

    if chunk_index is not None and total_chunks is not None:
        backpack_context += f"\n**Processing Chunk {chunk_index + 1} of {total_chunks}**\n"

    return backpack_context