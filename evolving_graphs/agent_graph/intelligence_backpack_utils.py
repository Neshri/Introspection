"""
intelligence_backpack_utils.py - Backpack chunking and processing utilities.

Provides functions for chunking backpack context and building prompt sections
for code execution and generation.
"""

import json  # JSON handling for plan data


# Configuration constants for iterative backpack processing
BACKPACK_CHUNK_SIZE_LIMIT = 4000  # Maximum tokens/chars per chunk
MAX_ITERATION_LIMIT = 5  # Maximum number of iterative LLM calls


def chunk_backpack_by_size(backpack, chunk_size_limit=BACKPACK_CHUNK_SIZE_LIMIT):
    """
    Splits the backpack into smaller chunks based on total code size.

    Args:
        backpack: List of dict items with 'file_path', 'justification', and 'full_code' keys
        chunk_size_limit: Maximum size (chars/tokens) per chunk

    Returns:
        list: List of backpack chunks, each under the size limit
    """
    if not backpack:
        return []

    chunks = []
    current_chunk = []
    current_size = 0

    for item in backpack:
        item_size = len(item.get('full_code', '')) + len(item.get('justification', '')) + len(item.get('file_path', ''))

        # If adding this item would exceed the limit and we have items in current chunk, start new chunk
        if current_size + item_size > chunk_size_limit and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0

        # If a single item exceeds the limit, include it in its own chunk (force it)
        if item_size > chunk_size_limit:
            if current_chunk:
                chunks.append(current_chunk)
            chunks.append([item])
            current_chunk = []
            current_size = 0
        else:
            current_chunk.append(item)
            current_size += item_size

    # Add the last chunk if it has items
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def load_architectural_rules():
    """Load architectural rules from rules.md file for dynamic embedding."""
    try:
        with open('rules.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Architectural rules not found. Ensure rules.md exists in the project root."


def _build_prompt_sections(architectural_rules, plan=None, working_dir=None):
    """Helper function to build common prompt sections to avoid duplication."""
    sections = []

    # Architectural rules
    sections.append(f"\n\n**Architectural Rules (MANDATORY COMPLIANCE):**\n{architectural_rules}\n")

    # File reference guidance
    sections.append("""
**File Naming and Reference Guidelines:**
- Use correct file names: e.g., 'agent_core.py' for Agent class, 'intelligence_plan_generator.py' for Planner, etc.
- Follow domain_responsibility.py pattern: e.g., 'pipeline_code_verifier.py', 'agent_backpack_formatter.py'
- Entry points: Use [context]_main.py format (e.g., 'agent_graph_main.py')
- Utility modules: Use [component]_utils_[purpose].py (e.g., 'utils_state_persistence.py')

**Import Guidelines:**
- Use ONLY relative imports: from .module_name import ClassName # Brief purpose comment
- Intra-component: from .sibling_module import X
- Inter-component: from ..directory_name.module_name import X
- Examples: from .agent_config import config # Configuration settings
- NO absolute imports except in entry point modules with mandatory comments
- NO __init__.py imports (all imports must be direct and explicit)

**Code Structure Requirements:**
- Files ≤ 300 non-empty, non-comment lines
- No duplicated logic blocks (5+ contiguous lines)
- Extract duplicates to utility modules like 'agent_graph_utils_core.py'
- Use semantic naming with clear responsibilities

""")

    # Plan context
    if plan:
        plan_json = json.dumps(plan, indent=2)
        sections.append(f"\n\n**Plan Context:**\n{plan_json}\n")

    # Working directory context
    if working_dir:
        sections.append(f"\n\n**Working Directory:**\nAll code changes should be generated relative to the working directory: {working_dir}\nIf writing files, ensure they target this candidate directory for consistency.\n")

    return "".join(sections)