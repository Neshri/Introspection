#!/usr/bin/env python3
"""
Test script for memory-augmented planning architecture.
This script demonstrates the new planning system with persistent learning capabilities.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolving_graphs.agent_graph.task_planner_graph import PlanGraph
from evolving_graphs.agent_graph.intelligence_memory_augmented_planner_utils import memory_augmented_update_plan
from evolving_graphs.agent_graph.intelligence_plan_memory_interface import planning_memory_interface


def test_memory_augmented_planning():
    """Test the memory-augmented planning system."""
    print("🧠 Testing Memory-Augmented Planning Architecture")
    print("=" * 60)

    # Create a test goal
    main_goal = "Implement a user authentication system with password hashing and session management"

    # Create initial plan
    plan = PlanGraph(main_goal)

    # Mock backpack with some relevant code context
    backpack = [
        {
            "content": """
class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, password):
        # TODO: Implement password verification
        pass
"""
        },
        {
            "content": """
import hashlib
import os

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000), salt
"""
        }
    ]

    # Mock codebase summary
    codebase_summary = """
The codebase is a Python web application with:
- User management models in models/user.py
- Authentication utilities in utils/auth.py
- Session handling in middleware/session.py
- Database connections in db/connection.py
"""

    print(f"🎯 Main Goal: {main_goal}")
    print(f"📚 Backpack contains {len(backpack)} code snippets")
    print(f"🏗️  Initial plan has {len(plan.nodes)} nodes")

    # Test memory-augmented planning
    print("\n🚀 Running memory-augmented planning...")
    try:
        updated_plan, memory_ids = memory_augmented_update_plan(
            main_goal=main_goal,
            backpack=backpack,
            plan=plan,
            codebase_summary=codebase_summary
        )

        print("✅ Memory-augmented planning completed successfully!")
        print(f"📊 Final plan has {len(updated_plan.nodes)} nodes")

        # Display the plan
        print("\n📋 Final Plan Structure:")
        updated_plan.display()

        # Show memory interface status
        print("\n🧠 Memory Interface Status:")
        print(f"   - Memory database path: memory_db/")
        print(f"   - Planning sessions recorded: {len(planning_memory_interface.memory_interface.collection.get()['ids'])}")

        return True

    except Exception as e:
        print(f"❌ Memory-augmented planning failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_memory_augmented_planning()
    sys.exit(0 if success else 1)