import logging
from .llm_util import chat_llm
from .agent_config import DEFAULT_MODEL

class ProseGenerator:
    def generate_summary(self, context: str, file_name: str) -> str:
        """Uses an LLM to synthesize a prose summary from a context string."""
        
        prompt = f"""
You are an expert software architect. Your task is to synthesize all available information into a single, comprehensive, and accurate summary for the module `{file_name}`.

**CONTEXT:**
{context}

**INSTRUCTIONS:**
Based on all the context above, produce a final summary in the following Markdown format.
- Be concise and accurate.
- Ground all claims in the provided context, especially the source code and verified interactions.
- Clearly explain the module's role, how it uses its dependencies, and what service it provides to its dependents.

**OUTPUT FORMAT:**
### Summary for `{file_name}`
**Core Responsibility:** (A single sentence that defines the module's primary purpose.)

**Dependency Interactions:**
- **`dependency_name.py`**: (A short, specific explanation of how and why this module uses this dependency.)

**Service to Dependents:**
(A short explanation of the service or functionality this module provides to the modules that import it.)

**Potential Issues Detected:**
- (A bulleted list of detected issues, such as unimplemented functions or logical inconsistencies.)
"""
        logging.info(f"[ProseGenerator] Generating summary for: {file_name}")
        return chat_llm(DEFAULT_MODEL, prompt)