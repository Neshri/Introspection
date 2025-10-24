import os  # File system operations for directory traversal and file reading
import ast  # Abstract syntax tree parsing for code analysis and element extraction
import json  # JSON handling for data serialization
import re  # Regular expressions for extracting JSON from markdown blocks
import logging  # Logging for debugging and progress tracking
import ollama  # LLM interface for semantic analysis of code relevance
from .intelligence_llm_service import chat_llm  # Standardized LLM service
from .agent_config import config  # Configuration settings for model selection and parameters

class Scout:
    def scout_project(self, main_goal: str) -> list[dict]:
        # Handle case where main_goal is None to prevent AttributeError
        if main_goal is None:
            logging.warning("main_goal is None, defaulting to empty string")
            main_goal = ""

        logging.info(f"Starting scout for goal: {main_goal}")

        # Extract keywords from goal using improved method
        keywords = self._extract_keywords_from_goal(main_goal)
        logging.info(f"Extracted keywords: {keywords}")

        # Traverse ./AgentTree/ for .py files
        py_files = []
        for root, dirs, files in os.walk('./AgentTree/'):
            for file in files:
                if file.endswith('.py'):
                    py_files.append(os.path.join(root, file))

        logging.info(f"Found {len(py_files)} Python files to analyze")

        # Phase 1: Syntactic Filtering (relaxed)
        candidates = []
        for file_path in py_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                tree = ast.parse(code)
                elements = self._extract_elements(tree)
                elements_str = ' '.join(elements).lower()

                # More permissive matching: check if any keyword appears anywhere in elements
                if any(keyword in elements_str for keyword in keywords):
                    candidates.append(file_path)
                    logging.debug(f"Phase 1 candidate: {file_path}")
            except Exception as e:
                logging.warning(f"Failed to parse {file_path}: {e}")
                continue

        logging.info(f"Phase 1 filtering: {len(candidates)} candidates from {len(py_files)} files")

        # Phase 2: Deep Semantic Analysis with structured JSON
        results = []
        for file_path in candidates:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                response_json = get_scout_response(main_goal, file_path, code)
                if response_json.get('relevant', False):
                    results.append({
                        "file_path": file_path,
                        "justification": response_json.get('justification', 'No justification provided'),
                        "key_elements": response_json.get('key_elements', []),
                        "full_code": code
                    })
                    logging.debug(f"Phase 2 relevant: {file_path}")
                else:
                    logging.debug(f"Phase 2 not relevant: {file_path}")
            except Exception as e:
                logging.error(f"Error in Phase 2 for {file_path}: {e}")
                continue

        logging.info(f"Phase 2 analysis: {len(results)} relevant files found")
        return results

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