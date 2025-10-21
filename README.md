# SelfEvolveExperiment

## Project Description

SelfEvolveExperiment is an autonomous AI agent system that implements self-evolving intelligence through iterative planning, execution, and critique cycles. The system leverages the Ollama library to power two distinct AI personalities - an Executor and a Critic - working together to accomplish user-defined goals. The agent maintains persistent memory through a working document that accumulates project state across iterations, enabling it to handle long-term, complex tasks like story writing or software development.

The core architecture features a continuous loop where the Executor proposes plans or executes approved steps, while the Critic evaluates these actions for alignment with the goal. A background thread monitors for user input, allowing dynamic goal updates and interruptions, making the system adaptable to changing requirements.

## Features

- **Dual AI Personality System**: Executor for planning/execution and Critic for evaluation
- **Persistent Memory**: Working document accumulates project state across iterations
- **Interactive User Feedback**: [ASK_USER] feature allows the agent to seek real-time user input during execution
- **Dynamic Goal Updates**: Background thread enables goal changes without stopping the process
- **Autonomous Operation**: Continuous loop with thoughtful delays between cycles
- **Thread-Safe State Management**: Shared state handling with atomic goal updates

### [ASK_USER] Feature

The [ASK_USER] feature enhances the agent's adaptability by allowing it to actively seek external input when needed. When the Executor determines it needs clarification or additional context, it can trigger [ASK_USER] to pause the standard evaluation cycle and prompt the user for feedback. This input is captured, formatted as [USER FEEDBACK], and integrated directly into the working document, enriching subsequent iterations with authentic user insights.

## Installation

### Prerequisites

- Python 3.7 or higher
- Ollama installed and running locally
- 'gemma3:12b-it-qat' model pulled in Ollama

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
   ollama pull gemma3:12b-it-qat
   ```

## Usage

Run the AI agent system using:

```bash
python Main.py
```

The agent will start with a default goal (story writing) and begin its iterative process. You can monitor the progress through console output showing:
- Current iteration and goal
- Executor plans and actions
- Critic evaluations
- Working document updates

### Interacting with the Agent

- **Goal Updates**: Input new goals through the console prompt when it appears
- **User Feedback**: Respond to [ASK_USER] prompts when the agent seeks clarification
- **Monitoring**: Observe the agent's progress through detailed console logging

## Technical Details

### Architecture Components

- **Main Loop**: Infinite execution cycle alternating between Executor and Critic phases
- **User Input Thread**: Background daemon thread for real-time goal updates
- **State Management**: Global agent state with per-goal local variables
- **Prompt Templates**: Structured prompts for Executor (planning/execution) and Critic (evaluation) roles

### Key Functions

- `main_agent_loop()`: Core execution loop with plan-execute-critique cycles
- `user_input_thread()`: Background input monitoring for dynamic goal changes
- `get_llm_response()`: Ollama integration for AI model interactions

### State Variables

- `agent_state`: Global dictionary tracking current goal and running status
- `working_document`: Accumulative project state and progress
- `current_plan`: Active proposed step from Executor
- `critique`: Feedback from Critic evaluation
- `iteration`: Cycle counter for progress tracking

### Integration Notes

The [ASK_USER] feature integrates seamlessly into the existing workflow by adding a conditional check after Executor output. When triggered, it bypasses the Critic phase for that iteration, captures user input, and resumes normal operation with enhanced context.