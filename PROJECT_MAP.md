# Project Context Map

## 🏛️ System Architecture
The system architecture rests on a firm foundation of configuration parameters and data models that define the core components used by AI agents for documentation purposes. Configuration Layer holds the system-wide settings, while Data Model Layer encapsulates essential objects such as Claim, GroundedText, Alert, and ModuleContext, which are crucial for generating thorough documentation. This data structure is then utilized by the Service Layer to orchestrate various tasks like generating markdown reports, parsing code, and grounding modules for policy compliance.

The Application Logic layer acts as the central processing unit of the system, responsible for manipulating and integrating the data model objects through utility functions provided in agent_core.py and semantic_gatekeeper.py. Utility Layer serves as a bridge between these core components, handling formatting input, generating model responses, and retrieving structured content to ensure smooth integration of documentation across different services.

Finally, the Entry Point Layer acts as the interface for end-users to initiate the entire workflow by parsing command-line arguments and executing the main script within the specified environment. This layer coordinates with both Service Layer and Utility Layer to execute technical tasks, analyze components, and generate final reports based on user-defined parameters.

---

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates the main function to parse command-line arguments, locate the _main.py file within the specified target folder, initializes a CrawlerAgent instance with the goal and found file path, and runs the crawler agent to execute the agent. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Parse command line arguments and assign parsed values to variables for passing to the main function [2]
- **`🔌 goal`**: Parse command-line arguments using argparse and pass them to the main function for execution [3]
- **`🔌 main`**: 'The main function searches for a file named _main.py in the specified target folder and directory, initializes a CrawlerAgent instance with the goal and found file path, and runs the crawler agent to execute the agent.\ [4]
- **`🔌 parser`**: Analyze the parsed command line arguments to extract the specific data structure or literal value assigned and summarize it in a sentence based on the provided facts, without using marketing language. [5]
- **`🔌 result`**: Parse command line arguments using argparse to retrieve values for goal and target_folder, then pass them to the main function which returns result. [6]
- **`🔌 target_folder`**: Assign `args.target_folder` to `target_folder` and call `main(goal, target_folder)` storing result in `result`. [7]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Instantiates class CrawlerAgent. [8]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `2da93c` [1]: Orchestrates the main function to parse command-line arguments, locate the _main.py file within the specified target folder, initializes a CrawlerAgent instance with the goal and found file path, and runs the crawler agent to execute the agent. _(Source: Synthesis (based on [6], [3], [7], [5], [2], [4]))_
> 🆔 `b2534c` [2]: Parse command line arguments and assign parsed values to variables for passing to the main function _(Source: args)_
> 🆔 `63ff8c` [3]: Parse command-line arguments using argparse and pass them to the main function for execution _(Source: goal)_
> 🆔 `fc96d0` [4]: 'The main function searches for a file named _main.py in the specified target folder and directory, initializes a CrawlerAgent instance with the goal and found file path, and runs the crawler agent to execute the agent.\ _(Source: main)_
> 🆔 `ae6f24` [5]: Analyze the parsed command line arguments to extract the specific data structure or literal value assigned and summarize it in a sentence based on the provided facts, without using marketing language. _(Source: parser)_
> 🆔 `1c11f8` [6]: Parse command line arguments using argparse to retrieve values for goal and target_folder, then pass them to the main function which returns result. _(Source: result)_
> 🆔 `91a804` [7]: Assign `args.target_folder` to `target_folder` and call `main(goal, target_folder)` storing result in `result`. _(Source: target_folder)_
> 🆔 `f54474` [8]: Uses `agent_core.py`: Instantiates class CrawlerAgent. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Manages goal initialization, memory management, and execution flow while orchestrating crawling, synthesis, reporting, and cleanup of data traces.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: 'The CrawlerAgent class initializes an instance with goal and target_root parameters, creates a ChromaMemory object for memory management, executes the run method to initiate crawling and data synthesis, renders a report based on synthesized data, and cleans up memories after each execution cycle.\ [2]
- **`🔌 🔌 CrawlerAgent.run`**: 'Executes the crawler agent, synthesizing project data and rendering a report while cleaning up memories after each turn.\ [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates class from summary_models.py. [4]
- **`memory_core.py`**: Uses `memory_core.py`: 'Instantiates ChromaMemory class\. [5]
- **`agent_config.py`**: Uses `agent_config.py`: 'Instantiates DEFAULT_MODEL and retrieves CONTEXT_LIMIT from agent_config.py\. [6]
- **`report_renderer.py`**: Uses `report_renderer.py`: 'Instantiates ReportRenderer class from report_renderer module and renders a report.\. [7]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Defines data structures or configuration.. [8]
- **`llm_util.py`**: Uses `llm_util.py`: 'Instantiates class from llm_util.py\. [9]
- **`agent_util.py`**: Uses `agent_util.py`: Defines data structures or configuration.. [10]
- **`map_synthesizer.py`**: Uses `map_synthesizer.py`: 'Instantiates MapSynthesizer class using gatekeeper argument\. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `4fe825` [1]: Manages goal initialization, memory management, and execution flow while orchestrating crawling, synthesis, reporting, and cleanup of data traces. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `242bcb` [2]: 'The CrawlerAgent class initializes an instance with goal and target_root parameters, creates a ChromaMemory object for memory management, executes the run method to initiate crawling and data synthesis, renders a report based on synthesized data, and cleans up memories after each execution cycle.\ _(Source: class CrawlerAgent)_
> 🆔 `8e7555` [3]: 'Executes the crawler agent, synthesizing project data and rendering a report while cleaning up memories after each turn.\ _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `6405c8` [4]: Uses `summary_models.py`: Instantiates class from summary_models.py. _(Source: Import summary_models.py)_
> 🆔 `e4a6cc` [5]: Uses `memory_core.py`: 'Instantiates ChromaMemory class\. _(Source: Import memory_core.py)_
> 🆔 `e734f8` [6]: Uses `agent_config.py`: 'Instantiates DEFAULT_MODEL and retrieves CONTEXT_LIMIT from agent_config.py\. _(Source: Import agent_config.py)_
> 🆔 `126c2e` [7]: Uses `report_renderer.py`: 'Instantiates ReportRenderer class from report_renderer module and renders a report.\. _(Source: Import report_renderer.py)_
> 🆔 `d99a4f` [8]: Uses `semantic_gatekeeper.py`: Defines data structures or configuration.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `dd4fb5` [9]: Uses `llm_util.py`: 'Instantiates class from llm_util.py\. _(Source: Import llm_util.py)_
> 🆔 `6d51ea` [10]: Uses `agent_util.py`: Defines data structures or configuration.. _(Source: Import agent_util.py)_
> 🆔 `b9852c` [11]: Uses `map_synthesizer.py`: 'Instantiates MapSynthesizer class using gatekeeper argument\. _(Source: Import map_synthesizer.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` 'Agent Core Orchestrates Project Summarization Workflow\

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: The specific data structure or literal value assigned in this statement is the ProjectGraph dictionary where keys are strings and values can be any type (ProjectGraph = Dict[str, Any]). [2]
- **`🔌 class ProjectSummarizer`**: Summarize the responsibility of Class `ProjectSummarizer` based on the provided facts, including its initialization attributes and methods. [3]
- **`🔌 project_pulse`**: 'The project_pulse function analyzes the specified file using GraphAnalyzer and ProjectSummarizer to generate contexts and processing order, returning them as a tuple.\ [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: The method initializes context hashes, creates SemanticGatekeeper and MapCritic instances, iterates over cycles to process paths, generates critique maps, updates critiques, computes current input hashes, checks for cached contexts, logs statistics, and may terminate early if no changes or critiques are available. [5]
- **`🔒 _create_module_context`**: 'The _create_module_context function generates and returns the module context based on provided parameters, setting the file path if necessary.\ [6]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: 'Instantiates ModuleContext and calls project_pulse.\. [7]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper. [8]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates ReportRenderer class with contexts and output_file set to temp_map_path. [9]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: 'Instantiates class GraphAnalyzer with target_file_path\. [10]
- **`map_critic.py`**: Uses `map_critic.py`: 'Instantiates MapCritic class using gatekeeper parameter\. [11]
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: Instantiates class ModuleContextualizer. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a099f3` [1]: 'Agent Core Orchestrates Project Summarization Workflow\ _(Source: Synthesis (based on [6], [5], [4], [3], [2]))_
> 🆔 `b615e4` [2]: The specific data structure or literal value assigned in this statement is the ProjectGraph dictionary where keys are strings and values can be any type (ProjectGraph = Dict[str, Any]). _(Source: ProjectGraph)_
> 🆔 `a55986` [3]: Summarize the responsibility of Class `ProjectSummarizer` based on the provided facts, including its initialization attributes and methods. _(Source: class ProjectSummarizer)_
> 🆔 `6e3458` [4]: 'The project_pulse function analyzes the specified file using GraphAnalyzer and ProjectSummarizer to generate contexts and processing order, returning them as a tuple.\ _(Source: project_pulse)_
> 🆔 `0e9380` [5]: The method initializes context hashes, creates SemanticGatekeeper and MapCritic instances, iterates over cycles to process paths, generates critique maps, updates critiques, computes current input hashes, checks for cached contexts, logs statistics, and may terminate early if no changes or critiques are available. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `083863` [6]: 'The _create_module_context function generates and returns the module context based on provided parameters, setting the file path if necessary.\ _(Source: _create_module_context)_
> 🆔 `f4eac6` [7]: Uses `summary_models.py`: 'Instantiates ModuleContext and calls project_pulse.\. _(Source: Import summary_models.py)_
> 🆔 `9a5d26` [8]: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `51e962` [9]: Uses `report_renderer.py`: Instantiates ReportRenderer class with contexts and output_file set to temp_map_path. _(Source: Import report_renderer.py)_
> 🆔 `36da2a` [10]: Uses `graph_analyzer.py`: 'Instantiates class GraphAnalyzer with target_file_path\. _(Source: Import graph_analyzer.py)_
> 🆔 `7251ae` [11]: Uses `map_critic.py`: 'Instantiates MapCritic class using gatekeeper parameter\. _(Source: Import map_critic.py)_
> 🆔 `e36515` [12]: Uses `module_contextualizer.py`: Instantiates class ModuleContextualizer. _(Source: Import module_contextualizer.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` 'Analyzes the systemic role of the Component Analyst module, coordinating data analysis and summarization processes without performing peripheral tasks.\

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: 'Analyzes the responsibility of Class ComponentAnalyst by parsing its source code into an Abstract Syntax Tree, applying transformations, retrieving logic-only data, constructing context information, solving tasks based on goals and dependencies, and summarizing findings in a concise manner.\ [2]
- **`🔌 class SkeletonTransformer`**: 'The SkeletonTransformer class is responsible for removing docstrings from FunctionDef, AsyncFunctionDef, and ClassDef nodes and recursively visiting child nodes of each ClassDef encountered.\ [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: 'Analyze the Components Method Describes\ [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: 'The source code is parsed into an AST, transformed using the SkeletonTransformer, and then unparsed back into modified source code.\ [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Describes the method of processing an AsyncFunctionDef node by removing any docstring and calling generic_visit on it. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: 'The visit_ClassDef method removes docstrings from ClassDef nodes, sets empty body to ast.Pass(), and recursively visits child nodes in the AST.\ [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: "visit_FunctionDef" removes the docstring from FunctionDef nodes and then calls generic_visit on them. [8]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: 'Instantiates SemanticGatekeeper class with gatekeeper parameter.\. [9]
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates class TaskExecutor.. [10]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates class_summary. [11]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `56420a` [1]: 'Analyzes the systemic role of the Component Analyst module, coordinating data analysis and summarization processes without performing peripheral tasks.\ _(Source: Synthesis (based on [8], [5], [2], [3], [7], [4], [6]))_
> 🆔 `2c954f` [2]: 'Analyzes the responsibility of Class ComponentAnalyst by parsing its source code into an Abstract Syntax Tree, applying transformations, retrieving logic-only data, constructing context information, solving tasks based on goals and dependencies, and summarizing findings in a concise manner.\ _(Source: class ComponentAnalyst)_
> 🆔 `521405` [3]: 'The SkeletonTransformer class is responsible for removing docstrings from FunctionDef, AsyncFunctionDef, and ClassDef nodes and recursively visiting child nodes of each ClassDef encountered.\ _(Source: class SkeletonTransformer)_
> 🆔 `c7078d` [4]: 'Analyze the Components Method Describes\ _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `0e520c` [5]: 'The source code is parsed into an AST, transformed using the SkeletonTransformer, and then unparsed back into modified source code.\ _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `ee897b` [6]: Describes the method of processing an AsyncFunctionDef node by removing any docstring and calling generic_visit on it. _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `5fc35a` [7]: 'The visit_ClassDef method removes docstrings from ClassDef nodes, sets empty body to ast.Pass(), and recursively visits child nodes in the AST.\ _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `0088a6` [8]: "visit_FunctionDef" removes the docstring from FunctionDef nodes and then calls generic_visit on them. _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `3d8a58` [9]: Uses `semantic_gatekeeper.py`: 'Instantiates SemanticGatekeeper class with gatekeeper parameter.\. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `55dff2` [10]: Uses `task_executor.py`: Instantiates class TaskExecutor.. _(Source: Import task_executor.py)_
> 🆔 `d581bb` [11]: Uses `summary_models.py`: Instantiates class_summary. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Defines an active service that analyzes module dependencies by retrieving upstream contexts, sanitizing roles, extracting symbols and interactions, summarizing snippets, and constructing explanation strings.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: 'The provided code snippet demonstrates the absence of logic to instantiate or utilize the DependencyAnalyst class, which likely requires initialization and methods like _sanitize_context and analyze_dependencies to function properly.\ [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes the usage of each dependency by retrieving upstream contexts, sanitizing module roles, extracting relevant symbols and interactions, summarizing snippets, and constructing an explanation string. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates class.... [4]
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates class TaskExecutor. [5]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext. [6]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `bc844d` [1]: Defines an active service that analyzes module dependencies by retrieving upstream contexts, sanitizing roles, extracting symbols and interactions, summarizing snippets, and constructing explanation strings. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `461c0e` [2]: 'The provided code snippet demonstrates the absence of logic to instantiate or utilize the DependencyAnalyst class, which likely requires initialization and methods like _sanitize_context and analyze_dependencies to function properly.\ _(Source: class DependencyAnalyst)_
> 🆔 `8057ae` [3]: Analyzes the usage of each dependency by retrieving upstream contexts, sanitizing module roles, extracting relevant symbols and interactions, summarizing snippets, and constructing an explanation string. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `90018b` [4]: Uses `semantic_gatekeeper.py`: Instantiates class.... _(Source: Import semantic_gatekeeper.py)_
> 🆔 `84ba83` [5]: Uses `task_executor.py`: Instantiates class TaskExecutor. _(Source: Import task_executor.py)_
> 🆔 `6ffcf1` [6]: Uses `summary_models.py`: Instantiates ModuleContext. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` The Map Critic module defines and executes a critique process that analyzes project modules for documentation errors using the SemanticGatekeeper.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: 'The MapCritic class parses project content, analyzes modules for documentation errors, and generates critiques using SemanticGatekeeper.\ [2]
- **`🔌 🔌 MapCritic.critique`**: Analyze the modules within a project map content and generate a list of critiques for each module, including the module name and corresponding instruction based on semantic analysis using a SemanticGatekeeper. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper, calls its constructor.. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1951bd` [1]: The Map Critic module defines and executes a critique process that analyzes project modules for documentation errors using the SemanticGatekeeper. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `586ee5` [2]: 'The MapCritic class parses project content, analyzes modules for documentation errors, and generates critiques using SemanticGatekeeper.\ _(Source: class MapCritic)_
> 🆔 `35bd67` [3]: Analyze the modules within a project map content and generate a list of critiques for each module, including the module name and corresponding instruction based on semantic analysis using a SemanticGatekeeper. _(Source: 🔌 MapCritic.critique)_
> 🆔 `29844b` [4]: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper, calls its constructor.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` The Map Synthesizer analyzes processing order, maps modules to target groups based on roles and layer mappings, generates feedback using gatekeeper execution, creates system synthesis output.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: 'The MapSynthesizer class analyzes processing_order, maps modules to target groups based on roles and layer mappings, generates feedback using gatekeeper execution, creates a system overview description, and produces the final synthesis output.\ [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: 'Analyze the method's purpose, which involves iterating over processing_order to map modules to target groups, synthesizing summaries for non-empty groups, and generating final system synthesis.\ [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: 'Instantiates class SemanticGatekeeper\. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext and calls synthesis functions. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `732fec` [1]: The Map Synthesizer analyzes processing order, maps modules to target groups based on roles and layer mappings, generates feedback using gatekeeper execution, creates system synthesis output. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `a98524` [2]: 'The MapSynthesizer class analyzes processing_order, maps modules to target groups based on roles and layer mappings, generates feedback using gatekeeper execution, creates a system overview description, and produces the final synthesis output.\ _(Source: class MapSynthesizer)_
> 🆔 `ddee2b` [3]: 'Analyze the method's purpose, which involves iterating over processing_order to map modules to target groups, synthesizing summaries for non-empty groups, and generating final system synthesis.\ _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `3f0525` [4]: Uses `semantic_gatekeeper.py`: 'Instantiates class SemanticGatekeeper\. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `a130d9` [5]: Uses `summary_models.py`: Instantiates ModuleContext and calls synthesis functions. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Orchestrates generating markdown reports detailing system architecture, module count, archetype categorization, and rendering paths for downstream consumers.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Render markdown reports based on system architecture and configurations, initializing attributes such as context map, output file name, system summary, and provided variables. [2]
- **`🔌 🔌 ReportRenderer.render`**: The function generates markdown content describing the system architecture, module count, archetype categorization, and rendering paths to an output file. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates class and calls function with ModuleContext parameters. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `cfd5eb` [1]: Orchestrates generating markdown reports detailing system architecture, module count, archetype categorization, and rendering paths for downstream consumers. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `5ad001` [2]: Render markdown reports based on system architecture and configurations, initializing attributes such as context map, output file name, system summary, and provided variables. _(Source: class ReportRenderer)_
> 🆔 `9ea45f` [3]: The function generates markdown content describing the system architecture, module count, archetype categorization, and rendering paths to an output file. _(Source: 🔌 ReportRenderer.render)_
> 🆔 `a12976` [4]: Uses `summary_models.py`: Instantiates class and calls function with ModuleContext parameters. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Manages the active parsing and grounding of code snippets, critically analyzing their content for policy compliance without marketing fluff.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines global constant `BANNED_ADJECTIVES`. [2]
- **`🔌 class SemanticGatekeeper`**: 'The SemanticGatekeeper class implements methods to verify grounding, critique content for policy compliance, extract balanced JSON, parse JSON safely, and process entire JSON structures while handling errors.\ [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Summarizes the method's purpose and functionality based on provided facts without using marketing language. [4]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py`: 'Instantiates agent_config.DEFAULT_MODEL and calls chat_llm for messages and verify_prompt.\. [5]
- **`llm_util.py`**: Uses `llm_util.py`: 'Instantiates chat model using llm_util.py imports\. [6]

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

> 🆔 `021a8d` [1]: Manages the active parsing and grounding of code snippets, critically analyzing their content for policy compliance without marketing fluff. _(Source: Synthesis (based on [4], [3], [2]))_
> 🆔 `4d3df2` [2]: Defines global constant `BANNED_ADJECTIVES`. _(Source: BANNED_ADJECTIVES)_
> 🆔 `47e632` [3]: 'The SemanticGatekeeper class implements methods to verify grounding, critique content for policy compliance, extract balanced JSON, parse JSON safely, and process entire JSON structures while handling errors.\ _(Source: class SemanticGatekeeper)_
> 🆔 `37b1bd` [4]: Summarizes the method's purpose and functionality based on provided facts without using marketing language. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `5bcb78` [5]: Uses `agent_config.py`: 'Instantiates agent_config.DEFAULT_MODEL and calls chat_llm for messages and verify_prompt.\. _(Source: Import agent_config.py)_
> 🆔 `a7af0b` [6]: Uses `llm_util.py`: 'Instantiates chat model using llm_util.py imports\. _(Source: Import llm_util.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` Executes complex technical tasks by coordinating the analysis and orchestration of code, refining synthesis results, and ensuring adherence to defined configurations through various method calls.

**Impact Analysis:** Changes to this module will affect: component_analyst.py, dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: 'The TaskExecutor class is responsible for executing complex tasks by initializing an instance of SemanticGatekeeper, cleaning and parsing gatekeeper responses, unwrapping text data structures, refining synthesis results, and defining specific configurations through a series of method calls.\ [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: 'Defines the data structures and configuration for the method.\ [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper from semantic_gatekeeper.py. [4]

### 👥 Used By (Downstream)
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ca2a19` [1]: Executes complex technical tasks by coordinating the analysis and orchestration of code, refining synthesis results, and ensuring adherence to defined configurations through various method calls. _(Source: Synthesis (based on [3], [2]))_
> 🆔 `f8eff2` [2]: 'The TaskExecutor class is responsible for executing complex tasks by initializing an instance of SemanticGatekeeper, cleaning and parsing gatekeeper responses, unwrapping text data structures, refining synthesis results, and defining specific configurations through a series of method calls.\ _(Source: class TaskExecutor)_
> 🆔 `31a466` [3]: 'Defines the data structures and configuration for the method.\ _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `e51793` [4]: Uses `semantic_gatekeeper.py`: Instantiates class SemanticGatekeeper from semantic_gatekeeper.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Defines a function that formats input into messages, utilizes an external library to generate responses tailored to the specified model, retrieves and returns structured content after processing, and handles exceptions by logging errors and providing error feedback.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: 'The chat_llm function transforms input into a structured list of messages, employs ollama.chat to produce responses tailored to the given model, retrieves and returns the generated content after eliminating excess whitespace, and manages exceptions by recording errors and delivering an error string.\ [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `af06fc` [1]: Defines a function that formats input into messages, utilizes an external library to generate responses tailored to the specified model, retrieves and returns structured content after processing, and handles exceptions by logging errors and providing error feedback. _(Source: Synthesis (based on [2]))_
> 🆔 `a5a35d` [2]: 'The chat_llm function transforms input into a structured list of messages, employs ollama.chat to produce responses tailored to the given model, retrieves and returns the generated content after eliminating excess whitespace, and manages exceptions by recording errors and delivering an error string.\ _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Defines and encapsulates a system for statically analyzing Python code files to build a dependency graph of modules and their relationships, including imports, assignments, annotations, class definitions, function signatures, cross-module interactions, and specific call nodes.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: 'The CodeEntityVisitor class is responsible for analyzing and recording various elements of the Python code structure, including file paths, import statements, assignments, annotations, class definitions, function signatures, privacy status, cross-module interactions, and specific call nodes during execution.\ [2]
- **`🔌 class GraphAnalyzer`**: 'The GraphAnalyzer class instantiates and initializes paths, builds an initial dependency graph using depth-first search, populates additional dependencies from the file system, and updates its attribute graph to contain the populated dependency graph.\ [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Pop from `self.current_context` and `self.header_stack` stacks when the `leave_ClassDef` function is executed. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: "leave_FunctionDef" executes by popping the last context from the stack if it's not empty, and then removes the header_stack attribute when leaving a function definition in the CodeEntityVisitor class. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: 'The leave_SimpleStatementLine method sets the current_statement attribute to None when processing a SimpleStatementLine node.\ [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: 'The `visit_AnnAssign` method analyzes AnnAssign nodes in an AST, extracting and categorizing variable names, their source code context, annotations, and privacy status if applicable.\ [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: 'The function visit_Assign processes each assignment node, extracting target names and source code, then records them as globals in the entities dictionary along with their name, source code, formatted signature, and privacy status based on naming convention.\ [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: "visit_Call" is defined within a class that inherits from "CodeEntityVisitor", takes a single argument of type "cst.Call", returns None, and checks if the node.func attribute is an instance of cst.Name; if true, it calls another method named _record_interaction passing in node.func.value and node as arguments. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: 'The visit_ClassDef method processes Python class definitions by collecting their source code, any docstring, and base classes, then constructing a header string and updating the visitor's internal dictionary for further analysis.\ [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: 'Analyze the function definition in Python source code by extracting its name, parameters, return type annotation, docstring, and determining if it is unimplemented or private, then categorize it as a method or standalone function based on its context.\ [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: 'The method processes each alias within an import statement, retrieves the corresponding module name using `self.module_node.code_for_node`, and adds the extracted external module names to the visitor's state set.\ [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes import statements to determine external imports, potential file paths for relative imports, and updates import map based on target files or directories. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: 'The _record_interaction method records interactions using node.value and node, but only if there is no current context or the last element in the current context does not match the node's value.\ [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Assigns the `node` parameter value to `current_statement` in the `CodeEntityVisitor` class during method execution. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: 'Analyze' the provided project structure by building an initial dependency graph using depth-first search from the specified root path, then populating additional dependencies within the file system before returning the populated dependency graph as self.graph.\ [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d724b6` [1]: Defines and encapsulates a system for statically analyzing Python code files to build a dependency graph of modules and their relationships, including imports, assignments, annotations, class definitions, function signatures, cross-module interactions, and specific call nodes. _(Source: Synthesis (based on [10], [16], [4], [14], [8], [7], [12], [3], [5], [6], [2], [9], [11], [13], [15]))_
> 🆔 `a146c2` [2]: 'The CodeEntityVisitor class is responsible for analyzing and recording various elements of the Python code structure, including file paths, import statements, assignments, annotations, class definitions, function signatures, privacy status, cross-module interactions, and specific call nodes during execution.\ _(Source: class CodeEntityVisitor)_
> 🆔 `81da1f` [3]: 'The GraphAnalyzer class instantiates and initializes paths, builds an initial dependency graph using depth-first search, populates additional dependencies from the file system, and updates its attribute graph to contain the populated dependency graph.\ _(Source: class GraphAnalyzer)_
> 🆔 `3c29b4` [4]: Pop from `self.current_context` and `self.header_stack` stacks when the `leave_ClassDef` function is executed. _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `8c5a02` [5]: "leave_FunctionDef" executes by popping the last context from the stack if it's not empty, and then removes the header_stack attribute when leaving a function definition in the CodeEntityVisitor class. _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `9956a9` [6]: 'The leave_SimpleStatementLine method sets the current_statement attribute to None when processing a SimpleStatementLine node.\ _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `4c086f` [7]: 'The `visit_AnnAssign` method analyzes AnnAssign nodes in an AST, extracting and categorizing variable names, their source code context, annotations, and privacy status if applicable.\ _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `49fb46` [8]: 'The function visit_Assign processes each assignment node, extracting target names and source code, then records them as globals in the entities dictionary along with their name, source code, formatted signature, and privacy status based on naming convention.\ _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `c2aa0d` [9]: "visit_Call" is defined within a class that inherits from "CodeEntityVisitor", takes a single argument of type "cst.Call", returns None, and checks if the node.func attribute is an instance of cst.Name; if true, it calls another method named _record_interaction passing in node.func.value and node as arguments. _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `135817` [10]: 'The visit_ClassDef method processes Python class definitions by collecting their source code, any docstring, and base classes, then constructing a header string and updating the visitor's internal dictionary for further analysis.\ _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `d85d6f` [11]: 'Analyze the function definition in Python source code by extracting its name, parameters, return type annotation, docstring, and determining if it is unimplemented or private, then categorize it as a method or standalone function based on its context.\ _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `79295d` [12]: 'The method processes each alias within an import statement, retrieves the corresponding module name using `self.module_node.code_for_node`, and adds the extracted external module names to the visitor's state set.\ _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `f26587` [13]: Analyzes import statements to determine external imports, potential file paths for relative imports, and updates import map based on target files or directories. _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `3cb50d` [14]: 'The _record_interaction method records interactions using node.value and node, but only if there is no current context or the last element in the current context does not match the node's value.\ _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `f368bf` [15]: Assigns the `node` parameter value to `current_statement` in the `CodeEntityVisitor` class during method execution. _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `13670a` [16]: 'Analyze' the provided project structure by building an initial dependency graph using depth-first search from the specified root path, then populating additional dependencies within the file system before returning the populated dependency graph as self.graph.\ _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Defines a system for managing and querying memories using the Chroma client, including adding new memory entries with unique identifiers and metadata, retrieving specific memories based on queries, updating last used turn, adjusting helpfulness scores, identifying and deleting low-score or stale memories.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: 'The ChromaMemory class is responsible for managing and querying memories using the Chroma client, including initializing attributes during instantiation to store memory data and metadata, retrieving or creating collections, generating unique identifiers, updating usage metrics, adjusting helpfulness scores, identifying low-score or stale memories, and deleting them as needed.\ [2]
- **`🔌 class MemoryInterface`**: Defines data structures or configuration. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: 'The method generates a unique memory identifier, creates combined metadata including turn_added details and any provided additional data, then adds the new memory entry to the specified collection using the Chroma client.\ [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: The code identifies and deletes memories from the specified collection that have a helpfulness score below 0.3 or have not been used for more than 50 turns, based on their IDs. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: The method queries memory, updates the last used turn for each matching metadata, and returns the results. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: "update_helpfulness" is designed to retrieve metadata for the specified memory ID and update its 'helpfulness' attribute with new value using database methods, then saving the modified data back to the collection. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `31c362` [1]: Defines a system for managing and querying memories using the Chroma client, including adding new memory entries with unique identifiers and metadata, retrieving specific memories based on queries, updating last used turn, adjusting helpfulness scores, identifying and deleting low-score or stale memories. _(Source: Synthesis (based on [5], [3], [7], [4], [6], [2], [8]))_
> 🆔 `746437` [2]: 'The ChromaMemory class is responsible for managing and querying memories using the Chroma client, including initializing attributes during instantiation to store memory data and metadata, retrieving or creating collections, generating unique identifiers, updating usage metrics, adjusting helpfulness scores, identifying low-score or stale memories, and deleting them as needed.\ _(Source: class ChromaMemory)_
> 🆔 `33d227` [3]: Defines data structures or configuration. _(Source: class MemoryInterface)_
> 🆔 `3738dd` [4]: 'The method generates a unique memory identifier, creates combined metadata including turn_added details and any provided additional data, then adds the new memory entry to the specified collection using the Chroma client.\ _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `2d254b` [5]: The code identifies and deletes memories from the specified collection that have a helpfulness score below 0.3 or have not been used for more than 50 turns, based on their IDs. _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `37f77e` [6]: The method queries memory, updates the last used turn for each matching metadata, and returns the results. _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `35b569` [7]: "update_helpfulness" is designed to retrieve metadata for the specified memory ID and update its 'helpfulness' attribute with new value using database methods, then saving the modified data back to the collection. _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Defines an architecture for classifying modules based on their structural characteristics using dependency analysis, class and function presence, and global assignment checks to assign archetypes such as Data Model, Configuration, Utility, Service, or Entry Point.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: 'The ModuleClassifier class analyzes module structure to determine its archetype based on dependencies, classes, functions, and global assignments.\ [3]
- **`🔌 🔌 ModuleClassifier.classify`**: 'The module is analyzed to determine its archetype based on the presence of dependencies, classes, functions, and global assignments.\ [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8f8a0b` [1]: Defines an architecture for classifying modules based on their structural characteristics using dependency analysis, class and function presence, and global assignment checks to assign archetypes such as Data Model, Configuration, Utility, Service, or Entry Point. _(Source: Synthesis (based on [3], [2], [4]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `84c969` [3]: 'The ModuleClassifier class analyzes module structure to determine its archetype based on dependencies, classes, functions, and global assignments.\ _(Source: class ModuleClassifier)_
> 🆔 `e4079f` [4]: 'The module is analyzed to determine its archetype based on the presence of dependencies, classes, functions, and global assignments.\ _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Defines a system for contextualizing and summarizing module roles based on architectural patterns and external interactions.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: 'The ModuleContextualizer class instantiates and initializes attributes to instantiate other classes, extract module information, build usage maps, clean text, gather upstream knowledge, populate alerts for missing functions/methods, and pass data through systemic synthesis based on provided parameters.\ [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyze the module's context and components based on provided data, initializing working memory for components and dependencies, populating alerts, and systemic synthesis instructions. [3]

### 🔗 Uses (Upstream)
- **`component_analyst.py`**: Uses `component_analyst.py`: 'Instantiates class ComponentAnalyst with parameters gatekeeper and task_executor\. [4]
- **`summary_models.py`**: Uses `summary_models.py`: 'Instantiates ModuleContext and sets alerts, module role in context.\. [5]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: 'Instantiates SemanticGatekeeper from semantic_gatekeeper module\. [6]
- **`module_classifier.py`**: Uses `module_classifier.py`: Instantiates class ModuleClassifier. [7]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst. [8]
- **`task_executor.py`**: Uses `task_executor.py`: 'Instantiates TaskExecutor class with gatekeeper argument\. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `43170b` [1]: Defines a system for contextualizing and summarizing module roles based on architectural patterns and external interactions. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `0b1fdd` [2]: 'The ModuleContextualizer class instantiates and initializes attributes to instantiate other classes, extract module information, build usage maps, clean text, gather upstream knowledge, populate alerts for missing functions/methods, and pass data through systemic synthesis based on provided parameters.\ _(Source: class ModuleContextualizer)_
> 🆔 `417088` [3]: Analyze the module's context and components based on provided data, initializing working memory for components and dependencies, populating alerts, and systemic synthesis instructions. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `056753` [4]: Uses `component_analyst.py`: 'Instantiates class ComponentAnalyst with parameters gatekeeper and task_executor\. _(Source: Import component_analyst.py)_
> 🆔 `bcc089` [5]: Uses `summary_models.py`: 'Instantiates ModuleContext and sets alerts, module role in context.\. _(Source: Import summary_models.py)_
> 🆔 `45b4ac` [6]: Uses `semantic_gatekeeper.py`: 'Instantiates SemanticGatekeeper from semantic_gatekeeper module\. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `d9ee5a` [7]: Uses `module_classifier.py`: Instantiates class ModuleClassifier. _(Source: Import module_classifier.py)_
> 🆔 `2b420b` [8]: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst. _(Source: Import dependency_analyst.py)_
> 🆔 `49a675` [9]: Uses `task_executor.py`: 'Instantiates TaskExecutor class with gatekeeper argument\. _(Source: Import task_executor.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Defines a system for encapsulating and representing various components such as Claim objects, GroundedText records, Alert notifications, and ModuleContext instances to generate detailed documentation for AI agents regarding module roles, dependencies, public APIs, and alerts.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: 'The Claim class generates and returns the SHA-1 hash of concatenated byte-encoded text, reference, and source_module attributes.\ [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: The responsibility of the ModuleContext class is to initialize default attribute values, manage and track module roles, dependencies, dependents, public API entries, alerts, and supporting claims within the system. [5]
- **`🔌 🔌 Claim.id`**: 'The method generates a SHA-1 hash of concatenated values including `text`, `reference`, and `source_module` by encoding them to bytes, computing the SHA-1 hash, and returning its hexadecimal string representation.\ [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Add the provided alert to the ModuleContext instance's alerts list using the add_alert function. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: 'The `add_dependency_context` method updates the state of a `ModuleContext` object by adding dependency context for a given module path, including an explanation and placeholders obtained from supporting claims.\ [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: 'The method adds explanatory text and claim IDs for a module path to the ModuleContext, storing them in a KeyDependents dictionary.\ [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: 'The method updates the public_api attribute, processes supporting claims to obtain placeholders and claim IDs, concatenates the description with placeholders to form full_text, and instantiates a GroundedText object with text=full_text and supporting_claim_ids.\ [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: 'The `set_module_role` function adds supporting claims to the provided text, concatenates them for storage in the module's role attribute as `GroundedText`, and records their IDs in the module role.\ [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ed6693` [1]: Defines a system for encapsulating and representing various components such as Claim objects, GroundedText records, Alert notifications, and ModuleContext instances to generate detailed documentation for AI agents regarding module roles, dependencies, public APIs, and alerts. _(Source: Synthesis (based on [11], [3], [5], [4], [10], [6], [2], [7], [9], [8]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `25f937` [3]: 'The Claim class generates and returns the SHA-1 hash of concatenated byte-encoded text, reference, and source_module attributes.\ _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `4b76c0` [5]: The responsibility of the ModuleContext class is to initialize default attribute values, manage and track module roles, dependencies, dependents, public API entries, alerts, and supporting claims within the system. _(Source: class ModuleContext)_
> 🆔 `bd33e0` [6]: 'The method generates a SHA-1 hash of concatenated values including `text`, `reference`, and `source_module` by encoding them to bytes, computing the SHA-1 hash, and returning its hexadecimal string representation.\ _(Source: 🔌 Claim.id)_
> 🆔 `d449c8` [7]: Add the provided alert to the ModuleContext instance's alerts list using the add_alert function. _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `f76831` [8]: 'The `add_dependency_context` method updates the state of a `ModuleContext` object by adding dependency context for a given module path, including an explanation and placeholders obtained from supporting claims.\ _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `deea4a` [9]: 'The method adds explanatory text and claim IDs for a module path to the ModuleContext, storing them in a KeyDependents dictionary.\ _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `b96e75` [10]: 'The method updates the public_api attribute, processes supporting claims to obtain placeholders and claim IDs, concatenates the description with placeholders to form full_text, and instantiates a GroundedText object with text=full_text and supporting_claim_ids.\ _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `001970` [11]: 'The `set_module_role` function adds supporting claims to the provided text, concatenates them for storage in the module's role attribute as `GroundedText`, and records their IDs in the module role.\ _(Source: 🔌 ModuleContext.set_module_role)_
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