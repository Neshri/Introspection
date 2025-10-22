# AgentTree

## Project Description

AgentTree is an autonomous AI agent that uses Monte Carlo Tree Search (MCTS) or linear pipeline approaches to generate and improve Python code. The system employs multiple AI personalities including Executor (code generation), Critic (quality evaluation), Evaluator (performance assessment), Tracker (learning and analytics), Scout (exploration), and Planner (strategy formulation) - working together through algorithmic processes to explore and optimize programming solutions.

The agent builds code iteratively by expanding a search tree where each node represents a code state. The MCTS algorithm balances exploration and exploitation to find the most promising code variations, guided by actual code execution results and the Critic's quality assessments. The system maintains persistent memory, allowing it to resume code generation across sessions, and includes self-improvement mechanisms that learn from successful prompt patterns.

## Features

- **MCTS-Powered Code Generation**: Uses Monte Carlo Tree Search to explore and optimize code development
- **Multi AI Personality System**: Executor generates new code, Critic evaluates functionality and correctness, Evaluator assesses performance, Tracker monitors learning, Scout explores new approaches, Planner creates strategic implementation plans
- **Code Execution Testing**: Runs generated code safely to validate functionality
- **Self-Improvement**: Learns from successful prompt patterns to improve future code generation
- **Persistent Memory**: Saves and loads code progress between sessions
- **Iterative Refinement**: Builds code through multiple search cycles with real execution feedback
- **Ollama Integration**: Leverages local LLM models for code generation and evaluation

## Installation

### Prerequisites

- Python 3.7 or higher
- Ollama installed and running locally
- 'gemma3:4b-it-qat' model pulled in Ollama

### Setup Steps

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd SelfEvolveExperiment
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure Ollama is running and the required model is available:
    ```bash
    ollama pull gemma3:4b-it-qat
    ```

## Usage

Run the code generation agent using:

```bash
python AgentTree/main.py
```

The agent will start with a default programming goal (Monte Carlo pi calculation) and begin generating code using MCTS. Monitor the progress through console output showing:
- Current turn number
- Code being committed to the solution
- MCTS cycle progress and execution results
- Performance metrics and improvement tracking

### Interacting with the Agent

- **Monitoring**: Observe code development, execution results, and improvement metrics
- **Interrupting**: Use Ctrl+C to stop the agent and save current progress
- **Resuming**: The agent automatically loads previous code sessions on restart
- **Self-Improvement**: Agent learns from successful patterns and adapts its approach

## Architecture Overview

AgentTree follows a modular architecture designed for autonomous code generation through Monte Carlo Tree Search (MCTS) or linear pipeline approaches. The system is organized into a hierarchical structure where each component plays a specific role in the iterative code refinement process.

### Core Architecture Components

The architecture consists of five main layers, each handling distinct responsibilities:

#### 1. **Orchestration Layer** (`agent/`)
- **Main Entry Point** (`main.py`): Simple launcher that initializes the agent
- **Agent Core** (`agent.py`): Continuous loop managing the overall agent lifecycle, turn progression, and state persistence

#### 2. **Search Engine Layer** (`agent/engine/`)
- **MCTS Engine** (`mcts.py`): Implements the four-phase MCTS algorithm (Selection, Expansion, Simulation, Backpropagation)
- **Node Structure** (`node.py`): Tree nodes containing code state, execution results, and performance metrics

#### 3. **Intelligence Layer** (`agent/intelligence/`)
- **LLM Executor** (`llm_executor.py`): Generates new code solutions and variations
- **LLM Critic** (`llm_critic.py`): Evaluates code quality, correctness, and functionality
- **LLM Evaluator** (`llm_evaluator.py`): Assesses performance metrics and optimization opportunities
- **LLM Tracker** (`llm_tracker.py`): Monitors learning patterns and analytics
- **Scout** (`scout.py`): Explores new code approaches and innovative solutions
- **Planner** (`planner.py`): Creates structured implementation plans and strategies

#### 4. **Utilities Layer** (`agent/utils/`)
- **State Manager** (`state_manager.py`): Persistent memory management across sessions
- **Configuration** (`config.py`): Centralized settings, prompt templates, and system parameters

#### 5. **Execution Environment**
- **Safe Code Execution**: Sandboxed subprocess execution with timeout protection
- **Test Case Validation**: Automatic parsing and running of goal-embedded test cases
- **Performance Tracking**: Self-improvement through historical prompt performance analysis

### Data Flow Architecture

The agent's operation follows a cyclical data flow pattern:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agent Loop    │───▶│   MCTS Cycle    │───▶│   Code State    │
│   (agent.py)    │    │   (mcts.py)     │    │   Updates       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  State Memory   │◀───│   LLM Calls     │    │  Execution     │
│ (state_manager) │    │ (intelligence)  │    │  Results       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Detailed Data Flow:

1. **Initialization**: Load previous session state or start with default code
2. **MCTS Selection**: Traverse tree using UCB1 formula to find promising nodes
3. **Expansion**: Generate new code variations via Executor LLM prompts, with Scout exploring alternative approaches
4. **Simulation**: Execute code safely and evaluate with multi-dimensional metrics:
   - Runtime execution results
   - Test case pass rates
   - Critic LLM quality assessment
   - Evaluator performance analysis
   - Tracker learning insights
5. **Backpropagation**: Update tree statistics up to root node
6. **Commitment**: Select best child node as next code state
7. **Persistence**: Save progress and repeat cycle

### Key Design Patterns

#### Multi AI Personality Pattern
```python
# Multiple AI personalities work together
response = llm_executor.generate_code(goal, current_code)
critic_score = llm_critic.evaluate_quality(goal, generated_code)
evaluator_score = llm_evaluator.assess_performance(generated_code)
tracker_insights = llm_tracker.analyze_patterns()
scout_exploration = scout.explore_alternatives(goal)
plan = planner.create_plan(goal, backpack_context)
```

#### Safe Execution Pattern
```python
# Isolated subprocess execution with resource limits
result = subprocess.run(['python', temp_file],
                       capture_output=True,
                       timeout=30,
                       cwd=temp_dir)
```

#### Self-Improvement Pattern
```python
# Learn from successful prompt patterns
best_prompts = get_best_prompt_variations(limit=3)
# Adapt future prompts based on historical performance
```

### MCTS Algorithm Implementation

The MCTS implementation follows the standard four-phase algorithm with code-specific adaptations:

#### Selection Phase
Uses UCB1 formula to balance exploration/exploitation:
```python
ucb_value = (node.value / node.visits) + math.sqrt(2 * math.log(parent.visits) / node.visits)
```

#### Expansion Phase
Generates new code variations when reaching unexplored nodes:
```python
new_code = llm_executor.generate_code(goal, node.document_state)
scout_variations = scout.explore_alternatives(goal, node.document_state)
combined_variations = [new_code] + scout_variations
new_nodes = [Node(document_state=variation, parent=node, plan=variation) for variation in combined_variations]
```

#### Simulation Phase
Combines actual execution with multi-dimensional AI evaluation:
```python
execution_result = execute_code(node.document_state)
critic_score = llm_critic.evaluate_quality(node.document_state, goal)
evaluator_score = llm_evaluator.assess_performance(node.document_state, execution_result)
tracker_insights = llm_tracker.analyze_learning(node.document_state, execution_result)
combined_score = (execution_result.score + critic_score + evaluator_score + tracker_insights) // 4
```

#### Backpropagation Phase
Updates statistics throughout the tree:
```python
while temp_node:
    temp_node.visits += 1
    temp_node.value += score
    temp_node = temp_node.parent
```

### Self-Improvement System

The agent maintains a learning loop through prompt performance tracking:

- **Performance Logging**: JSON-based storage of prompt effectiveness metrics
- **Success Pattern Analysis**: Identifies high-performing prompt variations
- **Adaptive Prompt Engineering**: Injects successful patterns into future generations
- **Historical Learning**: Maintains rolling window of recent performance data

### Key Insights

#### Architectural Strengths
- **Modular Design**: Clear separation of concerns enables easy extension and maintenance
- **Persistent State**: Session resumption prevents loss of progress
- **Safe Execution**: Sandboxed code running prevents system compromise
- **Dual Evaluation**: Combined runtime and AI assessment provides robust quality metrics
- **Self-Learning**: Continuous improvement through performance feedback loops

#### Technical Trade-offs
- **Computational Cost**: MCTS exploration requires multiple LLM calls per cycle
- **Memory Usage**: Growing search tree demands efficient pruning strategies
- **Execution Time**: Safe subprocess execution adds overhead compared to direct evaluation
- **Prompt Complexity**: Self-improvement system increases prompt engineering complexity

#### Scalability Considerations
- **Parallelization**: MCTS phases can be distributed across multiple processes
- **Caching**: Execution results and prompt responses can be cached for efficiency
- **Pruning**: Tree size management through selective node retention
- **Batch Processing**: Multiple test cases can be evaluated simultaneously

## Architectural Guidelines

- **File Size**: No file you create or modify may exceed 300 lines.
- **Refactoring Trigger**: If a file approaches this limit, immediately refactor by moving cohesive functions to a new, well-named module.
- **The Golden Rule - Import Signposts**: For every custom module you import, you must add a comment on the same line explaining that module's purpose and its role in the current file. This is the most important rule.
- **Directory Cohesion and Size**: A directory should represent a single, cohesive responsibility. When a directory contains more than seven files, or its files serve multiple purposes, it must be refactored by creating more specific, well-named subdirectories.

### Configuration

- **Model**: gemma3:4b-it-qat via Ollama
- **MCTS Iterations**: 10 cycles per turn
- **Goal**: Write Python function to calculate pi using Monte Carlo method
- **Memory**: agent_memory_current.txt and agent_memory_previous.txt
- **Performance Logs**: prompt_performance.json and improvement_history.txt