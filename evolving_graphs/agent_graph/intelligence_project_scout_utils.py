import json  # JSON parsing for LLM responses
from .llm_utils import (clean_llm_json_response, parse_llm_json_response,
                        make_llm_call_with_fallback)  # LLM response processing utilities
from .debug_utils import log_error  # Debug logging utilities


def decide_next_modules_to_visit(main_goal, current_module, current_path, current_code, available_modules, all_modules, keywords, depth):
    """Use Ollama to decide which modules to visit next based on the goal and current context."""
    if not available_modules:
        return []

    from .intelligence_relevance_utils import compute_keyword_score
    modules_info = [f"- {m}: {r} (kw: {compute_keyword_score(keywords, open(all_modules[m], 'r', encoding='utf-8').read()) if m in all_modules else 'N/A'})" for m, r in available_modules]
    modules_list = "\n".join(modules_info)

    prompt = f"""
Based on the goal: "{main_goal}"

Current module being analyzed: {current_module}

Available imported modules are provided as a list of short names:
{modules_list}

Please decide which of these imported modules should be visited next to best achieve the goal.

Respond in JSON format with the following structure. Crucially, the "module_name" MUST be one of the short names from the provided list.
{{
    "modules_to_visit": [
        {{
            "module_name": "short_module_name_from_list",
            "priority": number (0-10, where 0 is highest priority),
            "reasoning": "Why this module should be visited."
        }}
    ]
}}

Only include modules from the list that should actually be visited. Do not invent new module names.
Respond ONLY with the raw JSON object, without any introductory text, conversational pleasantries, or markdown formatting. Your entire response must be a single, valid JSON object.
"""

    try:
        resp = make_llm_call_with_fallback(prompt)
        cleaned_resp = clean_llm_json_response(resp)
        result = parse_llm_json_response(cleaned_resp)
        modules_to_visit = []
        for mod in result.get('modules_to_visit', []):
            mod_name = mod.get('module_name')
            if mod_name:
                # Sanitize module name: if LLM returns full path, take only the last part
                if '.' in mod_name:
                    mod_name = mod_name.split('.')[-1]

                priority = mod.get('priority', 10)
                reasoning = mod.get('reasoning', 'LLM determined important')
                modules_to_visit.append((mod_name, priority, reasoning))
        return modules_to_visit
    except Exception as e:
        log_error(f"LLM decision error: {e}")
        return [(m, 5, f"Fallback: {r}") for m, r in available_modules]


def get_scout_response(main_goal, file_path, file_content):
    """Use Ollama to determine file relevance and extract key elements based on the main goal."""
    prompt = f"""Analyze file {file_path} for goal "{main_goal}". Content: {file_content[:1000]}... Respond ONLY with the raw JSON object, without any introductory text, conversational pleasantries, or markdown formatting. Your entire response must be a single, valid JSON object: {{"relevant": true/false, "justification": "brief reason", "key_elements": ["important parts"]}}"""

    try:
        resp = make_llm_call_with_fallback(prompt)
        cleaned_resp = clean_llm_json_response(resp)
        return parse_llm_json_response(cleaned_resp)
    except Exception as e:
        log_error(f"Scout LLM error: {e}")
        return {"relevant": False, "justification": f"LLM error: {e}", "key_elements": []}