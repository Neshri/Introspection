"""Rule for checking code duplication."""

import os  # filesystem operations
from collections import defaultdict  # default dictionary factory

try:
    from .linter_utils_core import is_boilerplate, is_import_or_comment  # To identify boilerplate and import/comment lines.
except ImportError:
    # Fallback for standalone execution
    from linter_utils_core import is_boilerplate, is_import_or_comment


def check_duplication(target_files=None):
    """Detect potential code duplication in contiguous blocks within each graph."""
    violations = []

    # Determine which files to check
    if target_files is None:
        # Graph-scoped mode: find graphs by entry points and check files within each graph
        graphs_to_check = find_graphs_with_entrypoints()
        for graph_name, graph_path in graphs_to_check:
            graph_violations = check_duplication_in_graph(graph_name, graph_path)
            violations.extend(graph_violations)
    else:
        # Smart mode: analyze target files and group by graphs
        violations = analyze_files_by_graphs(target_files)

    return violations


def find_graphs_with_entrypoints():
    """Find graphs by identifying directories with [graph_name]_main.py files."""
    graphs = []
    
    # Try multiple possible locations for evolving_graphs directory
    possible_paths = [
        'evolving_graphs',  # Relative to current working directory
        '../evolving_graphs',  # Relative to linter_graph subdirectory
        '../../evolving_graphs',  # Relative to deeper subdirectories
    ]
    
    evolving_graphs_dir = None
    for path in possible_paths:
        if os.path.exists(path):
            evolving_graphs_dir = path
            break
    
    if not evolving_graphs_dir:
        return graphs
        
    for item in os.listdir(evolving_graphs_dir):
        item_path = os.path.join(evolving_graphs_dir, item)
        if os.path.isdir(item_path):
            entry_point = f"{item}_main.py"
            entry_point_path = os.path.join(item_path, entry_point)
            if os.path.exists(entry_point_path):
                graphs.append((item, item_path))
    
    return graphs


def check_duplication_in_graph(graph_name, graph_path):
    """Check for duplication within a specific graph directory."""
    violations = []
    blocks = defaultdict(list)  # signature -> list of (file, start_line, indent)
    
    # Collect all Python files within this specific graph
    files_to_check = []
    for root, dirs, files in os.walk(graph_path):
        for file in files:
            if file.endswith('.py'):
                files_to_check.append(os.path.join(root, file))
    
    # Analyze files within this graph for duplication
    graph_blocks = analyze_files_for_duplication(files_to_check, graph_name)
    violations.extend(graph_blocks)
    
    return violations


def analyze_files_by_graphs(files_to_check):
    """Analyze files by grouping them by graphs and checking for duplications within each graph."""
    violations = []
    
    # Group files by graph
    files_by_graph = {}
    graphs_to_check = find_graphs_with_entrypoints()
    
    # Create a mapping of graph names to their directories
    graph_dirs = {name: path for name, path in graphs_to_check}
    
    for filepath in files_to_check:
        # Determine which graph this file belongs to
        graph_name = None
        for gname, gpath in graphs_to_check:
            if filepath.startswith(os.path.abspath(gpath)):
                graph_name = gname
                break
        
        if graph_name:
            if graph_name not in files_by_graph:
                files_by_graph[graph_name] = []
            files_by_graph[graph_name].append(filepath)
    
    # Check for duplications within each graph
    for graph_name, graph_files in files_by_graph.items():
        if len(graph_files) >= 2:  # Only check if there are multiple files in the graph
            graph_violations = analyze_files_for_duplication(graph_files, graph_name)
            violations.extend(graph_violations)
    
    return violations


def analyze_files_for_duplication(files_to_check, graph_name=None):
    """Analyze a list of files for code duplication."""
    violations = []
    blocks = defaultdict(list)  # signature -> list of (file, start_line, indent)
    
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            current_block = []
            current_indent = None
            current_start_line = None
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                if is_import_or_comment(line) or is_boilerplate(line) or stripped == '':
                    if current_block:
                        if len(current_block) >= 5:
                            signature = (current_indent, tuple(current_block))
                            blocks[signature].append((filepath, current_start_line, current_indent))
                        current_block = []
                        current_indent = None
                        current_start_line = None
                    continue
                indent = len(line) - len(line.lstrip())
                if current_indent is None or indent != current_indent:
                    if current_block:
                        if len(current_block) >= 5:
                            signature = (current_indent, tuple(current_block))
                            blocks[signature].append((filepath, current_start_line, current_indent))
                    current_block = [stripped]
                    current_indent = indent
                    current_start_line = line_num
                else:
                    current_block.append(stripped)
            # Process the last block if it exists
            if current_block and len(current_block) >= 5:
                signature = (current_indent, tuple(current_block))
                blocks[signature].append((filepath, current_start_line, current_indent))
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    # Identify duplications across multiple files within the scope
    for signature, occurrences in blocks.items():
        if len(occurrences) >= 2:
            indent, block_lines = signature
            unique_files = set(f for f, s, i in occurrences)
            for file, start_line, _ in occurrences:
                other_files = unique_files - {file}
                graph_context = f" in graph '{graph_name}'" if graph_name else ""
                message = f"Code duplication detected{graph_context}: block of {len(block_lines)} lines at indentation level {indent} also found in files: {', '.join(other_files)}"
                violations.append({'file': file, 'line': start_line, 'message': message})

    return violations