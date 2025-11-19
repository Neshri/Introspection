"""
This module defines the data structures for the project's "Module Context Map".

The classes herein are designed to produce a comprehensive, grounded, and
actionable document for an AI agent to understand a module's role and status.
"""

import hashlib
import re
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

# --- Core Data Primitives ---

@dataclass(frozen=True)
class Claim:
    """Represents a single, immutable, verifiable statement about a piece of code."""
    text: str
    reference: str
    source_module: str

    @property
    def id(self) -> str:
        """Computes a stable and unique hash ID for the claim."""
        unique_string = f"{self.text}|{self.reference}|{self.source_module}"
        sha = hashlib.sha1(unique_string.encode()).hexdigest()
        return sha

@dataclass
class GroundedText:
    """A container for prose that is explicitly linked to a set of claims."""
    text: str = ""
    supporting_claim_ids: Set[str] = field(default_factory=set)

@dataclass
class Alert:
    """Represents an actionable alert or status note about the code."""
    category: str
    description: str
    reference: str = ""


# --- The Main Module Context Document ---

class ModuleContext:
    """
    A structured "map" of a module that actively manages its own consistency.
    """
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.module_role: GroundedText = GroundedText()
        self.key_dependencies: Dict[str, GroundedText] = {}
        self.key_dependents: Dict[str, GroundedText] = {}
        self.public_api: Dict[str, GroundedText] = {}
        self.alerts: List[Alert] = []
        self.claims: Dict[str, Claim] = {}

    def _add_claims_and_get_placeholders(self, claims: List[Claim]) -> Tuple[str, Set[str]]:
        """Internal helper to process a list of claims transactionally."""
        placeholders = []
        claim_ids = set()
        for claim in claims:
            # Add the claim to the central repository.
            self.claims[claim.id] = claim
            # Generate the placeholder string and collect the ID.
            placeholders.append(f"[ref:{claim.id}]")
            claim_ids.add(claim.id)
        return " ".join(placeholders), claim_ids

    # --- High-Level Transactional API ---

    def set_module_role(self, text: str, supporting_claims: List[Claim]):
        """Sets the module's role with explicitly linked, grounded claims."""
        placeholders, claim_ids = self._add_claims_and_get_placeholders(supporting_claims)
        full_text = f"{text} {placeholders}".strip()
        self.module_role = GroundedText(text=full_text, supporting_claim_ids=claim_ids)

    def add_dependency_context(self, module_path: str, explanation: str, supporting_claims: List[Claim]):
        """
        Adds a grounded explanation for why this module depends on another.
        Args:
            module_path: The path of the dependency.
            explanation: Prose explaining the usage.
            supporting_claims: Evidence from the code.
        """
        placeholders, claim_ids = self._add_claims_and_get_placeholders(supporting_claims)
        full_text = f"{explanation} {placeholders}".strip()
        self.key_dependencies[module_path] = GroundedText(text=full_text, supporting_claim_ids=claim_ids)

    def add_dependent_context(self, module_path: str, explanation: str, supporting_claims: List[Claim]):
        """
        Adds a grounded explanation for how another module uses this one.
        Args:
            module_path: The path of the dependent module.
            explanation: Prose explaining the usage.
            supporting_claims: Evidence from the code.
        """
        placeholders, claim_ids = self._add_claims_and_get_placeholders(supporting_claims)
        full_text = f"{explanation} {placeholders}".strip()
        self.key_dependents[module_path] = GroundedText(text=full_text, supporting_claim_ids=claim_ids)

    def add_public_api_entry(self, entity_name: str, description: str, supporting_claims: List[Claim]):
        """
        Adds a grounded description for a public class or function in this module.
        Args:
            entity_name: The name of the class or function (e.g., "ProjectSummarizer").
            description: Prose explaining what it does.
            supporting_claims: Evidence from the code.
        """
        placeholders, claim_ids = self._add_claims_and_get_placeholders(supporting_claims)
        full_text = f"{description} {placeholders}".strip()
        self.public_api[entity_name] = GroundedText(text=full_text, supporting_claim_ids=claim_ids)

    def add_alert(self, alert: Alert):
        """Adds a structured alert to the context."""
        self.alerts.append(alert)

    def __eq__(self, other: object) -> bool:
        """Required for the summarizer's convergence checking."""
        if not isinstance(other, ModuleContext):
            return NotImplemented
        # Compare the internal dictionary representation for equality.
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        """Provides a meaningful string representation of the ModuleContext."""
        file_info = self.file_path if self.file_path else "unknown file"
        role_info = self.module_role.text[:50] if self.module_role.text else "No role defined"
        
        return (f"ModuleContext(file='{file_info}', "
                f"role='{role_info}', "
                f"dependencies={len(self.key_dependencies)}, "
                f"dependents={len(self.key_dependents)}, "
                f"public_api={len(self.public_api)}, "
                f"alerts={len(self.alerts)}, "
                f"claims={len(self.claims)})")