import json  # JSON handling for structured plan output
import ollama  # LLM interface for generating plans based on goals and context
from .intelligence_llm_service import chat_llm  # Standardized LLM service
from .agent_config import config  # Configuration settings for model selection and prompt templates


class Planner:
    """
    The Planner class is responsible for creating structured plans to achieve programming goals.
    It analyzes the goal and relevant project files (backpack) to generate actionable strategies
    that guide the Executor in implementing code changes.
    """

    def create_plan(self, main_goal: str, backpack: list[dict]) -> str:
        """
        Generates a structured plan for achieving the given programming goal using relevant project context.

        Args:
            main_goal (str): The programming goal to achieve
            backpack (list[dict]): List of relevant files with their content and justification

        Returns:
            str: A structured plan in JSON format containing steps to achieve the goal
        """
        print(f"DEBUG: Planner received goal: {main_goal}")
        print(f"DEBUG: Planner received backpack with {len(backpack)} items")

        # Format backpack context for the prompt
        backpack_context = ""
        if backpack:
            for item in backpack:
                backpack_context += f"File: {item['file_path']}\n"
                backpack_context += f"Justification: {item['justification']}\n"
                backpack_context += f"Content:\n{item['full_code']}\n\n"
        else:
            backpack_context = "No relevant files identified."

        print(f"DEBUG: Planning based on goal '{main_goal}' with backpack context length: {len(backpack_context)}")

        # Create the prompt using the template
        prompt = config.PLANNER_PROMPT_TEMPLATE.format(
            goal=main_goal,
            backpack_context=backpack_context
        )

        print("DEBUG: Calling LLM to generate plan...")
        # Call the LLM to generate the plan
        plan = chat_llm(prompt)
        print(f"DEBUG: LLM generated plan: {plan[:100]}...")  # Truncate for brevity

        # Validate that the plan is valid JSON
        try:
            json.loads(plan)  # Validate JSON structure
            print("DEBUG: Generated plan is valid JSON")
        except json.JSONDecodeError:
            # If JSON parsing fails, wrap in a basic structure
            print("DEBUG: Plan JSON validation failed, wrapping in basic structure")
            plan = json.dumps({
                "goal": main_goal,
                "steps": [plan],
                "estimated_complexity": "medium",
                "risk_assessment": "Unable to parse structured plan from LLM response"
            })

        print(f"DEBUG: Returning final plan with length: {len(plan)}")
        return plan