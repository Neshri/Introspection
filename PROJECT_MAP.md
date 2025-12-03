# Project Context Map

## 🏛️ System Architecture
# High-Level System Overview

The system is structured around four main layers that work together to analyze and process data. The **Entry Point Layer** initiates the workflow by parsing command-line arguments and invoking core analysis functions defined in lower layers.

Moving down the stack, the **Service Layer** includes specialized modules that handle different aspects of the analysis. The `semantic_gatekeeper.py` enforces technical guidelines, while `report_renderer.py` and `task_executor.py` process requirements and generate insights based on feedback from the gatekeeper. The `component_analyst.py` synthesizes component structures by analyzing outputs from other modules.

The **Utility Layer** provides essential services such as data format conversion through `llm_util.py`, which interacts closely with core processing modules like `agent_core.py`. This layer ensures that input data is correctly formatted and output results are interpreted appropriately. Finally, the **Data Model Layer** defines critical structures and encapsulates classification logic for various data types, including claims, module contexts, and architectural information. Modules within this layer interact extensively with others to maintain consistent data representation and facilitate complex analyses.

Changes in any layer ripple through the system, highlighting the interconnected nature of the modules. For instance, modifications in `agent_config.py` impact core operational parameters across all components, underscoring the importance of careful coordination during updates. This layered architecture ensures modularity, scalability, and maintainability.

---

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates the execution of analysis workflows by initializing an argument parser to configure program parameters, parsing command-line arguments to initialize global variables for goal and target_folder, assigns values from parsed args to local variables, invokes main function to process specified goal within target folder, retrieves computed results, and returns completion message. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Parses command-line arguments using an argument parser to initialize global variables for goal, target_folder, and stores parsed args in local variable. [2]
- **`🔌 goal`**: Assigns the value of 'args.goal' to the local variable for further processing in the main function call. [3]
- **`🔌 main`**: Finds target root file ending in _main.py, initializes CrawlerAgent for specified goal and folder, executes agent run, and returns completion message. [4]
- **`🔌 parser`**: Configures an argument parser to specify program parameters. [5]
- **`🔌 result`**: Invokes main function to process specified goal within target folder and retrieves computed results. [6]
- **`🔌 target_folder`**: Assigns source directory path from command-line argument to processing configuration. [7]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Configures the timeout settings for the CrawlerAgent instance based on parameters from agent_core.py functions such as self.run().. [8]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `bbed8f` [1]: Orchestrates the execution of analysis workflows by initializing an argument parser to configure program parameters, parsing command-line arguments to initialize global variables for goal and target_folder, assigns values from parsed args to local variables, invokes main function to process specified goal within target folder, retrieves computed results, and returns completion message. _(Source: Synthesis (based on [5], [2], [7], [3], [4], [6]))_
> 🆔 `2b27db` [2]: Parses command-line arguments using an argument parser to initialize global variables for goal, target_folder, and stores parsed args in local variable. _(Source: args)_
> 🆔 `e5e08b` [3]: Assigns the value of 'args.goal' to the local variable for further processing in the main function call. _(Source: goal)_
> 🆔 `f71ead` [4]: Finds target root file ending in _main.py, initializes CrawlerAgent for specified goal and folder, executes agent run, and returns completion message. _(Source: main)_
> 🆔 `25f189` [5]: Configures an argument parser to specify program parameters. _(Source: parser)_
> 🆔 `f8cb6e` [6]: Invokes main function to process specified goal within target folder and retrieves computed results. _(Source: result)_
> 🆔 `4cbacd` [7]: Assigns source directory path from command-line argument to processing configuration. _(Source: target_folder)_
> 🆔 `7d1a5f` [8]: Uses `agent_core.py`: Configures the timeout settings for the CrawlerAgent instance based on parameters from agent_core.py functions such as self.run().. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Analyzes project modules, computes processing order, and manages contextual data across refinement cycles.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Encapsulates analysis workflows, manages project data, and logs completion details. [2]
- **`🔌 🔌 CrawlerAgent.run`**: Runs analysis for specified goal and target root, generates project map and system summary, renders report, cleans memories 5 times, and returns completion message. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper and configures its strict enforcement of technical analysis guidelines within agent_core.py.. [4]
- **`agent_util.py`**: Uses `agent_util.py`: configures the dependency graph analysis. [5]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates ReportRenderer as renderer = ReportRenderer(project_map, system_summary=system_summary), leveraging project context data to generate detailed reports within agent_core.py.. [6]
- **`memory_core.py`**: Uses `memory_core.py`: Initializes the ChromaMemory instance and passes necessary parameters for memory management.; Manages memory storage and retrieval within the Chroma database, facilitating persistent text embedding associations.. [7]
- **`llm_util.py`**: Uses `llm_util.py`: processes and formats user prompts before delegating them to the Ollama chat API.. [8]
- **`summary_models.py`**: Uses `summary_models.py`: Configures and manages module context data, dependencies, alerts, and supporting claims within agent_core.py using classes from summary_models.py such as ModuleContext to represent claims, grounded text records, and contextual relationships between modules.. [9]
- **`agent_config.py`**: Uses `agent_config.py`: Instantiates DEFAULT_MODEL and CONTEXT_LIMIT from agent_config to configure language model parameters for text processing operations.. [10]
- **`map_synthesizer.py`**: Uses `map_synthesizer.py`: Configures the MapSynthesizer instance for use in agent_core.py.. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `460507` [1]: Analyzes project modules, computes processing order, and manages contextual data across refinement cycles. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `c2a0a7` [2]: Encapsulates analysis workflows, manages project data, and logs completion details. _(Source: class CrawlerAgent)_
> 🆔 `4ee152` [3]: Runs analysis for specified goal and target root, generates project map and system summary, renders report, cleans memories 5 times, and returns completion message. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `2c01b8` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper and configures its strict enforcement of technical analysis guidelines within agent_core.py.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `aae8ce` [5]: Uses `agent_util.py`: configures the dependency graph analysis. _(Source: Import agent_util.py)_
> 🆔 `449212` [6]: Uses `report_renderer.py`: Instantiates ReportRenderer as renderer = ReportRenderer(project_map, system_summary=system_summary), leveraging project context data to generate detailed reports within agent_core.py.. _(Source: Import report_renderer.py)_
> 🆔 `5ad84c` [7]: Uses `memory_core.py`: Initializes the ChromaMemory instance and passes necessary parameters for memory management.; Manages memory storage and retrieval within the Chroma database, facilitating persistent text embedding associations.. _(Source: Import memory_core.py)_
> 🆔 `a21531` [8]: Uses `llm_util.py`: processes and formats user prompts before delegating them to the Ollama chat API.. _(Source: Import llm_util.py)_
> 🆔 `104d29` [9]: Uses `summary_models.py`: Configures and manages module context data, dependencies, alerts, and supporting claims within agent_core.py using classes from summary_models.py such as ModuleContext to represent claims, grounded text records, and contextual relationships between modules.. _(Source: Import summary_models.py)_
> 🆔 `e7be9a` [10]: Uses `agent_config.py`: Instantiates DEFAULT_MODEL and CONTEXT_LIMIT from agent_config to configure language model parameters for text processing operations.. _(Source: Import agent_config.py)_
> 🆔 `d60506` [11]: Uses `map_synthesizer.py`: Configures the MapSynthesizer instance for use in agent_core.py.. _(Source: Import map_synthesizer.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Analyzes project modules, computes processing order, and manages contextual data across refinement cycles.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Initializes ProjectGraph dictionary variable with Any type placeholder. [2]
- **`🔌 class ProjectSummarizer`**: Analyzes project modules, computes processing order, and manages contextual data across refinement cycles. [3]
- **`🔌 project_pulse`**: Manages project analysis by building a dependency graph, generating module contexts, and summarizing findings based on source code files. [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Manages module contexts across refinement cycles, evaluates changes using MapCritic, caches processed states, and tracks processing order. [5]
- **`🔒 _create_module_context`**: Analyzes module components, dependencies, and usage to build contextual information, adding alerts for detected errors. [6]

### 🔗 Uses (Upstream)
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: Initializes an instance of ModuleContextualizer with parameters path, graph, and dep_contexts.. [7]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Initializes the SemanticGatekeeper class for content validation and constraint enforcement.. [8]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates ReportRenderer with self.contexts and temp_map_path arguments to generate project context reports.. [9]
- **`summary_models.py`**: Uses `summary_models.py`: Configures the ModuleContext instances from summary_models.py for context management and dependency tracking.; Instantiates ModuleContext objects to represent module context data.. [10]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: Initializes the GraphAnalyzer instance using target_file_path to analyze dependencies and relationships.. [11]
- **`map_critic.py`**: Uses `map_critic.py`: Instantiates the MapCritic class and configures it by passing the gatekeeper argument to its constructor, which is then utilized to analyze project map content for critique-worthy modules.. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `75c973` [1]: Analyzes project modules, computes processing order, and manages contextual data across refinement cycles. _(Source: Synthesis (based on [4], [5], [2], [3], [6]))_
> 🆔 `9ac95d` [2]: Initializes ProjectGraph dictionary variable with Any type placeholder. _(Source: ProjectGraph)_
> 🆔 `bdbedb` [3]: Analyzes project modules, computes processing order, and manages contextual data across refinement cycles. _(Source: class ProjectSummarizer)_
> 🆔 `3c401d` [4]: Manages project analysis by building a dependency graph, generating module contexts, and summarizing findings based on source code files. _(Source: project_pulse)_
> 🆔 `87264f` [5]: Manages module contexts across refinement cycles, evaluates changes using MapCritic, caches processed states, and tracks processing order. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `db981d` [6]: Analyzes module components, dependencies, and usage to build contextual information, adding alerts for detected errors. _(Source: _create_module_context)_
> 🆔 `117aa7` [7]: Uses `module_contextualizer.py`: Initializes an instance of ModuleContextualizer with parameters path, graph, and dep_contexts.. _(Source: Import module_contextualizer.py)_
> 🆔 `be7b08` [8]: Uses `semantic_gatekeeper.py`: Initializes the SemanticGatekeeper class for content validation and constraint enforcement.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `1552e3` [9]: Uses `report_renderer.py`: Instantiates ReportRenderer with self.contexts and temp_map_path arguments to generate project context reports.. _(Source: Import report_renderer.py)_
> 🆔 `158bda` [10]: Uses `summary_models.py`: Configures the ModuleContext instances from summary_models.py for context management and dependency tracking.; Instantiates ModuleContext objects to represent module context data.. _(Source: Import summary_models.py)_
> 🆔 `379a1f` [11]: Uses `graph_analyzer.py`: Initializes the GraphAnalyzer instance using target_file_path to analyze dependencies and relationships.. _(Source: Import graph_analyzer.py)_
> 🆔 `83c863` [12]: Uses `map_critic.py`: Instantiates the MapCritic class and configures it by passing the gatekeeper argument to its constructor, which is then utilized to analyze project map content for critique-worthy modules.. _(Source: Import map_critic.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes component structures, synthesizes role summaries, and generates module skeletons based on provided method summaries.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes component structures, synthesizes role summaries, and generates module skeletons based on provided method summaries. [2]
- **`🔌 class SkeletonTransformer`**: Transforms Python function, async function, and class definitions into simplified structures. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Manages global variables and functions, analyzes their roles, and synthesizes class role summaries while resolving dependencies. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Analyzes source code structure, transforms function definitions by appending an ellipsis placeholder, processes classes conditionally, and generates a modified AST tree ready for unserialization. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Adds an ellipsis expression to the body of an asynchronous function definition node, modifying its structure by replacing statements with a constant placeholder. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Manages class definitions by removing first statement if it has a docstring, ensuring at least one body element via Pass node. [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Replaces function body with an ellipsis expression. [8]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Enforces technical analysis guidelines and content validation within code evaluation context using methods from SemanticGatekeeper to handle errors, style critiques, and monitor adherence to specified constraints.. [9]
- **`summary_models.py`**: Uses `summary_models.py`: Configures the ModuleContext and Claim data structures from summary_models.py to manage module context metadata, claims, relationships between modules, and supporting claim identifiers for generating grounded text descriptions.; Configures ModuleContext and Claim usage to analyze components, manage alerts, and define public API entries while updating dependency contexts and generating grounded text summaries based on claims.. [10]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c019ef` [1]: Analyzes component structures, synthesizes role summaries, and generates module skeletons based on provided method summaries. _(Source: Synthesis (based on [5], [4], [7], [3], [2], [6], [8]))_
> 🆔 `ca51e1` [2]: Analyzes component structures, synthesizes role summaries, and generates module skeletons based on provided method summaries. _(Source: class ComponentAnalyst)_
> 🆔 `9e043a` [3]: Transforms Python function, async function, and class definitions into simplified structures. _(Source: class SkeletonTransformer)_
> 🆔 `4032dd` [4]: Manages global variables and functions, analyzes their roles, and synthesizes class role summaries while resolving dependencies. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `154e31` [5]: Analyzes source code structure, transforms function definitions by appending an ellipsis placeholder, processes classes conditionally, and generates a modified AST tree ready for unserialization. _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `f419fb` [6]: Adds an ellipsis expression to the body of an asynchronous function definition node, modifying its structure by replacing statements with a constant placeholder. _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `7146da` [7]: Manages class definitions by removing first statement if it has a docstring, ensuring at least one body element via Pass node. _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `feb67f` [8]: Replaces function body with an ellipsis expression. _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `932704` [9]: Uses `semantic_gatekeeper.py`: Enforces technical analysis guidelines and content validation within code evaluation context using methods from SemanticGatekeeper to handle errors, style critiques, and monitor adherence to specified constraints.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `3a2fe5` [10]: Uses `summary_models.py`: Configures the ModuleContext and Claim data structures from summary_models.py to manage module context metadata, claims, relationships between modules, and supporting claim identifiers for generating grounded text descriptions.; Configures ModuleContext and Claim usage to analyze components, manage alerts, and define public API entries while updating dependency contexts and generating grounded text summaries based on claims.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Analyzes module dependencies by parsing import paths, extracting relevant data from upstream contexts, identifying used symbols, generating usage snippets, and creating verification sources for each dependency.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Handles module dependency analysis by parsing import paths, extracting relevant data, identifying used symbols, generating usage snippets, and creating verification sources for each dependency. [2]
- **`🔌 clean_ref`**: Finds bracketed references in text and removes them, returning the cleaned string. [3]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes module dependencies by parsing import paths, extracting relevant data from upstream contexts, identifying used symbols, generating usage snippets, and creating verification sources for each dependency. [4]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Uses `task_executor.py`: Creates an instance of TaskExecutor, initializing it with a SemanticGatekeeper and configuring timeout parameters via TaskExecutor.solve_complex_task.. [5]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper in dependency_analyst.py to enforce technical analysis constraints and perform content validation within code evaluation context.; Initializes a SemanticGatekeeper instance and passes BANNED_ADJECTIVES as part of the constructor arguments to enforce content validation constraints during code evaluation processes.. [6]
- **`summary_models.py`**: Uses `summary_models.py`: Configures Claim objects from summary_models.py to generate grounded text descriptions for claims based on module paths and supporting evidence in dependency_analyst.py.; Instantiates ModuleContext instances to manage module dependencies, add context explanations, generate claims for imports, analyze dependency relationships, register dependent contexts, and update internal state tracking dependencies.. [7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `0f2d5b` [1]: Analyzes module dependencies by parsing import paths, extracting relevant data from upstream contexts, identifying used symbols, generating usage snippets, and creating verification sources for each dependency. _(Source: Synthesis (based on [2], [3], [4]))_
> 🆔 `57407a` [2]: Handles module dependency analysis by parsing import paths, extracting relevant data, identifying used symbols, generating usage snippets, and creating verification sources for each dependency. _(Source: class DependencyAnalyst)_
> 🆔 `cd62ce` [3]: Finds bracketed references in text and removes them, returning the cleaned string. _(Source: clean_ref)_
> 🆔 `e9c6b5` [4]: Analyzes module dependencies by parsing import paths, extracting relevant data from upstream contexts, identifying used symbols, generating usage snippets, and creating verification sources for each dependency. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `2ff387` [5]: Uses `task_executor.py`: Creates an instance of TaskExecutor, initializing it with a SemanticGatekeeper and configuring timeout parameters via TaskExecutor.solve_complex_task.. _(Source: Import task_executor.py)_
> 🆔 `39ab17` [6]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper in dependency_analyst.py to enforce technical analysis constraints and perform content validation within code evaluation context.; Initializes a SemanticGatekeeper instance and passes BANNED_ADJECTIVES as part of the constructor arguments to enforce content validation constraints during code evaluation processes.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `bed631` [7]: Uses `summary_models.py`: Configures Claim objects from summary_models.py to generate grounded text descriptions for claims based on module paths and supporting evidence in dependency_analyst.py.; Instantiates ModuleContext instances to manage module dependencies, add context explanations, generate claims for imports, analyze dependency relationships, register dependent contexts, and update internal state tracking dependencies.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Analyzes project map content to identify critique-worthy modules and extracts instructions for up to three modules.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Analyzes project map content to identify critique-worthy modules and extracts instructions for up to three modules. [2]
- **`🔌 🔌 MapCritic.critique`**: Analyzes project map content to identify critique-worthy modules, extracting instructions for up to three modules. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates an instance of SemanticGatekeeper to enforce technical analysis guidelines and content validation.. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f9abbe` [1]: Analyzes project map content to identify critique-worthy modules and extracts instructions for up to three modules. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `86c7fc` [2]: Analyzes project map content to identify critique-worthy modules and extracts instructions for up to three modules. _(Source: class MapCritic)_
> 🆔 `41b733` [3]: Analyzes project map content to identify critique-worthy modules, extracting instructions for up to three modules. _(Source: 🔌 MapCritic.critique)_
> 🆔 `9800da` [4]: Uses `semantic_gatekeeper.py`: Instantiates an instance of SemanticGatekeeper to enforce technical analysis guidelines and content validation.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` Analyzes module contexts, categorizes them into groups based on archetype attributes, synthesizes summaries for each group, and generates a final system synthesis.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Categorizes module contexts, synthesizes summaries for each group, and generates cohesive system overviews. [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Analyzes module contexts, categorizes them into groups based on archetype attributes, synthesizes summaries for each group, and generates a final system synthesis. [3]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py`: configures the timeout settings and specifies the tiny-h model identifier for language modeling configuration in map_synthesizer.py based on DEFAULT_MODEL from agent_config.py.. [4]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Initializes SemanticGatekeeper with specified gatekeeper parameter and enforces technical analysis guidelines through strict adherence to constraints defined by BANNED_ADJECTIVES and SemanticGatekeeper._critique_content methods.. [5]
- **`llm_util.py`**: Uses `llm_util.py`: Calls the 'run()' method to execute the LLM generation process after formatting the user prompt into the required input structure for the chat_llm function from llm_util.py.. [6]
- **`summary_models.py`**: Uses `summary_models.py`: configures ModuleContext to represent claims, grounded text records, alerts, and module context metadata within summary_models.py for dependency analysis in map_synthesizer.py.. [7]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `091c76` [1]: Analyzes module contexts, categorizes them into groups based on archetype attributes, synthesizes summaries for each group, and generates a final system synthesis. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `b1aa1f` [2]: Categorizes module contexts, synthesizes summaries for each group, and generates cohesive system overviews. _(Source: class MapSynthesizer)_
> 🆔 `acdb0a` [3]: Analyzes module contexts, categorizes them into groups based on archetype attributes, synthesizes summaries for each group, and generates a final system synthesis. _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `ceee97` [4]: Uses `agent_config.py`: configures the timeout settings and specifies the tiny-h model identifier for language modeling configuration in map_synthesizer.py based on DEFAULT_MODEL from agent_config.py.. _(Source: Import agent_config.py)_
> 🆔 `5d017b` [5]: Uses `semantic_gatekeeper.py`: Initializes SemanticGatekeeper with specified gatekeeper parameter and enforces technical analysis guidelines through strict adherence to constraints defined by BANNED_ADJECTIVES and SemanticGatekeeper._critique_content methods.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `170332` [6]: Uses `llm_util.py`: Calls the 'run()' method to execute the LLM generation process after formatting the user prompt into the required input structure for the chat_llm function from llm_util.py.. _(Source: Import llm_util.py)_
> 🆔 `8f6bd2` [7]: Uses `summary_models.py`: configures ModuleContext to represent claims, grounded text records, alerts, and module context metadata within summary_models.py for dependency analysis in map_synthesizer.py.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Manages project context data, renders reports, and handles module documentation.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Manages project context data, renders reports, and handles module documentation. [2]
- **`🔌 replace_ref`**: Searches for references in text, replaces them with numbered identifiers from claim_map. [3]
- **`🔌 sub`**: Maps reference IDs to unique indices, replacing matched references in input text with indexed notations. [4]
- **`🔌 🔌 ReportRenderer.render`**: Generates a project context map report, detailing modules, dependencies, and archetype groups in a structured format. [5]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Configures ModuleContext objects through the _render_module method, managing module dependencies and context relationships for report generation.. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d1aaf9` [1]: Manages project context data, renders reports, and handles module documentation. _(Source: Synthesis (based on [2], [5], [4], [3]))_
> 🆔 `308600` [2]: Manages project context data, renders reports, and handles module documentation. _(Source: class ReportRenderer)_
> 🆔 `8fe851` [3]: Searches for references in text, replaces them with numbered identifiers from claim_map. _(Source: replace_ref)_
> 🆔 `40b8d9` [4]: Maps reference IDs to unique indices, replacing matched references in input text with indexed notations. _(Source: sub)_
> 🆔 `319709` [5]: Generates a project context map report, detailing modules, dependencies, and archetype groups in a structured format. _(Source: 🔌 ReportRenderer.render)_
> 🆔 `a0ee16` [6]: Uses `summary_models.py`: Configures ModuleContext objects through the _render_module method, managing module dependencies and context relationships for report generation.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Manages strict adherence to technical analysis guidelines and content validation within code evaluation context, enforcing constraints defined by BANNED_ADJECTIVES and SemanticGatekeeper._critique_content methods.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines a set of restricted adjectives that cannot be used in certain contexts. [2]
- **`🔌 class SemanticGatekeeper`**: Monitors and enforces strict adherence to technical analysis guidelines within the context of code evaluation and content validation. [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Analyzes input prompt to generate strict JSON output conforming to specified constraints, handling errors and style critiques across multiple attempts. [4]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py`: Configures DEFAULT_MODEL from agent_config.py to initialize the chat_llm function in semantic_gatekeeper.py.. [5]
- **`llm_util.py`**: Uses `llm_util.py`: Calls chat_llm() to process user messages and generate responses for each message in the input list.. [6]

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

> 🆔 `4f6369` [1]: Manages strict adherence to technical analysis guidelines and content validation within code evaluation context, enforcing constraints defined by BANNED_ADJECTIVES and SemanticGatekeeper._critique_content methods. _(Source: Synthesis (based on [4], [2], [3]))_
> 🆔 `1f7d58` [2]: Defines a set of restricted adjectives that cannot be used in certain contexts. _(Source: BANNED_ADJECTIVES)_
> 🆔 `4d9360` [3]: Monitors and enforces strict adherence to technical analysis guidelines within the context of code evaluation and content validation. _(Source: class SemanticGatekeeper)_
> 🆔 `137f5f` [4]: Analyzes input prompt to generate strict JSON output conforming to specified constraints, handling errors and style critiques across multiple attempts. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `c69578` [5]: Uses `agent_config.py`: Configures DEFAULT_MODEL from agent_config.py to initialize the chat_llm function in semantic_gatekeeper.py.. _(Source: Import agent_config.py)_
> 🆔 `c8205b` [6]: Uses `llm_util.py`: Calls chat_llm() to process user messages and generate responses for each message in the input list.. _(Source: Import llm_util.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` Analyzes task requirements, processes context data using SemanticGatekeeper for feedback, and generates actionable insights through TaskExecutor.solve_complex_task method.

**Impact Analysis:** Changes to this module will affect: dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Manages a system for handling tasks, processing responses, and deriving actionable insights. [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Analyzes context data to generate technical sub-questions, verifies evidence through execution prompts, and synthesizes findings into an intent description for the given goal. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper to enforce technical analysis guidelines within task_executor.py.. [4]

### 👥 Used By (Downstream)
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `97c1a8` [1]: Analyzes task requirements, processes context data using SemanticGatekeeper for feedback, and generates actionable insights through TaskExecutor.solve_complex_task method. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `684c97` [2]: Manages a system for handling tasks, processing responses, and deriving actionable insights. _(Source: class TaskExecutor)_
> 🆔 `5b88c1` [3]: Analyzes context data to generate technical sub-questions, verifies evidence through execution prompts, and synthesizes findings into an intent description for the given goal. _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `a4025f` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper to enforce technical analysis guidelines within task_executor.py.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Provides an interface for processing user prompts or messages, formatting them into LLM-compatible structures, and delegating to the Ollama chat API for generation, returning the model's response content.

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Processes user prompt or messages, formats them into an LLM-compatible structure, delegates to Ollama chat API for generation, and returns the model's response content. [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `bcebe1` [1]: Provides an interface for processing user prompts or messages, formatting them into LLM-compatible structures, and delegating to the Ollama chat API for generation, returning the model's response content. _(Source: Synthesis (based on [2]))_
> 🆔 `5fb0bc` [2]: Processes user prompt or messages, formats them into an LLM-compatible structure, delegates to Ollama chat API for generation, and returns the model's response content. _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Defines the systemic role of `graph_analyzer.py` as an entity that analyzes project dependencies and source code for TODO comments, building a graphical representation of relationships.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Analyzes Python code structure, tracks imports, globals, functions, and classes while maintaining traversal context. [2]
- **`🔌 class GraphAnalyzer`**: Analyzes project dependencies and source code for TODO comments, building a graphical representation of relationships. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Manages ClassDef nodes by popping current context and header stack, maintaining state during traversal. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Manages current context stack by popping elements when leaving function definitions. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Updates current statement context after processing SimpleStatementLine node. [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Manages global variable declarations by extracting names, source code, signatures, and privacy flags, adding them to entities['globals'] while filtering private variables starting with '_'. [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Identifies global variables from assignment statements, records their names, source code snippets, signatures indicating they are not private, and categorizes them as globals within the current module context. [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Analyzes function calls, categorizing imports as local or external based on module scope. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Analyzes class definition by extracting source code, docstring, base classes, and initializing class metadata in entities dictionary. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Analyzes function definitions by extracting signatures, docstrings, source code, and metadata, categorizing them as methods or standalone functions within class contexts. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Analyzes imported modules, categorizes them as external or relative imports, and maps import statements to their respective targets for cross-module interaction analysis. [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes imported modules, resolving relative imports within the project context, and maps them to their corresponding file paths. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Registers name usage context during traversal, recording interactions between nodes and current scope while traversing Python code AST. [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Registers the current statement node for further analysis. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds a dependency graph by traversing project files recursively, populates dependent relationships for analysis. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `cd0633` [1]: Defines the systemic role of `graph_analyzer.py` as an entity that analyzes project dependencies and source code for TODO comments, building a graphical representation of relationships. _(Source: Synthesis (based on [11], [3], [2], [7], [5], [13], [6], [14], [8], [16], [12], [4], [15], [10], [9]))_
> 🆔 `28a4c3` [2]: Analyzes Python code structure, tracks imports, globals, functions, and classes while maintaining traversal context. _(Source: class CodeEntityVisitor)_
> 🆔 `261726` [3]: Analyzes project dependencies and source code for TODO comments, building a graphical representation of relationships. _(Source: class GraphAnalyzer)_
> 🆔 `ee8ce6` [4]: Manages ClassDef nodes by popping current context and header stack, maintaining state during traversal. _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `6688b6` [5]: Manages current context stack by popping elements when leaving function definitions. _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `7b580e` [6]: Updates current statement context after processing SimpleStatementLine node. _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `464758` [7]: Manages global variable declarations by extracting names, source code, signatures, and privacy flags, adding them to entities['globals'] while filtering private variables starting with '_'. _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `a00228` [8]: Identifies global variables from assignment statements, records their names, source code snippets, signatures indicating they are not private, and categorizes them as globals within the current module context. _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `fa64a3` [9]: Analyzes function calls, categorizing imports as local or external based on module scope. _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `f9e620` [10]: Analyzes class definition by extracting source code, docstring, base classes, and initializing class metadata in entities dictionary. _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `1c9669` [11]: Analyzes function definitions by extracting signatures, docstrings, source code, and metadata, categorizing them as methods or standalone functions within class contexts. _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `c29885` [12]: Analyzes imported modules, categorizes them as external or relative imports, and maps import statements to their respective targets for cross-module interaction analysis. _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `6727f4` [13]: Analyzes imported modules, resolving relative imports within the project context, and maps them to their corresponding file paths. _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `8cc659` [14]: Registers name usage context during traversal, recording interactions between nodes and current scope while traversing Python code AST. _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `f50652` [15]: Registers the current statement node for further analysis. _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `a2f078` [16]: Builds a dependency graph by traversing project files recursively, populates dependent relationships for analysis. _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Defines interface signature (Abstract)

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Manages memory storage and retrieval within Chroma database, facilitating persistent text embedding associations. [2]
- **`🔌 class MemoryInterface`**: Provides abstract memory query capabilities for external systems. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Creates a unique memory ID, combines turn and helpfulness metadata, updates it with provided metadata if present, then stores the text, embedding, ID, and combined metadata in ChromaDB collection. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Deletes old memory entries from ChromaDB collection based on helpfulness score or recency, purging those below threshold to maintain relevance. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Queries the Chroma database for relevant memory entries based on input query, retrieves associated metadata including document content and timestamps each used entry by updating its last_used_turn attribute. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Updates the helpfulness metadata for a given memory by retrieving current metadata, modifying its helpfulness field, and persisting the changes to the ChromaDB collection. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `96aed9` [1]: Defines interface signature (Abstract) _(Source: Synthesis (based on [3], [4], [2], [7], [8], [6], [5]))_
> 🆔 `4dd1b8` [2]: Manages memory storage and retrieval within Chroma database, facilitating persistent text embedding associations. _(Source: class ChromaMemory)_
> 🆔 `2ff6df` [3]: Provides abstract memory query capabilities for external systems. _(Source: class MemoryInterface)_
> 🆔 `33b9a9` [4]: Creates a unique memory ID, combines turn and helpfulness metadata, updates it with provided metadata if present, then stores the text, embedding, ID, and combined metadata in ChromaDB collection. _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `e27125` [5]: Deletes old memory entries from ChromaDB collection based on helpfulness score or recency, purging those below threshold to maintain relevance. _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `baf251` [6]: Queries the Chroma database for relevant memory entries based on input query, retrieves associated metadata including document content and timestamps each used entry by updating its last_used_turn attribute. _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `899b8a` [7]: Updates the helpfulness metadata for a given memory by retrieving current metadata, modifying its helpfulness field, and persisting the changes to the ChromaDB collection. _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Defines ModuleArchetype records and encapsulates module classification logic to categorize architectural types based on provided attributes.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Analyzes module characteristics to categorize its architectural type based on provided attributes. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Determines module archetype based on name, entities, dependencies, source code, and classes/methods. [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `3f806a` [1]: Defines ModuleArchetype records and encapsulates module classification logic to categorize architectural types based on provided attributes. _(Source: Synthesis (based on [4], [3], [2]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `733c7f` [3]: Analyzes module characteristics to categorize its architectural type based on provided attributes. _(Source: class ModuleClassifier)_
> 🆔 `0c019d` [4]: Determines module archetype based on name, entities, dependencies, source code, and classes/methods. _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Defines a data structure for analyzing module context, contextualizing components, and synthesizing systemic roles based on dependencies and usage patterns.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Analyzes module context, contextualizes components, and synthesizes systemic roles based on dependencies and usage patterns. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyzes components, dependencies, and usage to build contextual module information, adding alerts if errors are detected. [3]

### 🔗 Uses (Upstream)
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst using gatekeeper and task_executor parameters.. [4]
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates TaskExecutor using gatekeeper feedback for contextual analysis and task execution.. [5]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper to enforce strict technical analysis guidelines and content validation within code evaluation context, handling errors and style critiques across multiple attempts while monitoring adherence to defined constraints.. [6]
- **`module_classifier.py`**: Uses `module_classifier.py`: Instantiates ModuleClassifier in _pass_systemic_synthesis to categorize modules based on module_name and data attributes, invoking module_classifier.py logic to determine archetype.; Determines module archetype based on name, entities, dependencies, source code, and classes/methods to categorize its architectural type using ModuleClassifier's Logic/Capabilities.. [7]
- **`summary_models.py`**: Uses `summary_models.py`: Initializes and configures ModuleContextualizer's internal state by setting up a ModuleContext instance using parameters from summary_models.py, enabling module context mapping functionality.; Instantiates and configures ModuleContext with file_path, graph_data, and dep_contexts attributes.. [8]
- **`component_analyst.py`**: Uses `component_analyst.py`: Instantiates the `ComponentAnalyst` class using `self.comp_analyst = ComponentAnalyst(self.gatekeeper)` in `module_contextualizer.py`.; Instantiates the `ComponentAnalyst` class using `self.gatekeeper` as an argument to enable module contextualization functionality.. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `3eb6d9` [1]: Defines a data structure for analyzing module context, contextualizing components, and synthesizing systemic roles based on dependencies and usage patterns. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `4b5cd5` [2]: Analyzes module context, contextualizes components, and synthesizes systemic roles based on dependencies and usage patterns. _(Source: class ModuleContextualizer)_
> 🆔 `f45b01` [3]: Analyzes components, dependencies, and usage to build contextual module information, adding alerts if errors are detected. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `81915d` [4]: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst using gatekeeper and task_executor parameters.. _(Source: Import dependency_analyst.py)_
> 🆔 `360a70` [5]: Uses `task_executor.py`: Instantiates TaskExecutor using gatekeeper feedback for contextual analysis and task execution.. _(Source: Import task_executor.py)_
> 🆔 `f41d0a` [6]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper to enforce strict technical analysis guidelines and content validation within code evaluation context, handling errors and style critiques across multiple attempts while monitoring adherence to defined constraints.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `3374fc` [7]: Uses `module_classifier.py`: Instantiates ModuleClassifier in _pass_systemic_synthesis to categorize modules based on module_name and data attributes, invoking module_classifier.py logic to determine archetype.; Determines module archetype based on name, entities, dependencies, source code, and classes/methods to categorize its architectural type using ModuleClassifier's Logic/Capabilities.. _(Source: Import module_classifier.py)_
> 🆔 `d41e09` [8]: Uses `summary_models.py`: Initializes and configures ModuleContextualizer's internal state by setting up a ModuleContext instance using parameters from summary_models.py, enabling module context mapping functionality.; Instantiates and configures ModuleContext with file_path, graph_data, and dep_contexts attributes.. _(Source: Import summary_models.py)_
> 🆔 `6c55fc` [9]: Uses `component_analyst.py`: Instantiates the `ComponentAnalyst` class using `self.comp_analyst = ComponentAnalyst(self.gatekeeper)` in `module_contextualizer.py`.; Instantiates the `ComponentAnalyst` class using `self.gatekeeper` as an argument to enable module contextualization functionality.. _(Source: Import component_analyst.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Defines and encapsulates the data structures for the Module Context Map, providing classes to represent claims, grounded text records, alerts, and module context metadata to capture relationships between modules and their dependencies.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Handles claims by generating unique identifiers for reference, text, and source module combinations. [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Owning module metadata, managing context data, and facilitating relationships between modules and dependencies. [5]
- **`🔌 🔌 Claim.id`**: Generates a SHA-1 hash based on text, reference, and source module, returning the hashed value. [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds an alert to the list of alerts, mutating the state by appending to self.alerts. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Associates module paths with dependency explanations and supporting claim identifiers, updating internal state to track dependencies. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Registers dependent contexts by adding grounded text explanations linked to supporting claims, updating key_dependents dictionary. [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds a public API entry by creating a grounded text description using supporting claims and storing it in the module's context. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Adds supporting claims to the module role text by adding placeholders, generates full text, and assigns it as grounded text with associated claim IDs. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `de1a41` [1]: Defines and encapsulates the data structures for the Module Context Map, providing classes to represent claims, grounded text records, alerts, and module context metadata to capture relationships between modules and their dependencies. _(Source: Synthesis (based on [8], [6], [9], [4], [5], [2], [10], [11], [7], [3]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `f86ab8` [3]: Handles claims by generating unique identifiers for reference, text, and source module combinations. _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `b7adab` [5]: Owning module metadata, managing context data, and facilitating relationships between modules and dependencies. _(Source: class ModuleContext)_
> 🆔 `9271ea` [6]: Generates a SHA-1 hash based on text, reference, and source module, returning the hashed value. _(Source: 🔌 Claim.id)_
> 🆔 `e5dbdb` [7]: Adds an alert to the list of alerts, mutating the state by appending to self.alerts. _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `6fead9` [8]: Associates module paths with dependency explanations and supporting claim identifiers, updating internal state to track dependencies. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `b732dc` [9]: Registers dependent contexts by adding grounded text explanations linked to supporting claims, updating key_dependents dictionary. _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `cef779` [10]: Adds a public API entry by creating a grounded text description using supporting claims and storing it in the module's context. _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `d0806b` [11]: Adds supporting claims to the module role text by adding placeholders, generates full text, and assigns it as grounded text with associated claim IDs. _(Source: 🔌 ModuleContext.set_module_role)_
</details>

---
## 🔧 Configuration

## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Assigns a maximum context length limit for text processing operations. [2]
- **`🔌 DEFAULT_MODEL`**: Assigns tiny-h model identifier to specified variable, managing default language modeling configuration. [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `449512` [1]: Defines configuration constants. _(Source: Archetype)_
> 🆔 `411fc0` [2]: Assigns a maximum context length limit for text processing operations. _(Source: CONTEXT_LIMIT)_
> 🆔 `a99509` [3]: Assigns tiny-h model identifier to specified variable, managing default language modeling configuration. _(Source: DEFAULT_MODEL)_
</details>

---