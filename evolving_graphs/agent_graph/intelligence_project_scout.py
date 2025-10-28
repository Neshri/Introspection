# Split intelligence_project_scout.py to reduce token count
# Scout class moved to intelligence_project_scout_core.py
# Utility functions moved to intelligence_project_scout_utils.py

from .intelligence_project_scout_core import Scout as CoreScout  # Core scout functionality


class Scout(CoreScout):
    """
    Scout class for exploring and analyzing project codebases based on goals.

    Note: This class inherits core functionality from intelligence_project_scout_core
    and utility functions from intelligence_project_scout_utils.
    """
    pass