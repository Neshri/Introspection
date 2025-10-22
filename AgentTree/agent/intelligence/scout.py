import os  # File system operations for directory traversal and file reading
import ast  # Abstract syntax tree parsing for code analysis and element extraction
import json  # JSON handling for data serialization (not currently used but may be needed)
import ollama  # LLM interface for semantic analysis of code relevance
from agent.utils import config  # Configuration settings for model selection and parameters

class Scout:
    def scout_project(self, goal: str) -> list[dict]:
        # Extract keywords from goal
        keywords = set(goal.lower().split())

        # Traverse ./AgentTree/ for .py files
        py_files = []
        for root, dirs, files in os.walk('./AgentTree/'):
            for file in files:
                if file.endswith('.py'):
                    py_files.append(os.path.join(root, file))

        # Phase 1: Syntactic Filtering
        candidates = []
        for file_path in py_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                tree = ast.parse(code)
                elements = self._extract_elements(tree)
                if any(keyword in ' '.join(elements).lower() for keyword in keywords):
                    candidates.append(file_path)
            except:
                continue

        # Phase 2: Deep Semantic Analysis
        results = []
        for file_path in candidates:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            prompt = f"""
Analyze if the following Python code is relevant to achieving the goal: "{goal}"

Code:
{code}

Respond with 'Yes' or 'No' followed by a brief justification.
"""
            response = ollama.chat(model=config.MODEL, messages=[{'role': 'user', 'content': prompt}])
            answer = response['message']['content'].strip().lower()
            if answer.startswith('yes'):
                justification = answer[3:].strip() if len(answer) > 3 else "Relevant based on semantic analysis."
                results.append({
                    "file_path": file_path,
                    "justification": justification,
                    "full_code": code
                })

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
        return elements

def get_scout_response(goal, file_path, file_content):
    """Generates a JSON response from the Scout prompt for analyzing code relevance."""
    prompt = config.SCOUT_PROMPT_TEMPLATE.format(goal=goal, file_path=file_path, file_content=file_content)
    response = ollama.chat(model=config.MODEL, messages=[{'role': 'user', 'content': prompt}])
    try:
        # Parse the JSON response from the LLM
        import json  # JSON parsing for LLM response validation
        json_response = json.loads(response['message']['content'].strip())
        return json_response
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "relevant": False,
            "justification": "Failed to parse LLM response as JSON",
            "key_elements": []
        }