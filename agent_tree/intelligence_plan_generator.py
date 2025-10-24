import json  # JSON handling for structured plan output
import ollama  # LLM interface for generating plans based on goals and context
from .intelligence_llm_service import chat_llm  # Standardized LLM service
from .agent_config import config  # Configuration settings for model selection and prompt templates


class Planner:
    """
    The Planner class creates structured plans to achieve programming goals.
    It uses a hierarchical, Map-Reduce strategy to handle large contexts, first generating
    insights from batches of files and then synthesizing them into a final, coherent plan.
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

        plan = chat_llm(prompt)
        print(f"DEBUG: LLM generated final plan: {plan[:100]}...")

        # Validate that the plan is valid JSON, with a robust fallback
        try:
            json.loads(plan)
            print("DEBUG: Generated plan is valid JSON")
            return plan
        except json.JSONDecodeError:
            print("DEBUG: Plan JSON validation failed, wrapping in basic structure")
            return json.dumps({
                "goal": main_goal,
                "steps": [f"LLM produced non-JSON plan: {plan}"],
                "estimated_complexity": "high",
                "risk_assessment": "Failed to synthesize a structured plan from insights. The LLM's output was not valid JSON."
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

            if current_batch_size + item_size > config.PLANNER_CONTEXT_LIMIT:
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

        print(f"DEBUG: Returning final plan with length: {len(final_plan)}")
        return final_plan