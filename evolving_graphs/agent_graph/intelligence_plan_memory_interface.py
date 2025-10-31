#
# intelligence_plan_memory_interface.py (Planning Memory Interface Role)
# This module provides memory-augmented planning capabilities with persistent learning
# from past planning sessions to prevent unproductive loops and enable intelligent progression.
#

from typing import Dict, List, Optional, Tuple, Any  # Type hints for function signatures and data structures
from .memory_interface import MemoryInterface  # Base memory interface for persistent storage operations
import json  # JSON serialization for storing complex data structures in memory
import time  # Time utilities for recording timestamps and session duration


class PlanningMemoryInterface:
    """
    Memory-augmented planning interface that learns from past planning patterns
    to prevent repetitive loops and guide intelligent plan construction.

    Extends the base MemoryInterface with planning-specific memory types:
    - planning_success_patterns: Successful command sequences that led to DONE
    - planning_failure_patterns: Command sequences that resulted in loops/stuck states
    - context_command_mappings: Historical mappings of plan contexts to effective commands
    - objective_decomposition_patterns: How objectives were successfully decomposed
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

        # Record command pattern for future learning
        self._record_command_pattern(command, plan_context, command_success, loop_detected)

    def _record_command_pattern(self, command: str, context: str, success: bool, loop_detected: bool):
        """Record command patterns for learning effective planning strategies."""
        pattern_data = {
            "command": command,
            "context_hash": hash(context),  # Simple hash for context similarity
            "success": success,
            "loop_detected": loop_detected,
            "context_keywords": self._extract_context_keywords(context)
        }

        # Determine memory type based on outcome
        memory_type = "planning_success_pattern" if success and not loop_detected else "planning_failure_pattern"
        score = 100.0 if success else 10.0

        self.memory_interface.add_memory(
            content=json.dumps(pattern_data),
            current_turn=self.current_turn,
            memory_type=memory_type,
            creator_role="planning_memory_interface",
            initial_score=score
        )

    def _extract_context_keywords(self, context: str) -> List[str]:
        """Extract keywords from planning context for pattern matching."""
        keywords = []
        # Look for command history patterns
        if "LIST" in context:
            keywords.append("list_command_recent")
        if "ADD_OBJECTIVE" in context:
            keywords.append("objective_being_added")
        if "DONE" in context:
            keywords.append("completion_attempted")
        if "pending" in context.lower():
            keywords.append("pending_objectives_exist")
        if len(context.split()) > 100:  # Complex context
            keywords.append("complex_plan_context")

        return keywords

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

        # Extract and store successful patterns if session succeeded
        if success:
            self._extract_successful_patterns(session_data)

    def _extract_successful_patterns(self, session_data: Dict):
        """Extract successful planning patterns from completed sessions."""
        commands = session_data.get("commands_issued", [])

        # Look for DONE command and preceding successful sequence
        done_index = None
        for i, cmd in enumerate(commands):
            if cmd["command"].upper() == "DONE" and cmd["success"]:
                done_index = i
                break

        if done_index and done_index > 0:
            # Extract the successful command sequence leading to DONE
            successful_sequence = commands[max(0, done_index-5):done_index+1]  # Last 5 commands + DONE

            # Truncate contexts to fit within token limits
            pattern_data = {
                "sequence": [cmd["command"] for cmd in successful_sequence],
                "contexts": [cmd["context"][:200] for cmd in successful_sequence],  # Limit context length
                "goal": session_data.get("main_goal", "")[:200],  # Limit goal length
                "command_count": len(successful_sequence)
            }

            self.memory_interface.add_memory(
                content=json.dumps(pattern_data),
                current_turn=self.current_turn,
                memory_type="successful_done_sequence",
                creator_role="planning_memory_interface",
                initial_score=90.0
            )

    def get_context_aware_command_suggestions(self, current_context: str, recent_commands: List[str],
                                           main_goal: str) -> List[Tuple[str, float]]:
        """
        Get command suggestions based on historical patterns and current context.

        Returns list of (command, confidence_score) tuples.
        """
        suggestions = []

        # Query for successful patterns with similar context
        context_keywords = self._extract_context_keywords(current_context)
        query_text = f"{main_goal} {' '.join(context_keywords)} {' '.join(recent_commands[-3:])}"

        similar_patterns = self.memory_interface.query_memory(
            query_text=query_text,
            current_turn=self.current_turn,
            n_results=5,
            min_score=20.0
        )

        for result in similar_patterns['documents']:
            try:
                if isinstance(result, list):
                    # Handle cases where result is already a list (skip or handle appropriately)
                    continue
                pattern_data = json.loads(result)

                if pattern_data.get("memory_type") == "successful_done_sequence":
                    # Extract next command suggestion from successful sequence
                    sequence = pattern_data.get("sequence", [])
                    if len(sequence) > len(recent_commands):
                        next_cmd_index = len(recent_commands)
                        if next_cmd_index < len(sequence):
                            suggested_cmd = sequence[next_cmd_index]
                            confidence = pattern_data.get("relevance_score", 50.0) / 100.0
                            suggestions.append((suggested_cmd, confidence))

                elif pattern_data.get("memory_type") in ["planning_success_pattern", "planning_failure_pattern"]:
                    # Direct command pattern match
                    if not pattern_data.get("loop_detected", False):
                        cmd = pattern_data.get("command", "")
                        confidence = pattern_data.get("relevance_score", 50.0) / 100.0
                        if pattern_data.get("memory_type") == "planning_failure_pattern":
                            confidence *= 0.3  # Penalize failure patterns
                        suggestions.append((cmd, confidence))

            except json.JSONDecodeError:
                continue

        # Remove duplicates and sort by confidence
        seen = set()
        unique_suggestions = []
        for cmd, conf in sorted(suggestions, key=lambda x: x[1], reverse=True):
            if cmd not in seen:
                unique_suggestions.append((cmd, conf))
                seen.add(cmd)

        return unique_suggestions[:5]  # Return top 5 suggestions

    def detect_loop_pattern(self, recent_commands: List[str], current_context: str) -> bool:
        """
        Detect if current planning is entering a repetitive loop pattern.
        """
        if len(recent_commands) < 4:
            return False

        # Check for repetitive LIST commands
        recent_list_count = sum(1 for cmd in recent_commands[-5:] if cmd.upper() == "LIST")
        if recent_list_count >= 3:
            return True

        # Check for command cycling (same commands repeating)
        recent_window = recent_commands[-6:]
        if len(set(recent_window)) <= 2:  # Very few unique commands
            return True

        # Query memory for similar stuck contexts
        query_text = f"stuck loop {' '.join(recent_commands[-3:])}"
        stuck_patterns = self.memory_interface.query_memory(
            query_text=query_text,
            current_turn=self.current_turn,
            n_results=2,
            min_score=30.0
        )

        return len(stuck_patterns['documents']) > 0

    def should_attempt_done(self, current_context: str, command_history: List[str]) -> float:
        """
        Determine confidence score for attempting DONE command based on historical patterns.
        """
        if not any("pending" in ctx.lower() for ctx in [current_context]):
            return 0.0  # No pending objectives, not ready for DONE

        # Query for successful DONE patterns
        query_text = f"DONE success {' '.join(command_history[-2:])}"
        done_patterns = self.memory_interface.query_memory(
            query_text=query_text,
            current_turn=self.current_turn,
            n_results=3,
            min_score=40.0
        )

        if not done_patterns['documents']:
            return 0.1  # Low confidence if no historical DONE successes

        # Calculate average confidence from successful DONE patterns
        total_score = sum(meta.get('relevance_score', 50.0)
                         for meta in done_patterns['metadatas'])
        avg_confidence = total_score / len(done_patterns['documents']) / 100.0

        return min(avg_confidence, 0.9)  # Cap at 90%

    def update_turn(self, new_turn: int):
        """Update the current turn counter for memory management."""
        self.current_turn = new_turn
        self.memory_interface.perform_maintenance(current_turn=new_turn)


# Global planning memory interface instance
planning_memory_interface = PlanningMemoryInterface()