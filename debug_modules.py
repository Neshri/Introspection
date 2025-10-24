#!/usr/bin/env python3
from evolving_graphs.agent_graph.utils_collect_modules import collect_modules

def debug_modules():
    print("Collecting modules from '.' (current dir):")
    modules = collect_modules('.')
    print(f"Found {len(modules)} modules:")
    for name, path in modules.items():
        print(f"  {name}: {path}")

    print("\nCollecting modules from 'evolving_graphs/agent_graph':")
    modules2 = collect_modules('evolving_graphs/agent_graph')
    print(f"Found {len(modules2)} modules:")
    for name, path in modules2.items():
        print(f"  {name}: {path}")

if __name__ == "__main__":
    debug_modules()