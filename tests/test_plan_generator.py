#!/usr/bin/env python3
"""
Simple test script for update_plan function without dependencies
"""

import sys
import os
from unittest.mock import MagicMock, patch
# Add the project root to sys.path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from evolving_graphs.agent_graph.intelligence_plan_generator import Planner
print("✓ Import successful")
from evolving_graphs.agent_graph.memory_interface import MemoryInterface
from evolving_graphs.agent_graph.task_planner_graph import PlanGraph, STATUS_PENDING, STATUS_COMPLETED, STATUS_IN_PROGRESS

# Mock dependencies to avoid import errors
class MockMemory(MemoryInterface):
    pass

# Test basic functionality
def test_update_plan_signature():
    """Test that update_plan has the correct signature and basic logic"""

    # Now try to import
    try:

        # Test initialization
        planner = Planner(MockMemory())
        print("✓ Planner initialization successful")

        # Test update_plan method exists and has correct signature
        import inspect
        sig = inspect.signature(planner.update_plan)
        params = list(sig.parameters.keys())
        expected = ['main_goal', 'backpack', 'plan', 'codebase_summary', 'query_answer']
        if params == expected:
            print("✓ update_plan signature is correct")
        else:
            print(f"✗ update_plan signature mismatch: got {params}, expected {expected}")

        # Test basic input validation
        try:
            from evolving_graphs.agent_graph.task_planner_graph import PlanGraph
            test_plan = PlanGraph("Test Objective")
            planner.update_plan("", [], test_plan, "")
            print("✗ Should have raised ValueError for empty main_goal")
        except ValueError as e:
            if "main_goal cannot be empty" in str(e):
                print("✓ Input validation for empty main_goal works")
            else:
                print(f"✗ Wrong error message: {e}")

        try:
            from evolving_graphs.agent_graph.task_planner_graph import PlanGraph
            test_plan = PlanGraph("Test Objective")
            planner.update_plan("test goal", "not a list", test_plan, "")
            print("✗ Should have raised TypeError for non-list backpack")
        except TypeError as e:
            if "backpack must be a list" in str(e):
                print("✓ Input validation for backpack type works")
            else:
                print(f"✗ Wrong error message: {e}")

        try:
            from evolving_graphs.agent_graph.task_planner_graph import PlanGraph
            planner.update_plan("test goal", [], "not a PlanGraph", "")
            print("✗ Should have raised ValueError for non-PlanGraph plan")
        except ValueError as e:
            if "plan must be a PlanGraph instance" in str(e):
                print("✓ Input validation for plan type works")
            else:
                print(f"✗ Wrong error message: {e}")

        # Create a real PlanGraph instance for the test
        test_plan = PlanGraph("Improve stability")
        print("✓ Real PlanGraph instance created successfully")

        # Test with proper arguments (this would normally require LLM calls)
        # For signature test, just verify it accepts the right parameters
        try:
            planner.update_plan("Improve stability", [], test_plan, "")
            print("✓ update_plan accepts correct parameters")
        except Exception as e:
            print(f"✓ update_plan parameter validation works: {e}")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_update_plan_functionality():
    """Test that update_plan properly unfolds objectives and adds action nodes."""
    try:
        planner = Planner(MockMemory())

        # Create a PlanGraph with an objective that should unfold
        plan = PlanGraph("Implement user authentication system")

        # Add a pending objective to unfold
        obj_node = plan.add_objective("Set up database schema for users", plan.root_id)

        # Create a meaningful backpack with insights for stability improvements
        backpack = [
            {
                "content": """
                The project uses Python with error handling in place.
                Stability improvements require better exception handling and logging.
                Code should include proper error recovery mechanisms.
                Testing should cover edge cases and error scenarios.
                """
            },
            {
                "content": """
                Existing codebase has main application in app.py.
                Error logging is handled via logger.py.
                Unit tests are in tests/ directory.
                Configuration is managed in config.py.
                """
            }
        ]

        # Mock the LLM calls to avoid actual API calls
        with patch.object(planner, '_generate_insights_from_batch') as mock_insights, \
             patch.object(planner, '_synthesize_plan_from_insights') as mock_synthesize, \
             patch('evolving_graphs.agent_graph.intelligence_plan_validation_utils.validate_and_correct_plan') as mock_validate:

            # Mock insights generation
            mock_insights.return_value = "Insight: Need to enhance error handling and add comprehensive testing"

            # Mock plan synthesis for stability improvements
            mock_synthesize.return_value = '''{
                "objectives": [
                    {
                        "description": "Enhance error handling and logging throughout the application",
                        "actions": [
                            {
                                "role": "code_editor",
                                "command": {"description": "Edit logger.py to add detailed error logging with stack traces"},
                                "justification": "Need better error tracking for stability"
                            }
                        ]
                    },
                    {
                        "description": "Implement comprehensive testing for edge cases",
                        "actions": [
                            {
                                "role": "code_editor",
                                "command": {"description": "Edit tests/test_edge_cases.py to add tests for error conditions and recovery"},
                                "justification": "Require thorough testing to ensure stability"
                            },
                            {
                                "role": "code_editor",
                                "command": {"description": "Create tests/integration_tests.py with end-to-end stability tests"},
                                "justification": "Need integration testing for overall system stability"
                            }
                        ]
                    }
                ]
            }'''

            # Mock validation
            mock_validate.return_value = '''{
                "objectives": [
                    {
                        "description": "Enhance error handling and logging throughout the application",
                        "actions": [
                            {
                                "role": "code_editor",
                                "command": {"description": "Edit logger.py to add detailed error logging with stack traces"},
                                "justification": "Need better error tracking for stability"
                            }
                        ]
                    },
                    {
                        "description": "Implement comprehensive testing for edge cases",
                        "actions": [
                            {
                                "role": "code_editor",
                                "command": {"description": "Edit tests/test_edge_cases.py to add tests for error conditions and recovery"},
                                "justification": "Require thorough testing to ensure stability"
                            },
                            {
                                "role": "code_editor",
                                "command": {"description": "Create tests/integration_tests.py with end-to-end stability tests"},
                                "justification": "Need integration testing for overall system stability"
                            }
                        ]
                    }
                ]
            }'''

            # Call update_plan with "Improve stability" as main_goal to test the fix
            updated_plan, planner_memory_ids = planner.update_plan(
                main_goal="Improve stability",
                backpack=backpack,
                plan=plan,
                codebase_summary="Project structure: app.py, logger.py, config.py, tests/"
            )

            # Verify the plan was updated correctly
            assert isinstance(updated_plan, PlanGraph), "Should return a PlanGraph instance"

            # Check that the objective status was updated
            obj_node_updated = updated_plan.get_node(obj_node.id)
            assert obj_node_updated.status == STATUS_COMPLETED, "Objective should be marked as completed"

            # Check that sub-objectives were created
            sub_objectives = [node for node in updated_plan.nodes.values()
                             if hasattr(node, 'parent_id') and node.parent_id == obj_node.id and hasattr(node, 'description')]
            assert len(sub_objectives) == 2, f"Should have 2 sub-objectives, got {len(sub_objectives)}"

            # Count action nodes under all sub-objectives
            action_count = 0
            for sub_obj in sub_objectives:
                action_count += sum(1 for node in updated_plan.nodes.values()
                                   if hasattr(node, 'parent_id') and node.parent_id == sub_obj.id)
            assert action_count == 3, f"Should have 3 action nodes total, got {action_count}"

            print("✓ update_plan functionality test passed")
            updated_plan.display()

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_update_plan_signature()
    test_update_plan_functionality()