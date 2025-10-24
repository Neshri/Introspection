import os

def collect_modules(project_dir):
    """Collect all Python modules in the project directory as a dict of module_name: path."""
    all_modules = {}
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, project_dir)
                module_name = rel_path.replace(os.sep, '.').replace('.py', '')
                all_modules[module_name] = path
    return all_modules