#!/usr/bin/env python3
"""
set_goal.py - Interactive Goal Setting Script
This script provides a command-line interface for setting goals using the AgentTree Agent class.
Handles validation, persistence, and user-friendly interactions.
"""

# Standard library imports
import sys
import signal
from typing import Optional

# AgentTree imports
from AgentTree.agent import Agent

def display_current_goal(agent: Agent) -> None:
    """Display the current goal in a formatted way."""
    current_goal = agent.get_goal()
    if current_goal:
        print("Current Goal:")
        print(f"  {current_goal}")
        print("-" * 50)
    else:
        print("No current goal set.")
        print("-" * 50)

def get_goal_input() -> Optional[str]:
    """Get goal input from user with validation hints."""
    print("\nEnter your new goal (10-500 characters):")
    print("Goal should be actionable and specific.")
    print("Type 'cancel' or press Ctrl+C to exit without changes.")
    print()

    try:
        goal = input("New goal: ").strip()
        if goal.lower() in ['cancel', 'quit', 'exit']:
            return None
        return goal
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return None
    except EOFError:
        print("\nInput stream ended. Exiting.")
        return None

def validate_and_set_goal(agent: Agent, goal: str) -> bool:
    """Validate and set the goal, returning success status."""
    if not goal:
        print("Error: Goal cannot be empty.")
        return False

    if len(goal) < 10:
        print(f"Error: Goal too short ({len(goal)} chars). Minimum 10 characters required.")
        return False

    if len(goal) > 500:
        print(f"Error: Goal too long ({len(goal)} chars). Maximum 500 characters allowed.")
        return False

    # Use Agent's validation method
    success = agent.set_goal(goal)

    if success:
        print("Goal set successfully!")
        print(f"New goal: {goal}")
    else:
        print("Error: Goal contains invalid or dangerous content.")
        print("Please rephrase and try again.")

    return success

def main() -> int:
    """Main function for the goal setting script."""
    print("AgentTree Goal Setting Tool")
    print("=" * 50)

    try:
        # Initialize agent
        agent = Agent()

        # Display current goal
        display_current_goal(agent)

        # Main input loop
        while True:
            goal = get_goal_input()
            if goal is None:
                print("Goal setting cancelled. No changes made.")
                return 0

            if validate_and_set_goal(agent, goal):
                return 0  # Success exit

            # If validation failed, continue loop
            print("\nPlease try again or type 'cancel' to exit.")
            print()

    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully."""
    print("\n\nOperation interrupted. Exiting...")
    sys.exit(1)

if __name__ == "__main__":
    # Setup signal handlers for graceful exit
    signal.signal(signal.SIGINT, signal_handler)
    try:
        signal.signal(signal.SIGTERM, signal_handler)
    except ValueError:
        # SIGTERM not available on Windows
        pass

    # Run main function
    sys.exit(main())