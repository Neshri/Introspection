"""Utilities for the linter package."""

from .lint_utils import (  # shared utility functions
    is_standard_library,
    has_inline_comment,
    has_following_comment,
    is_import_or_comment,
    is_boilerplate,
    count_code_lines,
)