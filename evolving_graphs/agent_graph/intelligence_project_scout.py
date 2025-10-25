import os  # File system operations for directory traversal and file reading
import logging  # Logging for debugging and progress tracking
import heapq  # Priority queue for goal-directed traversal
from .agent_config import config  # Configuration settings for model selection and parameters
from .utils_collect_modules import collect_modules  # To collect all Python modules in the project directory
from .intelligence_keyword_utils import extract_keywords_from_goal  # Keyword extraction utilities
from .intelligence_relevance_utils import (compute_keyword_score, compute_combined_relevance_score,
                                            should_enqueue_dependency, is_dependency_critical)  # Relevance scoring utilities
from .intelligence_import_utils import extract_imported_modules  # Import analysis utilities

class Scout:
    def __init__(self):
        self.working_dir = None

    def set_working_directory(self, candidate_path: str):
        """Set the working directory to the candidate path for scouting."""
        self.working_dir = candidate_path

    def scout_project(self, main_goal: str) -> list[dict]:
        # Handle case where main_goal is None to prevent AttributeError
        if main_goal is None:
            logging.warning("main_goal is None, defaulting to empty string")
            main_goal = ""

        logging.info(f"Starting goal-directed scout for goal: {main_goal}")

        # Extract keywords from goal for pre-filtering
        keywords = extract_keywords_from_goal(main_goal)
        logging.info(f"Extracted keywords: {keywords}")

        # Collect all .py modules in the project directory
        if not self.working_dir:
            raise ValueError("Working directory not set. Call set_working_directory first.")
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
            print(f"DEBUG: Visiting module '{current_module}' for reason: {reason}")

            # Evaluate relevance using LLM
            print(f"DEBUG: Evaluating relevance of '{current_module}'")
            try:
                with open(current_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                # Keyword pre-filtering
                keyword_score = compute_keyword_score(keywords, code)
                print(f"DEBUG: Keyword score for '{current_module}': {keyword_score}")

                # Only proceed with LLM if keyword score is above threshold or it's critical
                should_evaluate_llm = keyword_score >= config.RELEVANCE_THRESHOLD // 2 or depth == 0

                llm_relevant = False
                if should_evaluate_llm:
                    response_json = get_scout_response(main_goal, current_path, code)
                    llm_relevant = response_json.get('relevant', False)

                combined_score = compute_combined_relevance_score(keyword_score, llm_relevant, depth)

                if combined_score >= config.RELEVANCE_THRESHOLD or llm_relevant:
                    print(f"DEBUG: Module '{current_module}' is relevant (score: {combined_score}), adding to backpack")
                    backpack.append({
                        "file_path": current_path,
                        "justification": response_json.get('justification', 'Keyword-based relevance') if should_evaluate_llm else f"Keyword score: {keyword_score}",
                        "key_elements": response_json.get('key_elements', []) if should_evaluate_llm else [],
                        "full_code": code
                    })
                    logging.debug(f"Relevant: {current_module}")
                else:
                    print(f"DEBUG: Module '{current_module}' is not relevant (score: {combined_score})")
                    logging.debug(f"Not relevant: {current_module}")
            except Exception as e:
                logging.error(f"Error evaluating {current_module}: {e}")

            # Extract imported modules and enqueue based on priority
            next_modules = extract_imported_modules(code, current_path, all_modules)
            print(f"DEBUG: Extracted imports from {current_module}: {next_modules}")
            for mod_name, import_reason in next_modules:
                if mod_name not in visited and mod_name in all_modules:
                    # Compute priority for dependency
                    dep_path = all_modules[mod_name]
                    try:
                        with open(dep_path, 'r', encoding='utf-8') as f:
                            dep_code = f.read()
                        dep_keyword_score = compute_keyword_score(keywords, dep_code)
                        print(f"DEBUG: Keyword score for dependency '{mod_name}': {dep_keyword_score}")
                        dep_combined_score = compute_combined_relevance_score(dep_keyword_score, False, depth + 1)  # Assume not LLM relevant yet
                        print(f"DEBUG: Combined score for dependency '{mod_name}': {dep_combined_score}")
                        if should_enqueue_dependency(dep_combined_score, depth + 1):
                            # Priority is negative score (higher score = lower priority number)
                            priority = -dep_combined_score if is_dependency_critical(dep_combined_score) else -dep_combined_score + 10
                            heapq.heappush(priority_queue, (priority, depth + 1, mod_name, f"imported by {current_module} ({import_reason})", dep_path))
                            print(f"DEBUG: Enqueued '{mod_name}' with priority {priority}")
                        else:
                            print(f"DEBUG: Not enqueuing '{mod_name}' (score: {dep_combined_score}, depth: {depth + 1})")
                    except Exception as e:
                        logging.warning(f"Could not read dependency {mod_name}: {e}")

        print(f"DEBUG: Goal-directed scout completed, backpack contains {len(backpack)} relevant modules")
        logging.info(f"Goal-directed scout completed: {len(backpack)} relevant modules in backpack (explored {nodes_explored} nodes)")
        return backpack

        

def get_scout_response(main_goal, file_path, file_content):
    """Mocked version for testing - returns relevance based on file path keywords."""
    # Mock response based on file name and goal keywords
    filename = file_path.lower()
    goal_lower = main_goal.lower()

    # Check if file name contains goal keywords
    relevant_keywords = ['code', 'execution', 'executor', 'intelligence_code_executor', 'pipeline_pipeline_executor']
    is_relevant = any(keyword in filename for keyword in relevant_keywords)

    return {
        "relevant": is_relevant,
        "justification": f"Mock relevance based on filename '{filename}' matching goal keywords",
        "key_elements": ["mock_function_1", "mock_class_1"] if is_relevant else []
    }