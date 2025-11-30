# Evolving Graphs: Autonomous AI Agent Genome

## Introduction

Evolving Graphs is a self-contained autonomous AI agent system implementing a structured evolutionary approach to code generation and architectural compliance. The system operates as a "Genome" within the `/evolving_graphs/` directory, containing two primary Graphs: `agent_graph` and `linter_graph`.

The `agent_graph` translates natural language goals into executable Python code through an iterative pipeline of specialized intelligence services, ensuring safe execution and continuous improvement. The `linter_graph` maintains architectural integrity by enforcing shallow, AI-friendly rules across the entire Genome.

### Genome Structure
- **Root Directory**: `/evolving_graphs/` (the complete Genome)
- **Graphs**: Direct subdirectories containing designated entry points
- **Entry Points**: `[graph_name]_main.py` files for each Graph
- **Modules**: Semantic naming convention `domain_responsibility.py`
- **Constraints**: Shallow architecture (no nested subdirectories), 3000 token limit per module, empty `__init__.py` files

## Architecture Overview

The Genome adheres to **Scientific Standards** designed for objective verification and autonomous evolution:
- **Directed Acyclic Graph (DAG)**: Strictly acyclic dependencies.
- **Shallow Architecture**: Max depth of 1. No deep nesting.
- **Strict Isolation**: No cross-graph imports.
- **Atomic Modules**: Max 3000 tokens per module.
- **Code is Truth**: Documentation is derived from code structure, not comments.

## Graphs Description

### Agent Graph (`agent_graph/`)
**Entry Point**: `agent_graph_main.py`
**Purpose**: An autonomous "Crawler" agent that explores, analyzes, and evolves the codebase.

#### Core Infrastructure
- `agent_core.py`: The `CrawlerAgent` that orchestrates the analysis loop.
- `agent_config.py`: Centralized configuration (Models, Limits).
- `agent_util.py`: `ProjectSummarizer` and `project_pulse` for graph analysis.
- `memory_core.py`: Persistent memory management (ChromaDB wrapper).

#### Introspection Engine (The Eyes)
A subsystem that generates the "Objective Truth" Project Map (`PROJECT_MAP.md`).
- `graph_analyzer.py`: Statically analyzes code to build the dependency graph (AST-based).
- `module_classifier.py`: Classifies modules by structural role (Service vs Data).
- `module_contextualizer.py`: Translates code logic into reasoning-ready English.
- `report_renderer.py`: Renders the map, grouped by Archetype.
- `summary_models.py`: Data structures for Claims and Context.
- `component_analyst.py`: Detailed analysis of classes and functions.
- `dependency_analyst.py`: Analysis of module interactions.
- `map_critic.py`: Self-correction loop for documentation quality.

### Linter Graph (`linter_graph/`)
**Entry Point**: `linter_graph_main.py`
**Purpose**: Automated enforcement of Structural Invariants (DAG, Size, Depth).

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- Ollama installed and running locally
- Required Ollama model: `gemma3:4b-it-qat` (configurable in `evolving_graphs/agent_graph/agent_config.py`)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Ollama service and pull the required model:
   ```bash
   # Start Ollama (if not running)
   ollama serve

   # Pull the configured model
   ollama pull gemma3:4b-it-qat
   ```

4. Verify installation:
   ```bash
   # Test the linter
   python -m evolving_graphs.linter_graph.linter_graph_main

   # Test the agent with a simple goal
   python -m evolving_graphs.agent_graph.agent_graph_main --goal "Create a hello world function"
   ```

## Usage

### Running the Agent Graph

The agent is designed to be run via the `run_graphs.py` orchestrator, which handles sandboxing and execution.

```python
# run_graphs.py
from evolving_graphs.agent_graph.agent_graph_main import main
from evolving_graphs.sandboxer_graph.sandboxer_graph_main import main as sandboxer_main

# 1. Create a sandbox
sandbox_path = sandboxer_main("agent_graph")

# 2. Run the agent in the sandbox
agent_result = main("Your Goal Here", sandbox_path)
```

To run it directly from the command line (for testing):
```bash
python -m evolving_graphs.agent_graph.agent_graph_main --goal "Your Goal" --target_folder "/path/to/target"
```

The agent will:
- Validate and persist the goal (10-500 characters, no dangerous patterns)
- Load existing session state if available
- Execute the scout→planner→executor→verifier→commit pipeline iteratively
- Generate, test, and refine code through safe sandboxed execution
- Save progress and learned patterns automatically

### Running the Linter Graph

Check architectural compliance:

```bash
# Check entire Genome
python -m evolving_graphs.linter_graph.linter_graph_main

# Check specific file
python -m evolving_graphs.linter_graph.linter_graph_main evolving_graphs/agent_graph/agent_graph_main.py
```

The linter validates:
- Import compliance and mandatory signposts
- File size limits (3000 tokens)
- Code duplication (DRY principle)
- Entry point designation
- Orchestrator privilege patterns
- Cross-Graph import restrictions
- Structural conformance

### Workflow Integration

- **Development**: Use agent for autonomous code generation, linter for compliance validation
- **Evolution**: Agent creates child Genomes in `candidates/` subdirectories via recursive evolution protocol
- **Monitoring**: Observe detailed pipeline execution through console output
- **Interruption**: Ctrl+C preserves state for resumable sessions
- **Learning**: Memory system improves performance based on successful patterns

## Dependencies

### Core Dependencies
- **ollama**: Local LLM integration for AI model interactions
- **chromadb**: Persistent memory database (located at project root `/memory_db/`)

### System Requirements
- Python 3.7+
- Ollama runtime environment
- Local LLM model support (Ollama)

## Contributing

Contributions must adhere to Genome architectural rules defined in `rules.md`. All changes require:

1. Passing all linter checks: `python -m evolving_graphs.linter_graph.linter_graph_main`
2. Maintaining shallow architecture (modules in root or direct subdirectories only)
3. Including explanatory comments on all relative imports
4. Keeping modules under 3000 tokens
5. Avoiding code duplication (DRY enforcement)
6. Following semantic naming (`domain_responsibility.py`)
7. Ensuring empty `__init__.py` files
8. Graph decoupling (no cross-Graph imports)

### Development Workflow
1. Make changes within Genome structure
2. Run linter: `python -m evolving_graphs.linter_graph.linter_graph_main`
3. Test with agent goals
4. Update documentation as needed

## License

See LICENSE file for licensing information.