# Project Context Map

## 🏛️ System Architecture
The system's foundation is built on the Configuration layer, which defines settings for the entire system and manages configurations across agent_core.py and semantic_gatekeeper.py. This foundational data structure acts as the blueprint for how the system operates, providing essential parameters that guide the functionality of all other layers. Supported by this configuration are the Data Model and Utility layers, which handle memory management, summarization components, module classification, graph analysis, contextualization, prompt formatting, and LLM interaction.

---

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates searching for files ending in '_main.py' within a specified folder, initializing an instance of CrawlerAgent with the goal and target root, running the agent, and returning a completion message indicating successful execution. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 main`**: The `main` function searches for a file ending in `_main.py` within the specified `target_folder`, initializes an instance of `CrawlerAgent` with the goal and target root, runs the agent, and returns a completion message indicating successful execution. [2]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Instantiates CrawlerAgent from agent_core module.. [3]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `7a3b27` [1]: Orchestrates searching for files ending in '_main.py' within a specified folder, initializing an instance of CrawlerAgent with the goal and target root, running the agent, and returning a completion message indicating successful execution. _(Source: Synthesis (based on [2]))_
> 🆔 `369404` [2]: The `main` function searches for a file ending in `_main.py` within the specified `target_folder`, initializes an instance of `CrawlerAgent` with the goal and target root, runs the agent, and returns a completion message indicating successful execution. _(Source: main)_
> 🆔 `c59fc3` [3]: Uses `agent_core.py`: Instantiates CrawlerAgent from agent_core module.. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Project context, generates system summaries, and coordinates rendering of reports.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: The CrawlerAgent class is responsible for initializing with goal, target_root, and creating ChromaMemory instance. The run method retrieves project data, creates SemanticGatekeeper and MapSynthesizer instances, synthesizes system summary, renders report, cleans up memories, and returns analysis complete message. [2]
- **`🔌 🔌 CrawlerAgent.run`**: The method initializes by printing the goal and target root, retrieves project data using `project_pulse`, creates a `SemanticGatekeeper` instance, constructs a `MapSynthesizer` with it, synthesizes a system summary from the project map and processing order, renders a report with `ReportRenderer`, cleans up memories for 5 turns, and returns an analysis complete message. [3]

### 🔗 Uses (Upstream)
- **`memory_core.py`**: Uses `memory_core.py`: Instantiates ChromaMemory for memory operations.. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates class from ModuleContext.. [5]
- **`agent_util.py`**: Uses `agent_util.py`: Calls project_pulse from agent_util on target root. [6]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates ReportRenderer. [7]
- **`map_synthesizer.py`**: Uses `map_synthesizer.py`: Instantiates class `MapSynthesizer` using `gatekeeper. [8]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. [9]
- **`llm_util.py`**: Uses `llm_util.py`: Calls function `chat_llm()` from module.. [10]
- **`agent_config.py`**: Uses `agent_config.py`: Imports DEFAULT_MODEL and CONTEXT_LIMIT from agent_config.. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `08d4b7` [1]: Project context, generates system summaries, and coordinates rendering of reports. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `db63a0` [2]: The CrawlerAgent class is responsible for initializing with goal, target_root, and creating ChromaMemory instance. The run method retrieves project data, creates SemanticGatekeeper and MapSynthesizer instances, synthesizes system summary, renders report, cleans up memories, and returns analysis complete message. _(Source: class CrawlerAgent)_
> 🆔 `858592` [3]: The method initializes by printing the goal and target root, retrieves project data using `project_pulse`, creates a `SemanticGatekeeper` instance, constructs a `MapSynthesizer` with it, synthesizes a system summary from the project map and processing order, renders a report with `ReportRenderer`, cleans up memories for 5 turns, and returns an analysis complete message. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `054ec4` [4]: Uses `memory_core.py`: Instantiates ChromaMemory for memory operations.. _(Source: Import memory_core.py)_
> 🆔 `5373f5` [5]: Uses `summary_models.py`: Instantiates class from ModuleContext.. _(Source: Import summary_models.py)_
> 🆔 `20c235` [6]: Uses `agent_util.py`: Calls project_pulse from agent_util on target root. _(Source: Import agent_util.py)_
> 🆔 `e20784` [7]: Uses `report_renderer.py`: Instantiates ReportRenderer. _(Source: Import report_renderer.py)_
> 🆔 `56d66b` [8]: Uses `map_synthesizer.py`: Instantiates class `MapSynthesizer` using `gatekeeper. _(Source: Import map_synthesizer.py)_
> 🆔 `592dc2` [9]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `8d406c` [10]: Uses `llm_util.py`: Calls function `chat_llm()` from module.. _(Source: Import llm_util.py)_
> 🆔 `df6794` [11]: Uses `agent_config.py`: Imports DEFAULT_MODEL and CONTEXT_LIMIT from agent_config.. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` The Agent Util module orchestrates the analysis and management of system states through its defined functions, ensuring coordinated execution between modules and processes.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: A Python dictionary (`Dict[str, Any]`) is assigned to the variable `ProjectGraph`. [2]
- **`🔌 class ProjectSummarizer`**: The ProjectSummarizer class initializes attributes like graph, max_cycles, contexts, and _processing_order, computes topological order for processing modules based on dependencies, generates module contexts over specified cycles from upstream signatures and source code. [3]
- **`🔌 project_pulse`**: The function uses `GraphAnalyzer` to analyze the target file, then `ProjectSummarizer` to generate module contexts and processing order based on the resulting project graph. [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: The method generates module contexts for each path in the project graph, iteratively refining them over specified cycles by computing hash inputs from upstream signatures and source code, and updating contexts if changes occur. [5]
- **`🔒 _create_module_context`**: The function `_create_module_context` generates and returns an instance of `ModuleContext`. It initializes a `ModuleContextualizer`, calls its `contextualize_module` method, assigns the module's file path if not present, creates a new `ModuleContext` if no file path exists, logs the generation process, and returns the context. [6]

### 🔗 Uses (Upstream)
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: Instantiates ModuleContextualizer class.. [7]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates ReportRenderer class.. [8]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates class ModuleContext. [9]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class. [10]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer class for static analysis.. [11]
- **`map_critic.py`**: Uses `map_critic.py`: Calls MapCritic class with gatekeeper argument.. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `3b2f2e` [1]: The Agent Util module orchestrates the analysis and management of system states through its defined functions, ensuring coordinated execution between modules and processes. _(Source: Synthesis (based on [3], [5], [4], [6], [2]))_
> 🆔 `d3ce85` [2]: A Python dictionary (`Dict[str, Any]`) is assigned to the variable `ProjectGraph`. _(Source: ProjectGraph)_
> 🆔 `4fa3e9` [3]: The ProjectSummarizer class initializes attributes like graph, max_cycles, contexts, and _processing_order, computes topological order for processing modules based on dependencies, generates module contexts over specified cycles from upstream signatures and source code. _(Source: class ProjectSummarizer)_
> 🆔 `6f0bbc` [4]: The function uses `GraphAnalyzer` to analyze the target file, then `ProjectSummarizer` to generate module contexts and processing order based on the resulting project graph. _(Source: project_pulse)_
> 🆔 `568cfa` [5]: The method generates module contexts for each path in the project graph, iteratively refining them over specified cycles by computing hash inputs from upstream signatures and source code, and updating contexts if changes occur. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `82061d` [6]: The function `_create_module_context` generates and returns an instance of `ModuleContext`. It initializes a `ModuleContextualizer`, calls its `contextualize_module` method, assigns the module's file path if not present, creates a new `ModuleContext` if no file path exists, logs the generation process, and returns the context. _(Source: _create_module_context)_
> 🆔 `1308b8` [7]: Uses `module_contextualizer.py`: Instantiates ModuleContextualizer class.. _(Source: Import module_contextualizer.py)_
> 🆔 `390950` [8]: Uses `report_renderer.py`: Instantiates ReportRenderer class.. _(Source: Import report_renderer.py)_
> 🆔 `56a2b0` [9]: Uses `summary_models.py`: Instantiates class ModuleContext. _(Source: Import summary_models.py)_
> 🆔 `66aa04` [10]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `3aec47` [11]: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer class for static analysis.. _(Source: Import graph_analyzer.py)_
> 🆔 `081779` [12]: Uses `map_critic.py`: Calls MapCritic class with gatekeeper argument.. _(Source: Import map_critic.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes and synthesizes the roles of components within a system, integrating documentation and behavior understanding.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: The ComponentAnalyst class is responsible for analyzing and summarizing the roles, responsibilities, and dependencies of components in code. [2]
- **`🔌 class SkeletonTransformer`**: The class `SkeletonTransformer` is designed to remove docstrings from Python AST nodes, specifically within function and class definitions. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Describes the functionality of initializing class state in `__init__` method definition, including any clean code extracted from source. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: The method parses the provided source code string into an AST, applies a `SkeletonTransformer` to modify the tree structure, and then un-parses the transformed AST back into source code. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: The method removes the docstring from an async function node using `_remove_docstring`, then visits the node recursively with `generic_visit`. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: The method processes a class definition node by removing any docstring and setting its body to [ast.Pass()] if it is empty, then returns the result of calling `generic_visit`. [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: The method removes docstrings from the node using `_remove_docstring`, then recursively visits child nodes. [8]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates TaskExecutor class.. [9]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext and Claim objects. [10]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. [11]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `cc2da8` [1]: Analyzes and synthesizes the roles of components within a system, integrating documentation and behavior understanding. _(Source: Synthesis (based on [6], [7], [4], [2], [8], [5], [3]))_
> 🆔 `aeb118` [2]: The ComponentAnalyst class is responsible for analyzing and summarizing the roles, responsibilities, and dependencies of components in code. _(Source: class ComponentAnalyst)_
> 🆔 `f8b04e` [3]: The class `SkeletonTransformer` is designed to remove docstrings from Python AST nodes, specifically within function and class definitions. _(Source: class SkeletonTransformer)_
> 🆔 `a7d21f` [4]: Describes the functionality of initializing class state in `__init__` method definition, including any clean code extracted from source. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `e2563a` [5]: The method parses the provided source code string into an AST, applies a `SkeletonTransformer` to modify the tree structure, and then un-parses the transformed AST back into source code. _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `19a19b` [6]: The method removes the docstring from an async function node using `_remove_docstring`, then visits the node recursively with `generic_visit`. _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `55f50d` [7]: The method processes a class definition node by removing any docstring and setting its body to [ast.Pass()] if it is empty, then returns the result of calling `generic_visit`. _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `b2abbd` [8]: The method removes docstrings from the node using `_remove_docstring`, then recursively visits child nodes. _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `55cc1f` [9]: Uses `task_executor.py`: Instantiates TaskExecutor class.. _(Source: Import task_executor.py)_
> 🆔 `ec0a09` [10]: Uses `summary_models.py`: Instantiates ModuleContext and Claim objects. _(Source: Import summary_models.py)_
> 🆔 `46c36f` [11]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` The Dependency Analyst analyzes dependencies by iterating over each dependency path, extracting relevant upstream context and usage snippets from interactions, sanitizing input text to remove banned adjectives, and summarizing how the dependency is used in terms of symbols and snippets.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: The DependencyAnalyst class initializes two instance variables, `gatekeeper` and `task_executor`, from provided instances in its constructor. It sanitizes input text by removing banned adjectives using regex patterns before analyzing dependencies across dependency paths to extract context and usage snippets. [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: The method analyzes dependencies by iterating over each dependency path, extracting relevant upstream context and usage snippets from interactions, and summarizing how the dependency is used in terms of symbols and snippets. [3]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates class with gatekeeper and task_executor.. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext for dependency analysis. [5]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class for filtering inputs.. [6]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `7a0182` [1]: The Dependency Analyst analyzes dependencies by iterating over each dependency path, extracting relevant upstream context and usage snippets from interactions, sanitizing input text to remove banned adjectives, and summarizing how the dependency is used in terms of symbols and snippets. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `77712a` [2]: The DependencyAnalyst class initializes two instance variables, `gatekeeper` and `task_executor`, from provided instances in its constructor. It sanitizes input text by removing banned adjectives using regex patterns before analyzing dependencies across dependency paths to extract context and usage snippets. _(Source: class DependencyAnalyst)_
> 🆔 `380655` [3]: The method analyzes dependencies by iterating over each dependency path, extracting relevant upstream context and usage snippets from interactions, and summarizing how the dependency is used in terms of symbols and snippets. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `0199b4` [4]: Uses `task_executor.py`: Instantiates class with gatekeeper and task_executor.. _(Source: Import task_executor.py)_
> 🆔 `6ae1c1` [5]: Uses `summary_models.py`: Instantiates ModuleContext for dependency analysis. _(Source: Import summary_models.py)_
> 🆔 `86984d` [6]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class for filtering inputs.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Defines a service that analyzes project map content to critique module documentation quality based on predefined criteria such as lazy definitions, missing constants, and vague dependencies.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: The class `MapCritic` is designed to critique project maps by parsing them into modules, analyzing each module's documentation quality based on predefined criteria such as lazy definitions, missing constants, and vague dependencies, and providing up to three tuples of module names with their corresponding critiques. [2]
- **`🔌 🔌 MapCritic.critique`**: The method takes a project map content string, parses it into modules, analyzes each module using `_analyze_single_module`, and returns up to three tuples of module names and corresponding critiques. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates `SemanticGatekeeper` class from module.. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `351f07` [1]: Defines a service that analyzes project map content to critique module documentation quality based on predefined criteria such as lazy definitions, missing constants, and vague dependencies. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `25a4ba` [2]: The class `MapCritic` is designed to critique project maps by parsing them into modules, analyzing each module's documentation quality based on predefined criteria such as lazy definitions, missing constants, and vague dependencies, and providing up to three tuples of module names with their corresponding critiques. _(Source: class MapCritic)_
> 🆔 `996382` [3]: The method takes a project map content string, parses it into modules, analyzes each module using `_analyze_single_module`, and returns up to three tuples of module names and corresponding critiques. _(Source: 🔌 MapCritic.critique)_
> 🆔 `87618a` [4]: Uses `semantic_gatekeeper.py`: Instantiates `SemanticGatekeeper` class from module.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` The Map Synthesizer analyzes module contexts, categorizes them into layers based on archetypes, and generates functional summaries for each layer.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: The class `MapSynthesizer` initializes with an attribute `gatekeeper` and synthesizes system architecture by analyzing module contexts, categorizing modules into groups based on archetypes, generating functional summaries for each group using `_synthesize_group`, and finally creating a synthesis of the system using `layer_summaries [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: The method takes `contexts` and `processing_order`, categorizes modules into groups based on their archetype, synthesizes each group using `_synthesize_group`, and finally synthesizes the system using `layer_summaries`. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: The code instantiates `ModuleContext` and calls synthesis functions.. [4]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a3b2a4` [1]: The Map Synthesizer analyzes module contexts, categorizes them into layers based on archetypes, and generates functional summaries for each layer. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `4168d6` [2]: The class `MapSynthesizer` initializes with an attribute `gatekeeper` and synthesizes system architecture by analyzing module contexts, categorizing modules into groups based on archetypes, generating functional summaries for each group using `_synthesize_group`, and finally creating a synthesis of the system using `layer_summaries _(Source: class MapSynthesizer)_
> 🆔 `91d12b` [3]: The method takes `contexts` and `processing_order`, categorizes modules into groups based on their archetype, synthesizes each group using `_synthesize_group`, and finally synthesizes the system using `layer_summaries`. _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `462479` [4]: Uses `summary_models.py`: The code instantiates `ModuleContext` and calls synthesis functions.. _(Source: Import summary_models.py)_
> 🆔 `13362e` [5]: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Defines and orchestrates the generation of project context map reports in markdown format, categorizing modules into archetype groups, listing dependencies, and including verification claims.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: The ReportRenderer class is responsible for rendering project context map reports in markdown format, categorizing modules into archetype groups (Entry Point, Service, Utility, Data Model, Configuration), and listing dependencies along with verification claims. [2]
- **`🔌 🔌 ReportRenderer.render`**: The method renders a project context map report by generating markdown content, categorizing modules into archetype groups (Entry Point, Service, Utility, Data Model, Configuration), and others, including dependencies for each module. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates class ModuleContext with context_map and output_file. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `6efdcf` [1]: Defines and orchestrates the generation of project context map reports in markdown format, categorizing modules into archetype groups, listing dependencies, and including verification claims. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `a5c02e` [2]: The ReportRenderer class is responsible for rendering project context map reports in markdown format, categorizing modules into archetype groups (Entry Point, Service, Utility, Data Model, Configuration), and listing dependencies along with verification claims. _(Source: class ReportRenderer)_
> 🆔 `52f7e2` [3]: The method renders a project context map report by generating markdown content, categorizing modules into archetype groups (Entry Point, Service, Utility, Data Model, Configuration), and others, including dependencies for each module. _(Source: 🔌 ReportRenderer.render)_
> 🆔 `4b071c` [4]: Uses `summary_models.py`: Instantiates class ModuleContext with context_map and output_file. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Manages and analyzes code structures, coordinating tasks without being merely an instruction-following component.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines global constant `BANNED_ADJECTIVES`. [2]
- **`🔌 class SemanticGatekeeper`**: The SemanticGatekeeper class provides methods for executing prompts, verifying grounding against source code, critiquing content for banned terms and word count, extracting balanced JSON structures, and safely parsing JSON data. [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: The provided Python method, `execute_with_feedback`, takes an initial prompt and converts it into a final prompt by appending instructions for the technical analyst to return only valid JSON output. It then interacts with a language model using the ChatLM interface, attempting up to three times to generate a response that matches the expected JSON format specified by the `expect_json` parameter. If successful, the method returns the cleaned and validated JSON content; otherwise, it logs warnings and errors and attempts to provide feedback for improvement. [4]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py`: Instantiates class using DEFAULT_MODEL from agent_config.py. [5]
- **`llm_util.py`**: Uses `llm_util.py`: Instantiates class from `llm_util`.. [6]

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

> 🆔 `a27f95` [1]: Manages and analyzes code structures, coordinating tasks without being merely an instruction-following component. _(Source: Synthesis (based on [4], [2], [3]))_
> 🆔 `4d3df2` [2]: Defines global constant `BANNED_ADJECTIVES`. _(Source: BANNED_ADJECTIVES)_
> 🆔 `d27e3c` [3]: The SemanticGatekeeper class provides methods for executing prompts, verifying grounding against source code, critiquing content for banned terms and word count, extracting balanced JSON structures, and safely parsing JSON data. _(Source: class SemanticGatekeeper)_
> 🆔 `043ca2` [4]: The provided Python method, `execute_with_feedback`, takes an initial prompt and converts it into a final prompt by appending instructions for the technical analyst to return only valid JSON output. It then interacts with a language model using the ChatLM interface, attempting up to three times to generate a response that matches the expected JSON format specified by the `expect_json` parameter. If successful, the method returns the cleaned and validated JSON content; otherwise, it logs warnings and errors and attempts to provide feedback for improvement. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `000fc7` [5]: Uses `agent_config.py`: Instantiates class using DEFAULT_MODEL from agent_config.py. _(Source: Import agent_config.py)_
> 🆔 `4ada19` [6]: Uses `llm_util.py`: Instantiates class from `llm_util`.. _(Source: Import llm_util.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` The execution of complex tasks, managing dependencies and orchestration without performing any data processing itself.

**Impact Analysis:** Changes to this module will affect: component_analyst.py, dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: The class initializes an instance of TaskExecutor, setting the gatekeeper attribute to the provided SemanticGatekeeper object and assigning max_retries to 5. [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: The method attempts to execute a complex task by starting the process, logging the start of the task with specified parameters, and returning the result of `_run_goal_loop`. If an exception occurs during execution, it logs the error details and returns 'Analysis failed. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. [4]

### 👥 Used By (Downstream)
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `2a0be5` [1]: The execution of complex tasks, managing dependencies and orchestration without performing any data processing itself. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `1e3475` [2]: The class initializes an instance of TaskExecutor, setting the gatekeeper attribute to the provided SemanticGatekeeper object and assigning max_retries to 5. _(Source: class TaskExecutor)_
> 🆔 `81f671` [3]: The method attempts to execute a complex task by starting the process, logging the start of the task with specified parameters, and returning the result of `_run_goal_loop`. If an exception occurs during execution, it logs the error details and returns 'Analysis failed. _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `c92846` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Defines a utility function that formats prompts or messages into dictionaries and passes them to an external LLM for response generation, retrieving and returning the formatted content.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: The function takes a model and prompt or messages, formats them into a list of dictionaries with 'role' and 'content', passes them to `ollama.chat`, retrieves the content from the response, strips whitespace, and returns it. [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d4ff12` [1]: Defines a utility function that formats prompts or messages into dictionaries and passes them to an external LLM for response generation, retrieving and returning the formatted content. _(Source: Synthesis (based on [2]))_
> 🆔 `6111ae` [2]: The function takes a model and prompt or messages, formats them into a list of dictionaries with 'role' and 'content', passes them to `ollama.chat`, retrieves the content from the response, strips whitespace, and returns it. _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Defines and extracts code entities such as functions, classes, variables, imports, annotations, interactions, and dependencies from Python source files using an Abstract Syntax Tree (AST) visitor.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: The CodeEntityVisitor class is responsible for analyzing and interacting with code entities in an Abstract Syntax Tree (AST), including importing modules, assigning variables, handling annotations, visiting function and class definitions, recording interactions between them, and tracking source code details. [2]
- **`🔌 class GraphAnalyzer`**: The GraphAnalyzer class is responsible for analyzing Python project code, building a dependency graph using depth-first search (DFS), populating dependents information, and extracting TODO comments from the source files. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: The method pops the current context and header stack when leaving a ClassDef node, effectively removing them from the state as the visitor exits the class definition. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: The method `leave_FunctionDef` is called when leaving a function definition node in the Abstract Syntax Tree (AST). It pops the current context and header stack from the visitor's state if they are not empty. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: The method `leave_SimpleStatementLine` is called when processing leaves of the abstract syntax tree (AST). It sets the `current_statement` attribute to None. [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: The method `visit_AnnAssign` handles annotated assignment nodes, checking if the current context is empty, extracting the target name, retrieving source code using `module_node.code_for_node`, and appending an entity dictionary with details such as the variable name, source code, signature including annotation type, and whether it's private based on the naming convention. [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: The `visit_Assign` method processes assignments in the code, extracting target variable names as globals, and storing source code representation along with a default signature and privacy check. [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: The method records interactions for call nodes where the function being called is a name, using `_record_interaction()` to track `node.func.value` and `node`. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: The method handles visiting a class definition node, appends the class name to the current context, retrieves source code for the class, docstring, bases, constructs header string, stores entities dictionary with class info, and pushes header onto stack. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: The method visits `FunctionDef` nodes and extracts details such as signature, header, docstring, source code, whether it is unimplemented or private, nesting level, and determines if it's a class method. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: The method iterates over each alias in the imported node, retrieves the module name using `module_node.code_for_node`, and adds it to the `external_imports` set. [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: The method `visit_ImportFrom` handles relative and absolute imports from the given `node` of type `cst.ImportFrom`. It determines external modules to import, constructs module names for relative imports based on nested attributes, checks if imported files exist in `all_project_files`, and maps local variable names to their corresponding file paths. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: The method `visit_Name` records interactions when the current context is not empty and matches the node value. [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: The method assigns the current statement node to the variable `current_statement` when processing a `SimpleStatementLine` code entity. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: The method builds a dependency graph using DFS, populates dependents, and returns the graph. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b05fc7` [1]: Defines and extracts code entities such as functions, classes, variables, imports, annotations, interactions, and dependencies from Python source files using an Abstract Syntax Tree (AST) visitor. _(Source: Synthesis (based on [2], [10], [9], [6], [11], [15], [13], [7], [14], [12], [5], [3], [16], [4], [8]))_
> 🆔 `013523` [2]: The CodeEntityVisitor class is responsible for analyzing and interacting with code entities in an Abstract Syntax Tree (AST), including importing modules, assigning variables, handling annotations, visiting function and class definitions, recording interactions between them, and tracking source code details. _(Source: class CodeEntityVisitor)_
> 🆔 `90e568` [3]: The GraphAnalyzer class is responsible for analyzing Python project code, building a dependency graph using depth-first search (DFS), populating dependents information, and extracting TODO comments from the source files. _(Source: class GraphAnalyzer)_
> 🆔 `d0bf4a` [4]: The method pops the current context and header stack when leaving a ClassDef node, effectively removing them from the state as the visitor exits the class definition. _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `7ffd71` [5]: The method `leave_FunctionDef` is called when leaving a function definition node in the Abstract Syntax Tree (AST). It pops the current context and header stack from the visitor's state if they are not empty. _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `314922` [6]: The method `leave_SimpleStatementLine` is called when processing leaves of the abstract syntax tree (AST). It sets the `current_statement` attribute to None. _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `5d3f5b` [7]: The method `visit_AnnAssign` handles annotated assignment nodes, checking if the current context is empty, extracting the target name, retrieving source code using `module_node.code_for_node`, and appending an entity dictionary with details such as the variable name, source code, signature including annotation type, and whether it's private based on the naming convention. _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `e6a053` [8]: The `visit_Assign` method processes assignments in the code, extracting target variable names as globals, and storing source code representation along with a default signature and privacy check. _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `1d3de3` [9]: The method records interactions for call nodes where the function being called is a name, using `_record_interaction()` to track `node.func.value` and `node`. _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `08f1ef` [10]: The method handles visiting a class definition node, appends the class name to the current context, retrieves source code for the class, docstring, bases, constructs header string, stores entities dictionary with class info, and pushes header onto stack. _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `44995e` [11]: The method visits `FunctionDef` nodes and extracts details such as signature, header, docstring, source code, whether it is unimplemented or private, nesting level, and determines if it's a class method. _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `626daf` [12]: The method iterates over each alias in the imported node, retrieves the module name using `module_node.code_for_node`, and adds it to the `external_imports` set. _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `48966e` [13]: The method `visit_ImportFrom` handles relative and absolute imports from the given `node` of type `cst.ImportFrom`. It determines external modules to import, constructs module names for relative imports based on nested attributes, checks if imported files exist in `all_project_files`, and maps local variable names to their corresponding file paths. _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `5ea161` [14]: The method `visit_Name` records interactions when the current context is not empty and matches the node value. _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `4538fd` [15]: The method assigns the current statement node to the variable `current_statement` when processing a `SimpleStatementLine` code entity. _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `ba630d` [16]: The method builds a dependency graph using DFS, populates dependents, and returns the graph. _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Defines an interface and class for querying, adding, updating, and cleaning up memory documents using ChromaDB client in a specified directory, encapsulating the functionality of managing user-provided memories with attributes like turn_added, helpfulness, and additional metadata.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Class `ChromaMemory` manages memory retrieval, updating, and cleanup operations using a ChromaDB client pointing to './chroma_db' for storing embeddings and metadata of user-provided memories, including attributes like `turn_added`, `helpfulness`, and additional metadata. [2]
- **`🔌 class MemoryInterface`**: The class defines an interface for querying memory, specifying the method signature. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Adds a memory document to the Chroma collection with unique ID, embedding vector, and metadata including `turn_added`, `helpfulness`, and any additional user-provided metadata. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: The method retrieves all memories from the collection, iterates through each memory's ID and metadata, checking if helpfulness is below 0.3 or if it hasn't been used in over 50 turns since `current_turn`. If either condition is true, the memory ID is added to a list of IDs to delete. Finally, it deletes all memories with IDs in that list from the collection. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: The method queries the memory collection for documents matching the given query, updates the `last_used_turn` field in the metadata of each result document, and returns the query results including documents, metadatas, and distances. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: The method updates the `helpfulness` attribute of a specified memory in the collection by retrieving its current metadata, modifying it, and then updating the record in the database. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `78bb86` [1]: Defines an interface and class for querying, adding, updating, and cleaning up memory documents using ChromaDB client in a specified directory, encapsulating the functionality of managing user-provided memories with attributes like turn_added, helpfulness, and additional metadata. _(Source: Synthesis (based on [2], [6], [5], [3], [7], [8], [4]))_
> 🆔 `04e6a4` [2]: Class `ChromaMemory` manages memory retrieval, updating, and cleanup operations using a ChromaDB client pointing to './chroma_db' for storing embeddings and metadata of user-provided memories, including attributes like `turn_added`, `helpfulness`, and additional metadata. _(Source: class ChromaMemory)_
> 🆔 `96611c` [3]: The class defines an interface for querying memory, specifying the method signature. _(Source: class MemoryInterface)_
> 🆔 `a4465d` [4]: Adds a memory document to the Chroma collection with unique ID, embedding vector, and metadata including `turn_added`, `helpfulness`, and any additional user-provided metadata. _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `7e1873` [5]: The method retrieves all memories from the collection, iterates through each memory's ID and metadata, checking if helpfulness is below 0.3 or if it hasn't been used in over 50 turns since `current_turn`. If either condition is true, the memory ID is added to a list of IDs to delete. Finally, it deletes all memories with IDs in that list from the collection. _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `71d85c` [6]: The method queries the memory collection for documents matching the given query, updates the `last_used_turn` field in the metadata of each result document, and returns the query results including documents, metadatas, and distances. _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `970e33` [7]: The method updates the `helpfulness` attribute of a specified memory in the collection by retrieving its current metadata, modifying it, and then updating the record in the database. _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Defines an entity that analyzes and classifies Python modules into five specific archetypes based on their names, source code structure, entities, dependencies, and method behaviors.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: The class ModuleClassifier initializes an instance by setting the provided module_name and graph_data attributes, then analyzes the module to classify it into one of five archetypes based on name, source code, entities, dependencies, and method behavior. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: The method analyzes the module based on its name, source code, entities (functions and classes), dependencies, and behavior of methods to classify it as one of five archetypes: ENTRY_POINT, DATA_MODEL, CONFIGURATION, SERVICE, or UTILITY. [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8d3827` [1]: Defines an entity that analyzes and classifies Python modules into five specific archetypes based on their names, source code structure, entities, dependencies, and method behaviors. _(Source: Synthesis (based on [4], [2], [3]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `f71033` [3]: The class ModuleClassifier initializes an instance by setting the provided module_name and graph_data attributes, then analyzes the module to classify it into one of five archetypes based on name, source code, entities, dependencies, and method behavior. _(Source: class ModuleClassifier)_
> 🆔 `a3c46b` [4]: The method analyzes the module based on its name, source code, entities (functions and classes), dependencies, and behavior of methods to classify it as one of five archetypes: ENTRY_POINT, DATA_MODEL, CONFIGURATION, SERVICE, or UTILITY. _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Defines a system for contextualizing modules by analyzing components, dependencies, and systemic synthesis to generate role descriptions.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: The ModuleContextualizer class is responsible for initializing various components and attributes from provided inputs, contextualizing modules by analyzing components, dependencies, and systemic synthesis, building usage maps of interacting modules, cleaning reference text, counting tokens using CL100K Base encoding, gathering upstream knowledge, populating alerts based on todos and unimplemented functions, and passing systemic synthesis to define module capabilities. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: The method analyzes the module by first checking for errors in data, updating context with alerts if present. It then uses `comp_analyst` to analyze components and dependencies, populates alerts, passes systemic synthesis based on critique instruction, and returns updated context. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext class in summary_models.py. [4]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper.. [5]
- **`component_analyst.py`**: Uses `component_analyst.py`: Instantiates ComponentAnalyst class.. [6]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst class from dependency_analyst module.. [7]
- **`module_classifier.py`**: Uses `module_classifier.py`: Instantiates `ModuleClassifier` with module name and data.. [8]
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates TaskExecutor class. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d654bf` [1]: Defines a system for contextualizing modules by analyzing components, dependencies, and systemic synthesis to generate role descriptions. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `f212c2` [2]: The ModuleContextualizer class is responsible for initializing various components and attributes from provided inputs, contextualizing modules by analyzing components, dependencies, and systemic synthesis, building usage maps of interacting modules, cleaning reference text, counting tokens using CL100K Base encoding, gathering upstream knowledge, populating alerts based on todos and unimplemented functions, and passing systemic synthesis to define module capabilities. _(Source: class ModuleContextualizer)_
> 🆔 `a9869f` [3]: The method analyzes the module by first checking for errors in data, updating context with alerts if present. It then uses `comp_analyst` to analyze components and dependencies, populates alerts, passes systemic synthesis based on critique instruction, and returns updated context. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `8195fd` [4]: Uses `summary_models.py`: Instantiates ModuleContext class in summary_models.py. _(Source: Import summary_models.py)_
> 🆔 `f19a21` [5]: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `4cd0ca` [6]: Uses `component_analyst.py`: Instantiates ComponentAnalyst class.. _(Source: Import component_analyst.py)_
> 🆔 `3c9db2` [7]: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst class from dependency_analyst module.. _(Source: Import dependency_analyst.py)_
> 🆔 `407208` [8]: Uses `module_classifier.py`: Instantiates `ModuleClassifier` with module name and data.. _(Source: Import module_classifier.py)_
> 🆔 `698f6e` [9]: Uses `task_executor.py`: Instantiates TaskExecutor class. _(Source: Import task_executor.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Defines and manages the technical components of modules through classes that encapsulate Claim identifiers, GroundedText records for textual contexts, Alert notifications, and ModuleContext attributes such as file path, archetype, role, dependencies, dependents, public API, alerts, and claims.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: The Claim class generates a unique identifier by hashing the concatenation of `text`, `reference`, and `source_module` attributes. [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: The ModuleContext class is responsible for managing and documenting various aspects of a module, including its context (file path), role, dependencies, dependents, public API, alerts, and claims. It initializes attributes such as file_path, archetype, module_role, key_dependencies, key_dependents, public_api, alerts, and claims. Methods are available to add claims, set the module's role with supporting claim placeholders, add dependency/context entries, dependent/context entries, public API entries, alerts, and compare instances for equality. [5]
- **`🔌 🔌 Claim.id`**: The method calculates a SHA1 hash of the concatenation of `text`, `reference`, and `source_module` attributes, returning the hexadecimal digest as a string identifier. [6]
- **`🔌 🔌 ModuleContext.add_alert`**: The method adds an alert instance to the `alerts` list attribute of the class. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: The method adds dependency context for a module by combining an explanation and placeholders, then storing the result in `key_dependencies` dictionary. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: The method adds a dependent context entry for the specified module path, combining an explanation with placeholders generated from supporting claims. [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: The method adds an entry to the public API dictionary with the provided entity name and description, appending any supporting claim placeholders and IDs. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: The method `set_module_role` sets the module's role by combining provided text with placeholders from supporting claims, storing the full text and claim IDs in the instance. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `060530` [1]: Defines and manages the technical components of modules through classes that encapsulate Claim identifiers, GroundedText records for textual contexts, Alert notifications, and ModuleContext attributes such as file path, archetype, role, dependencies, dependents, public API, alerts, and claims. _(Source: Synthesis (based on [5], [10], [9], [7], [4], [11], [3], [2], [6], [8]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `bfab69` [3]: The Claim class generates a unique identifier by hashing the concatenation of `text`, `reference`, and `source_module` attributes. _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `3837aa` [5]: The ModuleContext class is responsible for managing and documenting various aspects of a module, including its context (file path), role, dependencies, dependents, public API, alerts, and claims. It initializes attributes such as file_path, archetype, module_role, key_dependencies, key_dependents, public_api, alerts, and claims. Methods are available to add claims, set the module's role with supporting claim placeholders, add dependency/context entries, dependent/context entries, public API entries, alerts, and compare instances for equality. _(Source: class ModuleContext)_
> 🆔 `d80ef9` [6]: The method calculates a SHA1 hash of the concatenation of `text`, `reference`, and `source_module` attributes, returning the hexadecimal digest as a string identifier. _(Source: 🔌 Claim.id)_
> 🆔 `a9babd` [7]: The method adds an alert instance to the `alerts` list attribute of the class. _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `f2cef1` [8]: The method adds dependency context for a module by combining an explanation and placeholders, then storing the result in `key_dependencies` dictionary. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `a27db7` [9]: The method adds a dependent context entry for the specified module path, combining an explanation with placeholders generated from supporting claims. _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `80ea60` [10]: The method adds an entry to the public API dictionary with the provided entity name and description, appending any supporting claim placeholders and IDs. _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `bc81dd` [11]: The method `set_module_role` sets the module's role by combining provided text with placeholders from supporting claims, storing the full text and claim IDs in the instance. _(Source: 🔌 ModuleContext.set_module_role)_
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