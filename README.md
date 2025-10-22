# AgentTree

## Project Description

AgentTree is an autonomous AI agent that uses Monte Carlo Tree Search (MCTS) to generate creative stories. The system employs two AI personalities - an Executor that generates new story paragraphs and a Critic that evaluates story quality - working together through the MCTS algorithm to explore and optimize narrative development.

The agent builds stories iteratively by expanding a search tree where each node represents a story state. The MCTS algorithm balances exploration and exploitation to find the most promising story continuations, guided by the Critic's quality assessments. The system maintains persistent memory, allowing it to resume story generation across sessions.

## Features

- **MCTS-Powered Story Generation**: Uses Monte Carlo Tree Search to explore and optimize story development
- **Dual AI Personality System**: Executor generates new paragraphs, Critic evaluates quality on a 1-10 scale
- **Persistent Memory**: Saves and loads story progress between sessions
- **Iterative Refinement**: Builds stories paragraph by paragraph through multiple search cycles
- **Ollama Integration**: Leverages local LLM models for creative writing and evaluation

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

Run the story generation agent using:

```bash
python AgentTree/main.py
```

The agent will start with a default story goal and begin generating content using MCTS. Monitor the progress through console output showing:
- Current turn number
- Story paragraphs being committed to the narrative
- MCTS cycle progress

### Interacting with the Agent

- **Monitoring**: Observe the story development through console output
- **Interrupting**: Use Ctrl+C to stop the agent and save current progress
- **Resuming**: The agent automatically loads previous sessions on restart

## Technical Details

### Architecture Components

- **MCTS Engine**: Core search algorithm that explores story continuations
- **Node Structure**: Tree nodes representing story states with document content and metadata
- **LLM Handler**: Manages communication with Ollama for Executor and Critic prompts
- **State Manager**: Handles persistent memory loading and saving
- **Configuration**: Centralized settings for model, goals, and MCTS parameters

### Key Functions

- `run_mcts_cycle()`: Performs one full MCTS thinking cycle and returns best next node
- `expand_node()`: Creates new child nodes by generating story paragraphs
- `simulate_node()`: Evaluates story quality using the Critic
- `backpropagate()`: Updates tree statistics after evaluation
- `load_document_on_startup()`: Restores previous session state
- `save_document_state()`: Persists current story progress

### MCTS Process

1. **Selection**: Navigate tree using UCB1 formula to balance exploration/exploitation
2. **Expansion**: Generate new story paragraph when reaching leaf node
3. **Simulation**: Evaluate new story state with Critic (1-10 scale)
4. **Backpropagation**: Update visit counts and values up the tree

### Configuration

- **Model**: gemma3:4b-it-qat via Ollama
- **MCTS Iterations**: 10 cycles per turn
- **Goal**: Write engaging story about robot discovering music
- **Memory**: agent_memory_current.txt and agent_memory_previous.txt