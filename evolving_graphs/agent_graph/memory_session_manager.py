#
# memory_session_manager.py (Memory Session Manager)
# Manages planning session lifecycle and memory recording for learning.
#

from typing import Dict, List, Optional, Tuple, Any
from .memory_interface import MemoryInterface  # Base memory interface for persistent storage operations
import json  # JSON serialization for storing complex data structures in memory
import time  # Time utilities for recording timestamps and session duration


class PlanningMemorySessionManager:
    """
    Manages planning session lifecycle including start, recording, and completion.
    Handles the recording of command attempts and session outcomes for learning.
    """

    def __init__(self, db_path: str = "memory_db", max_memory_tokens: int = 1000):
        self.memory_interface = MemoryInterface(db_path, max_memory_tokens)
        self.current_turn = 0

    def record_planning_session_start(self, main_goal: str, initial_context: str) -> str:
        """Record the start of a planning session for pattern learning."""
        session_data = {
            "main_goal": main_goal,
            "initial_context": initial_context,
            "start_time": time.time(),
            "commands_issued": [],
            "contexts_seen": [],
            "outcome": "in_progress"
        }

        session_id = self.memory_interface.add_memory(
            content=json.dumps(session_data),
            current_turn=self.current_turn,
            memory_type="planning_session",
            creator_role="planning_memory_interface",
            initial_score=50.0
        )
        return session_id

    def record_command_attempt(self, session_id: str, command: str, plan_context: str,
                              command_success: bool, loop_detected: bool = False):
        """Record a command attempt within a planning session."""
        # Retrieve current session
        session_memory = self.memory_interface.collection.get(ids=[session_id])
        if not session_memory['ids']:
            return

        session_data = json.loads(session_memory['documents'][0])
        metadata = session_memory['metadatas'][0]

        # Add command to sequence
        command_entry = {
            "command": command,
            "context": plan_context,
            "success": command_success,
            "loop_detected": loop_detected,
            "timestamp": time.time()
        }
        session_data["commands_issued"].append(command_entry)
        session_data["contexts_seen"].append(plan_context)

        # Update session memory
        self.memory_interface.collection.update(
            ids=[session_id],
            documents=[json.dumps(session_data)]
        )

    def record_session_outcome(self, session_id: str, success: bool, final_command_count: int,
                              loops_detected: int, time_to_completion: float):
        """Record the final outcome of a planning session."""
        session_memory = self.memory_interface.collection.get(ids=[session_id])
        if not session_memory['ids']:
            return

        session_data = json.loads(session_memory['documents'][0])
        metadata = session_memory['metadatas'][0]

        session_data.update({
            "outcome": "success" if success else "failure",
            "final_command_count": final_command_count,
            "loops_detected": loops_detected,
            "time_to_completion": time_to_completion,
            "end_time": time.time()
        })

        # Update score based on outcome
        if success:
            metadata['relevance_score'] = max(metadata.get('relevance_score', 50), 80.0)
        else:
            metadata['relevance_score'] = min(metadata.get('relevance_score', 50), 20.0)

        self.memory_interface.collection.update(
            ids=[session_id],
            documents=[json.dumps(session_data)],
            metadatas=[metadata]
        )

    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of a planning session."""
        session_memory = self.memory_interface.collection.get(ids=[session_id])
        if not session_memory['ids']:
            return None

        session_data = json.loads(session_memory['documents'][0])
        metadata = session_memory['metadatas'][0]

        return {
            'session_id': session_id,
            'main_goal': session_data.get('main_goal', ''),
            'outcome': session_data.get('outcome', 'unknown'),
            'command_count': len(session_data.get('commands_issued', [])),
            'loops_detected': session_data.get('loops_detected', 0),
            'time_to_completion': session_data.get('time_to_completion', 0.0),
            'relevance_score': metadata.get('relevance_score', 50.0)
        }

    def update_turn(self, new_turn: int):
        """Update the current turn counter for memory management."""
        self.current_turn = new_turn
        self.memory_interface.perform_maintenance(current_turn=new_turn)