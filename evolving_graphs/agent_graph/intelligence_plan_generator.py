import json  # JSON handling for structured plan output
import ollama  # LLM interface for generating plans based on goals and context
import re # Make sure to import the regular expression module at the top of the file
import os  # File system operations for path handling
from .intelligence_llm_service import chat_llm  # Standardized LLM service
from .agent_config import config  # Configuration settings for model selection and prompt templates
from .utils_collect_modules import collect_modules  # Utility to collect all Python modules in project


class Planner:
    """
    The Planner class creates structured plans to achieve programming goals.
    It uses a hierarchical, Map-Reduce strategy to handle large contexts, first generating
    insights from batches of files and then synthesizing them into a final, coherent plan.
    Additionally, it validates and corrects file references in generated plans to ensure
    they match the actual project structure and follow architectural rules.
    """

    def _generate_insights_from_batch(self, main_goal: str, batch_context: str) -> str:
        """(Map Phase) Generates insights for a single batch of files."""
        print(f"DEBUG: Generating insights for a batch of size {len(batch_context)}")
        prompt = config.PLANNER_INSIGHT_PROMPT_TEMPLATE.format(
            goal=main_goal,
            backpack_context=batch_context
        )
        return chat_llm(prompt)

    def _synthesize_plan_from_insights(self, main_goal: str, insights: list[str]) -> str:
        """(Reduce Phase) Synthesizes a final plan from a collection of insights."""
        print("DEBUG: Synthesizing final plan from all generated insights...")
        formatted_insights = "\n---\n".join(insights)
        prompt = config.PLANNER_SYNTHESIS_PROMPT_TEMPLATE.format(
            goal=main_goal,
            insights=formatted_insights
        )

        llm_output = chat_llm(prompt)
        print(f"DEBUG: LLM generated raw output: {llm_output[:120]}...")

        # --- NEW: Add this cleanup block ---
        # Robustly find and extract JSON from within markdown fences
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", llm_output, re.DOTALL)
        if json_match:
            print("DEBUG: Extracted JSON from markdown block.")
            plan = json_match.group(1)
        else:
            # If no markdown block is found, assume the output is already clean JSON
            plan = llm_output
        # --- End of cleanup block ---

        # Now, validate the cleaned plan
        try:
            json.loads(plan)
            print("DEBUG: Generated plan is valid JSON")
            return plan
        except json.JSONDecodeError:
            print("DEBUG: Plan JSON validation failed, wrapping in basic structure")
            return json.dumps({
                "goal": main_goal,
                "steps": [f"LLM produced non-JSON plan after cleanup attempt: {plan}"],
                "estimated_complexity": "high",
                "risk_assessment": "Failed to synthesize a structured plan from insights. The LLM's output was not valid JSON even after cleanup."
            })

    def create_plan(self, main_goal: str, backpack: list[dict]) -> str:
        """
        Generates a structured plan by breaking down a large context into manageable parts.

        Args:
            main_goal (str): The programming goal to achieve.
            backpack (list[dict]): List of relevant files with their content and justification.

        Returns:
            str: A structured plan in JSON format containing steps to achieve the goal.
        """
        print(f"DEBUG: Planner received goal: {main_goal}")
        print(f"DEBUG: Planner received backpack with {len(backpack)} items. Starting hierarchical planning.")

        if not backpack:
            print("DEBUG: Backpack is empty. Creating a simple plan based on goal alone.")
            return self._synthesize_plan_from_insights(main_goal, ["No file context was provided."])

        # Batch files to respect the context limit
        batches = []
        current_batch_content = ""
        current_batch_size = 0

        for item in backpack:
            item_content = f"File: {item['file_path']}\nJustification: {item['justification']}\nContent:\n{item['full_code']}\n\n"
            item_size = len(item_content)

            if current_batch_size + item_size > config.CONTEXT_LIMIT:
                if current_batch_content:
                    batches.append(current_batch_content)
                current_batch_content = item_content
                current_batch_size = item_size
            else:
                current_batch_content += item_content
                current_batch_size += item_size
        
        if current_batch_content:
            batches.append(current_batch_content)

        print(f"DEBUG: Split {len(backpack)} files into {len(batches)} batches for processing.")

        # --- MAP PHASE ---
        # Generate insights from each batch of files
        all_insights = []
        for i, batch in enumerate(batches):
            print(f"DEBUG: Processing batch {i + 1}/{len(batches)}...")
            insight = self._generate_insights_from_batch(main_goal, batch)
            all_insights.append(insight)
            print(f"DEBUG: Insight for batch {i + 1}: {insight[:100]}...")

        # --- REDUCE PHASE ---
        # Synthesize a single plan from all the generated insights
        final_plan = self._synthesize_plan_from_insights(main_goal, all_insights)

        # --- VALIDATION PHASE ---
        # Validate and correct file references in the generated plan
        final_plan = self._validate_and_correct_plan(final_plan)

        print(f"DEBUG: Returning final plan with length: {len(final_plan)}")
        return final_plan

    def _validate_and_correct_plan(self, plan_json_str: str) -> str:
        """
        Validates file references in the generated plan against the actual project structure
        and corrects any incorrect file names or paths. Ensures relative paths and architectural compliance.

        Args:
            plan_json_str (str): The JSON plan string from synthesis phase.

        Returns:
            str: The corrected JSON plan string with valid file references.
        """
        print("DEBUG: Starting plan validation and correction...")

        try:
            plan_dict = json.loads(plan_json_str)
        except json.JSONDecodeError:
            print("DEBUG: Plan JSON validation failed during correction, returning original")
            return plan_json_str

        # Collect current project modules for validation
        # Use the working directory from Scout if available, otherwise use current directory
        # For now, assume we're in the agent_graph directory, so go up two levels to project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        all_modules = collect_modules(project_root)

        # Extract filename mappings for quick lookup
        filename_to_path = {}
        for module_name, path in all_modules.items():
            filename = os.path.basename(path)
            filename_to_path[filename] = path
            # Also map without extension for easier matching
            filename_to_path[filename.replace('.py', '')] = path

        # Check and correct key_files_to_modify if present
        if 'key_files_to_modify' in plan_dict and isinstance(plan_dict['key_files_to_modify'], list):
            corrected_files = []
            for file_ref in plan_dict['key_files_to_modify']:
                corrected_file = self._correct_file_reference(file_ref, filename_to_path, project_root)
                if corrected_file:
                    corrected_files.append(corrected_file)
                else:
                    print(f"DEBUG: Could not correct file reference: {file_ref}")
            plan_dict['key_files_to_modify'] = corrected_files

        # Check and correct file references in steps
        if 'steps' in plan_dict and isinstance(plan_dict['steps'], list):
            corrected_steps = []
            for step in plan_dict['steps']:
                if isinstance(step, str):
                    corrected_step = self._correct_file_references_in_text(step, filename_to_path, project_root)
                    corrected_steps.append(corrected_step)
            plan_dict['steps'] = corrected_steps

        # Convert back to JSON string
        try:
            corrected_plan_json = json.dumps(plan_dict)
            print("DEBUG: Plan validation and correction completed successfully")
            return corrected_plan_json
        except Exception as e:
            print(f"DEBUG: Error converting corrected plan to JSON: {e}")
            return plan_json_str

    def _correct_file_reference(self, file_ref: str, filename_to_path: dict, project_root: str) -> str:
        """
        Corrects a single file reference to match the actual project structure.

        Args:
            file_ref (str): The file reference to correct (e.g., 'Agent.py', 'agent_core.py')
            filename_to_path (dict): Mapping of filenames to their full paths
            project_root (str): Root directory of the project

        Returns:
            str: The corrected relative file path or original if no correction needed
        """
        # Check if it's already a valid path
        if file_ref in filename_to_path:
            full_path = filename_to_path[file_ref]
            # Convert to relative path from project root
            rel_path = os.path.relpath(full_path, project_root)
            return rel_path

        # Try to find similar filenames (case-insensitive, ignore extension differences)
        file_ref_lower = file_ref.lower().replace('.py', '')
        for filename, path in filename_to_path.items():
            filename_lower = filename.lower().replace('.py', '')
            if file_ref_lower == filename_lower:
                rel_path = os.path.relpath(path, project_root)
                print(f"DEBUG: Corrected '{file_ref}' to '{rel_path}'")
                return rel_path

        # If no match found, try fuzzy matching on common misspellings
        corrections = {
            'agent.py': 'agent_core.py',
            'main.py': 'agent_graph_main.py',
            'config.py': 'agent_config.py',
            'runner.py': 'agent_runner.py',
            'core.py': 'agent_core.py'
        }

        if file_ref.lower() in corrections:
            corrected_name = corrections[file_ref.lower()]
            if corrected_name in filename_to_path:
                full_path = filename_to_path[corrected_name]
                rel_path = os.path.relpath(full_path, project_root)
                print(f"DEBUG: Corrected '{file_ref}' to '{rel_path}' using fuzzy matching")
                return rel_path

        # Return original if no correction found
        return file_ref

    def _correct_file_references_in_text(self, text: str, filename_to_path: dict, project_root: str) -> str:
        """
        Corrects file references found within text content (like step descriptions).

        Args:
            text (str): The text content that may contain file references
            filename_to_path (dict): Mapping of filenames to their full paths
            project_root (str): Root directory of the project

        Returns:
            str: The text with corrected file references
        """
        # Pattern to find file references like 'Agent.py', 'agent_core.py', etc.
        file_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\.py\b'

        def replace_file_ref(match):
            file_ref = match.group(0)
            corrected = self._correct_file_reference(file_ref, filename_to_path, project_root)
            return corrected

        corrected_text = re.sub(file_pattern, replace_file_ref, text)
        return corrected_text