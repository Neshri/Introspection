# Project Context Map

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Defines an entry point that orchestrates the initialization of a CrawlerAgent with specified goal and target folder parameters to run the main processing loop. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Retrieves command line arguments using ArgumentParser [2]
- **`🔌 goal`**: Assigns the value of goal argument to local variable for further processing in main function [3]
- **`🔌 main`**: Locates target main script file, initializes agent with goal and root path, runs agent's processing loop [4]
- **`🔌 parser`**: Initializes an argument parser to define command-line options for subsequent use [5]
- **`🔌 result`**: Calls main function to execute logic using goal and target_folder parameters [6]
- **`🔌 target_folder`**: Assigns value from args to variable target_folder [7]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Initializes CrawlerAgent and executes its run method to coordinate memory management, goal setting, project mapping, agent state initialization, and report rendering in agent_graph_main.py.. [8]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f6f34d` [1]: Defines an entry point that orchestrates the initialization of a CrawlerAgent with specified goal and target folder parameters to run the main processing loop. _(Source: Synthesis (based on [4], [5], [6], [7], [3], [2]))_
> 🆔 `f25a1c` [2]: Retrieves command line arguments using ArgumentParser _(Source: args)_
> 🆔 `d50d38` [3]: Assigns the value of goal argument to local variable for further processing in main function _(Source: goal)_
> 🆔 `62c669` [4]: Locates target main script file, initializes agent with goal and root path, runs agent's processing loop _(Source: main)_
> 🆔 `a1a2fa` [5]: Initializes an argument parser to define command-line options for subsequent use _(Source: parser)_
> 🆔 `a365ca` [6]: Calls main function to execute logic using goal and target_folder parameters _(Source: result)_
> 🆔 `ab6155` [7]: Assigns value from args to variable target_folder _(Source: target_folder)_
> 🆔 `e51fcf` [8]: Uses `agent_core.py`: Initializes CrawlerAgent and executes its run method to coordinate memory management, goal setting, project mapping, agent state initialization, and report rendering in agent_graph_main.py.. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` CrawlerAgent.run defines and coordinates memory storage management through ChromaMemory integration to orchestrate agent operations.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Manages goal, root path, memory storage and orchestrates agent operations [2]
- **`🔌 🔌 CrawlerAgent.run`**: Calls memory cleaner, initializes agent state, retrieves project map and processing order, creates gatekeeper and synthesizer, synthesizes system summary, renders report, returns response. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper and calls its run method within agent_core.py. [4]
- **`agent_config.py`**: Imports `agent_config.py`. [5]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates an instance of ReportRenderer. [6]
- **`llm_util.py`**: Uses `llm_util.py`: {'code': 'agent_core.py executes chat_llm() from llm_util.py within its run() method to process prompts, call LLM functions, and extract responses.'}. [7]
- **`memory_core.py`**: Uses `memory_core.py`: Initializes memory management by instantiating ChromaMemory in agent_core.py. [8]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates and configures ModuleContext within agent_core.py to define module roles, dependencies, API entries, alerts, and placeholders for AI agent processing.. [9]
- **`agent_util.py`**: Uses `agent_util.py`: Analyzes project structure by processing target graph and generating context maps using `project_pulse` from `agent_util.py` in `agent_core.py`. [10]
- **`map_synthesizer.py`**: Uses `map_synthesizer.py`: Instantiates the MapSynthesizer class to organize and synthesize module details into system narratives based on archetype, coordinating the synthesis of module details and system summaries.. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ff2ab0` [1]: CrawlerAgent.run defines and coordinates memory storage management through ChromaMemory integration to orchestrate agent operations. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `9fb0cc` [2]: Manages goal, root path, memory storage and orchestrates agent operations _(Source: class CrawlerAgent)_
> 🆔 `636508` [3]: Calls memory cleaner, initializes agent state, retrieves project map and processing order, creates gatekeeper and synthesizer, synthesizes system summary, renders report, returns response. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `a99ca4` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper and calls its run method within agent_core.py. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `d23947` [5]: Imports `agent_config.py`. _(Source: Import agent_config.py)_
> 🆔 `a39bec` [6]: Uses `report_renderer.py`: Instantiates an instance of ReportRenderer. _(Source: Import report_renderer.py)_
> 🆔 `00e1d8` [7]: Uses `llm_util.py`: {'code': 'agent_core.py executes chat_llm() from llm_util.py within its run() method to process prompts, call LLM functions, and extract responses.'}. _(Source: Import llm_util.py)_
> 🆔 `456a30` [8]: Uses `memory_core.py`: Initializes memory management by instantiating ChromaMemory in agent_core.py. _(Source: Import memory_core.py)_
> 🆔 `11bf3e` [9]: Uses `summary_models.py`: Instantiates and configures ModuleContext within agent_core.py to define module roles, dependencies, API entries, alerts, and placeholders for AI agent processing.. _(Source: Import summary_models.py)_
> 🆔 `ab85f7` [10]: Uses `agent_util.py`: Analyzes project structure by processing target graph and generating context maps using `project_pulse` from `agent_util.py` in `agent_core.py`. _(Source: Import agent_util.py)_
> 🆔 `960425` [11]: Uses `map_synthesizer.py`: Instantiates the MapSynthesizer class to organize and synthesize module details into system narratives based on archetype, coordinating the synthesis of module details and system summaries.. _(Source: Import map_synthesizer.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Defines a service that analyzes project structure to generate detailed module context maps for AI agents.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Declares ProjectGraph as a dictionary mapping string keys to any values [2]
- **`🔌 class ProjectSummarizer`**: Computes topological order for modules based on dependencies, aggregates module contexts through cycles until convergence or maximum cycles are reached [3]
- **`🔌 project_pulse`**: Analyzes project structure by creating graph and summarizing contexts [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Aggregates module contexts by processing dependencies, critiques, and source code hashes in cycles until convergence is reached or maximum cycles are exhausted, then updates internal context storage. [5]
- **`🔒 _create_module_context`**: Generates module context by contextualizing path, graph, dependencies, and critique instruction [6]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Initializes and configures the SemanticGatekeeper service, establishing controlled access mechanisms for coordinated functionality across associated components such as agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, and task_executor.py.. [7]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext objects to encapsulate module role, dependencies, API entries, alerts, and placeholders for analysis.. [8]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer from graph_analyzer.py in agent_util.py, passing target_file_path as an argument to analyze dependencies.. [9]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates ReportRenderer from report_renderer.py, passing contexts and output_file arguments to configure context map report generation logic in agent_util.py. [10]
- **`map_critic.py`**: Uses `map_critic.py`: Creates a MapCritic instance and executes its associated functions in agent_util.py. [11]
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: Creates an instance of ModuleContextualizer using specified path, graph, and dep_contexts parameters to encapsulate module context information for agent_util.py.. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `cbab9b` [1]: Defines a service that analyzes project structure to generate detailed module context maps for AI agents. _(Source: Synthesis (based on [6], [2], [5], [3], [4]))_
> 🆔 `c4aec0` [2]: Declares ProjectGraph as a dictionary mapping string keys to any values _(Source: ProjectGraph)_
> 🆔 `f14626` [3]: Computes topological order for modules based on dependencies, aggregates module contexts through cycles until convergence or maximum cycles are reached _(Source: class ProjectSummarizer)_
> 🆔 `f247e3` [4]: Analyzes project structure by creating graph and summarizing contexts _(Source: project_pulse)_
> 🆔 `e7f942` [5]: Aggregates module contexts by processing dependencies, critiques, and source code hashes in cycles until convergence is reached or maximum cycles are exhausted, then updates internal context storage. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `49f5c6` [6]: Generates module context by contextualizing path, graph, dependencies, and critique instruction _(Source: _create_module_context)_
> 🆔 `acb3d4` [7]: Uses `semantic_gatekeeper.py`: Initializes and configures the SemanticGatekeeper service, establishing controlled access mechanisms for coordinated functionality across associated components such as agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, and task_executor.py.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `af840f` [8]: Uses `summary_models.py`: Instantiates ModuleContext objects to encapsulate module role, dependencies, API entries, alerts, and placeholders for analysis.. _(Source: Import summary_models.py)_
> 🆔 `d513c9` [9]: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer from graph_analyzer.py in agent_util.py, passing target_file_path as an argument to analyze dependencies.. _(Source: Import graph_analyzer.py)_
> 🆔 `ecb93b` [10]: Uses `report_renderer.py`: Instantiates ReportRenderer from report_renderer.py, passing contexts and output_file arguments to configure context map report generation logic in agent_util.py. _(Source: Import report_renderer.py)_
> 🆔 `2cc440` [11]: Uses `map_critic.py`: Creates a MapCritic instance and executes its associated functions in agent_util.py. _(Source: Import map_critic.py)_
> 🆔 `43a03a` [12]: Uses `module_contextualizer.py`: Creates an instance of ModuleContextualizer using specified path, graph, and dep_contexts parameters to encapsulate module context information for agent_util.py.. _(Source: Import module_contextualizer.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Defines a service that analyzes component code structure, dependencies, mechanisms, and coordinates transformations to generate summaries based on specified parameters.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes component code structure, dependencies, mechanisms, and generates summaries based on specified parameters [2]
- **`🔌 class SkeletonTransformer`**: Transforms function, class, and async function definitions by manipulating their bodies to include or exclude specific expressions containing ellipsis constants based on transformation requirements [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Extracts module name from file path, processes globals and functions data, resolves dependencies, analyzes mechanisms and summarizes findings for each component type. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Transforms AST to mark functions as incomplete by appending ellipsis, modifies classes by removing docstrings and adding Pass if empty, then unparses back to source code. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Creates new node by adding an expression that evaluates to Ellipsis [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes leading docstring from class definition body [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Creates new function definition node by adding Expr with Ellipsis constant to body [8]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper and configures its parameters during initialization. [9]
- **`summary_models.py`**: Uses `summary_models.py`: Analyzes and updates module contexts by instantiating ModuleContext objects, resolving dependency contexts using Claim objects, and aggregating API entries, alerts, and placeholders within component_analyst.py.. [10]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `97b211` [1]: Defines a service that analyzes component code structure, dependencies, mechanisms, and coordinates transformations to generate summaries based on specified parameters. _(Source: Synthesis (based on [2], [8], [4], [5], [6], [7], [3]))_
> 🆔 `4c9d17` [2]: Analyzes component code structure, dependencies, mechanisms, and generates summaries based on specified parameters _(Source: class ComponentAnalyst)_
> 🆔 `f3a8b2` [3]: Transforms function, class, and async function definitions by manipulating their bodies to include or exclude specific expressions containing ellipsis constants based on transformation requirements _(Source: class SkeletonTransformer)_
> 🆔 `7c986d` [4]: Extracts module name from file path, processes globals and functions data, resolves dependencies, analyzes mechanisms and summarizes findings for each component type. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `d9e03f` [5]: Transforms AST to mark functions as incomplete by appending ellipsis, modifies classes by removing docstrings and adding Pass if empty, then unparses back to source code. _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `dfa559` [6]: Creates new node by adding an expression that evaluates to Ellipsis _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `ea9760` [7]: Removes leading docstring from class definition body _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `59bb0a` [8]: Creates new function definition node by adding Expr with Ellipsis constant to body _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `9283ad` [9]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper and configures its parameters during initialization. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `c1157d` [10]: Uses `summary_models.py`: Analyzes and updates module contexts by instantiating ModuleContext objects, resolving dependency contexts using Claim objects, and aggregating API entries, alerts, and placeholders within component_analyst.py.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Defines a service that analyzes dependencies by retrieving context, sanitizing text, determining used symbols from interactions, and gathering relevant entries from upstream APIs.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Safeguards and analyzes dependencies by retrieving context, sanitizing text, determining used symbols, gathering relevant entries, and compiling usage snippets from interactions. [2]
- **`🔌 clean_ref`**: Removes bracketed reference patterns from input text and trims whitespace [3]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes dependencies by iterating over each dependency path, retrieves context, sanitizes role text, determines used symbols from interactions, gathers relevant entries from upstream API, and compiles usage snippets. [4]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Inits an instance of SemanticGatekeeper during DependencyAnalyst class instantiation. [5]
- **`summary_models.py`**: Uses `summary_models.py`: Analyzes module dependencies and context using ModuleContext, add_dependency_context method, and Claim class from summary_models to encapsulate dependency information for analysis.. [6]
- **`task_executor.py`**: Uses `task_executor.py`: Initializes and configures the TaskExecutor class for managing gatekeeper data processing tasks within dependency_analyst.py. [7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `875a70` [1]: Defines a service that analyzes dependencies by retrieving context, sanitizing text, determining used symbols from interactions, and gathering relevant entries from upstream APIs. _(Source: Synthesis (based on [3], [4], [2]))_
> 🆔 `84dd8e` [2]: Safeguards and analyzes dependencies by retrieving context, sanitizing text, determining used symbols, gathering relevant entries, and compiling usage snippets from interactions. _(Source: class DependencyAnalyst)_
> 🆔 `46f3ff` [3]: Removes bracketed reference patterns from input text and trims whitespace _(Source: clean_ref)_
> 🆔 `497780` [4]: Analyzes dependencies by iterating over each dependency path, retrieves context, sanitizes role text, determines used symbols from interactions, gathers relevant entries from upstream API, and compiles usage snippets. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `a33454` [5]: Uses `semantic_gatekeeper.py`: Inits an instance of SemanticGatekeeper during DependencyAnalyst class instantiation. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `25ea22` [6]: Uses `summary_models.py`: Analyzes module dependencies and context using ModuleContext, add_dependency_context method, and Claim class from summary_models to encapsulate dependency information for analysis.. _(Source: Import summary_models.py)_
> 🆔 `90606f` [7]: Uses `task_executor.py`: Initializes and configures the TaskExecutor class for managing gatekeeper data processing tasks within dependency_analyst.py. _(Source: Import task_executor.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Defines a service that analyzes project map content, extracts module names and descriptions, performs documentation audits on modules, critiques top three modules, and generates critique list

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Analyzes project map content, extracts module names and descriptions, performs documentation audits on modules [2]
- **`🔌 🔌 MapCritic.critique`**: Parses project map content, analyzes modules, critiques top three modules, and generates critique list [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates the SemanticGatekeeper class within map_critic.py. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `e3870a` [1]: Defines a service that analyzes project map content, extracts module names and descriptions, performs documentation audits on modules, critiques top three modules, and generates critique list _(Source: Synthesis (based on [3], [2]))_
> 🆔 `dc6bd4` [2]: Analyzes project map content, extracts module names and descriptions, performs documentation audits on modules _(Source: class MapCritic)_
> 🆔 `69f041` [3]: Parses project map content, analyzes modules, critiques top three modules, and generates critique list _(Source: 🔌 MapCritic.critique)_
> 🆔 `cbc93d` [4]: Uses `semantic_gatekeeper.py`: Instantiates the SemanticGatekeeper class within map_critic.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` Defines a service that coordinates and synthesizes module details into system narratives based on their archetype.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Organizes and synthesizes module details into system narratives based on archetype. [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Organizes modules into groups based on their archetype and synthesizes each group, then synthesizes the system from summaries [3]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Uses `llm_util.py`: Calls the chat_llm function to initiate an LLM interaction and process the response content. [4]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: {'action_text': 'Instantiates SemanticGatekeeper', 'status': 'ACTIVE'}. [5]
- **`summary_models.py`**: Uses `summary_models.py`: Analyzes module dependencies and API context, synthesizing module summaries using ModuleContext instances from summary_models.py. [6]
- **`agent_config.py`**: Imports `agent_config.py`. [7]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `89a192` [1]: Defines a service that coordinates and synthesizes module details into system narratives based on their archetype. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `67df6b` [2]: Organizes and synthesizes module details into system narratives based on archetype. _(Source: class MapSynthesizer)_
> 🆔 `1cd984` [3]: Organizes modules into groups based on their archetype and synthesizes each group, then synthesizes the system from summaries _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `349580` [4]: Uses `llm_util.py`: Calls the chat_llm function to initiate an LLM interaction and process the response content. _(Source: Import llm_util.py)_
> 🆔 `10f6a0` [5]: Uses `semantic_gatekeeper.py`: {'action_text': 'Instantiates SemanticGatekeeper', 'status': 'ACTIVE'}. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `b063a5` [6]: Uses `summary_models.py`: Analyzes module dependencies and API context, synthesizing module summaries using ModuleContext instances from summary_models.py. _(Source: Import summary_models.py)_
> 🆔 `24af77` [7]: Imports `agent_config.py`. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Defines a service that coordinates the generation of project context map reports by organizing modules according to their archetypes and managing reference replacements while processing various data structures.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Organizes, processes, and generates context reports for modules while managing data structures and rendering outputs. [2]
- **`🔌 replace_ref`**: Manages references by replacing them with unique identifiers, preserving original text structure [3]
- **`🔌 sub`**: Manages claim references by assigning unique IDs [4]
- **`🔌 🔌 ReportRenderer.render`**: Generates project context map report, organizes modules by archetype, writes to output file [5]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext from summary_models and passes context_map parameter to report_renderer.py's initialization. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `684115` [1]: Defines a service that coordinates the generation of project context map reports by organizing modules according to their archetypes and managing reference replacements while processing various data structures. _(Source: Synthesis (based on [4], [2], [3], [5]))_
> 🆔 `5f8c8a` [2]: Organizes, processes, and generates context reports for modules while managing data structures and rendering outputs. _(Source: class ReportRenderer)_
> 🆔 `9e98b2` [3]: Manages references by replacing them with unique identifiers, preserving original text structure _(Source: replace_ref)_
> 🆔 `4f8922` [4]: Manages claim references by assigning unique IDs _(Source: sub)_
> 🆔 `cc11fb` [5]: Generates project context map report, organizes modules by archetype, writes to output file _(Source: 🔌 ReportRenderer.render)_
> 🆔 `906fc6` [6]: Uses `summary_models.py`: Instantiates ModuleContext from summary_models and passes context_map parameter to report_renderer.py's initialization. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Defines a service that manages and organizes data structures while providing controlled access mechanisms to coordinate and analyze the functionality of associated components.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Declares a set containing disallowed adjectives, creating an exclusion list for filtering language usage in application code [2]
- **`🔌 class SemanticGatekeeper`**: Organizes and manages data structures while providing controlled access mechanisms [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Constructs a prompt for feedback, generates messages, performs parsing, critiques content style, verifies grounding, and returns formatted JSON output. [4]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py`: Invokes the chat_llm function with DEFAULT_MODEL as an argument to process queries and generate responses.. [5]
- **`llm_util.py`**: Uses `llm_util.py`: Calls chat_llm to process prompts and extract LLM responses across multiple modules. [6]

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

> 🆔 `c4ec9a` [1]: Defines a service that manages and organizes data structures while providing controlled access mechanisms to coordinate and analyze the functionality of associated components. _(Source: Synthesis (based on [4], [3], [2]))_
> 🆔 `bfe077` [2]: Declares a set containing disallowed adjectives, creating an exclusion list for filtering language usage in application code _(Source: BANNED_ADJECTIVES)_
> 🆔 `b2a332` [3]: Organizes and manages data structures while providing controlled access mechanisms _(Source: class SemanticGatekeeper)_
> 🆔 `51f1ce` [4]: Constructs a prompt for feedback, generates messages, performs parsing, critiques content style, verifies grounding, and returns formatted JSON output. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `f7d6db` [5]: Uses `agent_config.py`: Invokes the chat_llm function with DEFAULT_MODEL as an argument to process queries and generate responses.. _(Source: Import agent_config.py)_
> 🆔 `3d21da` [6]: Uses `llm_util.py`: Calls chat_llm to process prompts and extract LLM responses across multiple modules. _(Source: Import llm_util.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` Defines a service that manages initialization, cleaning, parsing, and response handling of gatekeeper data.

**Impact Analysis:** Changes to this module will affect: dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Manages the initialization, cleaning, parsing, and response handling of gatekeeper data [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Extracts plan from semantic gatekeeper [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Initializes and configures the SemanticGatekeeper class within task_executor.py, establishing necessary parameters for data management and controlled access mechanisms across related components.. [4]

### 👥 Used By (Downstream)
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `089f3a` [1]: Defines a service that manages initialization, cleaning, parsing, and response handling of gatekeeper data. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `ad36fb` [2]: Manages the initialization, cleaning, parsing, and response handling of gatekeeper data _(Source: class TaskExecutor)_
> 🆔 `f15f0b` [3]: Extracts plan from semantic gatekeeper _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `06f578` [4]: Uses `semantic_gatekeeper.py`: Initializes and configures the SemanticGatekeeper class within task_executor.py, establishing necessary parameters for data management and controlled access mechanisms across related components.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Defines a utility function that converts prompts to messages, calls an LLM chat function, and extracts the response content.

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Converts prompt to messages, calls LLM chat function, extracts response content [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `0d894e` [1]: Defines a utility function that converts prompts to messages, calls an LLM chat function, and extracts the response content. _(Source: Synthesis (based on [2]))_
> 🆔 `1d20aa` [2]: Converts prompt to messages, calls LLM chat function, extracts response content _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Defines a dependency graph structure representing the relationships between modules, functions, classes, and global variables in a Python project.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Analyzes and organizes code structure, imports, functions, classes, globals, and interactions within a project context [2]
- **`🔌 class GraphAnalyzer`**: Collects project files, constructs dependency graph structure, and populates dependents data sets using DFS traversal. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes current class context from stack [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Maintains current context stack by popping when function definition is left [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Updates current statement to None [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Records annotated variable names as global entities in current context [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Records global variable assignments from current module node [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Captures function names called within current module, records interactions [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Registers class definition by appending to context, retrieving source code, extracting docstring and bases, constructing header string, storing metadata in entities dictionary [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Records function details, generates signature, checks for docstring and implementation, determines if method or standalone function, updates entities dictionary with relevant data [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Collects external module names from imported nodes and adds them to set [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes import from nodes to determine relative or external imports, updates paths in project files list, and populates import map for names. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records interactions when node context matches [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Updates current statement attribute to node during SimpleStatementLine visitation [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds graph using DFS traversal and populates dependents dictionary [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `6b6cec` [1]: Defines a dependency graph structure representing the relationships between modules, functions, classes, and global variables in a Python project. _(Source: Synthesis (based on [10], [8], [7], [3], [12], [13], [6], [2], [11], [16], [5], [15], [4], [14], [9]))_
> 🆔 `a3937d` [2]: Analyzes and organizes code structure, imports, functions, classes, globals, and interactions within a project context _(Source: class CodeEntityVisitor)_
> 🆔 `2befe3` [3]: Collects project files, constructs dependency graph structure, and populates dependents data sets using DFS traversal. _(Source: class GraphAnalyzer)_
> 🆔 `e796cb` [4]: Removes current class context from stack _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `c39c1b` [5]: Maintains current context stack by popping when function definition is left _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `83fdf7` [6]: Updates current statement to None _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `175c31` [7]: Records annotated variable names as global entities in current context _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `0f94b3` [8]: Records global variable assignments from current module node _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `ff8f1e` [9]: Captures function names called within current module, records interactions _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `054892` [10]: Registers class definition by appending to context, retrieving source code, extracting docstring and bases, constructing header string, storing metadata in entities dictionary _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `ac28e8` [11]: Records function details, generates signature, checks for docstring and implementation, determines if method or standalone function, updates entities dictionary with relevant data _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `4fc121` [12]: Collects external module names from imported nodes and adds them to set _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `519580` [13]: Analyzes import from nodes to determine relative or external imports, updates paths in project files list, and populates import map for names. _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `feec87` [14]: Records interactions when node context matches _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `e18c57` [15]: Updates current statement attribute to node during SimpleStatementLine visitation _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `b83342` [16]: Builds graph using DFS traversal and populates dependents dictionary _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Defines

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Manages the creation, retrieval, updating, and cleanup of memory entries using Chroma's text embedding capabilities [2]
- **`🔌 class MemoryInterface`**: Manages memory queries and defines the interface for accessing stored data [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Creates unique identifier for memory, combines metadata into dictionary, updates metadata from input parameters, and adds document to Chroma collection. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Retrieves memories from collection, identifies low usefulness or unused ones, deletes them [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Retrieves memory results for query, updates last used turn in metadata [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Retrieves metadata for specified memory, creates copy, updates helpfulness value, stores updated metadata back to collection [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1083b4` [1]: Defines _(Source: Synthesis (based on [4], [7], [6], [3], [8], [5], [2]))_
> 🆔 `fa4ec0` [2]: Manages the creation, retrieval, updating, and cleanup of memory entries using Chroma's text embedding capabilities _(Source: class ChromaMemory)_
> 🆔 `7c0b6c` [3]: Manages memory queries and defines the interface for accessing stored data _(Source: class MemoryInterface)_
> 🆔 `23045c` [4]: Creates unique identifier for memory, combines metadata into dictionary, updates metadata from input parameters, and adds document to Chroma collection. _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `ed847b` [5]: Retrieves memories from collection, identifies low usefulness or unused ones, deletes them _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `3f01a6` [6]: Retrieves memory results for query, updates last used turn in metadata _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `3be5fb` [7]: Retrieves metadata for specified memory, creates copy, updates helpfulness value, stores updated metadata back to collection _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Defines a data container and classification mechanism for module archetypes in Python.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Analyzes module data structures, dependencies, and signatures to determine its archetype programmatically [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Determines module archetype by analyzing name, source code structure, entities, dependencies, functions, classes, global variables, and method signatures. [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `18edab` [1]: Defines a data container and classification mechanism for module archetypes in Python. _(Source: Synthesis (based on [3], [2], [4]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `45c705` [3]: Analyzes module data structures, dependencies, and signatures to determine its archetype programmatically _(Source: class ModuleClassifier)_
> 🆔 `d0b963` [4]: Determines module archetype by analyzing name, source code structure, entities, dependencies, functions, classes, global variables, and method signatures. _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Defines a class that encapsulates module context information

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Organizes and analyzes module's components, dependencies, usage patterns, and upstream knowledge [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Manages module contextualization by analyzing components, dependencies, and systemic synthesis based on critique instruction. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates the SemanticGatekeeper class without any arguments to establish controlled access mechanisms for coordinating functionality across components in module_contextualizer.py. [4]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst from dependency_analyst.py within module_contextualizer.py by passing gatekeeper and task_executor arguments to create an instance for performing dependency analysis.. [5]
- **`module_classifier.py`**: Uses `module_classifier.py`: Imports ModuleClassifier and ModuleArchetype from module_classifier.py. [6]
- **`component_analyst.py`**: Uses `component_analyst.py`: Instantiates ComponentAnalyst within module_contextualizer.py. [7]
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates TaskExecutor. [8]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates an instance of ModuleContext to encapsulate module context information, including role text, dependencies, dependents, API entries, alerts, and placeholders.. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `bce758` [1]: Defines a class that encapsulates module context information _(Source: Synthesis (based on [3], [2]))_
> 🆔 `cef4da` [2]: Organizes and analyzes module's components, dependencies, usage patterns, and upstream knowledge _(Source: class ModuleContextualizer)_
> 🆔 `820f3d` [3]: Manages module contextualization by analyzing components, dependencies, and systemic synthesis based on critique instruction. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `bc492a` [4]: Uses `semantic_gatekeeper.py`: Instantiates the SemanticGatekeeper class without any arguments to establish controlled access mechanisms for coordinating functionality across components in module_contextualizer.py. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `28e797` [5]: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst from dependency_analyst.py within module_contextualizer.py by passing gatekeeper and task_executor arguments to create an instance for performing dependency analysis.. _(Source: Import dependency_analyst.py)_
> 🆔 `89660c` [6]: Uses `module_classifier.py`: Imports ModuleClassifier and ModuleArchetype from module_classifier.py. _(Source: Import module_classifier.py)_
> 🆔 `a2fe19` [7]: Uses `component_analyst.py`: Instantiates ComponentAnalyst within module_contextualizer.py. _(Source: Import component_analyst.py)_
> 🆔 `b5877d` [8]: Uses `task_executor.py`: Instantiates TaskExecutor. _(Source: Import task_executor.py)_
> 🆔 `3df260` [9]: Uses `summary_models.py`: Instantiates an instance of ModuleContext to encapsulate module context information, including role text, dependencies, dependents, API entries, alerts, and placeholders.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Defines and encapsulates a data structure for a module context map to allow an AI agent to comprehend a module's role, dependencies, API entries, alerts, and placeholders without using the term 'comprehensive'.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Creates unique identifiers by combining text, reference, source module information and applying a hashing algorithm [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Encapsulates state for module context management, including role text, dependencies, dependents, API entries, alerts, and placeholders. [5]
- **`🔌 🔌 Claim.id`**: Creates unique identifier by concatenating text, reference, source module, hashing string [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Appends alert to alerts list [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Manages dependencies by adding context for module path, explanation, and supporting claims to key_dependencies dictionary. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Accumulates dependent context information for module path, combining explanation and claim placeholders into full text and storing in key_dependents dictionary [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds public API entry by combining description and placeholders, storing in state dictionary. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Adds module role text to grounded text, includes supporting claims in output. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8d2e52` [1]: Defines and encapsulates a data structure for a module context map to allow an AI agent to comprehend a module's role, dependencies, API entries, alerts, and placeholders without using the term 'comprehensive'. _(Source: Synthesis (based on [3], [7], [5], [8], [6], [9], [11], [4], [10], [2]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `3b7597` [3]: Creates unique identifiers by combining text, reference, source module information and applying a hashing algorithm _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `6e8475` [5]: Encapsulates state for module context management, including role text, dependencies, dependents, API entries, alerts, and placeholders. _(Source: class ModuleContext)_
> 🆔 `9a0df0` [6]: Creates unique identifier by concatenating text, reference, source module, hashing string _(Source: 🔌 Claim.id)_
> 🆔 `66123b` [7]: Appends alert to alerts list _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `994083` [8]: Manages dependencies by adding context for module path, explanation, and supporting claims to key_dependencies dictionary. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `9d4321` [9]: Accumulates dependent context information for module path, combining explanation and claim placeholders into full text and storing in key_dependents dictionary _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `cab211` [10]: Adds public API entry by combining description and placeholders, storing in state dictionary. _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `a0c73e` [11]: Adds module role text to grounded text, includes supporting claims in output. _(Source: 🔌 ModuleContext.set_module_role)_
</details>

---
## 🔧 Configuration

## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Assigns an integer value to a global variable named CONTEXT_LIMIT, setting it equal to 4096. [2]
- **`🔌 DEFAULT_MODEL`**: Assigns string literal value to global variable indicating model identifier [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `449512` [1]: Defines configuration constants. _(Source: Archetype)_
> 🆔 `5b6ae6` [2]: Assigns an integer value to a global variable named CONTEXT_LIMIT, setting it equal to 4096. _(Source: CONTEXT_LIMIT)_
> 🆔 `305fde` [3]: Assigns string literal value to global variable indicating model identifier _(Source: DEFAULT_MODEL)_
</details>

---