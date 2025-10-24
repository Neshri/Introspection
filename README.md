# AgentTree

## Project Description

AgentTree is an autonomous AI agent system that implements an iterative pipeline approach to generate and improve Python code. The system leverages multiple specialized intelligence services working together through coordinated algorithmic processes to transform natural language goals into executable, high-quality code solutions.

The agent operates through a structured pipeline that integrates exploration, planning, code generation, execution, and evaluation phases. Each iteration refines the codebase through safe execution testing and multi-dimensional quality assessment. The system maintains persistent state across sessions and incorporates learning mechanisms to improve performance based on successful patterns.

## Features

- **Pipeline-Based Code Generation**: Iterative pipeline approach for systematic code development and improvement
- **Multi AI Intelligence System**: Specialized intelligence services including Scout (exploration), Planner (strategy), LLM Service (Ollama integration), Code Evaluator (quality assessment), Code Executor (safe execution), Critic (review), and Prompt Tracker (learning)
- **Safe Code Execution**: Sandboxed subprocess execution with timeout protection and resource limits
- **Architectural Compliance**: Automated linting system ensuring adherence to shallow architecture principles
- **State Persistence**: Saves and loads project state across sessions for continuous development
- **Modular Intelligence Services**: Extensible architecture for adding new AI capabilities and specializations
- **Ollama Integration**: Local LLM model support for code generation and evaluation
- **Goal-Driven Development**: Accepts natural language goals and translates them into executable code

## Installation

### Prerequisites

- Python 3.7 or higher
- Ollama installed and running locally
- Required Ollama model: `gemma3:4b-it-qat` (or as configured in `agent_tree/agent_config.py`)

### Setup Steps

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd SelfEvolveExperiment
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
    python -m linter.linter_main

    # Test the agent with a simple goal
    python -m agent_tree.agent_tree_main --goal "Create a hello world function"
    ```

## Usage

Run the AgentTree system using the command-line interface:

```bash
python -m agent_tree.agent_tree_main --goal "Your programming goal here"
```

For example:
```bash
python -m agent_tree.agent_tree_main --goal "Write a Python function to calculate pi using Monte Carlo simulation with 10000 samples"
```

The agent will:
- Initialize with the specified goal
- Load any existing project state from previous sessions
- Execute the development pipeline iteratively
- Save progress automatically
- Continue until the goal is achieved or maximum turns reached

### Additional Commands

**Run the Linter to check architectural compliance:**
```bash
python -m linter.linter_main
```

**Run on a specific main file:**
```bash
python -m linter.linter_main agent_tree/agent_tree_main.py
```

### Interacting with the Agent

- **Monitoring**: Observe pipeline execution through detailed console output
- **Interrupting**: Use Ctrl+C to gracefully stop execution and preserve state
- **Resuming**: Previous sessions automatically resume from saved state
- **Goal Management**: Goals are validated and persisted across sessions

## Architecture Overview

AgentTree follows a shallow, AI-friendly architecture designed for autonomous code generation. The system adheres to strict architectural rules that enforce modularity, clarity, and maintainability. All modules reside either in the root directory or direct subdirectories, with no nested subdirectories allowed.

### Core Architecture Principles

The architecture is governed by the rules defined in `rules.md`, ensuring:

- **Shallow Architecture**: All modules in root directory or direct subdirectories only
- **Semantic Naming**: Clear domain_responsibility.py naming convention
- **Import Signposts**: Every import includes explanatory comments
- **File Size Limits**: No file exceeds 300 lines
- **DRY Enforcement**: No duplicated code blocks
- **Designated Entry Points**: Main executables named [context]_main.py

### Core Components

#### **Agent Tree Module** (`agent_tree/`)
The main autonomous agent system with the following key components:

- **Main Entry Point** (`agent_tree_main.py`): Command-line interface accepting goal parameters
- **Agent Core** (`agent_core.py`): Agent class managing goal-setting, validation, and execution loops
- **Configuration** (`agent_config.py`): Centralized settings and model configurations
- **Intelligence Services**:
  - `intelligence_llm_service.py`: Standardized LLM chat interface using Ollama
  - `intelligence_project_scout.py`: Project exploration and capability assessment
  - `intelligence_plan_generator.py`: Strategic planning and implementation strategies
  - `intelligence_code_evaluator.py`: Code quality and performance evaluation
  - `intelligence_code_executor.py`: Safe code execution in sandboxed environments
  - `intelligence_llm_critic.py`: Code critique and improvement suggestions
  - `intelligence_prompt_tracker.py`: Learning from successful prompt patterns

- **Pipeline Services**:
  - `pipeline_pipeline_runner.py`: Main pipeline orchestration and execution
  - `pipeline_pipeline_executor.py`: Code modification and application
  - `pipeline_code_verifier.py`: Code validation and quality checks

- **Engine Components**:
  - `engine_mcts_algorithm.py`: Monte Carlo Tree Search implementation
  - `engine_search_node.py`: Search tree node structures and utilities

- **Utilities**:
  - `utils_collect_modules.py`: Module discovery and analysis
  - `utils_state_persistence.py`: Session state saving and loading
  - `backpack_formatter.py`: Context formatting for LLM interactions

#### **Linter Module** (`linter/`)
Automated code quality and architectural compliance checker:

- **Main Entry Point** (`linter_main.py`): Command-line interface for rule validation
- **Rule Checkers**:
  - `linter_rules_recovery.py`: Architectural recovery and violation diagnosis
  - `linter_rules_importcomments.py`: Import comment validation
  - `linter_rules_importcompliance.py`: Import structure compliance
  - `linter_rules_duplication.py`: Code duplication detection
  - `linter_rules_filesize.py`: File size limit enforcement
  - `linter_rules_compliance.py`: Final compliance verification
- **Core Utilities** (`linter_utils_core.py`): Shared linter functionality

### Data Flow Architecture

The AgentTree system follows a pipeline-based data flow with integrated intelligence services:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Goal Input    │───▶│   Agent Core    │───▶│   Pipeline      │
│   (--goal)      │    │   (agent_core)  │    │   Runner        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                        │                        │
          │                        │                        │
          ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  State Memory   │◀───│ Intelligence    │───▶│  Code Output    │
│ (persistence)   │    │ Services        │    │  (execution)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Detailed Pipeline Flow:

1. **Goal Processing**: Parse and validate natural language goals
2. **State Loading**: Resume from previous session state if available
3. **Intelligence Gathering**: Scout explores requirements, Planner creates strategy
4. **Code Generation**: LLM service generates initial code solutions
5. **Code Execution**: Safe sandboxed execution with timeout protection
6. **Evaluation Loop**: Code Evaluator and Critic assess quality and functionality
7. **Iteration**: Pipeline runner coordinates multiple cycles of improvement
8. **Persistence**: Save successful results and learned patterns

### Key Design Patterns

#### Intelligence Service Pattern
```python
# Modular intelligence services with clear responsibilities
scout = Scout()  # Exploration and capability assessment
planner = Planner()  # Strategic planning and goal decomposition
llm_service = LLMService()  # Standardized AI model interactions
evaluator = CodeEvaluator()  # Quality and performance assessment
executor = CodeExecutor()  # Safe code execution
```

#### Pipeline Orchestration Pattern
```python
# Coordinated pipeline execution with state management
pipeline_runner = PipelineRunner(goal, current_state)
while not goal_achieved and turns < max_turns:
    result = pipeline_runner.run_pipeline()
    if result['success']:
        goal_achieved = True
    turns += 1
```

#### Safe Execution Pattern
```python
# Sandboxed execution with resource controls
result = subprocess.run(['python', code_file],
                        capture_output=True,
                        timeout=30,
                        cwd=safe_directory)
```

### State Persistence Architecture

The system maintains comprehensive state across sessions:

- **Goal Persistence**: Current development goals saved and validated
- **Code State**: Current codebase state with execution history
- **Learning Data**: Performance metrics and successful patterns
- **Configuration**: Model settings and system parameters

### Compliance and Quality Assurance

Built-in architectural compliance through the linter system ensures:

- **Import Clarity**: All custom imports include explanatory comments
- **File Size Control**: Automatic refactoring triggers for large files
- **Duplication Prevention**: Detection and elimination of code clones
- **Naming Standards**: Semantic domain_responsibility.py naming
- **Architecture Integrity**: Shallow structure maintenance

## Dependencies

This project has minimal dependencies focused on AI model integration and testing:

### Core Dependencies
- **ollama**: Local LLM model integration for AI-powered code generation and evaluation
- **pytest**: Testing framework for validation and quality assurance

### System Requirements
- Python 3.7+
- Ollama runtime environment
- Local LLM model (gemma3:4b-it-qat by default)

## Contributing

This project follows strict architectural guidelines defined in `rules.md`. All contributions must:

1. Pass all linter checks: `python -m linter.linter_main`
2. Maintain shallow architecture (no nested subdirectories)
3. Include explanatory comments on all custom imports
4. Keep files under 300 lines
5. Avoid code duplication
6. Follow semantic naming conventions (domain_responsibility.py)

### Development Workflow

1. Make changes to relevant modules
2. Run linter to check compliance: `python -m linter.linter_main`
3. Test functionality with sample goals
4. Update documentation as needed

## License

See LICENSE file for licensing information.