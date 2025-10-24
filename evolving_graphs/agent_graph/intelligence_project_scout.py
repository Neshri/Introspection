import os  # File system operations for directory traversal and file reading
import ast  # Abstract syntax tree parsing for code analysis and element extraction
import json  # JSON handling for data serialization
import re  # Regular expressions for extracting JSON from markdown blocks
import logging  # Logging for debugging and progress tracking
import ollama  # LLM interface for semantic analysis of code relevance
from .intelligence_llm_service import chat_llm  # Standardized LLM service
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

        logging.info(f"Starting BFS scout for goal: {main_goal}")

        # Collect all .py modules in the project directory
        if not self.working_dir:
            raise ValueError("Working directory not set. Call set_working_directory first.")
        all_modules = collect_modules(self.working_dir)

        logging.info(f"Found {len(all_modules)} modules in project")

        # Start BFS from root module
        start_module = 'agent_graph_main'
        start_path = os.path.join(self.working_dir, 'agent_graph_main.py')
        if start_module not in all_modules:
            logging.error("Root module agent_graph_main.py not found")
            return []

        queue = [(start_module, "entry point", start_path)]  # (module_name, reason, path)
        visited = set()
        backpack = []

        while queue:
            current_module, reason, current_path = queue.pop(0)
            if current_module in visited:
                continue
            visited.add(current_module)
            print(f"DEBUG: Marked '{current_module}' as visited")

            logging.info(f"Visiting {current_module} for reason: {reason}")
            print(f"DEBUG: Visiting module '{current_module}' for reason: {reason}")

            # Evaluate relevance using LLM
            print(f"DEBUG: Evaluating relevance of '{current_module}'")
            try:
                with open(current_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                response_json = get_scout_response(main_goal, current_path, code)
                if response_json.get('relevant', False):
                    print(f"DEBUG: Module '{current_module}' is relevant, adding to backpack")
                    backpack.append({
                        "file_path": current_path,
                        "justification": response_json.get('justification', 'No justification provided'),
                        "key_elements": response_json.get('key_elements', []),
                        "full_code": code
                    })
                    logging.debug(f"Relevant: {current_module}")
                else:
                    print(f"DEBUG: Module '{current_module}' is not relevant")
                    logging.debug(f"Not relevant: {current_module}")
            except Exception as e:
                logging.error(f"Error evaluating {current_module}: {e}")

            # Extract imported modules and add to queue
            next_modules = self._extract_imported_modules(code, current_path, all_modules)
            print(f"DEBUG: Extracted imports from {current_module}: {next_modules}")
            for mod_name, import_reason in next_modules:
                if mod_name not in visited and mod_name in all_modules:
                    print(f"DEBUG: Enqueuing next module '{mod_name}' (imported by {current_module})")
                    queue.append((mod_name, f"imported by {current_module} ({import_reason})", all_modules[mod_name]))

        print(f"DEBUG: BFS completed, backpack contains {len(backpack)} relevant modules")
        logging.info(f"BFS completed: {len(backpack)} relevant modules in backpack")
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
        """Extract meaningful keywords from goal, filtering out stop words and punctuation."""
        if not goal:
            return set()

        # Common stop words to filter out
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'when', 'where', 'who', 'why'
        }

        # Split and clean words
        words = goal.lower().split()
        keywords = set()

        for word in words:
            # Remove punctuation and filter short words
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 2 and clean_word not in stop_words:
                keywords.add(clean_word)

        return keywords
        

def get_scout_response(main_goal, file_path, file_content):
    """Generates a JSON response from the Scout prompt for analyzing code relevance."""
    try:
        prompt = config.SCOUT_PROMPT_TEMPLATE.format(goal=main_goal, file_path=file_path, file_content=file_content)
        content = chat_llm(prompt)
        logging.debug(f"LLM response for {file_path}: {content[:200]}...")

        # Try direct JSON parsing first
        try:
            json_response = json.loads(content)
            return json_response
        except json.JSONDecodeError:
            # Attempt to extract JSON from markdown code blocks
            logging.debug(f"Direct JSON parsing failed for {file_path}, attempting extraction from markdown blocks")
            match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
            if match:
                extracted_json = match.group(1).strip()
                try:
                    json_response = json.loads(extracted_json)
                    logging.info(f"Successfully extracted and parsed JSON from markdown block for {file_path}")
                    return json_response
                except json.JSONDecodeError as extract_e:
                    logging.warning(f"Failed to parse extracted JSON from markdown block for {file_path}: {extract_e}")
            else:
                logging.warning(f"No ```json markdown code block found in LLM response for {file_path}")
            # Fall back to default response if parsing fails
            return {
                "relevant": False,
                "justification": "Failed to parse LLM response as JSON, including after attempting extraction from markdown code blocks",
                "key_elements": []
            }
    except Exception as e:
        logging.error(f"Error getting scout response for {file_path}: {e}")
        return {
            "relevant": False,
            "justification": f"Error during LLM call: {e}",
            "key_elements": []
        }