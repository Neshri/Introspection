import logging
from collections import defaultdict
from .llm_util import chat_llm
from .agent_config import DEFAULT_MODEL

def _sanitize_llm_output(text: str) -> str:
    """A local copy to avoid circular dependency."""
    import re
    text = re.sub(r'^\s*#+\s.*$', '', text, flags=re.MULTILINE)
    return text.strip()

def generate_role_summary(file_name: str, dependency_summaries_str: str, api_context: str) -> str:
    """Generates the 'System-Level Role' summary."""
    prompt = f"You are a software architect. Based on the summaries of the modules it depends on, and its own public API, what is the high-level role of `{file_name}` in the system? Answer in a single, concise paragraph.\n\n**Summaries of Dependencies:**\n{dependency_summaries_str if dependency_summaries_str else 'None.'}\n\n**Public API of `{file_name}`:**\n{api_context}\n\n**System-Level Role (one concise paragraph):**"
    return _sanitize_llm_output(chat_llm(DEFAULT_MODEL, prompt))

def generate_core_summary(file_name: str, source_code_context: str) -> str:
    """Generates the 'Core Responsibility' summary."""
    prompt = f"You are a code analyst. Based on its source code, what is the primary purpose of `{file_name}`? Answer in a single, concise sentence.\n\n{source_code_context}\n\n**Core Responsibility (one sentence):**"
    return _sanitize_llm_output(chat_llm(DEFAULT_MODEL, prompt))

def generate_service_summary(file_name: str, api_context: str) -> str:
    """Generates the 'Service to Dependents' summary."""
    prompt = f"You are a software architect. Based ONLY on the Public API of `{file_name}`, create a bulleted list describing the service it provides. **If there are no public functions or classes, state 'This module provides no callable services to dependents.'**\n\n{api_context}\n\n**Service to Dependents:**"
    return _sanitize_llm_output(chat_llm(DEFAULT_MODEL, prompt))

def generate_deps_summary(interactions: list, external_imports: set) -> str:
    """
    Generates the 'Dependency Interactions' summary deterministically from structured data.
    """
    lines = []
    
    # Group internal interactions by target module for cleaner output
    if interactions:
        grouped_interactions = defaultdict(list)
        for call in interactions:
            grouped_interactions[call['target_module']].append(call['symbol'])
        
        lines.append("- Direct interactions with other modules in this project:")
        for module, symbols in sorted(grouped_interactions.items()):
            unique_symbols = sorted(list(set(symbols)))
            symbols_str = ", ".join([f"`{s}`" for s in unique_symbols])
            lines.append(f"  - Uses symbols from `{module}`: {symbols_str}.")

    # Correctly handle and list external library imports
    if external_imports:
        lines.append("- Direct interactions with external libraries:")
        for lib in sorted(list(external_imports)):
            lines.append(f"  - Imports and uses the `{lib}` library.")
            
    if not lines:
        return "This module has no direct interactions with other project modules or external libraries."
        
    return "\n".join(lines)