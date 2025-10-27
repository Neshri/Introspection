import os  # File system operations for directory traversal and file reading
import logging  # Logging for debugging and progress tracking
import heapq  # Priority queue for goal-directed traversal
import json  # JSON parsing for LLM responses
from .memory_interface import MemoryInterface  # External memory interface for querying knowledge
from .agent_config import config  # Configuration settings for model selection and parameters
from .utils_collect_modules import collect_modules  # To collect all Python modules in the project directory
from .intelligence_keyword_utils import extract_keywords_from_goal  # Keyword extraction utilities
from .intelligence_relevance_utils import (compute_keyword_score, compute_combined_relevance_score,
                                             should_enqueue_dependency, is_dependency_critical)  # Relevance scoring utilities
from .intelligence_import_utils import extract_imported_modules  # Import analysis utilities
from .intelligence_llm_service import chat_llm  # Ollama integration for intelligent decisions

class Scout:
    def __init__(self, memory: MemoryInterface, working_directory: str):
        self.working_dir = working_directory
        self.memory = memory

    def scout_project(self, main_goal: str, current_turn: int) -> tuple[list[dict], list[str]]:
        # Handle case where main_goal is None to prevent AttributeError
        if main_goal is None:
            logging.warning("main_goal is None, defaulting to empty string")
            main_goal = ""

        logging.info(f"Starting goal-directed scout for goal: {main_goal}")

        # Query memory for relevant knowledge
        memory_results = self.memory.query_memory(main_goal, current_turn=current_turn, n_results=5)
        used_memory_ids = memory_results['ids'][0] if memory_results['ids'] else []
        memory_context = "\n".join(memory_results['documents'][0]) if memory_results['documents'] else ""

        # Extract keywords from goal and memory context for pre-filtering
        keywords = extract_keywords_from_goal(main_goal + " " + memory_context)
        logging.info(f"Extracted keywords: {keywords}")

        # Collect all .py modules in the project directory
        all_modules = collect_modules(self.working_dir)

        logging.info(f"Found {len(all_modules)} modules in project")

        # Start priority-based search from root module
        start_module = 'agent_graph_main'
        start_path = os.path.join(self.working_dir, 'agent_graph_main.py')
        if start_module not in all_modules:
            logging.error("Root module agent_graph_main.py not found")
            return []

        # Priority queue: (priority, depth, module_name, reason, path)
        # Lower priority number means higher priority
        priority_queue = [(0, 0, start_module, "entry point", start_path)]
        visited = set()
        backpack = []
        nodes_explored = 0

        while priority_queue and nodes_explored < config.MAX_SCOUT_NODES:
            _, depth, current_module, reason, current_path = heapq.heappop(priority_queue)

            if current_module in visited or depth > config.MAX_SCOUT_DEPTH:
                continue
            visited.add(current_module)
            nodes_explored += 1
            print(f"DEBUG: Marked '{current_module}' as visited (depth: {depth}, nodes: {nodes_explored})")

            logging.info(f"Visiting {current_module} for reason: {reason}")
            print(f"DEBUG: Visiting '{current_module}' for {reason}")
            print(f"DEBUG: Evaluating relevance of '{current_module}'")
            try:
                with open(current_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                # Keyword pre-filtering
                keyword_score = compute_keyword_score(keywords, code)
                print(f"DEBUG: Keyword score for '{current_module}': {keyword_score}")

                should_llm = keyword_score >= config.RELEVANCE_THRESHOLD // 2 or depth == 0
                llm_resp = get_scout_response(main_goal, current_path, code) if should_llm else {}
                llm_rel = llm_resp.get('relevant', False)
                comb_score = compute_combined_relevance_score(keyword_score, llm_rel, depth)
                if comb_score >= config.RELEVANCE_THRESHOLD or llm_rel:
                    print(f"DEBUG: Module '{current_module}' relevant (score: {comb_score}), adding to backpack")
                    backpack.append({
                        "file_path": current_path,
                        "justification": llm_resp.get('justification', f"Keyword score: {keyword_score}"),
                        "key_elements": llm_resp.get('key_elements', []),
                        "full_code": code
                    })
                    logging.debug(f"Relevant: {current_module}")
                else:
                    print(f"DEBUG: Module '{current_module}' not relevant (score: {comb_score})")
                    logging.debug(f"Not relevant: {current_module}")
            except Exception as e:
                logging.error(f"Error evaluating {current_module}: {e}")

            # Extract imported modules and decide which to visit next using LLM
            next_modules = extract_imported_modules(code, current_path, all_modules)
            print(f"DEBUG: Extracted imports from {current_module}: {next_modules}")

            # Use LLM to decide which modules to visit next and why
            modules_to_enqueue = decide_next_modules_to_visit(main_goal, current_module, current_path, code, next_modules, all_modules, keywords, depth)

            for mod_name, priority, reasoning in modules_to_enqueue:
                if mod_name not in visited and mod_name in all_modules:
                    dep_path = all_modules[mod_name]
                    heapq.heappush(priority_queue, (priority, depth + 1, mod_name, f"imported by {current_module} - {reasoning}", dep_path))
                    print(f"DEBUG: Enqueued '{mod_name}' with priority {priority} - {reasoning}")

        print(f"DEBUG: Goal-directed scout completed, backpack contains {len(backpack)} relevant modules")
        logging.info(f"Goal-directed scout completed: {len(backpack)} relevant modules in backpack (explored {nodes_explored} nodes)")
        return backpack, used_memory_ids

    def query(self, main_goal: str, subtask: str) -> tuple:
        # Combine main_goal and subtask for querying
        combined_goal = main_goal + " - " + subtask

        # Query memory for relevant knowledge
        memory_results = self.memory.query_memory(combined_goal, current_turn=0, n_results=5)
        used_memory_ids = memory_results['ids'][0] if memory_results['ids'] else []
        memory_context = "\n".join(memory_results['documents'][0]) if memory_results['documents'] else ""

        # Extract keywords from combined goal and memory context
        keywords = extract_keywords_from_goal(combined_goal + " " + memory_context)
        logging.info(f"Extracted keywords for query: {keywords}")

        # Collect all .py modules in the project directory
        all_modules = collect_modules(self.working_dir)

        # Filter relevant modules based on keywords
        backpack = []
        for mod_name, mod_path in all_modules.items():
            try:
                with open(mod_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                keyword_score = compute_keyword_score(keywords, code)
                if keyword_score >= config.RELEVANCE_THRESHOLD:
                    backpack.append({
                        "file_path": mod_path,
                        "justification": f"Keyword score: {keyword_score}",
                        "key_elements": [],
                        "full_code": code
                    })
                    logging.debug(f"Relevant module for query: {mod_name}")
            except Exception as e:
                logging.error(f"Error reading {mod_path} during query: {e}")

        # Generate response using LLM based on goal, subtask, and context
        prompt = f"Based on the main goal '{main_goal}' and subtask '{subtask}', using the memory context and relevant modules found, provide a response."
        prompt += f"\nMemory context: {memory_context[:500]}..."
        prompt += f"\nNumber of relevant modules: {len(backpack)}"
        try:
            response = chat_llm(prompt)
        except Exception as e:
            logging.error(f"Error generating response in query: {e}")
            response = f"Error generating response: {e}"

        return backpack, used_memory_ids, response



def decide_next_modules_to_visit(main_goal, current_module, current_path, current_code, available_modules, all_modules, keywords, depth):
    """Use Ollama to decide which modules to visit next based on the goal and current context."""
    if not available_modules:
        return []

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
        resp = chat_llm(prompt)
        resp = resp.strip().lstrip("```json").rstrip("```").strip()
        result = json.loads(resp)
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
    except (json.JSONDecodeError, Exception) as e:
        logging.error(f"LLM decision error: {e}")
        return [(m, 5, f"Fallback: {r}") for m, r in available_modules]


def get_scout_response(main_goal, file_path, file_content):
    """Use Ollama to determine file relevance and extract key elements based on the main goal."""
    prompt = f"""Analyze file {file_path} for goal "{main_goal}". Content: {file_content[:1000]}... Respond ONLY with the raw JSON object, without any introductory text, conversational pleasantries, or markdown formatting. Your entire response must be a single, valid JSON object: {{"relevant": true/false, "justification": "brief reason", "key_elements": ["important parts"]}}"""

    try:
        resp = chat_llm(prompt)
        resp = resp.strip().lstrip("```json").rstrip("```").strip()
        return json.loads(resp)
    except (json.JSONDecodeError, Exception) as e:
        logging.error(f"Scout LLM error: {e}")
        return {"relevant": False, "justification": f"LLM error: {e}", "key_elements": []}