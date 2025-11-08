import logging
from .llm_util import chat_llm
from .agent_config import DEFAULT_MODEL
import re

def _parse_auditor_response(response: str) -> tuple[bool, str]:
    """Parses the LLM's audit response to find a verdict and reasoning."""
    logging.info(f"--- AUDITOR RAW RESPONSE ---\n{response}\n--------------------------")
    verdict_match = re.search(r'verdict:\s*(PASS|FAIL)', response, re.IGNORECASE)
    
    verdict_found = verdict_match and verdict_match.group(1).upper() == "FAIL"
    
    reasoning = response
    if verdict_match:
        reasoning = response[:verdict_match.start()].strip()

    if not reasoning or reasoning.lower().startswith("reasoning"):
        reasoning = f"Auditor provided a '{'FAIL' if verdict_found else 'PASS'}' verdict without detailed reasoning. Full response: {response}"

    return verdict_found, reasoning


def run_duplication_auditor(draft_summary: str) -> bool:
    """A simple, deterministic check for duplicate markdown headers."""
    headers = [line for line in draft_summary.split('\n') if line.startswith('#### ')]
    return len(headers) != len(set(headers))


def run_completeness_auditor(draft_summary: str) -> bool:
    """A simple, deterministic check for the presence of all required sections."""
    required = ["#### System-Level Role", "#### Core Responsibility", "#### Dependency Interactions", "#### Service to Dependents", "#### Potential Issues Detected"]
    return not all(section in draft_summary for section in required)

def run_service_auditor(file_name: str, draft_summary: str, public_api_str: str) -> tuple[bool, str]:
    """
    A fully deterministic auditor for the 'Service to Dependents' section.
    This corrected version uses a more robust regex and logic.
    """
    try:
        match = re.search(r'#### Service to Dependents\n(.*?)(?=\n####|$)', draft_summary, re.DOTALL)
        if not match:
            return True, f"Deterministic Check FAILED: Could not find the 'Service to Dependents' section."
        service_section_text = match.group(1).strip()
        
        # Flaw 1: Does the summary mention non-public entities (those starting with '_')?
        # This regex now correctly looks for symbols starting with `_` inside backticks.
        private_symbols = re.findall(r'`(_[a-zA-Z0-9_]+)`', service_section_text)
        if private_symbols:
            return True, f"Deterministic Check FAILED: The summary mentions a private symbol: `{private_symbols[0]}`."

        # Flaw 2: Does the summary incorrectly claim there are no services?
        has_public_api = "No public API defined." not in public_api_str
        claims_no_services = "no callable services" in service_section_text.lower()
        
        if claims_no_services and has_public_api:
            return True, "Deterministic Check FAILED: The summary claims there are no services, but a public API was detected."

        return False, "Deterministic Check PASSED."
        
    except Exception as e:
        return True, f"Deterministic Check FAILED: An exception occurred during parsing: {e}"

def run_dependency_grounding_auditor(draft_summary: str, interactions: list, external_imports: set) -> tuple[bool, str]:
    """A fully deterministic auditor to fact-check the 'Dependency Interactions' section."""
    try:
        match = re.search(r'#### Dependency Interactions\n(.*?)(?=\n####|$)', draft_summary, re.DOTALL)
        if not match:
            return True, "Deterministic Check FAILED: Could not find the 'Dependency Interactions' section."
        deps_text = match.group(1).strip()

        # Check for every external import identified by the static analyzer
        for lib in external_imports:
            if f"`{lib}`" not in deps_text:
                return True, f"Deterministic Check FAILED: The summary is missing the external dependency: `{lib}`."

        # Check for every internal module interaction identified by the static analyzer
        internal_modules = {call['target_module'] for call in interactions}
        for module in internal_modules:
            if f"`{module}`" not in deps_text:
                return True, f"Deterministic Check FAILED: The summary is missing the internal dependency: `{module}`."
        
        return False, "Deterministic Check PASSED."
    except Exception as e:
        return True, f"Deterministic Check FAILED: An exception occurred during parsing: {e}"

def run_grounding_auditor(file_name: str, prose_text: str, source_code: str) -> tuple[bool, str]:
    """An LLM-based auditor that fact-checks ONLY the prose sections of the summary."""
    prompt = f"""
You are a pragmatic and concise Chief Software Architect. Your goal is to identify true "hallucinations" in a code summary's prose.

**Core Instructions**

1.  **YOUR SCOPE:** You are ONLY responsible for auditing the "System-Level Role" and "Core Responsibility" sections provided below. You must ignore all other aspects of the file.
2.  **What is a FLAW:** A flaw is a "hallucination" — a statement with NO BASIS in the provided source code.
3.  **What is ACCEPTABLE:** An acceptable summary makes reasonable inferences about a module's role based on its name, class names, and function signatures.
4.  **Special Rule for Simple Files:** For very simple files (e.g., config files that only declare constants), the most obvious inference IS an acceptable inference.

**YOUR TASK**
Review ONLY the following prose from the summary for `{file_name}`. Is it a reasonable interpretation grounded in the code?

**Full Source Code of `{file_name}`:**
```python
{source_code}
```

**Prose to Fact-Check:**
---
{prose_text}
---

**Instructions for Your Output:**
1.  Provide your reasoning as a **concise, bulleted list**.
2.  If you find a flaw, quote the hallucinated statement directly.
3.  Conclude with the verdict on a new line. The verdict must be exactly "Verdict: PASS" or "Verdict: FAIL".

**Reasoning and Verdict:**
"""
    response = chat_llm(DEFAULT_MODEL, prompt)
    return _parse_auditor_response(response)