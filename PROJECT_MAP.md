# Project Context Map

## 🏛️ System Architecture
The system's foundation is established by the Configuration layer which defines constants used by agent_core.py and semantic_gatekeeper.py, dictating their behavior. This configuration data serves as the basis for all subsequent operations within the system. The Data Model Layer owns memory management within a persistent Chroma database, including adding memories with metadata, querying via text embeddings, updating helpfulness, and cleaning up unused entries. This data structure is then utilized by agent_core.py to interact with the system's core functionalities.

---

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates parsing of command-line arguments to define goal and target folder, searches for _main.py file in the target folder, initializes CrawlerAgent with the specified goal and path, runs the agent's run method, and returns a completion message. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: args = parser.parse_args() [2]
- **`🔌 goal`**: goal is assigned the value of args.goal [3]
- **`🔌 main`**: The main function searches the target folder for a file ending in _main.py, creates an instance of CrawlerAgent with the goal and path to that file, runs the agent's run method, and returns a completion message. [4]
- **`🔌 parser`**: A variable named `parser` is assigned an instance of the argparse.ArgumentParser class, which is used for parsing command-line arguments in Python scripts. [5]
- **`🔌 result`**: Assigns the return value of main(goal, target_folder) to result. [6]
- **`🔌 target_folder`**: The variable target_folder is assigned the literal value from args.target_folder argument. [7]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Instantiates CrawlerAgent from agent_core. [8]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8b7ff5` [1]: Orchestrates parsing of command-line arguments to define goal and target folder, searches for _main.py file in the target folder, initializes CrawlerAgent with the specified goal and path, runs the agent's run method, and returns a completion message. _(Source: Synthesis (based on [6], [7], [5], [4], [2], [3]))_
> 🆔 `b90b26` [2]: args = parser.parse_args() _(Source: args)_
> 🆔 `d89c62` [3]: goal is assigned the value of args.goal _(Source: goal)_
> 🆔 `95f9a8` [4]: The main function searches the target folder for a file ending in _main.py, creates an instance of CrawlerAgent with the goal and path to that file, runs the agent's run method, and returns a completion message. _(Source: main)_
> 🆔 `65ab4d` [5]: A variable named `parser` is assigned an instance of the argparse.ArgumentParser class, which is used for parsing command-line arguments in Python scripts. _(Source: parser)_
> 🆔 `24ea89` [6]: Assigns the return value of main(goal, target_folder) to result. _(Source: result)_
> 🆔 `2facfb` [7]: The variable target_folder is assigned the literal value from args.target_folder argument. _(Source: target_folder)_
> 🆔 `df49c7` [8]: Uses `agent_core.py`: Instantiates CrawlerAgent from agent_core. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` The Agent Core coordinates and orchestrates task execution, service interaction, and workflow management within the application framework, ensuring proper communication and functionality across various components.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: CrawlerAgent is responsible for initializing with a goal and target root, setting up memory with ChromaMemory, running the crawler to retrieve project map and processing order, synthesizing system summary using semantic gatekeeper and synthesizer, rendering report renderer, cleaning up memories after 5 turns, and returning analysis complete response. [2]
- **`🔌 🔌 CrawlerAgent.run`**: The method runs a crawler agent, retrieves a project map and processing order from the target root, synthesizes system summary using a semantic gatekeeper and synthesizer, renders a report renderer, cleans up memories for 5 turns, and returns an analysis complete response. [3]

### 🔗 Uses (Upstream)
- **`memory_core.py`**: Uses `memory_core.py`: Instantiates ChromaMemory class from memory_core module.. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Calls class from summary_models module.. [5]
- **`agent_util.py`**: Uses `agent_util.py`: Calls project_pulse from agent_util.py.. [6]
- **`llm_util.py`**: Uses `llm_util.py`: Calls chat_llm from llm_util.. [7]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates ReportRenderer class. [8]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class. [9]
- **`agent_config.py`**: Uses `agent_config.py`: Imports DEFAULT_MODEL, CONTEXT_LIMIT from agent_config. [10]
- **`map_synthesizer.py`**: Uses `map_synthesizer.py`: Instantiates MapSynthesizer from .map_synthesizer. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ecc5a9` [1]: The Agent Core coordinates and orchestrates task execution, service interaction, and workflow management within the application framework, ensuring proper communication and functionality across various components. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `7f59af` [2]: CrawlerAgent is responsible for initializing with a goal and target root, setting up memory with ChromaMemory, running the crawler to retrieve project map and processing order, synthesizing system summary using semantic gatekeeper and synthesizer, rendering report renderer, cleaning up memories after 5 turns, and returning analysis complete response. _(Source: class CrawlerAgent)_
> 🆔 `fc9cf6` [3]: The method runs a crawler agent, retrieves a project map and processing order from the target root, synthesizes system summary using a semantic gatekeeper and synthesizer, renders a report renderer, cleans up memories for 5 turns, and returns an analysis complete response. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `dd0997` [4]: Uses `memory_core.py`: Instantiates ChromaMemory class from memory_core module.. _(Source: Import memory_core.py)_
> 🆔 `03b06c` [5]: Uses `summary_models.py`: Calls class from summary_models module.. _(Source: Import summary_models.py)_
> 🆔 `7cc64a` [6]: Uses `agent_util.py`: Calls project_pulse from agent_util.py.. _(Source: Import agent_util.py)_
> 🆔 `fe4a53` [7]: Uses `llm_util.py`: Calls chat_llm from llm_util.. _(Source: Import llm_util.py)_
> 🆔 `635521` [8]: Uses `report_renderer.py`: Instantiates ReportRenderer class. _(Source: Import report_renderer.py)_
> 🆔 `9e3e59` [9]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `11bf4e` [10]: Uses `agent_config.py`: Imports DEFAULT_MODEL, CONTEXT_LIMIT from agent_config. _(Source: Import agent_config.py)_
> 🆔 `f32c05` [11]: Uses `map_synthesizer.py`: Instantiates MapSynthesizer from .map_synthesizer. _(Source: Import map_synthesizer.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Manages orchestration of module contexts for AI agents, coordinating dependencies and generating structured summaries to inform decision-making and enable task execution.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: A dictionary is assigned to ProjectGraph, containing key-value pairs of type str and Any. [2]
- **`🔌 class ProjectSummarizer`**: The ProjectSummarizer class initializes an instance, setting attributes for the project graph and maximum cycles, creating an empty contexts dictionary, and computing a processing order based on module dependencies. It provides methods to compute topological orders of modules in the graph and generate context information for each cycle. [3]
- **`🔌 project_pulse`**: The `project_pulse` function performs project analysis starting from the specified target file path. It checks if the target path is a valid file, logs the start of analysis, creates an instance of `GraphAnalyzer` to analyze the project graph, generates summaries using the analyzed graph with `ProjectSummarizer`, and returns the generated contexts and processing order. [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: The generate_contexts method iterates through cycles to create module contexts, applying critiques from MapCritic if available. It compares current and old contexts, updating only when different. The method returns the final contexts dictionary and processing order list. [5]
- **`🔒 _create_module_context`**: The function `_create_module_context` takes a module path, project graph, existing dependency contexts, and an optional critique instruction as input. It logs the generation of context for the specified module. It creates an instance of `ModuleContextualizer`, passing in the module path, project graph, and dependency contexts. It then calls the `contextualize_module` method on the contextualizer with the critique instruction to generate a new context object. If the generated context has no `file_path`, it sets it to the input module path. Finally, it logs the generation of the context for the module and returns the resulting context. [6]

### 🔗 Uses (Upstream)
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: Instantiates ModuleContextualizer from .module_contextualizer with path, graph, dep_contexts.. [7]
- **`map_critic.py`**: Uses `map_critic.py`: Instantiates MapCritic class with gatekeeper argument.. [8]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext from summary_models. [9]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates ReportRenderer class.. [10]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. [11]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer class for target file.. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `76db0d` [1]: Manages orchestration of module contexts for AI agents, coordinating dependencies and generating structured summaries to inform decision-making and enable task execution. _(Source: Synthesis (based on [6], [3], [4], [5], [2]))_
> 🆔 `86bb9f` [2]: A dictionary is assigned to ProjectGraph, containing key-value pairs of type str and Any. _(Source: ProjectGraph)_
> 🆔 `12e679` [3]: The ProjectSummarizer class initializes an instance, setting attributes for the project graph and maximum cycles, creating an empty contexts dictionary, and computing a processing order based on module dependencies. It provides methods to compute topological orders of modules in the graph and generate context information for each cycle. _(Source: class ProjectSummarizer)_
> 🆔 `1d1d93` [4]: The `project_pulse` function performs project analysis starting from the specified target file path. It checks if the target path is a valid file, logs the start of analysis, creates an instance of `GraphAnalyzer` to analyze the project graph, generates summaries using the analyzed graph with `ProjectSummarizer`, and returns the generated contexts and processing order. _(Source: project_pulse)_
> 🆔 `693f03` [5]: The generate_contexts method iterates through cycles to create module contexts, applying critiques from MapCritic if available. It compares current and old contexts, updating only when different. The method returns the final contexts dictionary and processing order list. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `10b9e6` [6]: The function `_create_module_context` takes a module path, project graph, existing dependency contexts, and an optional critique instruction as input. It logs the generation of context for the specified module. It creates an instance of `ModuleContextualizer`, passing in the module path, project graph, and dependency contexts. It then calls the `contextualize_module` method on the contextualizer with the critique instruction to generate a new context object. If the generated context has no `file_path`, it sets it to the input module path. Finally, it logs the generation of the context for the module and returns the resulting context. _(Source: _create_module_context)_
> 🆔 `347203` [7]: Uses `module_contextualizer.py`: Instantiates ModuleContextualizer from .module_contextualizer with path, graph, dep_contexts.. _(Source: Import module_contextualizer.py)_
> 🆔 `a48153` [8]: Uses `map_critic.py`: Instantiates MapCritic class with gatekeeper argument.. _(Source: Import map_critic.py)_
> 🆔 `8f13a7` [9]: Uses `summary_models.py`: Instantiates ModuleContext from summary_models. _(Source: Import summary_models.py)_
> 🆔 `390950` [10]: Uses `report_renderer.py`: Instantiates ReportRenderer class.. _(Source: Import report_renderer.py)_
> 🆔 `f9ff16` [11]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `5b82fb` [12]: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer class for target file.. _(Source: Import graph_analyzer.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Component Analyst coordinates the analysis of modules, extracting their purpose and mechanism through automated code parsing and natural language processing techniques without performing any direct computation or transformation.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: ComponentAnalyst is a class designed to analyze components, generate module skeletons, and synthesize the roles of specified classes based on provided source code. [2]
- **`🔌 class SkeletonTransformer`**: The SkeletonTransformer class is designed to remove docstrings from AST nodes, specifically FunctionDef, AsyncFunctionDef, and ClassDef nodes, by checking for an Expr child node containing a Constant string value and removing it. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Describes this method without executing any logic due to the presence of abstract signature or insufficient code implementation. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: The method parses the provided source code string, applies a SkeletonTransformer to generate a new AST, and returns the unparsed code as a string. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: The method visit_AsyncFunctionDef removes any docstring from the given AsyncFunctionDef node and then recursively visits its children nodes. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: The method visit_ClassDef processes a class definition node, removes any docstring from it, adds an empty body if the body is currently empty by replacing it with [ast.Pass()], and then recursively visits other nodes. [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: The method removes any docstring from the given FunctionDef node and then recursively visits its children nodes. [8]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Calls add_public_api_entry to add API entry for class summary.. [9]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class in semantic_gatekeeper.py. [10]
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates TaskExecutor class.. [11]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `99dd00` [1]: Component Analyst coordinates the analysis of modules, extracting their purpose and mechanism through automated code parsing and natural language processing techniques without performing any direct computation or transformation. _(Source: Synthesis (based on [8], [4], [7], [5], [3], [2], [6]))_
> 🆔 `f10676` [2]: ComponentAnalyst is a class designed to analyze components, generate module skeletons, and synthesize the roles of specified classes based on provided source code. _(Source: class ComponentAnalyst)_
> 🆔 `d5ca88` [3]: The SkeletonTransformer class is designed to remove docstrings from AST nodes, specifically FunctionDef, AsyncFunctionDef, and ClassDef nodes, by checking for an Expr child node containing a Constant string value and removing it. _(Source: class SkeletonTransformer)_
> 🆔 `3089ec` [4]: Describes this method without executing any logic due to the presence of abstract signature or insufficient code implementation. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `5e3047` [5]: The method parses the provided source code string, applies a SkeletonTransformer to generate a new AST, and returns the unparsed code as a string. _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `f859a6` [6]: The method visit_AsyncFunctionDef removes any docstring from the given AsyncFunctionDef node and then recursively visits its children nodes. _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `545811` [7]: The method visit_ClassDef processes a class definition node, removes any docstring from it, adds an empty body if the body is currently empty by replacing it with [ast.Pass()], and then recursively visits other nodes. _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `25419b` [8]: The method removes any docstring from the given FunctionDef node and then recursively visits its children nodes. _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `afba2e` [9]: Uses `summary_models.py`: Calls add_public_api_entry to add API entry for class summary.. _(Source: Import summary_models.py)_
> 🆔 `cfd2a8` [10]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class in semantic_gatekeeper.py. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `55cc1f` [11]: Uses `task_executor.py`: Instantiates TaskExecutor class.. _(Source: Import task_executor.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Dependency Analyst manages and analyzes code dependencies, coordinating the orchestration of module interactions without performing any actions itself.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: The DependencyAnalyst class is responsible for analyzing dependencies by iterating over provided dependencies, fetching upstream context if available, and determining usage based on interactions. It constructs explanations for imports or uses of each dependency, including relevant upstream context, usage snippets, and intent-based descriptions. [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: The method analyzes dependencies by iterating over the provided dependencies, fetching upstream context if available, and determining usage based on interactions. It constructs explanations for imports or uses of each dependency, including relevant upstream context, usage snippets, and intent-based descriptions. [3]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates TaskExecutor in __init__.. [4]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class. [5]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext and Claim classes in summary_models.py. [6]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `e60313` [1]: Dependency Analyst manages and analyzes code dependencies, coordinating the orchestration of module interactions without performing any actions itself. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `05624a` [2]: The DependencyAnalyst class is responsible for analyzing dependencies by iterating over provided dependencies, fetching upstream context if available, and determining usage based on interactions. It constructs explanations for imports or uses of each dependency, including relevant upstream context, usage snippets, and intent-based descriptions. _(Source: class DependencyAnalyst)_
> 🆔 `5d8eda` [3]: The method analyzes dependencies by iterating over the provided dependencies, fetching upstream context if available, and determining usage based on interactions. It constructs explanations for imports or uses of each dependency, including relevant upstream context, usage snippets, and intent-based descriptions. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `fb5450` [4]: Uses `task_executor.py`: Instantiates TaskExecutor in __init__.. _(Source: Import task_executor.py)_
> 🆔 `844f2d` [5]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `6c6b87` [6]: Uses `summary_models.py`: Instantiates ModuleContext and Claim classes in summary_models.py. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` The Map Critic module actively analyzes project map content to identify specific flaws in module documentation based on defined criteria and provides detailed feedback for improvement.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: The MapCritic class initializes an instance by setting the gatekeeper attribute to a provided SemanticGatekeeper object, critiques project map content into modules and analyzes each module for specific flaws, parses content into modules based on headers, and analyzes documentation for individual modules. [2]
- **`🔌 🔌 MapCritic.critique`**: The method critiques a project map content, parsing it into modules and analyzing each module to generate critiques. It stops after finding three critiques. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ba507a` [1]: The Map Critic module actively analyzes project map content to identify specific flaws in module documentation based on defined criteria and provides detailed feedback for improvement. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `fdee87` [2]: The MapCritic class initializes an instance by setting the gatekeeper attribute to a provided SemanticGatekeeper object, critiques project map content into modules and analyzes each module for specific flaws, parses content into modules based on headers, and analyzes documentation for individual modules. _(Source: class MapCritic)_
> 🆔 `a16008` [3]: The method critiques a project map content, parsing it into modules and analyzing each module to generate critiques. It stops after finding three critiques. _(Source: 🔌 MapCritic.critique)_
> 🆔 `075c2b` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` The Map Synthesizer analyzes modules and their dependencies to generate system architecture narratives, synthesizing functional summaries for each layer based on archetype attributes.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: MapSynthesizer is a class that synthesizes system architecture by categorizing modules into groups based on archetype attributes and generating summaries for each group, ultimately constructing a narrative describing data flow and control through the system. [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: The method takes in contexts and processing order, categorizes modules into groups based on their archetype attributes, synthesizes each group using the _synthesize_group method, and then synthesizes the entire system from these summaries. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Calls synthesize on summary_models ModuleContext. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `5c0500` [1]: The Map Synthesizer analyzes modules and their dependencies to generate system architecture narratives, synthesizing functional summaries for each layer based on archetype attributes. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `4728bd` [2]: MapSynthesizer is a class that synthesizes system architecture by categorizing modules into groups based on archetype attributes and generating summaries for each group, ultimately constructing a narrative describing data flow and control through the system. _(Source: class MapSynthesizer)_
> 🆔 `9846a8` [3]: The method takes in contexts and processing order, categorizes modules into groups based on their archetype attributes, synthesizes each group using the _synthesize_group method, and then synthesizes the entire system from these summaries. _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `d4ddd1` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `936c11` [5]: Uses `summary_models.py`: Calls synthesize on summary_models ModuleContext. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Defines a service that orchestrates the generation of markdown reports detailing system architecture, module roles, dependencies, and verification claims based on provided context data.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: The ReportRenderer class is responsible for rendering project context reports in markdown format, including system summary, module details, dependencies, and verification claims based on provided data. [2]
- **`🔌 🔌 ReportRenderer.render`**: The render method generates a markdown report of the project context map, including system summary, total modules, module dependencies, and categorized paths based on their archetype. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext class from summary_models module. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `6040a3` [1]: Defines a service that orchestrates the generation of markdown reports detailing system architecture, module roles, dependencies, and verification claims based on provided context data. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `be1843` [2]: The ReportRenderer class is responsible for rendering project context reports in markdown format, including system summary, module details, dependencies, and verification claims based on provided data. _(Source: class ReportRenderer)_
> 🆔 `74e79b` [3]: The render method generates a markdown report of the project context map, including system summary, total modules, module dependencies, and categorized paths based on their archetype. _(Source: 🔌 ReportRenderer.render)_
> 🆔 `93fbef` [4]: Uses `summary_models.py`: Instantiates ModuleContext class from summary_models module. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Manages coordinating the analysis and orchestration of system processes, ensuring integration and active execution without embellishments.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines global constant `BANNED_ADJECTIVES`. [2]
- **`🔌 class SemanticGatekeeper`**: Class SemanticGatekeeper provides methods to execute prompts, verify grounding of claims against source code, critique content for banned terms and minimum word count, extract balanced JSON substrings, and safely parse JSON data while handling various parsing errors and edge cases. [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: The method execute_with_feedback takes several parameters including initial_prompt, json_key, forbidden_terms, verification_source, log_context, expect_json, and min_words. It sets the final_prompt based on whether expect_json is True or False. If expect_json is True, it appends an important note to the prompt instructing the output should be valid JSON with a specific key. It then sends messages to a chat LLM (chat_llm) function with the system and user roles and content. It attempts to parse the raw response as JSON using _parse_json_safe, with up to MAX_RETRIES (3) attempts. If parsing fails or if there are style issues or grounding issues (verified by _verify_grounding), it logs warnings, appends feedback messages to the assistant role in messages, and prompts the user to rewrite the output. Finally, it returns the cleaned value which should be valid JSON. [4]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Uses `llm_util.py`: Instantiates class from .llm_util for chat functionality. [5]
- **`agent_config.py`**: Uses `agent_config.py`: Imports DEFAULT_MODEL from agent_config for use in chat_llm.. [6]

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

> 🆔 `0b3c7f` [1]: Manages coordinating the analysis and orchestration of system processes, ensuring integration and active execution without embellishments. _(Source: Synthesis (based on [2], [3], [4]))_
> 🆔 `4d3df2` [2]: Defines global constant `BANNED_ADJECTIVES`. _(Source: BANNED_ADJECTIVES)_
> 🆔 `5db263` [3]: Class SemanticGatekeeper provides methods to execute prompts, verify grounding of claims against source code, critique content for banned terms and minimum word count, extract balanced JSON substrings, and safely parse JSON data while handling various parsing errors and edge cases. _(Source: class SemanticGatekeeper)_
> 🆔 `cd2097` [4]: The method execute_with_feedback takes several parameters including initial_prompt, json_key, forbidden_terms, verification_source, log_context, expect_json, and min_words. It sets the final_prompt based on whether expect_json is True or False. If expect_json is True, it appends an important note to the prompt instructing the output should be valid JSON with a specific key. It then sends messages to a chat LLM (chat_llm) function with the system and user roles and content. It attempts to parse the raw response as JSON using _parse_json_safe, with up to MAX_RETRIES (3) attempts. If parsing fails or if there are style issues or grounding issues (verified by _verify_grounding), it logs warnings, appends feedback messages to the assistant role in messages, and prompts the user to rewrite the output. Finally, it returns the cleaned value which should be valid JSON. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `25b651` [5]: Uses `llm_util.py`: Instantiates class from .llm_util for chat functionality. _(Source: Import llm_util.py)_
> 🆔 `e8188f` [6]: Uses `agent_config.py`: Imports DEFAULT_MODEL from agent_config for use in chat_llm.. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` The execution of complex tasks by coordinating multiple components and services, ensuring integration and operation within an active system.

**Impact Analysis:** Changes to this module will affect: component_analyst.py, dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: The TaskExecutor class initializes an instance with a SemanticGatekeeper object and sets max_retries to 3. It provides methods to clean and parse responses, unwrap text recursively for specific keys or join dictionary values, and solve complex tasks with logging and error handling. [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Describes how the solve_complex_task method in the TaskExecutor class handles starting and running a task, logging its progress, and returning results or error messages. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class. [4]

### 👥 Used By (Downstream)
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1871a3` [1]: The execution of complex tasks by coordinating multiple components and services, ensuring integration and operation within an active system. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `46bede` [2]: The TaskExecutor class initializes an instance with a SemanticGatekeeper object and sets max_retries to 3. It provides methods to clean and parse responses, unwrap text recursively for specific keys or join dictionary values, and solve complex tasks with logging and error handling. _(Source: class TaskExecutor)_
> 🆔 `6c8266` [3]: Describes how the solve_complex_task method in the TaskExecutor class handles starting and running a task, logging its progress, and returning results or error messages. _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `7aebe5` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Defines a utility function that formats prompts or messages and uses an external LLM API to generate responses, stripping whitespace from the output.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: The chat_llm function takes a model string and either a prompt string or list of message dictionaries, formats them into messages, calls the ollama.chat method to generate a response, extracts the content from the response, strips whitespace, and returns it. [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `76ee70` [1]: Defines a utility function that formats prompts or messages and uses an external LLM API to generate responses, stripping whitespace from the output. _(Source: Synthesis (based on [2]))_
> 🆔 `f5779d` [2]: The chat_llm function takes a model string and either a prompt string or list of message dictionaries, formats them into messages, calls the ollama.chat method to generate a response, extracts the content from the response, strips whitespace, and returns it. _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Defines and orchestrates the analysis of Python code structure by building a detailed dependency graph that includes modules, dependencies, interactions between components, external imports, and any TODO comments found within the files.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: The CodeEntityVisitor class is responsible for analyzing and extracting various code entities such as functions, classes, global variables, imports, and cross-module interactions from the given Python code using Abstract Syntax Tree (AST) parsing. [2]
- **`🔌 class GraphAnalyzer`**: The GraphAnalyzer class is responsible for analyzing the structure of Python code in a specified project directory, building a dependency graph that includes modules, dependencies, interactions between components, external imports, and any TODO comments found within the files. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: The leave_ClassDef method is called when leaving a class definition node in the AST (Abstract Syntax Tree). It removes the current context and header stack from the CodeEntityVisitor instance. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: The leave_FunctionDef method is called when leaving a FunctionDef node in the code analysis process. It pops the current context and header stack, indicating that the function definition has ended. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: The leave_SimpleStatementLine method is called when leaving a SimpleStatementLine node in the CST (Concrete Syntax Tree). It sets the current_statement attribute to None, indicating that no specific statement is currently being processed. [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: The visit_AnnAssign method processes annotated assignment nodes in Python code. It checks if there is a current context, then verifies the target is a name. If so, it retrieves the name and source code for the annotation node. The method appends an entity to the globals list containing the name, source code, inferred signature based on the annotation, and whether the name starts with an underscore indicating privacy. [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: The method visit_Assign handles assignment nodes in the code, appending details of global variables to the entities list if the current context is empty. It retrieves the target name and source code for each assignment, creates a signature string, and marks names starting with an underscore as private. [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: The method visit_Call handles call expressions in the abstract syntax tree (AST) and records interactions between nodes based on whether the function being called is a simple name or not. It specifically records interactions for names using the _record_interaction method. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: The method `visit_ClassDef` is called when encountering a class definition in the Abstract Syntax Tree (AST). It processes the class node by appending its name to the current context, retrieves the source code of the class, docstring, and bases (inheritance) if any, constructs a header string for the class definition, stores the class details in the entities dictionary under 'classes', pushes the class header onto the header stack, and initializes an empty list for methods. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Describes the `visit_FunctionDef` method in `CodeEntityVisitor`, which visits a function definition node, extracts signature, docstring, body, and other metadata, determines if it's private or unimplemented, and adds it to either functions or class methods. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: The visit_Import method processes an import node, extracting the module name for each alias and adding it to the external_imports set. [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: The method visit_ImportFrom processes an import statement from another module, determining if it is relative or external, and populates the relative_imports set and import_map dictionary accordingly. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: The method visit_Name records interactions between the context and the name value if they are not already in the current context. It skips recording if there is an interaction already. [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: The method visit_SimpleStatementLine is called when parsing a SimpleStatementLine node in the code. It sets the current_statement attribute to the provided node. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: The `analyze` method builds the dependency graph by recursively traversing the project structure, populates dependents for each node, and returns the constructed graph as a dictionary. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `680273` [1]: Defines and orchestrates the analysis of Python code structure by building a detailed dependency graph that includes modules, dependencies, interactions between components, external imports, and any TODO comments found within the files. _(Source: Synthesis (based on [13], [4], [5], [10], [8], [7], [15], [9], [14], [6], [3], [11], [16], [12], [2]))_
> 🆔 `f971d4` [2]: The CodeEntityVisitor class is responsible for analyzing and extracting various code entities such as functions, classes, global variables, imports, and cross-module interactions from the given Python code using Abstract Syntax Tree (AST) parsing. _(Source: class CodeEntityVisitor)_
> 🆔 `9dc31e` [3]: The GraphAnalyzer class is responsible for analyzing the structure of Python code in a specified project directory, building a dependency graph that includes modules, dependencies, interactions between components, external imports, and any TODO comments found within the files. _(Source: class GraphAnalyzer)_
> 🆔 `13a150` [4]: The leave_ClassDef method is called when leaving a class definition node in the AST (Abstract Syntax Tree). It removes the current context and header stack from the CodeEntityVisitor instance. _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `145b6c` [5]: The leave_FunctionDef method is called when leaving a FunctionDef node in the code analysis process. It pops the current context and header stack, indicating that the function definition has ended. _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `9c6cd0` [6]: The leave_SimpleStatementLine method is called when leaving a SimpleStatementLine node in the CST (Concrete Syntax Tree). It sets the current_statement attribute to None, indicating that no specific statement is currently being processed. _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `7333e8` [7]: The visit_AnnAssign method processes annotated assignment nodes in Python code. It checks if there is a current context, then verifies the target is a name. If so, it retrieves the name and source code for the annotation node. The method appends an entity to the globals list containing the name, source code, inferred signature based on the annotation, and whether the name starts with an underscore indicating privacy. _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `54869e` [8]: The method visit_Assign handles assignment nodes in the code, appending details of global variables to the entities list if the current context is empty. It retrieves the target name and source code for each assignment, creates a signature string, and marks names starting with an underscore as private. _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `851fc2` [9]: The method visit_Call handles call expressions in the abstract syntax tree (AST) and records interactions between nodes based on whether the function being called is a simple name or not. It specifically records interactions for names using the _record_interaction method. _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `2236eb` [10]: The method `visit_ClassDef` is called when encountering a class definition in the Abstract Syntax Tree (AST). It processes the class node by appending its name to the current context, retrieves the source code of the class, docstring, and bases (inheritance) if any, constructs a header string for the class definition, stores the class details in the entities dictionary under 'classes', pushes the class header onto the header stack, and initializes an empty list for methods. _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `adffc8` [11]: Describes the `visit_FunctionDef` method in `CodeEntityVisitor`, which visits a function definition node, extracts signature, docstring, body, and other metadata, determines if it's private or unimplemented, and adds it to either functions or class methods. _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `ee238c` [12]: The visit_Import method processes an import node, extracting the module name for each alias and adding it to the external_imports set. _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `0894ed` [13]: The method visit_ImportFrom processes an import statement from another module, determining if it is relative or external, and populates the relative_imports set and import_map dictionary accordingly. _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `8886c6` [14]: The method visit_Name records interactions between the context and the name value if they are not already in the current context. It skips recording if there is an interaction already. _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `74d148` [15]: The method visit_SimpleStatementLine is called when parsing a SimpleStatementLine node in the code. It sets the current_statement attribute to the provided node. _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `af8046` [16]: The `analyze` method builds the dependency graph by recursively traversing the project structure, populates dependents for each node, and returns the constructed graph as a dictionary. _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Defines a system for encapsulating memory management within a persistent Chroma database, allowing for adding memories with associated metadata, querying these memories based on text embeddings, updating the helpfulness of specific memories, and automatically cleaning up unused or low-helpfulness entries.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: ChromaMemory is a class that manages memory records in a Chroma database, allowing initialization of a PersistentClient and collection, adding memories with text, embeddings, metadata, querying memories by query, updating helpfulness scores, and cleaning up low-helpfulness or unused memories. [2]
- **`🔌 class MemoryInterface`**: Defines the interface for querying memory data. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Adds a memory to the Chroma database collection with provided text, embedding vector, turn_added, helpfulness values and optional additional metadata. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: The method cleanup_memories deletes memories from the collection if their helpfulness is below 0.3 or they haven't been used in more than 50 turns. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: The method queries the memory collection for documents matching the given query, retrieves metadata for each document ID, updates the last_used_turn field in the metadata to the current turn value, and returns the results including ids, documents, metadatas, and distances. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: The method updates the 'helpfulness' attribute of a specified memory in the ChromaDB collection by retrieving its current metadata, creating a copy, modifying the 'helpfulness' value, and then updating the metadata in the database. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b7df0a` [1]: Defines a system for encapsulating memory management within a persistent Chroma database, allowing for adding memories with associated metadata, querying these memories based on text embeddings, updating the helpfulness of specific memories, and automatically cleaning up unused or low-helpfulness entries. _(Source: Synthesis (based on [5], [2], [8], [4], [7], [3], [6]))_
> 🆔 `7357ba` [2]: ChromaMemory is a class that manages memory records in a Chroma database, allowing initialization of a PersistentClient and collection, adding memories with text, embeddings, metadata, querying memories by query, updating helpfulness scores, and cleaning up low-helpfulness or unused memories. _(Source: class ChromaMemory)_
> 🆔 `daa213` [3]: Defines the interface for querying memory data. _(Source: class MemoryInterface)_
> 🆔 `c6a6da` [4]: Adds a memory to the Chroma database collection with provided text, embedding vector, turn_added, helpfulness values and optional additional metadata. _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `3b24da` [5]: The method cleanup_memories deletes memories from the collection if their helpfulness is below 0.3 or they haven't been used in more than 50 turns. _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `e9cacc` [6]: The method queries the memory collection for documents matching the given query, retrieves metadata for each document ID, updates the last_used_turn field in the metadata to the current turn value, and returns the results including ids, documents, metadatas, and distances. _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `d48487` [7]: The method updates the 'helpfulness' attribute of a specified memory in the ChromaDB collection by retrieving its current metadata, creating a copy, modifying the 'helpfulness' value, and then updating the metadata in the database. _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Defines an automated classification system that categorizes modules into archetypes such as entry point, configuration, data model, utility, or service based on their name, source code structure, and associated entities.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Classifies modules based on name, source code, and data model information to determine archetype like entry point or service dependencies. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: The classify method analyzes the module's name, source code, and data model information to determine its archetype based on predefined criteria such as entry point, data model components (models, schemas, contexts), configuration settings, utility functions, or service dependencies. [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `5b93d4` [1]: Defines an automated classification system that categorizes modules into archetypes such as entry point, configuration, data model, utility, or service based on their name, source code structure, and associated entities. _(Source: Synthesis (based on [4], [2], [3]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `edced0` [3]: Classifies modules based on name, source code, and data model information to determine archetype like entry point or service dependencies. _(Source: class ModuleClassifier)_
> 🆔 `117d02` [4]: The classify method analyzes the module's name, source code, and data model information to determine its archetype based on predefined criteria such as entry point, data model components (models, schemas, contexts), configuration settings, utility functions, or service dependencies. _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Defines and synthesizes role descriptions for software modules by integrating their internal mechanisms, upstream dependencies, downstream consumers, and architectural roles into a cohesive narrative.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: The ModuleContextualizer class initializes attributes related to module analysis, including file path, graph data, dependency contexts, and various components for analysis, classification, and synthesis based on predefined criteria. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: The method contextualize_module analyzes a module by performing component analysis, dependency analysis, populating alerts, and systemic synthesis based on critique instruction. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext class from summary_models.. [4]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. [5]
- **`module_classifier.py`**: Uses `module_classifier.py`: Instantiates ModuleClassifier with module_name and data.. [6]
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates TaskExecutor class. [7]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst. [8]
- **`component_analyst.py`**: Uses `component_analyst.py`: Instantiates ComponentAnalyst. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `9a046b` [1]: Defines and synthesizes role descriptions for software modules by integrating their internal mechanisms, upstream dependencies, downstream consumers, and architectural roles into a cohesive narrative. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `cda3bb` [2]: The ModuleContextualizer class initializes attributes related to module analysis, including file path, graph data, dependency contexts, and various components for analysis, classification, and synthesis based on predefined criteria. _(Source: class ModuleContextualizer)_
> 🆔 `59e9c0` [3]: The method contextualize_module analyzes a module by performing component analysis, dependency analysis, populating alerts, and systemic synthesis based on critique instruction. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `9baf36` [4]: Uses `summary_models.py`: Instantiates ModuleContext class from summary_models.. _(Source: Import summary_models.py)_
> 🆔 `175cb1` [5]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `1c0cd6` [6]: Uses `module_classifier.py`: Instantiates ModuleClassifier with module_name and data.. _(Source: Import module_classifier.py)_
> 🆔 `698f6e` [7]: Uses `task_executor.py`: Instantiates TaskExecutor class. _(Source: Import task_executor.py)_
> 🆔 `2b420b` [8]: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst. _(Source: Import dependency_analyst.py)_
> 🆔 `6275af` [9]: Uses `component_analyst.py`: Instantiates ComponentAnalyst. _(Source: Import component_analyst.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Defines and manages a data structure for organizing and contextualizing module information within a system, encapsulating roles, dependencies, dependents, public APIs, alerts, and associated claims through various classes and methods.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: The Claim class computes and stores a SHA-1 hash of the unique string composed of its text, reference, and source_module attributes. [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: The ModuleContext class manages and organizes various components of a module, including its file path, role (GroundedText), dependencies, dependents, public API, alerts, and associated claims. It initializes with these attributes and provides methods to add context information like dependencies, dependents, and placeholders for roles or APIs. [5]
- **`🔌 🔌 Claim.id`**: The method computes a SHA-1 hash of a unique string composed of the instance's text, reference, and source_module attributes. [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds an alert to the list of alerts for the ModuleContext instance. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: The add_dependency_context method adds dependency information for a module to the ModuleContext instance. It takes the module_path, an explanation string, and a list of supporting Claim objects. The method calls _add_claims_and_get_placeholders on the supporting claims to get placeholders and claim IDs. It then combines the explanation with any placeholders and stores the result in key_dependencies dictionary using module_path as the key. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: The function `add_dependent_context` adds a dependent module context to the `key_dependents` dictionary of the ModuleContext instance, combining an explanation and placeholders for supporting claims extracted from provided claim objects. [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: The method adds an entry to the public API dictionary for a given entity name and description, combining it with placeholders from supporting claims. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: The method `set_module_role` takes a string `text` and a list of `Claim`s, adds the claims to the module context, generates placeholders, combines the text with placeholders, creates a new `GroundedText` object for `module_role`, and stores it in the class. It also retrieves claim IDs from the supporting claims. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `cfc017` [1]: Defines and manages a data structure for organizing and contextualizing module information within a system, encapsulating roles, dependencies, dependents, public APIs, alerts, and associated claims through various classes and methods. _(Source: Synthesis (based on [3], [9], [8], [11], [10], [7], [4], [5], [2], [6]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `2e199a` [3]: The Claim class computes and stores a SHA-1 hash of the unique string composed of its text, reference, and source_module attributes. _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `b9090f` [5]: The ModuleContext class manages and organizes various components of a module, including its file path, role (GroundedText), dependencies, dependents, public API, alerts, and associated claims. It initializes with these attributes and provides methods to add context information like dependencies, dependents, and placeholders for roles or APIs. _(Source: class ModuleContext)_
> 🆔 `fda318` [6]: The method computes a SHA-1 hash of a unique string composed of the instance's text, reference, and source_module attributes. _(Source: 🔌 Claim.id)_
> 🆔 `84b594` [7]: Adds an alert to the list of alerts for the ModuleContext instance. _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `4e9e22` [8]: The add_dependency_context method adds dependency information for a module to the ModuleContext instance. It takes the module_path, an explanation string, and a list of supporting Claim objects. The method calls _add_claims_and_get_placeholders on the supporting claims to get placeholders and claim IDs. It then combines the explanation with any placeholders and stores the result in key_dependencies dictionary using module_path as the key. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `3371fb` [9]: The function `add_dependent_context` adds a dependent module context to the `key_dependents` dictionary of the ModuleContext instance, combining an explanation and placeholders for supporting claims extracted from provided claim objects. _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `80135c` [10]: The method adds an entry to the public API dictionary for a given entity name and description, combining it with placeholders from supporting claims. _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `7014a8` [11]: The method `set_module_role` takes a string `text` and a list of `Claim`s, adds the claims to the module context, generates placeholders, combines the text with placeholders, creates a new `GroundedText` object for `module_role`, and stores it in the class. It also retrieves claim IDs from the supporting claims. _(Source: 🔌 ModuleContext.set_module_role)_
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