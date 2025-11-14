import logging
from collections import defaultdict
from .llm_util import chat_llm
from .agent_config import DEFAULT_MODEL

def _sanitize_llm_output(text: str) -> str:
    """A local copy to avoid circular dependency."""
    import re
    text = re.sub(r'^\s*#+\s.*$', '', text, flags=re.MULTILINE)
    return text.strip()

def generate_component_summary(component_signature: str, component_code: str) -> str:
    """
    A specialized agent that generates a one-sentence summary for a single function or method.
    """
    prompt = f"""You are a senior software engineer writing concise documentation.
Based on the source code of the component provided below, what is its primary purpose?
Answer in a single, concise sentence.

**Component Signature:** `{component_signature}`

**Source Code:**
```python
{component_code}
```

**Primary Purpose (one sentence):**"""
    return _sanitize_llm_output(chat_llm(DEFAULT_MODEL, prompt))

def generate_role_summary(file_name: str, dependency_summaries_str: str, component_summaries_str: str, previous_answer: str = None, feedback: str = None) -> str:
    """Generates or revises the 'System-Level Role' summary."""
    if previous_answer and feedback:
        prompt = f"""You are a software architect correcting a high-level summary. Your previous 'System-Level Role' summary for `{file_name}` was flagged as a "hallucination". Your task is to revise it to be more grounded in fact.

**PREVIOUS (INCORRECT) SUMMARY:**
{previous_answer}

**AUDITOR FEEDBACK (REASON FOR FAILURE):**
{feedback}

**INSTRUCTIONS:**
Rewrite the 'System-Level Role' paragraph. The new summary must be a reasonable interpretation based *only* on the context provided below.

**Original Context (Dependencies and Internal Components):**
**Summaries of Dependencies:**
{dependency_summaries_str if dependency_summaries_str else 'None.'}

**Summaries of Internal Functions/Methods:**
{component_summaries_str if component_summaries_str else 'This module has no public functions or methods.'}

**Corrected 'System-Level Role' (one concise paragraph):**"""
    else:
        prompt = f"""You are a senior software architect. Your goal is to write a "System-Level Role" for the module `{file_name}`. This description must explain the module's UNIQUE purpose within the larger system.

**PRIMARY CONTEXT: The Module's Own Components**
This is your most important source of truth. The module's role is defined by what its own functions and classes do.
- **Summaries of Internal Functions/Methods:**
{component_summaries_str if component_summaries_str else 'This module has no public functions or methods.'}

**SECONDARY CONTEXT: How It Interacts with Dependencies**
Use this information only to understand how `{file_name}` fits in. Do NOT describe the dependencies themselves.
- **Summaries of Dependencies:**
{dependency_summaries_str if dependency_summaries_str else 'None.'}

**RULES:**
1.  **Prioritize the Primary Context.** The role of `{file_name}` is defined by ITS OWN components, not its dependencies.
2.  **Focus on the "Why".** Don't just list what the functions do; explain what unique capability they provide to the system.
3.  **Do NOT describe the dependencies.** Do not state "This module uses X to do Y". Instead, state "This module's purpose is to do Z."

**Your Task:**
Based on the rules and context above, write a concise, one-paragraph "System-Level Role" for `{file_name}`."""

    return _sanitize_llm_output(chat_llm(DEFAULT_MODEL, prompt))

def generate_core_summary(file_name: str, component_summaries_str: str, previous_answer: str = None, feedback: str = None) -> str:
    """Generates or revises the 'Core Responsibility' summary."""
    if previous_answer and feedback:
        prompt = f"""You are a code analyst correcting a high-level summary. Your previous 'Core Responsibility' summary for `{file_name}` was flagged as a "hallucination". Your task is to revise it to be more grounded in fact.

**PREVIOUS (INCORRECT) SUMMARY:**
{previous_answer}

**AUDITOR FEEDBACK (REASON FOR FAILURE):**
{feedback}

**INSTRUCTIONS:**
Rewrite the 'Core Responsibility' sentence. The new summary must be a reasonable interpretation based *only* on the context provided below.

**Original Context (Internal Components):**
**Summaries of Internal Functions/Methods:**
{component_summaries_str if component_summaries_str else 'This module has no public functions or methods.'}

**Corrected 'Core Responsibility' (one sentence):**"""
    else:
        prompt = f"""You are a code analyst. Based on the summaries of its functions and methods, what is the primary purpose of the module `{file_name}`?
Answer in a single, concise sentence.

**Summaries of Internal Functions/Methods:**
{component_summaries_str if component_summaries_str else 'This module has no public functions or methods.'}

**Core Responsibility (one sentence):**"""

    return _sanitize_llm_output(chat_llm(DEFAULT_MODEL, prompt))

def generate_service_summary(file_name: str, api_context: str, previous_answer: str = None, feedback: str = None) -> str:
    """
    Generates or revises the 'Service to Dependents' summary.
    """
    # If feedback and a previous answer are provided, use the revision prompt.
    if previous_answer and feedback:
        prompt = f"""You are a software architect correcting technical documentation. Your previous summary for the module `{file_name}` failed an audit. Your task is to revise it based on the feedback.

**PREVIOUS (INCORRECT) SUMMARY:**
{previous_answer}

**AUDITOR FEEDBACK (REASON FOR FAILURE):**
{feedback}

**INSTRUCTIONS:**
Rewrite the summary to correct the error identified by the auditor. The new summary must be grounded in the Public API provided below.

**Public API of `{file_name}`:**
{api_context}

**Corrected 'Service to Dependents' Summary:**"""
    # Otherwise, use the standard generation prompt.
    else:
        prompt = f"""You are a software architect writing technical documentation. Your task is to describe the services a module provides to its dependents, based ONLY on its public API.

**Rule:** You MUST NOT list any function or method that starts with an underscore `_`.

**Example:**
- **GOOD:** "The module provides a `GraphAnalyzer` class that can be initialized with a root path and used to `analyze()` a project."
- **BAD:** "The module provides a `_find_todos` function."

Now, for the module `{file_name}`, create a bulleted list describing the service it provides. **If there are no public functions or classes, state 'This module provides no callable services to dependents.'**

**Public API of `{file_name}`:**
{api_context}

**Service to Dependents:**"""

    return _sanitize_llm_output(chat_llm(DEFAULT_MODEL, prompt))

def generate_deps_summary(interactions: list, external_imports: set) -> str:
    """
    Generates the 'Dependency Interactions' summary deterministically from structured data.
    """
    lines = []
    
    if interactions:
        grouped_interactions = defaultdict(list)
        for call in interactions:
            grouped_interactions[call['target_module']].append(call['symbol'])
        
        lines.append("- Direct interactions with other modules in this project:")
        for module, symbols in sorted(grouped_interactions.items()):
            unique_symbols = sorted(list(set(symbols)))
            symbols_str = ", ".join([f"`{s}`" for s in unique_symbols])
            lines.append(f"  - Uses symbols from `{module}`: {symbols_str}.")

    if external_imports:
        lines.append("- Direct interactions with external libraries:")
        for lib in sorted(list(external_imports)):
            lines.append(f"  - Imports and uses the `{lib}` library.")
            
    if not lines:
        return "This module has no direct interactions with other project modules or external libraries."
        
    return "\n".join(lines)