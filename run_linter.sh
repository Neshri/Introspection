#!/bin/bash
# This script runs the architectural linter for the entire project.
# It ensures all code complies with the master ruleset.

echo "Running architectural linter..."
python3 -m evolving_graphs.linter_graph.linter_graph_main