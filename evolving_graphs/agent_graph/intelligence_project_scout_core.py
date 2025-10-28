import os  # File system operations for directory traversal and file reading
import heapq  # Priority queue for goal-directed traversal
import logging
from .memory_interface import MemoryInterface  # External memory interface for querying knowledge
from .agent_config import config  # Configuration settings for model selection and parameters
from .task_planner_graph import PlanGraph # Used for handling complex queries
from .utils_collect_modules import collect_modules  # To collect all Python modules in the project directory
from .intelligence_keyword_utils import extract_keywords_from_goal  # Keyword extraction utilities
from .intelligence_relevance_utils import compute_keyword_score  # Relevance scoring utilities
from .intelligence_import_utils import extract_imported_modules  # Import analysis utilities
from .scout_utils import (query_memory_for_goal, create_backpack_item, log_scout_progress, extract_keywords_and_compute_relevance)  # Scout utility functions
from .file_utils import read_file_for_analysis  # Safe file reading utilities
from .debug_utils import debug_print, log_error  # Debug logging utilities
from .intelligence_project_scout_utils import decide_next_modules_to_visit, get_scout_response  # Scout utility functions


class Scout:
    def __init__(self, memory: MemoryInterface, working_directory: str):
        self.working_dir = working_directory
        self.memory = memory

    def scout_project(self, main_goal: str, current_turn: int) -> tuple[list[dict], list[str]]:
        # Handle case where main_goal is None to prevent AttributeError
        if main_goal is None:
            log_scout_progress("main_goal is None, defaulting to empty string", "warning")
            main_goal = ""

        log_scout_progress(f"Starting goal-directed scout for goal: {main_goal}")

        # Query memory for relevant knowledge
        used_memory_ids, memory_context = query_memory_for_goal(self.memory, main_goal, current_turn, n_results=5)

        # Extract keywords from goal and memory context for pre-filtering
        keywords = extract_keywords_from_goal(main_goal + " " + memory_context)
        log_scout_progress(f"Extracted keywords: {keywords}")

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
            debug_print(f"Marked '{current_module}' as visited (depth: {depth}, nodes: {nodes_explored})")

            log_scout_progress(f"Visiting {current_module} for reason: {reason}")
            debug_print(f"Visiting '{current_module}' for {reason}")
            debug_print(f"Evaluating relevance of '{current_module}'")
            try:
                code = read_file_for_analysis(current_path)

                # Keyword pre-filtering
                keyword_score, comb_score = extract_keywords_and_compute_relevance(keywords, code, depth)
                debug_print(f"Keyword score for '{current_module}': {keyword_score}")

                should_llm = keyword_score >= config.RELEVANCE_THRESHOLD // 2 or depth == 0
                llm_resp = get_scout_response(main_goal, current_path, code) if should_llm else {}
                llm_rel = llm_resp.get('relevant', False)

                # Update combined score if we have LLM response
                if should_llm:
                    from .intelligence_relevance_utils import compute_combined_relevance_score
                    comb_score = compute_combined_relevance_score(keyword_score, llm_rel, depth)

                if comb_score >= config.RELEVANCE_THRESHOLD or llm_rel:
                    debug_print(f"Module '{current_module}' relevant (score: {comb_score}), adding to backpack")
                    backpack_item = create_backpack_item(
                        current_path,
                        llm_resp.get('justification', f"Keyword score: {keyword_score}"),
                        llm_resp,
                        code
                    )
                    backpack.append(backpack_item)
                    log_scout_progress(f"Relevant: {current_module}", "debug")
                else:
                    debug_print(f"Module '{current_module}' not relevant (score: {comb_score})")
                    log_scout_progress(f"Not relevant: {current_module}", "debug")
            except Exception as e:
                log_error(f"Error evaluating {current_module}: {e}")

            # Extract imported modules and decide which to visit next using LLM
            next_modules = extract_imported_modules(code, current_path, all_modules)
            debug_print(f"Extracted imports from {current_module}: {next_modules}")

            # Use LLM to decide which modules to visit next and why
            modules_to_enqueue = decide_next_modules_to_visit(main_goal, current_module, current_path, code, next_modules, all_modules, keywords, depth)

            for mod_name, priority, reasoning in modules_to_enqueue:
                if mod_name not in visited and mod_name in all_modules:
                    dep_path = all_modules[mod_name]
                    heapq.heappush(priority_queue, (priority, depth + 1, mod_name, f"imported by {current_module} - {reasoning}", dep_path))
                    debug_print(f"Enqueued '{mod_name}' with priority {priority} - {reasoning}")

        debug_print(f"Goal-directed scout completed, backpack contains {len(backpack)} relevant modules")
        log_scout_progress(f"Goal-directed scout completed: {len(backpack)} relevant modules in backpack (explored {nodes_explored} nodes)")
        return backpack, used_memory_ids

    def query(self, main_goal: str, plan: PlanGraph) -> tuple:
        for task in plan.get_pending_actions_for_role("scout"):
            # Use task.justification as subtask description instead of str(task.command)
            # to avoid passing large command dictionaries as query strings
            subtask_description = task.justification if task.justification else str(task.command)

            # Combine main_goal and subtask for querying
            combined_goal = main_goal + " - " + subtask_description

            # Query memory for relevant knowledge
            used_memory_ids, memory_context = query_memory_for_goal(self.memory, combined_goal, current_turn=0, n_results=5)

            # Extract keywords from combined goal and memory context
            keywords = extract_keywords_from_goal(combined_goal + " " + memory_context)
            log_scout_progress(f"Extracted keywords for query: {keywords}")

            # Collect all .py modules in the project directory
            all_modules = collect_modules(self.working_dir)

            # Filter relevant modules based on keywords
            backpack = []
            for mod_name, mod_path in all_modules.items():
                try:
                    code = read_file_for_analysis(mod_path)

                    keyword_score = compute_keyword_score(keywords, code)
                    if keyword_score >= config.RELEVANCE_THRESHOLD:
                        backpack_item = create_backpack_item(
                            mod_path,
                            f"Keyword score: {keyword_score}",
                            {},  # No LLM response for query method
                            code
                        )
                        backpack.append(backpack_item)
                        log_scout_progress(f"Relevant module for query: {mod_name}", "debug")
                except Exception as e:
                    log_error(f"Error reading {mod_path} during query: {e}")

            # Generate response using LLM based on goal, subtask, and context
            from .llm_utils import make_llm_call_with_fallback
            prompt = f"Based on the main goal '{main_goal}' and subtask '{subtask_description}', using the memory context and relevant modules found, provide a response."
            prompt += f"\nMemory context: {memory_context[:500]}..."
            prompt += f"\nNumber of relevant modules: {len(backpack)}"
            try:
                response = make_llm_call_with_fallback(prompt)
            except Exception as e:
                log_error(f"Error generating response in query: {e}")
                response = f"Error generating response: {e}"

        return backpack, used_memory_ids, response