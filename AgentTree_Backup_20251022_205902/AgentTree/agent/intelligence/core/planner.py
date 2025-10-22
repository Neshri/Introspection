import json  # JSON handling for structured plan output
import ollama  # LLM interface for generating plans based on goals and context
from agent.utils import config  # Configuration settings for model selection and prompt templates


class Planner:
    """
    The Planner class is responsible for creating structured plans to achieve programming goals.
    It analyzes the goal and relevant project files (backpack) to generate actionable strategies
    that guide the Executor in implementing code changes.
    """

    def create_plan(self, goal: str, backpack: list[dict]) -> str:
        """
        Generates a structured plan for achieving the given programming goal using relevant project context.

        Args:
            goal (str): The programming goal to achieve
            backpack (list[dict]): List of relevant files with their content and justification

        Returns:
            str: A structured plan in JSON format containing steps to achieve the goal
        """
        # Format backpack context for the prompt
        backpack_context = ""
        if backpack:
            for item in backpack:
                backpack_context += f"File: {item['file_path']}\n"
                backpack_context += f"Justification: {item['justification']}\n"
                backpack_context += f"Content:\n{item['full_code']}\n\n"
        else:
            backpack_context = "No relevant files identified."

        # Create the prompt using the template
        prompt = config.PLANNER_PROMPT_TEMPLATE.format(
            goal=goal,
            backpack_context=backpack_context
        )

        # Call the LLM to generate the plan
        response = ollama.chat(model=config.MODEL, messages=[{'role': 'user', 'content': prompt}])

        # Extract and return the plan
        plan = response['message']['content'].strip()

        # Validate that the plan is valid JSON
        try:
            json.loads(plan)  # Validate JSON structure
        except json.JSONDecodeError:
            # If JSON parsing fails, wrap in a basic structure
            plan = json.dumps({
                "goal": goal,
                "steps": [plan],
                "estimated_complexity": "medium",
                "risk_assessment": "Unable to parse structured plan from LLM response"
            })

        return plan