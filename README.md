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

The Genome adheres to strict architectural rules designed for AI comprehension and autonomous evolution:

### Core Principles
- **Shallow Architecture**: All modules reside in root or direct subdirectories only
- **Semantic Naming**: `domain_responsibility.py` convention for module files
- **Designated Entry Points**: Each Graph has exactly one `[graph_name]_main.py` file
- **Graph Decoupling**: No cross-Graph imports; interaction via subprocess execution only
- **Strictly Relative Paths**: All paths relative to module location, no upward traversal beyond `/evolving_graphs/`
- **Intra-Graph Relative Imports**: Within a Graph, imports must be relative with mandatory explanatory comments
- **Acyclic Dependencies**: Import graphs must be Directed Acyclic Graphs (DAGs)
- **Role Isolation**: Intelligence services cannot directly interact; all data flows through orchestrators
- **Orchestrator Privilege**: Only designated classes (e.g., PipelineRunner) may hold instances of multiple roles
- **DRY Enforcement**: Extract 5+ line duplications to `_utils.py` modules
- **Empty `__init__.py`**: All initialization files must remain empty

### Execution and Evolution
- **Recursive Evolution Protocol**: Child Genomes created in `candidates/` subdirectories
- **Safe Sandboxing**: Isolated execution with resource limits (30s CPU, temporary directories)
- **Memory Integration**: Persistent learning with token limits (1000 per memory) and decay
- **State Persistence**: Session management across restarts

## Graphs Description

### Agent Graph (`agent_graph/`)
**Entry Point**: `agent_graph_main.py`  
**Purpose**: Autonomous AI agent implementing iterative code generation pipeline for natural language goals.

#### Core Infrastructure
- `agent_core.py`: Agent class for goal validation (10-500 chars, no dangerous patterns), persistence, and execution loops
- `agent_config.py`: Centralized configuration for LLM models, timeouts, and system parameters
- `pipeline_pipeline_runner.py`: Main orchestrator implementing scout→planner→executor→verifier→commit pipeline
- `memory_interface.py`: External persistent memory system (ChromaDB-based, outside Genome) with token limits and decay mechanisms

#### Intelligence Services (Role Isolation Pattern)
- `intelligence_project_scout.py`: Scout class exploring project structure and relevance via keyword analysis and LLM evaluation
- `intelligence_plan_generator.py`: Planner class creating strategic implementation plans from scout data
- `intelligence_llm_service.py`: Standardized Ollama integration for AI model interactions
- `intelligence_code_executor.py`: Safe code generation with iterative refinement
- `intelligence_llm_critic.py`: Code quality assessment and critique
- `intelligence_prompt_tracker.py`: Learning from successful prompt patterns

#### Execution and Safety
- `pipeline_pipeline_executor.py`: Code modification and application logic
- `pipeline_code_verifier.py`: Architecture compliance and syntax validation
- Sandbox system (`sandbox_*.py`): Isolated execution with resource limits and temporary directories

#### Utilities
- `utils_state_persistence.py`: Session management across restarts
- `utils_collect_modules.py`: Project structure analysis
- `agent_backpack_formatter.py`: Context preparation for LLM interactions

### Linter Graph (`linter_graph/`)
**Entry Point**: `linter_graph_main.py`  
**Purpose**: Automated compliance checker ensuring adherence to shallow, AI-friendly architectural rules.

#### Rule Validation Systems
- `linter_rules_recovery.py`: Architectural recovery protocol implementation
- `linter_rules_compliance.py`: Final compliance verification
- `linter_rules_crossgraph.py`: Cross-Graph import validation
- `linter_rules_duplication.py`: DRY enforcement and duplication detection
- `linter_rules_entrypoints.py`: Designated entry point validation
- `linter_rules_filesize.py`: 3000 token limit enforcement
- `linter_rules_importcomments.py`: Mandatory import signpost validation
- `linter_rules_importcompliance.py`: Intra-Graph import structure compliance
- `linter_rules_initfiles.py`: Empty `__init__.py` enforcement
- `linter_rules_orchestrator.py`: Orchestrator privilege pattern validation

#### Core Utilities
- `linter_utils_core.py`: Shared utilities for comment detection and import analysis

## AI-Friendly Features

The Genome is explicitly designed for AI comprehension and autonomous operation:

- **Explicit Structure**: Clear naming, directory layout, and entry points enable "crawlable" codebase exploration
- **Import Signposts**: Mandatory same-line comments explain every relative import's purpose
- **Modular Roles**: Intelligence services are isolated, single-responsibility classes
- **Comprehensive Linting**: Automated validation ensures consistent, rule-compliant code
- **Memory Learning**: Performance-based feedback with decay and pruning improves autonomous performance
- **Pipeline Orchestration**: Linear data flow prevents complex interdependencies
- **Sandbox Safety**: Protected execution prevents system damage during code generation
- **Token Limits**: File size constraints ensure focused responsibilities and manageability
- **Role Isolation**: Data flows through orchestrators, enabling clear responsibility boundaries
- **Semantic Naming**: Domain-driven filenames provide immediate context understanding

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

Execute the agent with a natural language goal:

```bash
python -m evolving_graphs.agent_graph.agent_graph_main --goal "Your programming goal here"
```

Example:
```bash
python -m evolving_graphs.agent_graph.agent_graph_main --goal "Write a Python function to calculate pi using Monte Carlo simulation with 10000 samples"
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