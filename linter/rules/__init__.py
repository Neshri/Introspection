"""Rules for the linter package."""

from .import_comments import check_import_comments  # rule for import comments
from .import_compliance import check_imports_compliance  # rule for import compliance
from .duplication import check_duplication  # rule for code duplication
from .file_sizes import check_file_sizes  # rule for file sizes
from .line_counts import analyze_lines_count  # rule for line counts analysis
from .shared_modules import check_shared_module_placement  # rule for shared modules
from .directory_structure import analyze_directory_structure  # rule for directory structure