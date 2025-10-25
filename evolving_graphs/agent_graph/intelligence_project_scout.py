import os  # File system operations for directory traversal and file reading
import ast  # Abstract syntax tree parsing for code analysis and element extraction
import json  # JSON handling for data serialization
import re  # Regular expressions for extracting JSON from markdown blocks
import logging  # Logging for debugging and progress tracking
import heapq  # Priority queue for goal-directed traversal
# import ollama  # LLM interface for semantic analysis of code relevance - mocked for testing
# from .intelligence_llm_service import chat_llm  # Standardized LLM service - mocked for testing
from .agent_config import config  # Configuration settings for model selection and parameters
from .utils_collect_modules import collect_modules  # To collect all Python modules in the project directory

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
        keywords = self._extract_keywords_from_goal(main_goal)
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
                keyword_score = self._compute_keyword_score(keywords, code)
                print(f"DEBUG: Keyword score for '{current_module}': {keyword_score}")

                # Only proceed with LLM if keyword score is above threshold or it's critical
                should_evaluate_llm = keyword_score >= config.RELEVANCE_THRESHOLD // 2 or depth == 0

                llm_relevant = False
                if should_evaluate_llm:
                    response_json = get_scout_response(main_goal, current_path, code)
                    llm_relevant = response_json.get('relevant', False)

                combined_score = self._compute_combined_relevance_score(keyword_score, llm_relevant, depth)

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
            next_modules = self._extract_imported_modules(code, current_path, all_modules)
            print(f"DEBUG: Extracted imports from {current_module}: {next_modules}")
            for mod_name, import_reason in next_modules:
                if mod_name not in visited and mod_name in all_modules:
                    # Compute priority for dependency
                    dep_path = all_modules[mod_name]
                    try:
                        with open(dep_path, 'r', encoding='utf-8') as f:
                            dep_code = f.read()
                        dep_keyword_score = self._compute_keyword_score(keywords, dep_code)
                        print(f"DEBUG: Keyword score for dependency '{mod_name}': {dep_keyword_score}")
                        dep_combined_score = self._compute_combined_relevance_score(dep_keyword_score, False, depth + 1)  # Assume not LLM relevant yet
                        print(f"DEBUG: Combined score for dependency '{mod_name}': {dep_combined_score}")
                        if self._should_enqueue_dependency(dep_combined_score, depth + 1):
                            # Priority is negative score (higher score = lower priority number)
                            priority = -dep_combined_score if self._is_dependency_critical(dep_combined_score) else -dep_combined_score + 10
                            heapq.heappush(priority_queue, (priority, depth + 1, mod_name, f"imported by {current_module} ({import_reason})", dep_path))
                            print(f"DEBUG: Enqueued '{mod_name}' with priority {priority}")
                        else:
                            print(f"DEBUG: Not enqueuing '{mod_name}' (score: {dep_combined_score}, depth: {depth + 1})")
                    except Exception as e:
                        logging.warning(f"Could not read dependency {mod_name}: {e}")

        print(f"DEBUG: Goal-directed scout completed, backpack contains {len(backpack)} relevant modules")
        logging.info(f"Goal-directed scout completed: {len(backpack)} relevant modules in backpack (explored {nodes_explored} nodes)")
        return backpack

    def _extract_imported_modules(self, code, current_path, all_modules):

        current_rel_path = os.path.relpath(current_path, self.working_dir)
        current_module = current_rel_path.replace(os.sep, '.').replace('.py', '')
        current_package_parts = current_module.split('.')[:-1]

        imported = set()
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        level = node.level if hasattr(node, 'level') and node.level else 0
                        mod_name = node.module
                        if level == 0:
                            possible = [mod_name, mod_name.split('.')[-1]]
                        elif level == 1:
                            possible = ['.'.join(current_package_parts + [mod_name]), mod_name]
                        elif level == 2:
                            parent_parts = current_package_parts[:-1] if len(current_package_parts) > 0 else []
                            possible = ['.'.join(parent_parts + [mod_name]), mod_name]
                        else:
                            possible = [mod_name]
                        for p in possible:
                            if p in all_modules:
                                imported.add((p, f"imported {node.module}"))
                                break
        except Exception as e:
            logging.warning(f"Failed to parse imports in {current_path}: {e}")
        return list(imported)

    def _extract_elements(self, tree):
        elements = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                elements.append(node.name)
            elif isinstance(node, ast.ClassDef):
                elements.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    elements.append(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    elements.append(node.module.split('.')[0])
                for alias in node.names:
                    elements.append(alias.name)
        return elements

    def _extract_keywords_from_goal(self, goal: str) -> set:
        """Extract meaningful keywords from goal, including action words and reducing stop word filtering."""
        if not goal:
            return set()

        # Reduced stop words - keep action words and important connectors
        stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'in', 'on', 'at', 'to', 'from', 'by', 'with', 'as', 'for', 'of'
        }

        # Action words to prioritize
        action_words = {
            'improve', 'enhance', 'fix', 'add', 'remove', 'update', 'optimize',
            'refactor', 'implement', 'create', 'build', 'test', 'debug', 'analyze',
            'design', 'plan', 'execute', 'run', 'start', 'stop', 'load', 'save',
            'process', 'handle', 'manage', 'monitor', 'validate', 'check'
        }

        # Split and clean words
        words = goal.lower().split()
        keywords = set()

        for word in words:
            # Remove punctuation
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 1 and clean_word not in stop_words:
                keywords.add(clean_word)

        # Add synonyms if enabled
        if config.ENABLE_SYNONYM_EXPANSION:
            keywords.update(self._expand_synonyms(keywords))

        return keywords

    def _expand_synonyms(self, keywords: set) -> set:
        """Expand keywords with synonyms for goal terms."""
        synonyms = {
            'stability': ['reliability', 'robustness', 'resilience', 'durability'],
            'performance': ['speed', 'efficiency', 'optimization'],
            'security': ['protection', 'safety', 'encryption'],
            'reliability': ['stability', 'robustness', 'dependability'],
            'efficiency': ['performance', 'optimization', 'speed'],
            'robustness': ['stability', 'reliability', 'resilience'],
            'logging': ['log', 'trace', 'monitor', 'track'],
            'error': ['exception', 'failure', 'bug', 'issue'],
            'test': ['testing', 'validation', 'verification'],
            'code': ['implementation', 'logic', 'algorithm'],
            'execution': ['run', 'execute', 'process', 'handle']
        }

        expanded = set()
        for keyword in keywords:
            expanded.add(keyword)
            if keyword in synonyms:
                expanded.update(synonyms[keyword])
        return expanded

    def _compute_keyword_score(self, keywords: set, code: str) -> int:
        """Compute multi-level keyword-based relevance score with exact, partial matches, and context bonuses."""
        score = 0
        code_lower = code.lower()

        for keyword in keywords:
            keyword_lower = keyword.lower()
            exact_match = keyword_lower in code_lower

            if exact_match:
                score += 10  # Higher base score for exact matches
                # Additional points for multiple occurrences
                occurrences = code_lower.count(keyword_lower)
                score += min(occurrences - 1, 5)
            else:
                # Check for partial matches (substrings)
                partial_found = False
                for i in range(len(keyword_lower) - 2):  # At least 3 chars
                    substring = keyword_lower[i:i+3]
                    if substring in code_lower:
                        score += 3  # Partial match bonus
                        partial_found = True
                        break
                if not partial_found:
                    # Check camelCase/snake_case variations if enabled
                    if config.ENABLE_CASE_VARIATIONS:
                        variations = self._generate_case_variations(keyword)
                        for variation in variations:
                            if variation in code:
                                score += 8  # Case variation bonus
                                break

            # Context pattern matching bonus if enabled
            if config.ENABLE_CONTEXT_PATTERN_MATCHING and exact_match:
                context_bonus = self._compute_context_bonus(keyword, code)
                score += context_bonus

        return score

    def _generate_case_variations(self, keyword: str) -> list:
        """Generate camelCase and snake_case variations of a keyword."""
        variations = []

        # Convert to snake_case: stability -> stability, improve_stability -> improve_stability
        snake_case = keyword.replace('-', '_').lower()
        variations.append(snake_case)

        # Convert to camelCase: stability -> stability, improve_stability -> improveStability
        if '_' in keyword:
            parts = keyword.split('_')
            camel = parts[0] + ''.join(word.capitalize() for word in parts[1:])
            variations.append(camel)
        else:
            variations.append(keyword)  # Already might be camelCase

        # Convert from camelCase to snake_case
        import re
        # stability -> stability
        # improveStability -> improve_stability
        snake_from_camel = re.sub(r'(?<!^)(?=[A-Z])', '_', keyword).lower()
        if snake_from_camel != keyword.lower():
            variations.append(snake_from_camel)

        return variations

    def _compute_context_bonus(self, keyword: str, code: str) -> int:
        """Compute context bonus based on keyword surroundings."""
        bonus = 0
        code_lower = code.lower()
        keyword_lower = keyword.lower()

        # Look for keyword in function/class names, comments, docstrings
        lines = code.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            if keyword_lower in line_lower:
                # Bonus for comments/docstrings
                if line_lower.startswith('#') or '"""' in line_lower or "'''" in line_lower:
                    bonus += 2
                # Bonus for function/class definitions
                elif 'def ' in line_lower or 'class ' in line_lower:
                    bonus += 3
                # Bonus for variable names
                elif '=' in line and keyword_lower in line_lower.split('=')[0]:
                    bonus += 1

        return min(bonus, 5)  # Cap context bonus

    def _compute_combined_relevance_score(self, keyword_score: int, llm_relevance: bool, depth: int) -> int:
        """Compute combined relevance score using keyword score, LLM relevance, and depth."""
        base_score = keyword_score * 1.5  # Weight keyword scores higher
        if llm_relevance:
            base_score += config.RELEVANCE_THRESHOLD * 2
        base_score -= depth * 1  # Reduce depth penalty for early exploration
        return max(0, base_score)

    def _should_enqueue_dependency(self, score: int, depth: int) -> bool:
        """Determine if a dependency should be enqueued based on score and depth."""
        # Allow exploration even with lower scores, but prioritize higher ones
        return (score >= config.RELEVANCE_THRESHOLD // 2 or depth <= 1) and depth < config.MAX_SCOUT_DEPTH

    def _is_dependency_critical(self, score: int) -> bool:
        """Determine if a dependency is critical based on its relevance score."""
        return score > config.RELEVANCE_THRESHOLD * 1.5
        

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