# Project Context Map

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates the initialization of an agent by iterating through files in a specified folder to find the main script file ending with `_main.py`, initializes CrawlerAgent with the goal and target root path, runs the agent to process the project, and returns a completion message. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 main`**: The function iterates through files in the specified folder, identifies the main script file ending with `_main.py`, initializes an agent with the goal and target root path, runs the agent to process the project, and returns a completion message. [2]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Orchestrates the agent to analyze project structures by initializing memory storage, synthesizing system summaries, and rendering reports. [3]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `5d98dd` [1]: Orchestrates the initialization of an agent by iterating through files in a specified folder to find the main script file ending with `_main.py`, initializes CrawlerAgent with the goal and target root path, runs the agent to process the project, and returns a completion message. _(Source: Synthesis (based on [2]))_
> 🆔 `59bd8b` [2]: The function iterates through files in the specified folder, identifies the main script file ending with `_main.py`, initializes an agent with the goal and target root path, runs the agent to process the project, and returns a completion message. _(Source: main)_
> 🆔 `443fe8` [3]: Orchestrates the agent to analyze project structures by initializing memory storage, synthesizing system summaries, and rendering reports. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Orchestrates an agent to analyze project structures by defining memory storage, synthesizing system summaries, and rendering reports.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Initializes CrawlerAgent with specified goal and target root, creating ChromaMemory instance for data storage. [2]
- **`🔌 🔌 CrawlerAgent.run`**: Initializes CrawlerAgent, retrieves project map and processing order, synthesizes system summary, renders report, cleans up memories for 5 turns, and returns analysis complete response. [3]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Defines configuration constants for the agent, including model selection and context handling limits. [4]
- **`summary_models.py`**: Encapsulates module role, dependencies, dependents, public API, alerts, and claims for the `agent_core.py` module. [5]
- **`report_renderer.py`**: Orchestrates generation of project context map documentation by organizing modules into archetype groups, formatting lines, and writing to an output file. [6]
- **`semantic_gatekeeper.py`**: Validates LLM responses and extracts structured data while enforcing policy compliance to ensure output quality and adherence to defined constraints. [7]
- **`memory_core.py`**: Integrates memory management functionalities to store, query, and update memories in the agent's workflow. [8]
- **`agent_util.py`**: Orchestrates generation and refinement of Module Context Maps for AI agents by delegating to `project_pulse` function. [9]
- **`map_synthesizer.py`**: Orchestrates synthesis of system architecture narratives based on anchor details, supporting cast, and project goal using the MapSynthesizer service. [10]
- **`llm_util.py`**: Formats and prepares user input for LLM model, handles chat function calls, extracts response content while managing exceptions. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `93d07b` [1]: Orchestrates an agent to analyze project structures by defining memory storage, synthesizing system summaries, and rendering reports. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `e13c5c` [2]: Initializes CrawlerAgent with specified goal and target root, creating ChromaMemory instance for data storage. _(Source: class CrawlerAgent)_
> 🆔 `db686c` [3]: Initializes CrawlerAgent, retrieves project map and processing order, synthesizes system summary, renders report, cleans up memories for 5 turns, and returns analysis complete response. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `17cb7d` [4]: Defines configuration constants for the agent, including model selection and context handling limits. _(Source: Import agent_config.py)_
> 🆔 `e71da2` [5]: Encapsulates module role, dependencies, dependents, public API, alerts, and claims for the `agent_core.py` module. _(Source: Import summary_models.py)_
> 🆔 `c1120a` [6]: Orchestrates generation of project context map documentation by organizing modules into archetype groups, formatting lines, and writing to an output file. _(Source: Import report_renderer.py)_
> 🆔 `118daa` [7]: Validates LLM responses and extracts structured data while enforcing policy compliance to ensure output quality and adherence to defined constraints. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `d2a4fb` [8]: Integrates memory management functionalities to store, query, and update memories in the agent's workflow. _(Source: Import memory_core.py)_
> 🆔 `067d19` [9]: Orchestrates generation and refinement of Module Context Maps for AI agents by delegating to `project_pulse` function. _(Source: Import agent_util.py)_
> 🆔 `fe3c77` [10]: Orchestrates synthesis of system architecture narratives based on anchor details, supporting cast, and project goal using the MapSynthesizer service. _(Source: Import map_synthesizer.py)_
> 🆔 `2bb80e` [11]: Formats and prepares user input for LLM model, handles chat function calls, extracts response content while managing exceptions. _(Source: Import llm_util.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Orchestrates the multi-pass process of generating and refining Module Context Maps for AI agents.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns a dictionary to the variable `ProjectGraph`. [2]
- **`🔌 class ProjectSummarizer`**: Initializes ProjectSummarizer by setting attributes for graph, max cycles, empty contexts, and processing order using topological sort. [3]
- **`🔌 project_pulse`**: Analyzes project structure by creating dependency graph, summarizing it, and generating contexts and processing order. [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Iterates through cycles, updating module contexts based on dependencies and critiques, caching unchanged paths, and returning the updated context dictionary and processing order. [5]
- **`🔒 _create_module_context`**: Generates module context by creating an instance of ModuleContextualizer, calling contextualize_module, setting file_path if missing, and returning the ModuleContext. [6]

### 🔗 Uses (Upstream)
- **`graph_analyzer.py`**: Analyzes Python modules to build and traverse dependency graphs, identifying import paths and relationships between code entities for static analysis in `agent_util.py`. [7]
- **`summary_models.py`**: Defines data structure for encapsulating and representing role, dependencies, dependents, public API, alerts, and claims of a module in a software system. [8]
- **`report_renderer.py`**: Orchestrates generation of project context map documentation by listing modules, categorizing them into archetype groups, writing formatted lines to an output file, and managing claims. [9]
- **`semantic_gatekeeper.py`**: Validates and parses LLM-generated JSON responses, ensuring data integrity and policy compliance before further processing. [10]
- **`module_contextualizer.py`**: Synthesizes systemic critique by analyzing module capabilities and dependencies to provide context-aware documentation for `agent_util.py`. [11]
- **`map_critic.py`**: Analyzes project map content, parses modules, and generates critiques for up to three modules based on predefined documentation quality criteria using SemanticGatekeeper. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `9172b7` [1]: Orchestrates the multi-pass process of generating and refining Module Context Maps for AI agents. _(Source: Synthesis (based on [4], [2], [6], [3], [5]))_
> 🆔 `4ba765` [2]: Assigns a dictionary to the variable `ProjectGraph`. _(Source: ProjectGraph)_
> 🆔 `db5a7f` [3]: Initializes ProjectSummarizer by setting attributes for graph, max cycles, empty contexts, and processing order using topological sort. _(Source: class ProjectSummarizer)_
> 🆔 `2759a0` [4]: Analyzes project structure by creating dependency graph, summarizing it, and generating contexts and processing order. _(Source: project_pulse)_
> 🆔 `e0b349` [5]: Iterates through cycles, updating module contexts based on dependencies and critiques, caching unchanged paths, and returning the updated context dictionary and processing order. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `7ed535` [6]: Generates module context by creating an instance of ModuleContextualizer, calling contextualize_module, setting file_path if missing, and returning the ModuleContext. _(Source: _create_module_context)_
> 🆔 `8a734f` [7]: Analyzes Python modules to build and traverse dependency graphs, identifying import paths and relationships between code entities for static analysis in `agent_util.py`. _(Source: Import graph_analyzer.py)_
> 🆔 `23ef96` [8]: Defines data structure for encapsulating and representing role, dependencies, dependents, public API, alerts, and claims of a module in a software system. _(Source: Import summary_models.py)_
> 🆔 `0e7671` [9]: Orchestrates generation of project context map documentation by listing modules, categorizing them into archetype groups, writing formatted lines to an output file, and managing claims. _(Source: Import report_renderer.py)_
> 🆔 `acca2c` [10]: Validates and parses LLM-generated JSON responses, ensuring data integrity and policy compliance before further processing. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `b04c3d` [11]: Synthesizes systemic critique by analyzing module capabilities and dependencies to provide context-aware documentation for `agent_util.py`. _(Source: Import module_contextualizer.py)_
> 🆔 `165026` [12]: Analyzes project map content, parses modules, and generates critiques for up to three modules based on predefined documentation quality criteria using SemanticGatekeeper. _(Source: Import map_critic.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes source code to extract functions, classes, and methods, synthesizing their roles into public API entries.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Initializes an instance by setting `gatekeeper` and `task_executor` attributes. [2]
- **`🔌 class SkeletonTransformer`**: Removes docstrings from Python function and class definitions. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes the provided entities and context to identify global constants, functions, and classes, summarizing their roles in the specified module. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Parses the source code into an AST, applies a SkeletonTransformer to generate a skeleton structure, and then unparses it back into source code. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Removes docstring from async function node and visits the node. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from node and adds `Pass()` if no body [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Removes docstring from function definition node and returns result of generic visit [8]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Orchestrates and coordinates high-level task execution, delegating to TaskExecutor for underlying processing logic, while logging start, invoking goal processing loop, and returning results or failure messages. [9]
- **`summary_models.py`**: Aggregates and represents module metadata for dependency and API analysis within component_analyst.py. [10]
- **`semantic_gatekeeper.py`**: Validates and extracts structured data from LLM outputs, ensuring policy compliance while orchestrating interactions between components in `component_analyst.py`. [11]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `eb2496` [1]: Analyzes source code to extract functions, classes, and methods, synthesizing their roles into public API entries. _(Source: Synthesis (based on [8], [2], [4], [5], [6], [7], [3]))_
> 🆔 `3b4bdb` [2]: Initializes an instance by setting `gatekeeper` and `task_executor` attributes. _(Source: class ComponentAnalyst)_
> 🆔 `d1b8b0` [3]: Removes docstrings from Python function and class definitions. _(Source: class SkeletonTransformer)_
> 🆔 `66eb48` [4]: Analyzes the provided entities and context to identify global constants, functions, and classes, summarizing their roles in the specified module. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `6b040d` [5]: Parses the source code into an AST, applies a SkeletonTransformer to generate a skeleton structure, and then unparses it back into source code. _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `6fc08f` [6]: Removes docstring from async function node and visits the node. _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `bcae81` [7]: Removes docstring from node and adds `Pass()` if no body _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `28977a` [8]: Removes docstring from function definition node and returns result of generic visit _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `ed3e46` [9]: Orchestrates and coordinates high-level task execution, delegating to TaskExecutor for underlying processing logic, while logging start, invoking goal processing loop, and returning results or failure messages. _(Source: Import task_executor.py)_
> 🆔 `2a6f2b` [10]: Aggregates and represents module metadata for dependency and API analysis within component_analyst.py. _(Source: Import summary_models.py)_
> 🆔 `48bc84` [11]: Validates and extracts structured data from LLM outputs, ensuring policy compliance while orchestrating interactions between components in `component_analyst.py`. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Analyzes dependencies and orchestrates integration of imported modules.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Analyzes upstream API usage and context for imported dependencies, providing usage snippets and guidance on proper integration within the specified module. [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes upstream API usage and context for imported dependencies, providing usage snippets and guidance on proper integration within the specified module. [3]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Orchestrates execution of tasks by delegating to underlying executor service, managing retries and logging task start/finish. [4]
- **`summary_models.py`**: Aggregates module metadata and relationships for reporting in `dependency_analyst.py`. [5]
- **`module_classifier.py`**: Determines module archetype by analyzing characteristics, source code entities, dependencies, and behavior to categorize modules into predefined archetypes. [6]
- **`semantic_gatekeeper.py`**: Validates LLM responses by parsing, enforcing policy compliance, and extracting structured data. [7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `10854a` [1]: Analyzes dependencies and orchestrates integration of imported modules. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `d4fe3f` [2]: Analyzes upstream API usage and context for imported dependencies, providing usage snippets and guidance on proper integration within the specified module. _(Source: class DependencyAnalyst)_
> 🆔 `a42f9e` [3]: Analyzes upstream API usage and context for imported dependencies, providing usage snippets and guidance on proper integration within the specified module. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `9c629b` [4]: Orchestrates execution of tasks by delegating to underlying executor service, managing retries and logging task start/finish. _(Source: Import task_executor.py)_
> 🆔 `d22d3f` [5]: Aggregates module metadata and relationships for reporting in `dependency_analyst.py`. _(Source: Import summary_models.py)_
> 🆔 `4d74a8` [6]: Determines module archetype by analyzing characteristics, source code entities, dependencies, and behavior to categorize modules into predefined archetypes. _(Source: Import module_classifier.py)_
> 🆔 `8d9b77` [7]: Validates LLM responses by parsing, enforcing policy compliance, and extracting structured data. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Defines and executes a critique process that analyzes project map content for specific module descriptions, generating critiques up to three modules focusing on defining documentation quality based on predefined criteria.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Initializes with a SemanticGatekeeper instance, parses project map into module descriptions, and generates critiques for up to three modules. [2]
- **`🔌 🔌 MapCritic.critique`**: Analyzes the project map content, parses modules, and generates critiques for up to three modules. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Validates LLM output structure and policy compliance before passing to downstream services. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f0b55d` [1]: Defines and executes a critique process that analyzes project map content for specific module descriptions, generating critiques up to three modules focusing on defining documentation quality based on predefined criteria. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `691157` [2]: Initializes with a SemanticGatekeeper instance, parses project map into module descriptions, and generates critiques for up to three modules. _(Source: class MapCritic)_
> 🆔 `6a650c` [3]: Analyzes the project map content, parses modules, and generates critiques for up to three modules. _(Source: 🔌 MapCritic.critique)_
> 🆔 `09802b` [4]: Validates LLM output structure and policy compliance before passing to downstream services. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` Defines an active service that coordinates and orchestrates module contexts to synthesize a system architecture narrative based on provided anchor details, supporting cast, and project goal.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Initializes an instance by assigning the provided gatekeeper to the MapSynthesizer instance's gatekeeper attribute. Synthesizes by identifying anchors, detailing anchor specifics, gathering supporting cast, and running grounded synthesis with ranked paths based on relevance scores. [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Identifies anchors, details anchor specifics, gathers supporting cast, and runs grounded synthesis. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Aggregates role, dependencies, dependents, public API, alerts, and claims for the module within `map_synthesizer.py`. [4]
- **`semantic_gatekeeper.py`**: Validates and parses LLM output from `map_synthesizer.py`. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `996485` [1]: Defines an active service that coordinates and orchestrates module contexts to synthesize a system architecture narrative based on provided anchor details, supporting cast, and project goal. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `669fac` [2]: Initializes an instance by assigning the provided gatekeeper to the MapSynthesizer instance's gatekeeper attribute. Synthesizes by identifying anchors, detailing anchor specifics, gathering supporting cast, and running grounded synthesis with ranked paths based on relevance scores. _(Source: class MapSynthesizer)_
> 🆔 `1e3293` [3]: Identifies anchors, details anchor specifics, gathers supporting cast, and runs grounded synthesis. _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `08cfde` [4]: Aggregates role, dependencies, dependents, public API, alerts, and claims for the module within `map_synthesizer.py`. _(Source: Import summary_models.py)_
> 🆔 `9825d9` [5]: Validates and parses LLM output from `map_synthesizer.py`. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Defines and orchestrates the generation of project context map documentation by listing modules, categorizing them into archetype groups, writing formatted lines to an output file, and managing claims.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Initializes the ReportRenderer class with context_map, output_file, system_summary, an empty claim_map dictionary, and starts ref_counter at 1. [2]
- **`🔌 🔌 ReportRenderer.render`**: Generates project context map documentation by listing modules, categorizing them into archetype groups, and writing the formatted lines to an output file. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Collects and organizes metadata about the module's role, dependencies, dependents, public API, alerts, and claims for use in generating reports. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `929ece` [1]: Defines and orchestrates the generation of project context map documentation by listing modules, categorizing them into archetype groups, writing formatted lines to an output file, and managing claims. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `79bbdd` [2]: Initializes the ReportRenderer class with context_map, output_file, system_summary, an empty claim_map dictionary, and starts ref_counter at 1. _(Source: class ReportRenderer)_
> 🆔 `d37fe3` [3]: Generates project context map documentation by listing modules, categorizing them into archetype groups, and writing the formatted lines to an output file. _(Source: 🔌 ReportRenderer.render)_
> 🆔 `fbc05c` [4]: Collects and organizes metadata about the module's role, dependencies, dependents, public API, alerts, and claims for use in generating reports. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Analyzes and validates LLM outputs, extracting structured data while enforcing policy compliance.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines global constant `BANNED_ADJECTIVES`. [2]
- **`🔌 class SemanticGatekeeper`**: Manages execution of LLM responses, validates JSON format, critiques content for policy compliance, extracts and parses JSON data from input text. [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Executes a given prompt through an LLM, parsing and validating the JSON response according to specified parameters. [4]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Defines the default model for semantic gatekeeper to use, ensuring consistent configuration across agent execution. [5]
- **`llm_util.py`**: Transforms user messages into structured inputs for the LLM, invokes the chat function to generate responses, and extracts relevant content from the model's output. [6]

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

> 🆔 `ed6002` [1]: Analyzes and validates LLM outputs, extracting structured data while enforcing policy compliance. _(Source: Synthesis (based on [4], [2], [3]))_
> 🆔 `4d3df2` [2]: Defines global constant `BANNED_ADJECTIVES`. _(Source: BANNED_ADJECTIVES)_
> 🆔 `a0ee85` [3]: Manages execution of LLM responses, validates JSON format, critiques content for policy compliance, extracts and parses JSON data from input text. _(Source: class SemanticGatekeeper)_
> 🆔 `22470d` [4]: Executes a given prompt through an LLM, parsing and validating the JSON response according to specified parameters. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `2930c4` [5]: Defines the default model for semantic gatekeeper to use, ensuring consistent configuration across agent execution. _(Source: Import agent_config.py)_
> 🆔 `6b6258` [6]: Transforms user messages into structured inputs for the LLM, invokes the chat function to generate responses, and extracts relevant content from the model's output. _(Source: Import llm_util.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` Coordinates high-level tasks and delegates execution to the underlying executor service.

**Impact Analysis:** Changes to this module will affect: component_analyst.py, dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Initializes an instance of TaskExecutor, setting the gatekeeper attribute to the provided SemanticGatekeeper object and setting max_retries to 5. [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Commences task execution by logging start, invoking private loop for goal processing, and returns result or failure message on exception [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Ensures LLM outputs conform to predefined policies and structural requirements by validating JSON responses, extracting structured data, and enforcing compliance. [4]

### 👥 Used By (Downstream)
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `2e8234` [1]: Coordinates high-level tasks and delegates execution to the underlying executor service. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `60ccde` [2]: Initializes an instance of TaskExecutor, setting the gatekeeper attribute to the provided SemanticGatekeeper object and setting max_retries to 5. _(Source: class TaskExecutor)_
> 🆔 `927850` [3]: Commences task execution by logging start, invoking private loop for goal processing, and returns result or failure message on exception _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `83dc89` [4]: Ensures LLM outputs conform to predefined policies and structural requirements by validating JSON responses, extracting structured data, and enforcing compliance. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Defines and provides an LLM chat function that formats user input into appropriate messages for an LLM model, prepares the messages, calls the chat function to generate responses, extracts and returns the content of the response while handling exceptions.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Processes an LLM model by preparing messages and calling the chat function, returning the response content. [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `625c37` [1]: Defines and provides an LLM chat function that formats user input into appropriate messages for an LLM model, prepares the messages, calls the chat function to generate responses, extracts and returns the content of the response while handling exceptions. _(Source: Synthesis (based on [2]))_
> 🆔 `7b52f4` [2]: Processes an LLM model by preparing messages and calling the chat function, returning the response content. _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Defines and builds a dependency graph representing the structure of Python modules by traversing code entities such as imports, assignments, annotations, function bodies, class definitions, interactions, and external dependencies.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Traverses and analyzes code entities, collecting information about imports, assignments, annotations, function bodies, class definitions, interactions, and updates entity data structures. [2]
- **`🔌 class GraphAnalyzer`**: Initializes the GraphAnalyzer instance by setting absolute root path, project root directory, collecting all Python files in the project structure, and creating empty graph and visited sets. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes the current class definition from context and header stack. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Removes the current context from the stack and pops the header stack when leaving a function definition node, indicating the end of a function block. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Sets current_statement to None when leaving SimpleStatementLine node. [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Analyzes assignment nodes, extracting the target name, source code, signature including annotation, and determines if the name is private based on starting underscore. [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Collects global variables assigned in the current module, storing their name, source code representation, inferred default value placeholder, and determines if they are private based on naming convention. [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Records cross-module interaction for function calls. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: When visiting a class definition node, appends the class name to the current context, retrieves the source code for the class, gets the docstring, identifies bases and constructs a string representation of them, creates a header string, pushes the header onto a stack, initializes an entry in the entities dictionary for classes with metadata, and clears any methods list. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Analyzes function definition node, generates signature and header, checks for docstring and unimplemented body, determines if private or method, and stores component data in entities. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Iterates over each alias in the import node, retrieves the corresponding module name using `module_node.code_for_node`, and adds it to the set of external imports. [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes imports from and within modules, determining external or relative imports based on module paths. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Checks current context and records interaction for `Name` nodes. [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Updates the current_statement attribute to store the processed SimpleStatementLine node. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds dependency graph using DFS, populates dependents, and returns the graph. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `e3dfd6` [1]: Defines and builds a dependency graph representing the structure of Python modules by traversing code entities such as imports, assignments, annotations, function bodies, class definitions, interactions, and external dependencies. _(Source: Synthesis (based on [6], [3], [5], [7], [13], [9], [15], [16], [4], [2], [10], [12], [8], [14], [11]))_
> 🆔 `924881` [2]: Traverses and analyzes code entities, collecting information about imports, assignments, annotations, function bodies, class definitions, interactions, and updates entity data structures. _(Source: class CodeEntityVisitor)_
> 🆔 `0f5a9a` [3]: Initializes the GraphAnalyzer instance by setting absolute root path, project root directory, collecting all Python files in the project structure, and creating empty graph and visited sets. _(Source: class GraphAnalyzer)_
> 🆔 `814978` [4]: Removes the current class definition from context and header stack. _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `250be1` [5]: Removes the current context from the stack and pops the header stack when leaving a function definition node, indicating the end of a function block. _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `09ca83` [6]: Sets current_statement to None when leaving SimpleStatementLine node. _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `330c21` [7]: Analyzes assignment nodes, extracting the target name, source code, signature including annotation, and determines if the name is private based on starting underscore. _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `ac3557` [8]: Collects global variables assigned in the current module, storing their name, source code representation, inferred default value placeholder, and determines if they are private based on naming convention. _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `5055d6` [9]: Records cross-module interaction for function calls. _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `961f0d` [10]: When visiting a class definition node, appends the class name to the current context, retrieves the source code for the class, gets the docstring, identifies bases and constructs a string representation of them, creates a header string, pushes the header onto a stack, initializes an entry in the entities dictionary for classes with metadata, and clears any methods list. _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `f67260` [11]: Analyzes function definition node, generates signature and header, checks for docstring and unimplemented body, determines if private or method, and stores component data in entities. _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `a1724e` [12]: Iterates over each alias in the import node, retrieves the corresponding module name using `module_node.code_for_node`, and adds it to the set of external imports. _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `339a71` [13]: Analyzes imports from and within modules, determining external or relative imports based on module paths. _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `e04190` [14]: Checks current context and records interaction for `Name` nodes. _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `694ed3` [15]: Updates the current_statement attribute to store the processed SimpleStatementLine node. _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `76f27a` [16]: Builds dependency graph using DFS, populates dependents, and returns the graph. _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` The Memory Core module defines an interface and class that encapsulates memory management functionalities, including adding memories with unique IDs and embeddings, querying memories based on queries, updating helpfulness scores, and cleaning up low-use or outdated memories.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Initializes Chroma client, creates or retrieves 'memories' collection, adds memories with unique ID, embedding, metadata, queries for matching documents, updates last_used_turn, adjusts helpfulness score, and cleans up low-use or outdated memories. [2]
- **`🔌 class MemoryInterface`**: Defines the interface for querying memory. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Adds a memory to the `ChromaMemory` collection with unique ID, embedding, and metadata including turn_added, helpfulness, and last_used_turn. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Iterates through memories, identifying and deleting those with low usefulness or not used recently. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Queries the memory collection for documents matching the given query, updates the last_used_turn of matched memories to the current turn. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Updates the helpfulness score of a specified memory in the Chroma database. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `be9f8f` [1]: The Memory Core module defines an interface and class that encapsulates memory management functionalities, including adding memories with unique IDs and embeddings, querying memories based on queries, updating helpfulness scores, and cleaning up low-use or outdated memories. _(Source: Synthesis (based on [2], [3], [7], [5], [8], [4], [6]))_
> 🆔 `24feb5` [2]: Initializes Chroma client, creates or retrieves 'memories' collection, adds memories with unique ID, embedding, metadata, queries for matching documents, updates last_used_turn, adjusts helpfulness score, and cleans up low-use or outdated memories. _(Source: class ChromaMemory)_
> 🆔 `4c5db5` [3]: Defines the interface for querying memory. _(Source: class MemoryInterface)_
> 🆔 `c6d090` [4]: Adds a memory to the `ChromaMemory` collection with unique ID, embedding, and metadata including turn_added, helpfulness, and last_used_turn. _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `991015` [5]: Iterates through memories, identifying and deleting those with low usefulness or not used recently. _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `c6faf9` [6]: Queries the memory collection for documents matching the given query, updates the last_used_turn of matched memories to the current turn. _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `51b383` [7]: Updates the helpfulness score of a specified memory in the Chroma database. _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Defines a system that classifies modules into predefined archetypes based on their characteristics, source code analysis, entities, dependencies, and behavior.

**Impact Analysis:** Changes to this module will affect: dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Initializes the ModuleClassifier instance by assigning the provided module name and graph data to its attributes; Classifies input modules based on their characteristics, source code, entities, dependencies using `classify` method. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Analyzes module name, source code, entities, dependencies to determine archetype and returns ModuleArchetype based on analysis. [4]

### 👥 Used By (Downstream)
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `681c53` [1]: Defines a system that classifies modules into predefined archetypes based on their characteristics, source code analysis, entities, dependencies, and behavior. _(Source: Synthesis (based on [4], [3], [2]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `852845` [3]: Initializes the ModuleClassifier instance by assigning the provided module name and graph data to its attributes; Classifies input modules based on their characteristics, source code, entities, dependencies using `classify` method. _(Source: class ModuleClassifier)_
> 🆔 `61cf79` [4]: Analyzes module name, source code, entities, dependencies to determine archetype and returns ModuleArchetype based on analysis. _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Defines a system for contextualizing technical documentation by integrating module capabilities, upstream and downstream relationships, and human-readable roles based on source code analysis.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Inits dependencies and initializes class variables in constructor. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Executes analysis on the module by running component and dependency analysis, populating alerts, and synthesizing systemic critique. [3]

### 🔗 Uses (Upstream)
- **`component_analyst.py`**: Analyzes source code to synthesize roles into public API entries for the module. [4]
- **`module_classifier.py`**: Analyzes module characteristics and dependencies to determine its archetype for contextual processing. [5]
- **`task_executor.py`**: Coordinates and delegates execution of high-level tasks to the underlying executor service, logging start, processing goals, and handling exceptions. [6]
- **`summary_models.py`**: Aggregates and organizes role, dependencies, dependents, public API, alerts, and claims information for modules to streamline analysis and documentation. [7]
- **`semantic_gatekeeper.py`**: Validates LLM output JSON and enforces policy compliance by parsing structured data from the response. [8]
- **`dependency_analyst.py`**: Analyzes and integrates dependencies for the module_contextualizer.py, providing usage guidance and integration snippets based on upstream API context to ensure effective functionality. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `416d8c` [1]: Defines a system for contextualizing technical documentation by integrating module capabilities, upstream and downstream relationships, and human-readable roles based on source code analysis. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `f8b051` [2]: Inits dependencies and initializes class variables in constructor. _(Source: class ModuleContextualizer)_
> 🆔 `e02e3b` [3]: Executes analysis on the module by running component and dependency analysis, populating alerts, and synthesizing systemic critique. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `0af523` [4]: Analyzes source code to synthesize roles into public API entries for the module. _(Source: Import component_analyst.py)_
> 🆔 `b915ef` [5]: Analyzes module characteristics and dependencies to determine its archetype for contextual processing. _(Source: Import module_classifier.py)_
> 🆔 `daa255` [6]: Coordinates and delegates execution of high-level tasks to the underlying executor service, logging start, processing goals, and handling exceptions. _(Source: Import task_executor.py)_
> 🆔 `2207b4` [7]: Aggregates and organizes role, dependencies, dependents, public API, alerts, and claims information for modules to streamline analysis and documentation. _(Source: Import summary_models.py)_
> 🆔 `638b39` [8]: Validates LLM output JSON and enforces policy compliance by parsing structured data from the response. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `94fe17` [9]: Analyzes and integrates dependencies for the module_contextualizer.py, providing usage guidance and integration snippets based on upstream API context to ensure effective functionality. _(Source: Import dependency_analyst.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Defines a data structure for encapsulating and representing the role, dependencies, dependents, public API, alerts, and claims of a module in a software system.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Computes SHA1 hash of combined text, reference, and source_module attributes. [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Initializes attributes for file path, archetype, module role, dependencies, dependents, public API, alerts, and claims. [5]
- **`🔌 🔌 Claim.id`**: Computes a SHA1 hash of a string combining `text`, `reference`, and `source_module` attributes. [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds an alert to the list of alerts. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Adds module dependency context by combining explanation and supporting claims, storing the result in `key_dependencies` dictionary. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds dependent context to the module by combining explanation and supporting claims, storing in `key_dependents`. [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds an entry to the public API dictionary with entity name, combined description and placeholders from supporting claims. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Sets the module's role by concatenating provided text with placeholders and claim IDs from supporting claims. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ba760f` [1]: Defines a data structure for encapsulating and representing the role, dependencies, dependents, public API, alerts, and claims of a module in a software system. _(Source: Synthesis (based on [5], [11], [9], [10], [7], [8], [4], [6], [3], [2]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `be3661` [3]: Computes SHA1 hash of combined text, reference, and source_module attributes. _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `145518` [5]: Initializes attributes for file path, archetype, module role, dependencies, dependents, public API, alerts, and claims. _(Source: class ModuleContext)_
> 🆔 `bc14df` [6]: Computes a SHA1 hash of a string combining `text`, `reference`, and `source_module` attributes. _(Source: 🔌 Claim.id)_
> 🆔 `74db95` [7]: Adds an alert to the list of alerts. _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `91fdce` [8]: Adds module dependency context by combining explanation and supporting claims, storing the result in `key_dependencies` dictionary. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `3be8ca` [9]: Adds dependent context to the module by combining explanation and supporting claims, storing in `key_dependents`. _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `64f896` [10]: Adds an entry to the public API dictionary with entity name, combined description and placeholders from supporting claims. _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `1914e2` [11]: Sets the module's role by concatenating provided text with placeholders and claim IDs from supporting claims. _(Source: 🔌 ModuleContext.set_module_role)_
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