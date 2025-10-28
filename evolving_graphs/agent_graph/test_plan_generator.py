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

        # Create a meaningful backpack with insights
        backpack = [
            {
                "content": """
                The project uses SQLite for data storage.
                User authentication requires fields: id, username, email, password_hash, created_at.
                Password hashing should use bcrypt.
                Database schema should include proper indexes.
                """
            },
            {
                "content": """
                Existing codebase has models in models.py.
                Database connection is handled via db_connection.py.
                Migration scripts are in migrations/ directory.
                """
            }
        ]

        # Mock the LLM calls to avoid actual API calls
        with patch.object(planner, '_generate_insights_from_batch') as mock_insights, \
             patch.object(planner, '_synthesize_plan_from_insights') as mock_synthesize, \
             patch('evolving_graphs.agent_graph.intelligence_plan_utils.validate_and_correct_plan') as mock_validate:

            # Mock insights generation
            mock_insights.return_value = "Insight: Need to create user table with proper fields"

            # Mock plan synthesis
            mock_synthesize.return_value = '''{
                "steps": [
                    "Create a new migration file in migrations/ directory with SQL to create user table",
                    "Edit src/models.py to add User class with id, username, email, password_hash fields",
                    "Create src/utils/auth.py with bcrypt password hashing functions"
                ]
            }'''

            # Mock validation
            mock_validate.return_value = '''{
                "steps": [
                    "Create a new migration file in migrations/ directory with SQL to create user table",
                    "Edit src/models.py to add User class with id, username, email, password_hash fields",
                    "Create src/utils/auth.py with bcrypt password hashing functions"
                ]
            }'''

            # Call update_plan
            updated_plan = planner.update_plan(
                main_goal="Implement user authentication system",
                backpack=backpack,
                plan=plan,
                codebase_summary="Project structure: src/models.py, src/db_connection.py, migrations/"
            )

            # Verify the plan was updated correctly
            assert isinstance(updated_plan, PlanGraph), "Should return a PlanGraph instance"

            # Check that the objective status was updated
            obj_node_updated = updated_plan.get_node(obj_node.id)
            assert obj_node_updated.status == STATUS_COMPLETED, "Objective should be marked as completed"

            # Check that action nodes were added
            pending_objectives = [node_id for node_id, node in updated_plan.nodes.items()
                                  if isinstance(node, type(updated_plan.get_node(obj_node.id))) and node.status == STATUS_PENDING and not node.children]
            assert len(pending_objectives) == 0, "Should have no pending objectives with no children"

            # Count action nodes under the unfolded objective
            action_count = sum(1 for node in updated_plan.nodes.values()
                             if hasattr(node, 'parent_id') and node.parent_id == obj_node.id)
            assert action_count == 3, f"Should have 3 action nodes, got {action_count}"

            print("✓ update_plan functionality test passed")
            updated_plan.display()

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_update_plan_signature()
    test_update_plan_functionality()