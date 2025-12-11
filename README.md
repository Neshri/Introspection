# agent_graph: Code Understanding Agent

## Overview

agent_graph is a hybrid code analysis agent that uses AST-based static analysis for precise structural mapping, combined with LLM-based verification to generate grounded documentation. It prioritizes traceability by linking every description back to a specific code hash, allowing users to audit the AI's understanding.

## Architecture

The codebase follows structural standards:
- Shallow architecture (max depth 1)
- No cross-graph imports
- Atomic modules with semantic naming
- Generated documentation from code structure analysis

## Components

### Agent Graph (`evolving_graphs/agent_graph/`)

**Entry Point**: `agent_graph_main.py`

**Core Components**:
- `agent_core.py`: CrawlerAgent implementation
- `agent_config.py`: Configuration (DEFAULT_MODEL = "granite4:3b")
- `memory_core.py`: ChromaDB wrapper for persistent storage
- `report_renderer.py`: Project analysis report generation

**Analysis Engine**:
- `graph_analyzer.py`: AST-based dependency mapping (structural analysis)
- `module_classifier.py`: Structural role analysis
- `module_contextualizer.py`: Code logic translation to natural language
- `component_analyst.py`: Class and function analysis
- `dependency_analyst.py`: Module interaction analysis
- `semantic_gatekeeper.py`: Analysis quality assurance
- `task_executor.py`: Goal-oriented analysis orchestration

### Linter Graph (`evolving_graphs/linter_graph/`)

**Entry Point**: `linter_graph_main.py`

Validates architectural compliance:
- Import compliance and documentation requirements
- File size optimization
- Code duplication detection
- Entry point clarity
- Cross-graph isolation
- Structural conformance

### Log Analyzer Graph (`evolving_graphs/loganalyzer_graph/`)

**Entry Point**: `loganalyzer_graph_main.py`

Log analysis implementation (architecture in place).

## Setup

### Prerequisites
- Python 3.7+
- Ollama installed and running
- Required model: `granite4:3b` (configured in `evolving_graphs/agent_graph/agent_config.py`)

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start Ollama and pull model:
   ```bash
   ollama serve
   ollama pull granite4:3b
   ```

3. Verify installation:
   ```bash
   python -m evolving_graphs.linter_graph.linter_graph_main
   python -m evolving_graphs.agent_graph.agent_graph_main --goal "Analyze project structure" --target_folder "/path/to/project"
   ```

## Usage

### Running the Agent

```python
from evolving_graphs.agent_graph.agent_graph_main import main

result = main("Analyze project structure", "/path/to/target")
print(result)
```

### Running the Linter

```bash
python -m evolving_graphs.linter_graph.linter_graph_main
```

## System Components and Limitations

**What Each Component Actually Does:**

1. **AST Analysis (Deterministic)**: Provides precise structural mapping of code relationships without hallucination. This includes dependency graphs, import analysis, and structural classification.

2. **LLM Synthesis (Probabilistic)**: Generates semantic descriptions and natural language explanations. These descriptions CAN hallucinate and should be treated as interpretations rather than facts.

3. **Verification System**: Provides provenance tracking by linking descriptions to specific code hashes, allowing audit of AI understanding. This tracks WHAT was analyzed, not WHETHER the analysis is correct.

**System Limitations:**
- LLM-generated descriptions may contain factual errors, misinterpretations, or hallucinations
- AST analysis is deterministic but limited to structural relationships
- "Verification" only proves traceability to source code, not correctness of interpretations
- Formatting errors and meta-commentary hallucinations still occur
- System links descriptions to code hashes but doesn't prevent semantic misinterpretation

**What This System Actually Solves:**
- Provides deterministic structural analysis of code relationships
- Offers traceable AI-generated descriptions linked to specific code locations
- Enables auditability of AI understanding through hash-based provenance

**What This System Doesn't Solve:**
- Does not eliminate LLM hallucinations in generated descriptions
- Does not guarantee correctness of semantic interpretations
- Does not replace human code review or validation

**Completed Components**:
- Module graph analysis
- Dependency graph generation using deterministic AST analysis
- Code logic understanding and contextualization
- Project report rendering
- ChromaDB memory management
- Architectural compliance validation

## Dependencies

### Core Dependencies
- **ollama**: Local LLM integration
- **chromadb**: Persistent memory database (stored at `./chroma_db`)

### System Requirements
- Python 3.7+
- Ollama runtime environment
- Local LLM model support

## Development

Contributions must adhere to architectural rules defined in `rules.md`:

1. Pass linter checks: `python -m evolving_graphs.linter_graph.linter_graph_main`
2. Maintain shallow architecture
3. Follow semantic naming (`domain_responsibility.py`)
4. Ensure empty `__init__.py` files
5. No cross-graph imports

## Technical Configuration

- **Memory Database**: ChromaDB configured for `./chroma_db`
- **Default Model**: `granite4:3b` in `agent_config.py`
- **Context Limit**: 4096 tokens
- **Analysis Method**: Hybrid system using deterministic AST analysis + probabilistic LLM descriptions
- **Quality Assurance**: Verification provides provenance tracking, not correctness validation

## License

See LICENSE file for licensing information.