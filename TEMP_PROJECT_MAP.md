# Project Context Map

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates the initialization of an agent that runs to retrieve project map and processing order. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 main`**: Initializes an agent, runs it to retrieve project map and processing order, synthesizes system summary, renders report, cleans up memory for 5 turns, and returns analysis complete response. [2]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Orchestrates retrieval of project maps and processing orders, synthesizes system summaries, renders reports, and manages memory cleanup for five turns using CrawlerAgent. [3]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `4a2f71` [1]: Orchestrates the initialization of an agent that runs to retrieve project map and processing order. _(Source: Synthesis (based on [2]))_
> 🆔 `376e89` [2]: Initializes an agent, runs it to retrieve project map and processing order, synthesizes system summary, renders report, cleans up memory for 5 turns, and returns analysis complete response. _(Source: main)_
> 🆔 `75b648` [3]: Orchestrates retrieval of project maps and processing orders, synthesizes system summaries, renders reports, and manages memory cleanup for five turns using CrawlerAgent. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` The Agent Core module Orchestrates the CrawlerAgent to manage the retrieval of project maps and processing orders, synthesizes system summaries, renders reports, and coordinates cleanup of memory states over five turns while defining various configurations and dependencies.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Initializes attributes such as goal, target root, and creates ChromaMemory instance; runs CrawlerAgent to retrieve project map, processing order, synthesizes system summary, renders report, cleans up memory for 5 turns, and returns analysis complete response. [2]
- **`🔌 🔌 CrawlerAgent.run`**: Runs the CrawlerAgent, retrieves project map and processing order, synthesizes system summary, renders report, cleans up memory for 5 turns, and returns analysis complete response. [3]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Formats and processes the response content from the Ollama chat API, stripping unnecessary whitespace before returning it for further use. [4]
- **`agent_config.py`**: Defines constants for model and context limit used by agent_core. [5]
- **`semantic_gatekeeper.py`**: Validates and filters inputs to ensure compliance before passing them for further processing. [6]
- **`report_renderer.py`**: Orchestrates generation of markdown report detailing project context map, including system summary, module counts, categorized modules with dependencies, and presentation order. [7]
- **`memory_core.py`**: Manages the interaction between agent_core.py and ChromaDB to persistently store, query, update, and cleanup memory data for enhanced context-aware decision-making. [8]
- **`summary_models.py`**: Aggregates and organizes technical documentation elements for modules, dependencies, dependents, public API entries, alerts, and claims within the software project. [9]
- **`map_synthesizer.py`**: Synthesizes architectural summaries by grouping modules according to their archetypes, generating detailed group syntheses, and producing an overarching system architecture narrative through structured JSON output. [10]
- **`agent_util.py`**: Analyzes project dependencies to generate a context map for AI agents and delegates dependency analysis tasks to `project_pulse` function. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b211bc` [1]: The Agent Core module Orchestrates the CrawlerAgent to manage the retrieval of project maps and processing orders, synthesizes system summaries, renders reports, and coordinates cleanup of memory states over five turns while defining various configurations and dependencies. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `6e51a7` [2]: Initializes attributes such as goal, target root, and creates ChromaMemory instance; runs CrawlerAgent to retrieve project map, processing order, synthesizes system summary, renders report, cleans up memory for 5 turns, and returns analysis complete response. _(Source: class CrawlerAgent)_
> 🆔 `812d96` [3]: Runs the CrawlerAgent, retrieves project map and processing order, synthesizes system summary, renders report, cleans up memory for 5 turns, and returns analysis complete response. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `99d9c7` [4]: Formats and processes the response content from the Ollama chat API, stripping unnecessary whitespace before returning it for further use. _(Source: Import llm_util.py)_
> 🆔 `ed4486` [5]: Defines constants for model and context limit used by agent_core. _(Source: Import agent_config.py)_
> 🆔 `435c0a` [6]: Validates and filters inputs to ensure compliance before passing them for further processing. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `fc63a6` [7]: Orchestrates generation of markdown report detailing project context map, including system summary, module counts, categorized modules with dependencies, and presentation order. _(Source: Import report_renderer.py)_
> 🆔 `193de6` [8]: Manages the interaction between agent_core.py and ChromaDB to persistently store, query, update, and cleanup memory data for enhanced context-aware decision-making. _(Source: Import memory_core.py)_
> 🆔 `0f79d7` [9]: Aggregates and organizes technical documentation elements for modules, dependencies, dependents, public API entries, alerts, and claims within the software project. _(Source: Import summary_models.py)_
> 🆔 `680f9b` [10]: Synthesizes architectural summaries by grouping modules according to their archetypes, generating detailed group syntheses, and producing an overarching system architecture narrative through structured JSON output. _(Source: Import map_synthesizer.py)_
> 🆔 `6aef23` [11]: Analyzes project dependencies to generate a context map for AI agents and delegates dependency analysis tasks to `project_pulse` function. _(Source: Import agent_util.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Analyzes project dependencies to generate a context map for AI agents.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns the result of `Dict[str, Any]` to `ProjectGraph`. [2]
- **`🔌 class ProjectSummarizer`**: Installs necessary dependencies and initializes processing for the project, computing topological order of modules. [3]
- **`🔌 project_pulse`**: Creates a dependency graph, summarizes it, and returns module contexts and processing order [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Iterates over cycles, updating module contexts based on dependencies and critiques. [5]
- **`🔒 _create_module_context`**: Creates module context by initializing ModuleContextualizer, calling contextualize_module with critique instruction, setting file_path if missing, and returning the ModuleContext. [6]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Validates and filters inputs to ensure compliance before passing them for further processing. [7]
- **`graph_analyzer.py`**: Analyzes Python module structure, extracts dependencies and TODO comments, constructs dependency graph to understand cross-module interactions within `agent_util.py`. [8]
- **`report_renderer.py`**: Orchestrates generation of markdown report detailing project context map, including system summary and categorized modules with dependencies for presentation order. [9]
- **`map_critic.py`**: Orchestrates documentation quality analysis by parsing project map content into modules and providing detailed critiques for up to three modules. [10]
- **`summary_models.py`**: Centralizes management of module roles, dependencies, dependents, public API entries, alerts, and claims for technical documentation. [11]
- **`module_contextualizer.py`**: Populates the module context by performing component, dependency, and archetype analysis based on classifier classification of module data. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d709bc` [1]: Analyzes project dependencies to generate a context map for AI agents. _(Source: Synthesis (based on [2], [3], [5], [6], [4]))_
> 🆔 `250d88` [2]: Assigns the result of `Dict[str, Any]` to `ProjectGraph`. _(Source: ProjectGraph)_
> 🆔 `b4ce7a` [3]: Installs necessary dependencies and initializes processing for the project, computing topological order of modules. _(Source: class ProjectSummarizer)_
> 🆔 `e97ccc` [4]: Creates a dependency graph, summarizes it, and returns module contexts and processing order _(Source: project_pulse)_
> 🆔 `c356eb` [5]: Iterates over cycles, updating module contexts based on dependencies and critiques. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `d1ff4c` [6]: Creates module context by initializing ModuleContextualizer, calling contextualize_module with critique instruction, setting file_path if missing, and returning the ModuleContext. _(Source: _create_module_context)_
> 🆔 `6460fa` [7]: Validates and filters inputs to ensure compliance before passing them for further processing. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `36db32` [8]: Analyzes Python module structure, extracts dependencies and TODO comments, constructs dependency graph to understand cross-module interactions within `agent_util.py`. _(Source: Import graph_analyzer.py)_
> 🆔 `e37d2d` [9]: Orchestrates generation of markdown report detailing project context map, including system summary and categorized modules with dependencies for presentation order. _(Source: Import report_renderer.py)_
> 🆔 `e555e0` [10]: Orchestrates documentation quality analysis by parsing project map content into modules and providing detailed critiques for up to three modules. _(Source: Import map_critic.py)_
> 🆔 `d5e32f` [11]: Centralizes management of module roles, dependencies, dependents, public API entries, alerts, and claims for technical documentation. _(Source: Import summary_models.py)_
> 🆔 `816726` [12]: Populates the module context by performing component, dependency, and archetype analysis based on classifier classification of module data. _(Source: Import module_contextualizer.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes system components to extract their structural and behavioral characteristics, synthesizing detailed role summaries.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Instantiates `ComponentAnalyst` class, setting its `gatekeeper` and `task_executor` attributes. [2]
- **`🔌 class SkeletonTransformer`**: Removes docstrings and empty bodies from function, async function, and class definition nodes in Python AST. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes function signatures and associated behavior for each method, summarizing their purpose based on code structure and naming conventions. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Analyzes source code, applies SkeletonTransformer to generate module skeleton, and returns modified code or original if exception occurs. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Removes docstring from async function node and visits the node. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from class definition node, replaces empty body with `Pass()` statement if necessary, and recursively visits child nodes. [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Removes docstring from function definition node and recursively visits the node. [8]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Provides structured management and analysis of technical documentation elements related to module roles, dependencies, dependents, public API entries, alerts, and claims. [9]
- **`task_executor.py`**: Orchestrates execution flow, manages retries, and coordinates task processing without directly performing computations or data manipulation. [10]
- **`semantic_gatekeeper.py`**: Validates and filters user inputs to ensure they meet specified criteria before passing them for further processing in `component_analyst.py. [11]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `02c1c0` [1]: Analyzes system components to extract their structural and behavioral characteristics, synthesizing detailed role summaries. _(Source: Synthesis (based on [3], [8], [7], [6], [2], [4], [5]))_
> 🆔 `9211d4` [2]: Instantiates `ComponentAnalyst` class, setting its `gatekeeper` and `task_executor` attributes. _(Source: class ComponentAnalyst)_
> 🆔 `1d5ada` [3]: Removes docstrings and empty bodies from function, async function, and class definition nodes in Python AST. _(Source: class SkeletonTransformer)_
> 🆔 `b301cb` [4]: Analyzes function signatures and associated behavior for each method, summarizing their purpose based on code structure and naming conventions. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `d7a14a` [5]: Analyzes source code, applies SkeletonTransformer to generate module skeleton, and returns modified code or original if exception occurs. _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `6fc08f` [6]: Removes docstring from async function node and visits the node. _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `4f8ad8` [7]: Removes docstring from class definition node, replaces empty body with `Pass()` statement if necessary, and recursively visits child nodes. _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `1f069d` [8]: Removes docstring from function definition node and recursively visits the node. _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `6e3e17` [9]: Provides structured management and analysis of technical documentation elements related to module roles, dependencies, dependents, public API entries, alerts, and claims. _(Source: Import summary_models.py)_
> 🆔 `fde626` [10]: Orchestrates execution flow, manages retries, and coordinates task processing without directly performing computations or data manipulation. _(Source: Import task_executor.py)_
> 🆔 `d92631` [11]: Validates and filters user inputs to ensure they meet specified criteria before passing them for further processing in `component_analyst.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Analyzes and coordinates dependencies across modules, identifying relationships between services and components.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Initializes instance with provided gatekeeper and task_executor attributes, sanitizes text context by removing banned adjectives and trimming whitespace, determines guidance based on caller-callee type relationships in analysis of upstream context for imported dependencies using public API interactions and symbol usage patterns. [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes upstream context and usage of imported dependencies, generating explanations based on public API interactions and symbol usage patterns. [3]

### 🔗 Uses (Upstream)
- **`module_classifier.py`**: Classifies Python modules into entry points, data models, configurations, utilities, or services based on their names and source code structure. [4]
- **`summary_models.py`**: Aggregates and organizes technical documentation elements such as module roles, dependencies, dependents, public API entries, alerts, and claims for analysis in dependency_analyst.py. [5]
- **`task_executor.py`**: Orchestrates task execution flow and manages retries for goal logic in dependency_analyst.py. [6]
- **`semantic_gatekeeper.py`**: Validates and filters inputs to ensure compliance before passing them for further processing in dependency_analyst.py. [7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `bb53b3` [1]: Analyzes and coordinates dependencies across modules, identifying relationships between services and components. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `243c88` [2]: Initializes instance with provided gatekeeper and task_executor attributes, sanitizes text context by removing banned adjectives and trimming whitespace, determines guidance based on caller-callee type relationships in analysis of upstream context for imported dependencies using public API interactions and symbol usage patterns. _(Source: class DependencyAnalyst)_
> 🆔 `4cf002` [3]: Analyzes upstream context and usage of imported dependencies, generating explanations based on public API interactions and symbol usage patterns. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `2cb7f3` [4]: Classifies Python modules into entry points, data models, configurations, utilities, or services based on their names and source code structure. _(Source: Import module_classifier.py)_
> 🆔 `fe1c90` [5]: Aggregates and organizes technical documentation elements such as module roles, dependencies, dependents, public API entries, alerts, and claims for analysis in dependency_analyst.py. _(Source: Import summary_models.py)_
> 🆔 `2d58ba` [6]: Orchestrates task execution flow and manages retries for goal logic in dependency_analyst.py. _(Source: Import task_executor.py)_
> 🆔 `6909a4` [7]: Validates and filters inputs to ensure compliance before passing them for further processing in dependency_analyst.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Defines an active service that orchestrates code documentation auditing by parsing project map content into modules and analyzing each module for documentation quality to provide specific instructions for improvement.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Initializes an instance of MapCritic by assigning the provided gatekeeper to its gatekeeper attribute. Parses project map content into modules, analyzes each module for documentation quality, and critiques up to three modules with detailed instructions. [2]
- **`🔌 🔌 MapCritic.critique`**: Analyzes the parsed modules from `project_map_content`, generates critiques for each module, and returns up to three critiques as tuples of module name and critique instruction. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Validates and filters LLM outputs to ensure compliance, style, grounding, claim accuracy, word count, response length criteria, and banned content before passing for further processing in `map_critic.py`. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d3d90a` [1]: Defines an active service that orchestrates code documentation auditing by parsing project map content into modules and analyzing each module for documentation quality to provide specific instructions for improvement. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `d50d82` [2]: Initializes an instance of MapCritic by assigning the provided gatekeeper to its gatekeeper attribute. Parses project map content into modules, analyzes each module for documentation quality, and critiques up to three modules with detailed instructions. _(Source: class MapCritic)_
> 🆔 `70ce78` [3]: Analyzes the parsed modules from `project_map_content`, generates critiques for each module, and returns up to three critiques as tuples of module name and critique instruction. _(Source: 🔌 MapCritic.critique)_
> 🆔 `3ca18a` [4]: Validates and filters LLM outputs to ensure compliance, style, grounding, claim accuracy, word count, response length criteria, and banned content before passing for further processing in `map_critic.py`. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` The Map Synthesizer module defines and executes a service for synthesizing architectural summaries by grouping modules according to their archetypes, generating detailed group syntheses, and producing an overarching system architecture narrative through structured JSON output.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Inits an instance of MapSynthesizer by assigning the provided gatekeeper to its gatekeeper attribute. [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Groups modules by archetype and processing order, synthesizes each group, then synthesizes the system. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Aggregates technical documentation components and relationships to construct project documentation summary. [4]
- **`semantic_gatekeeper.py`**: Validates and filters LLM responses to ensure compliance before passing them for further processing in the map synthesizer pipeline. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `30ac62` [1]: The Map Synthesizer module defines and executes a service for synthesizing architectural summaries by grouping modules according to their archetypes, generating detailed group syntheses, and producing an overarching system architecture narrative through structured JSON output. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `265673` [2]: Inits an instance of MapSynthesizer by assigning the provided gatekeeper to its gatekeeper attribute. _(Source: class MapSynthesizer)_
> 🆔 `026bdf` [3]: Groups modules by archetype and processing order, synthesizes each group, then synthesizes the system. _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `c50c16` [4]: Aggregates technical documentation components and relationships to construct project documentation summary. _(Source: Import summary_models.py)_
> 🆔 `b747b8` [5]: Validates and filters LLM responses to ensure compliance before passing them for further processing in the map synthesizer pipeline. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Orchestrates the generation of a markdown report detailing the project context map, including system summary, module counts, categorized modules with dependencies, and renders each category in presentation order.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Initializes instance variables including context_map, output_file, system_summary; creates empty claim_map and sets ref_counter to 1. Renders markdown report of project context map detailing system summary, module counts, categorized modules with dependencies, and presentation order. [2]
- **`🔌 🔌 ReportRenderer.render`**: Generates a markdown report of the project context map, including system summary, module counts, categorized modules with dependencies, and renders each category in presentation order. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Aggregates and formats technical documentation elements such as module roles, dependencies, dependents, public API entries, alerts, and claims for reporting purposes. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `e5c844` [1]: Orchestrates the generation of a markdown report detailing the project context map, including system summary, module counts, categorized modules with dependencies, and renders each category in presentation order. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `96cac8` [2]: Initializes instance variables including context_map, output_file, system_summary; creates empty claim_map and sets ref_counter to 1. Renders markdown report of project context map detailing system summary, module counts, categorized modules with dependencies, and presentation order. _(Source: class ReportRenderer)_
> 🆔 `893a04` [3]: Generates a markdown report of the project context map, including system summary, module counts, categorized modules with dependencies, and renders each category in presentation order. _(Source: 🔌 ReportRenderer.render)_
> 🆔 `18e70d` [4]: Aggregates and formats technical documentation elements such as module roles, dependencies, dependents, public API entries, alerts, and claims for reporting purposes. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Validates and filters inputs to ensure compliance before passing them for further processing.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines global constant `BANNED_ADJECTIVES`. [2]
- **`🔌 class SemanticGatekeeper`**: The SemanticGatekeeper class is designed to execute provided prompts through an LLM, parse and validate the resulting JSON response, critique content style and grounding, handle retries on failure, verify claim accuracy against code with a score and explanation, critique content for banned adjectives, forbidden terms, word count, and response length criteria, extract balanced JSON substrings while ignoring specified adjectives, safely parse JSON strings handling various methods and edge cases, and attempt to parse raw JSON into Python dictionaries by extracting the balanced JSON substring between first opening brace and last closing brace if present. [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Executes provided prompt through LLM, parses and validates JSON response, critiques style and grounding, retries on failure, returns cleaned JSON or error message. [4]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Transforms and formats model and message inputs for Ollama chat API, retrieves and cleans the response content. [5]
- **`agent_config.py`**: Defines configuration constants for the semantic gatekeeper module, specifically setting the default model used in agent_core.py and semantic_gatekeeper.py. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_critic.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`task_executor.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b3f7e0` [1]: Validates and filters inputs to ensure compliance before passing them for further processing. _(Source: Synthesis (based on [2], [4], [3]))_
> 🆔 `4d3df2` [2]: Defines global constant `BANNED_ADJECTIVES`. _(Source: BANNED_ADJECTIVES)_
> 🆔 `b36ba8` [3]: The SemanticGatekeeper class is designed to execute provided prompts through an LLM, parse and validate the resulting JSON response, critique content style and grounding, handle retries on failure, verify claim accuracy against code with a score and explanation, critique content for banned adjectives, forbidden terms, word count, and response length criteria, extract balanced JSON substrings while ignoring specified adjectives, safely parse JSON strings handling various methods and edge cases, and attempt to parse raw JSON into Python dictionaries by extracting the balanced JSON substring between first opening brace and last closing brace if present. _(Source: class SemanticGatekeeper)_
> 🆔 `574a73` [4]: Executes provided prompt through LLM, parses and validates JSON response, critiques style and grounding, retries on failure, returns cleaned JSON or error message. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `05d496` [5]: Transforms and formats model and message inputs for Ollama chat API, retrieves and cleans the response content. _(Source: Import llm_util.py)_
> 🆔 `7aa1d3` [6]: Defines configuration constants for the semantic gatekeeper module, specifically setting the default model used in agent_core.py and semantic_gatekeeper.py. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` Coordinates high-level operations and orchestrates the flow of tasks within the system, ensuring execution without directly handling individual computations or data manipulation.

**Impact Analysis:** Changes to this module will affect: component_analyst.py, dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Executes the given code block, handling up to 5 retries if necessary. [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Starts task execution by logging start, calling internal loop to run goal logic, and returns result or error message if exception occurs. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Validates and filters inputs before passing them to further processing in the task execution pipeline, ensuring compliance and correctness of data structures. [4]

### 👥 Used By (Downstream)
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `aeade1` [1]: Coordinates high-level operations and orchestrates the flow of tasks within the system, ensuring execution without directly handling individual computations or data manipulation. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `cfbd2e` [2]: Executes the given code block, handling up to 5 retries if necessary. _(Source: class TaskExecutor)_
> 🆔 `40bb3a` [3]: Starts task execution by logging start, calling internal loop to run goal logic, and returns result or error message if exception occurs. _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `94fbd4` [4]: Validates and filters inputs before passing them to further processing in the task execution pipeline, ensuring compliance and correctness of data structures. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Defines a function that processes model and messages, sends requests to Ollama chat API, retrieves response content, strips whitespace, and returns the formatted content.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Processes the model and messages, sends the request to Ollama chat API, retrieves the response content, strips whitespace, and returns the content. [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `659b4d` [1]: Defines a function that processes model and messages, sends requests to Ollama chat API, retrieves response content, strips whitespace, and returns the formatted content. _(Source: Synthesis (based on [2]))_
> 🆔 `65f984` [2]: Processes the model and messages, sends the request to Ollama chat API, retrieves the response content, strips whitespace, and returns the content. _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Defines an abstract data structure that represents and analyzes the code structure of Python modules, encapsulating entities such as functions, classes, imports, cross-module interactions, and TODO comments.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Collects code entities, tracks imports and cross-module interactions, analyzes function bodies for special cases like `Pass`, `Raise`, or exception handling. [2]
- **`🔌 class GraphAnalyzer`**: Analyzes code structure, builds dependency graph, extracts TODO comments and dependencies, and populates graph with dependents. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes the current class context and header from stack on leave event. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Removes the current context from the stack and pops the header stack when leaving a function definition node, maintaining proper nesting levels during code analysis. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Sets `current_statement` to None when leaving a `SimpleStatementLine` node. [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Collects annotated assignment information and adds it to the entities list. [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Collects global variable assignments, extracting names and source code, adding them to the entities list with type 'globals', and determining if they are private based on naming convention. [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Records cross-module interaction for function calls. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Registers class definition in current context, retrieves source code, docstring, bases for the class, and initializes empty methods list. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Analyzes a function definition node, generates its signature and header, retrieves the docstring and source code, checks if it is unimplemented or private, stores component data, determines if it is a method of a class, and appends to functions or adds to methods of the corresponding class. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Collects module names from imported nodes and adds them to the set of external imports. [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Processes relative imports and maps them to files, adding imported paths to the import map. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records interactions for `Name` nodes if they are not already recorded in the current context, updating the interaction map and cross-module interactions. [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Updates the current statement to the provided node in the visitor method for `SimpleStatementLine` nodes, storing it in the `current_statement` attribute. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds the dependency graph using DFS, populates dependents in the `_build_graph_dfs` and `_populate_dependents` methods, then returns the `graph`. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c8ad67` [1]: Defines an abstract data structure that represents and analyzes the code structure of Python modules, encapsulating entities such as functions, classes, imports, cross-module interactions, and TODO comments. _(Source: Synthesis (based on [7], [12], [8], [11], [9], [5], [10], [14], [13], [16], [15], [6], [4], [3], [2]))_
> 🆔 `fc2bdc` [2]: Collects code entities, tracks imports and cross-module interactions, analyzes function bodies for special cases like `Pass`, `Raise`, or exception handling. _(Source: class CodeEntityVisitor)_
> 🆔 `e64fd3` [3]: Analyzes code structure, builds dependency graph, extracts TODO comments and dependencies, and populates graph with dependents. _(Source: class GraphAnalyzer)_
> 🆔 `d8baf5` [4]: Removes the current class context and header from stack on leave event. _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `565b65` [5]: Removes the current context from the stack and pops the header stack when leaving a function definition node, maintaining proper nesting levels during code analysis. _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `d48607` [6]: Sets `current_statement` to None when leaving a `SimpleStatementLine` node. _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `0e5810` [7]: Collects annotated assignment information and adds it to the entities list. _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `1d38b2` [8]: Collects global variable assignments, extracting names and source code, adding them to the entities list with type 'globals', and determining if they are private based on naming convention. _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `5055d6` [9]: Records cross-module interaction for function calls. _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `8bd701` [10]: Registers class definition in current context, retrieves source code, docstring, bases for the class, and initializes empty methods list. _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `4f82c2` [11]: Analyzes a function definition node, generates its signature and header, retrieves the docstring and source code, checks if it is unimplemented or private, stores component data, determines if it is a method of a class, and appends to functions or adds to methods of the corresponding class. _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `18e9b6` [12]: Collects module names from imported nodes and adds them to the set of external imports. _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `95573c` [13]: Processes relative imports and maps them to files, adding imported paths to the import map. _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `910c8b` [14]: Records interactions for `Name` nodes if they are not already recorded in the current context, updating the interaction map and cross-module interactions. _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `c683b2` [15]: Updates the current statement to the provided node in the visitor method for `SimpleStatementLine` nodes, storing it in the `current_statement` attribute. _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `a4556f` [16]: Builds the dependency graph using DFS, populates dependents in the `_build_graph_dfs` and `_populate_dependents` methods, then returns the `graph`. _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` The Memory Core module defines an interface for querying memory and encapsulates functionality to add, query, update helpfulness scores, and cleanup memories in a ChromaDB collection.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Creates ChromaMemory instance, initializes PersistentClient and collection named 'memories', adds memories with metadata and embeddings, queries memories by similarity, updates helpfulness scores, and cleans up low-score or stale memories. [2]
- **`🔌 class MemoryInterface`**: Defines interface signature for querying memory. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Adds a memory to the collection with unique ID, combined metadata including turn_added and helpfulness, and provided embedding. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Deletes memories from the collection if helpfulness is below 0.3 or last used turn is more than 50 turns ago. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Queries the memory collection for matching documents, updates the last_used_turn in metadata for the found memories, and returns the query results including ids, documents, metadatas, and distances. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Updates the helpfulness score of a specified memory in the ChromaDB collection by retrieving its metadata, modifying the `helpfulness` field, and persisting the updated metadata back to the database. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b84410` [1]: The Memory Core module defines an interface for querying memory and encapsulates functionality to add, query, update helpfulness scores, and cleanup memories in a ChromaDB collection. _(Source: Synthesis (based on [6], [4], [3], [5], [8], [2], [7]))_
> 🆔 `b2d17d` [2]: Creates ChromaMemory instance, initializes PersistentClient and collection named 'memories', adds memories with metadata and embeddings, queries memories by similarity, updates helpfulness scores, and cleans up low-score or stale memories. _(Source: class ChromaMemory)_
> 🆔 `1d9f7a` [3]: Defines interface signature for querying memory. _(Source: class MemoryInterface)_
> 🆔 `1d8052` [4]: Adds a memory to the collection with unique ID, combined metadata including turn_added and helpfulness, and provided embedding. _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `4c0eef` [5]: Deletes memories from the collection if helpfulness is below 0.3 or last used turn is more than 50 turns ago. _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `1609fb` [6]: Queries the memory collection for matching documents, updates the last_used_turn in metadata for the found memories, and returns the query results including ids, documents, metadatas, and distances. _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `cd5299` [7]: Updates the helpfulness score of a specified memory in the ChromaDB collection by retrieving its metadata, modifying the `helpfulness` field, and persisting the updated metadata back to the database. _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Defines functionality to classify Python modules into entry points, data models, configurations, utilities, or services based on their names and source code structure.

**Impact Analysis:** Changes to this module will affect: dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Initializes `module_name` and `data`. Classifies module as entry point, data model, configuration, utility, or service. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Classifies the module as an entry point, data model, configuration, utility, or service based on its name and source code structure. [4]

### 👥 Used By (Downstream)
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `0176b4` [1]: Defines functionality to classify Python modules into entry points, data models, configurations, utilities, or services based on their names and source code structure. _(Source: Synthesis (based on [4], [2], [3]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `ad001f` [3]: Initializes `module_name` and `data`. Classifies module as entry point, data model, configuration, utility, or service. _(Source: class ModuleClassifier)_
> 🆔 `352bc4` [4]: Classifies the module as an entry point, data model, configuration, utility, or service based on its name and source code structure. _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Defines and orchestrates the analysis of system functionality based on source code annotations.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Inits class components and dependencies for module analysis, initializes context, builds usage map, and sets archetype based on classifier classification of the module data. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyzes module context by performing component analysis, dependency analysis, populating alerts, and processing critique instructions. [3]

### 🔗 Uses (Upstream)
- **`dependency_analyst.py`**: Analyzes upstream context to determine import rationale and dependency relationships for `module_contextualizer.py. [4]
- **`semantic_gatekeeper.py`**: Validates and filters inputs to ensure compliance before passing them for further processing in the module. [5]
- **`task_executor.py`**: Orchestrates the execution flow of tasks, coordinating high-level operations without directly handling computations or data manipulation. [6]
- **`module_classifier.py`**: Analyzes module structure and name to categorize modules as entry points, data models, configurations, utilities, or services for contextual understanding in `module_contextualizer.py`. [7]
- **`summary_models.py`**: Aggregates and contextualizes module metadata including roles, dependencies, dependents, public API entries, alerts, and claims for documentation generation. [8]
- **`component_analyst.py`**: Analyzes system components to provide detailed role summaries, supporting contextualization and behavior interpretation within the module. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `cd5498` [1]: Defines and orchestrates the analysis of system functionality based on source code annotations. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `eb2ef9` [2]: Inits class components and dependencies for module analysis, initializes context, builds usage map, and sets archetype based on classifier classification of the module data. _(Source: class ModuleContextualizer)_
> 🆔 `f9d504` [3]: Analyzes module context by performing component analysis, dependency analysis, populating alerts, and processing critique instructions. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `099d0b` [4]: Analyzes upstream context to determine import rationale and dependency relationships for `module_contextualizer.py. _(Source: Import dependency_analyst.py)_
> 🆔 `2aeed0` [5]: Validates and filters inputs to ensure compliance before passing them for further processing in the module. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `365ec3` [6]: Orchestrates the execution flow of tasks, coordinating high-level operations without directly handling computations or data manipulation. _(Source: Import task_executor.py)_
> 🆔 `817114` [7]: Analyzes module structure and name to categorize modules as entry points, data models, configurations, utilities, or services for contextual understanding in `module_contextualizer.py`. _(Source: Import module_classifier.py)_
> 🆔 `310f96` [8]: Aggregates and contextualizes module metadata including roles, dependencies, dependents, public API entries, alerts, and claims for documentation generation. _(Source: Import summary_models.py)_
> 🆔 `70456d` [9]: Analyzes system components to provide detailed role summaries, supporting contextualization and behavior interpretation within the module. _(Source: Import component_analyst.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Defines a set of classes and methods for encapsulating and managing technical documentation related to module roles, dependencies, dependents, public API entries, alerts, and claims within a software project.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Computes SHA1 hash of concatenated string created from attributes. [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Initializes default attributes and empty collections for archetype, module role, dependencies, dependents, public API, alerts, and claims. [5]
- **`🔌 🔌 Claim.id`**: Computes SHA1 hash of concatenated string created from attributes. [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds an alert to the alerts list. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Adds dependency context to the module by creating a combined text of explanation and placeholders, then storing it in `key_dependencies` dictionary. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds dependent context for a module by combining explanation and supporting claims, storing in `key_dependents` dictionary. [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds an entry to the public API dictionary, combining description and supporting claims into full text and storing it with claim IDs. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Sets the module role by combining provided text with placeholders and claim IDs from supporting claims. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `18000d` [1]: Defines a set of classes and methods for encapsulating and managing technical documentation related to module roles, dependencies, dependents, public API entries, alerts, and claims within a software project. _(Source: Synthesis (based on [10], [3], [5], [9], [11], [4], [2], [8], [6], [7]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `5db3bf` [3]: Computes SHA1 hash of concatenated string created from attributes. _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `7739c9` [5]: Initializes default attributes and empty collections for archetype, module role, dependencies, dependents, public API, alerts, and claims. _(Source: class ModuleContext)_
> 🆔 `f79d6c` [6]: Computes SHA1 hash of concatenated string created from attributes. _(Source: 🔌 Claim.id)_
> 🆔 `fd2ffa` [7]: Adds an alert to the alerts list. _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `d45341` [8]: Adds dependency context to the module by creating a combined text of explanation and placeholders, then storing it in `key_dependencies` dictionary. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `7fdca0` [9]: Adds dependent context for a module by combining explanation and supporting claims, storing in `key_dependents` dictionary. _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `3a689b` [10]: Adds an entry to the public API dictionary, combining description and supporting claims into full text and storing it with claim IDs. _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `a7eaac` [11]: Sets the module role by combining provided text with placeholders and claim IDs from supporting claims. _(Source: 🔌 ModuleContext.set_module_role)_
</details>

---
## 🔧 Configuration

## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Defines global constant `CONTEXT_LIMIT`. [2]
- **`🔌 DEFAULT_MODEL`**: Defines global constant `DEFAULT_MODEL`. [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `449512` [1]: Defines configuration constants. _(Source: Archetype)_
> 🆔 `ef0563` [2]: Defines global constant `CONTEXT_LIMIT`. _(Source: CONTEXT_LIMIT)_
> 🆔 `9c5b38` [3]: Defines global constant `DEFAULT_MODEL`. _(Source: DEFAULT_MODEL)_
</details>

---