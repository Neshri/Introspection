# Project Context Map

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates running of CrawlerAgent, initializes command line arguments, delegates to main logic for processing goals and target folders, synthesizes system summary and renders report [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Assigns command-line arguments to local variables using ArgumentParser [2]
- **`🔌 goal`**: Assigns parsed goal argument value to local variable for further processing in main function [3]
- **`🔌 main`**: Locates main.py file, initializes CrawlerAgent, runs agent, reports completion [4]
- **`🔌 parser`**: Initializes an argument parser for command line input, allowing users to specify parameters when running the program. [5]
- **`🔌 result`**: Calls main function to process goal and target folder [6]
- **`🔌 target_folder`**: Assigns target folder argument to local variable for use in main function [7]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Executes CrawlerAgent, initializing memory, fetching project map and processing order, synthesizing system summary, rendering report, cleaning memories, and returning completion response.. [8]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b1492b` [1]: Orchestrates running of CrawlerAgent, initializes command line arguments, delegates to main logic for processing goals and target folders, synthesizes system summary and renders report _(Source: Synthesis (based on [4], [6], [7], [3], [2], [5]))_
> 🆔 `f5dfdc` [2]: Assigns command-line arguments to local variables using ArgumentParser _(Source: args)_
> 🆔 `5bb5ec` [3]: Assigns parsed goal argument value to local variable for further processing in main function _(Source: goal)_
> 🆔 `093358` [4]: Locates main.py file, initializes CrawlerAgent, runs agent, reports completion _(Source: main)_
> 🆔 `f8c36a` [5]: Initializes an argument parser for command line input, allowing users to specify parameters when running the program. _(Source: parser)_
> 🆔 `2b4862` [6]: Calls main function to process goal and target folder _(Source: result)_
> 🆔 `52de2f` [7]: Assigns target folder argument to local variable for use in main function _(Source: target_folder)_
> 🆔 `741740` [8]: Uses `agent_core.py`: Executes CrawlerAgent, initializing memory, fetching project map and processing order, synthesizing system summary, rendering report, cleaning memories, and returning completion response.. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Analyzes code structure, synthesizes system summary, renders detailed report based on processed input

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Synthesizes system summary and renders report based on processed data [2]
- **`🔌 🔌 CrawlerAgent.run`**: Runs CrawlerAgent by initializing memory, fetching project map and processing order, synthesizing system summary, rendering report, cleaning memories, and returning completion response. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Installs and configures gatekeeper for data processing before passing to agent_core.py. [4]
- **`map_synthesizer.py`**: Uses `map_synthesizer.py`: Orchestrates the synthesis of modules into categorized groups, synthesizes each group, then synthesizes overall system architecture. [5]
- **`agent_util.py`**: Uses `agent_util.py`: Instructs agent_core.py to call project_pulse from agent_util.py during execution, establishing dependencies and influencing core module functionality analysis and processing.. [6]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates and configures the ReportRenderer class to organize, process, and render context data from agent_core.py into structured reports for downstream services using the provided project_map.. [7]
- **`summary_models.py`**: Uses `summary_models.py`: Defines and manages module contexts, roles, dependencies, and public APIs for agent_core.py components using ModuleContext from summary_models.py.. [8]
- **`llm_util.py`**: Uses `llm_util.py`: Brings in the functionality of chat_llm module from llm_util, specifically for processing input messages into structured prompts, retrieving LLM responses, extracting pertinent information, and managing errors during execution within agent_core.py. [9]
- **`memory_core.py`**: Uses `memory_core.py`: Creates an instance of ChromaMemory to encapsulate memory records as documents in the Chroma database and define query operations for managing metadata.; Manages and updates memory records by generating unique IDs, creating combined metadata, updating metadata with last used turn, evaluating helpfulness scores to delete low-score or stale memories, and retrieving metadata from the ChromaMemory class.. [10]
- **`agent_config.py`**: Imports `agent_config.py`. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `5e0bf5` [1]: Analyzes code structure, synthesizes system summary, renders detailed report based on processed input _(Source: Synthesis (based on [3], [2]))_
> 🆔 `1e9a0c` [2]: Synthesizes system summary and renders report based on processed data _(Source: class CrawlerAgent)_
> 🆔 `0753df` [3]: Runs CrawlerAgent by initializing memory, fetching project map and processing order, synthesizing system summary, rendering report, cleaning memories, and returning completion response. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `9e6382` [4]: Uses `semantic_gatekeeper.py`: Installs and configures gatekeeper for data processing before passing to agent_core.py. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `1d7d1e` [5]: Uses `map_synthesizer.py`: Orchestrates the synthesis of modules into categorized groups, synthesizes each group, then synthesizes overall system architecture. _(Source: Import map_synthesizer.py)_
> 🆔 `4248ea` [6]: Uses `agent_util.py`: Instructs agent_core.py to call project_pulse from agent_util.py during execution, establishing dependencies and influencing core module functionality analysis and processing.. _(Source: Import agent_util.py)_
> 🆔 `b6b1ba` [7]: Uses `report_renderer.py`: Instantiates and configures the ReportRenderer class to organize, process, and render context data from agent_core.py into structured reports for downstream services using the provided project_map.. _(Source: Import report_renderer.py)_
> 🆔 `77da93` [8]: Uses `summary_models.py`: Defines and manages module contexts, roles, dependencies, and public APIs for agent_core.py components using ModuleContext from summary_models.py.. _(Source: Import summary_models.py)_
> 🆔 `e8a204` [9]: Uses `llm_util.py`: Brings in the functionality of chat_llm module from llm_util, specifically for processing input messages into structured prompts, retrieving LLM responses, extracting pertinent information, and managing errors during execution within agent_core.py. _(Source: Import llm_util.py)_
> 🆔 `c28791` [10]: Uses `memory_core.py`: Creates an instance of ChromaMemory to encapsulate memory records as documents in the Chroma database and define query operations for managing metadata.; Manages and updates memory records by generating unique IDs, creating combined metadata, updating metadata with last used turn, evaluating helpfulness scores to delete low-score or stale memories, and retrieving metadata from the ChromaMemory class.. _(Source: Import memory_core.py)_
> 🆔 `d23947` [11]: Imports `agent_config.py`. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Orchestrates service execution by delegating tasks to underlying utilities

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns ProjectGraph as a dictionary mapping string keys to any values [2]
- **`🔌 class ProjectSummarizer`**: Organizes project dependencies, computes processing order, and dynamically generates context data based on source code analysis and critical requirements [3]
- **`🔌 project_pulse`**: Analyzes project structure by constructing dependency graph, summarizing modules, and generating contexts [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Iteratively refines module contexts through cycles, updating based on source code, upstream API, and critique instructions [5]
- **`🔒 _create_module_context`**: Generates module context by contextualizing module with critique instruction [6]

### 🔗 Uses (Upstream)
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer and executes its run() method to analyze code structure and return a dependency graph as JSON, providing insights into target_file_path's dependencies.. [7]
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: Analyzes module context, identifies dependencies, synthesizes role based on usage patterns using ModuleContextualizer class instantiated with path, graph, and dep_contexts arguments.. [8]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper to assemble prompts, send them to LLM, parse responses, critique style against banned terms, verify grounding if source provided, and return formatted JSON description.. [9]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates an instance of ReportRenderer to organize, process, and render context data into structured reports for downstream services.. [10]
- **`map_critic.py`**: Uses `map_critic.py`: Creates an instance of MapCritic using gatekeeper as argument. [11]
- **`summary_models.py`**: Uses `summary_models.py`: Manages and instantiates ModuleContext objects, creates unique identifiers using SHA1 hashing, updates module roles with placeholders, defines claim-based APIs, collects alerts, and organizes module states, dependencies, and contexts within agent_util.py by leveraging the capabilities defined in summary_models.py.. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `0ae3b9` [1]: Orchestrates service execution by delegating tasks to underlying utilities _(Source: Synthesis (based on [6], [5], [4], [3], [2]))_
> 🆔 `ef5724` [2]: Assigns ProjectGraph as a dictionary mapping string keys to any values _(Source: ProjectGraph)_
> 🆔 `b3b652` [3]: Organizes project dependencies, computes processing order, and dynamically generates context data based on source code analysis and critical requirements _(Source: class ProjectSummarizer)_
> 🆔 `a3fc6e` [4]: Analyzes project structure by constructing dependency graph, summarizing modules, and generating contexts _(Source: project_pulse)_
> 🆔 `4a219d` [5]: Iteratively refines module contexts through cycles, updating based on source code, upstream API, and critique instructions _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `3b5bbe` [6]: Generates module context by contextualizing module with critique instruction _(Source: _create_module_context)_
> 🆔 `25cfae` [7]: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer and executes its run() method to analyze code structure and return a dependency graph as JSON, providing insights into target_file_path's dependencies.. _(Source: Import graph_analyzer.py)_
> 🆔 `99f698` [8]: Uses `module_contextualizer.py`: Analyzes module context, identifies dependencies, synthesizes role based on usage patterns using ModuleContextualizer class instantiated with path, graph, and dep_contexts arguments.. _(Source: Import module_contextualizer.py)_
> 🆔 `777231` [9]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper to assemble prompts, send them to LLM, parse responses, critique style against banned terms, verify grounding if source provided, and return formatted JSON description.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `6c121c` [10]: Uses `report_renderer.py`: Instantiates an instance of ReportRenderer to organize, process, and render context data into structured reports for downstream services.. _(Source: Import report_renderer.py)_
> 🆔 `92f6c6` [11]: Uses `map_critic.py`: Creates an instance of MapCritic using gatekeeper as argument. _(Source: Import map_critic.py)_
> 🆔 `c5a952` [12]: Uses `summary_models.py`: Manages and instantiates ModuleContext objects, creates unique identifiers using SHA1 hashing, updates module roles with placeholders, defines claim-based APIs, collects alerts, and organizes module states, dependencies, and contexts within agent_util.py by leveraging the capabilities defined in summary_models.py.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes code components, generates module skeletons, and orchestrates documentation transformation

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes, interprets, and transforms code components within specified module context [2]
- **`🔌 class SkeletonTransformer`**: Manages the structure and documentation of function definitions and class bodies, modifying content as needed. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes components by examining global variables, functions, and classes in specified module context. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Transforms abstract syntax tree by adding ellipsis to function and class bodies, removing docstrings from classes, and unparse back to source code [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Modifies function definition body to include ellipsis constant [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes first docstring line from class definition body [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Modifies function definition body by appending ellipsis expression [8]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Analyzes and manages module identifiers, public APIs, dependencies, claims, and alerts using methods from `summary_models.py` in `component_analyst.py`.. [9]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper to configure component logic and execution parameters for analyst module interaction.. [10]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `0740a0` [1]: Analyzes code components, generates module skeletons, and orchestrates documentation transformation _(Source: Synthesis (based on [4], [7], [3], [5], [8], [2], [6]))_
> 🆔 `9ad4f4` [2]: Analyzes, interprets, and transforms code components within specified module context _(Source: class ComponentAnalyst)_
> 🆔 `43d799` [3]: Manages the structure and documentation of function definitions and class bodies, modifying content as needed. _(Source: class SkeletonTransformer)_
> 🆔 `15dcff` [4]: Analyzes components by examining global variables, functions, and classes in specified module context. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `7ccace` [5]: Transforms abstract syntax tree by adding ellipsis to function and class bodies, removing docstrings from classes, and unparse back to source code _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `c00299` [6]: Modifies function definition body to include ellipsis constant _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `4256d2` [7]: Removes first docstring line from class definition body _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `7e2976` [8]: Modifies function definition body by appending ellipsis expression _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `770f9b` [9]: Uses `summary_models.py`: Analyzes and manages module identifiers, public APIs, dependencies, claims, and alerts using methods from `summary_models.py` in `component_analyst.py`.. _(Source: Import summary_models.py)_
> 🆔 `ef2392` [10]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper to configure component logic and execution parameters for analyst module interaction.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Analyzes dependency context, sanitizes input text, and generates explanations based on analysis results

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Analyzes dependency context, sanitizes input text, and generates explanations based on analysis results [2]
- **`🔌 clean_ref`**: Removes bracketed reference patterns from input text using regex and trims whitespace [3]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes dependency context for each import, determines used symbols, extracts relevant state and logic, and generates explanation labels based on analysis results. [4]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Analyzes dependencies by creating unique identifiers, managing module contexts with explanations and claim placeholders, adding dependency context to modules, and combining text, references, module paths, and explanations using ModuleContext class and Claim function.. [5]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class and invokes its run() method to generate and analyze prompts for language models, ensuring adherence to banned adjectives defined in BANNED_ADJECTIVES constant from semantic_gatekeeper.py.; Integrates configuration parameters and semantic validation routines from semantic_gatekeeper.py to enhance data handling and model execution fidelity in dependency_analyst.py. [6]
- **`task_executor.py`**: Uses `task_executor.py`: Instantiates the TaskExecutor class. [7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1b46c6` [1]: Analyzes dependency context, sanitizes input text, and generates explanations based on analysis results _(Source: Synthesis (based on [3], [4], [2]))_
> 🆔 `e15564` [2]: Analyzes dependency context, sanitizes input text, and generates explanations based on analysis results _(Source: class DependencyAnalyst)_
> 🆔 `4033bb` [3]: Removes bracketed reference patterns from input text using regex and trims whitespace _(Source: clean_ref)_
> 🆔 `bbf90e` [4]: Analyzes dependency context for each import, determines used symbols, extracts relevant state and logic, and generates explanation labels based on analysis results. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `18d9d4` [5]: Uses `summary_models.py`: Analyzes dependencies by creating unique identifiers, managing module contexts with explanations and claim placeholders, adding dependency context to modules, and combining text, references, module paths, and explanations using ModuleContext class and Claim function.. _(Source: Import summary_models.py)_
> 🆔 `3632a0` [6]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper class and invokes its run() method to generate and analyze prompts for language models, ensuring adherence to banned adjectives defined in BANNED_ADJECTIVES constant from semantic_gatekeeper.py.; Integrates configuration parameters and semantic validation routines from semantic_gatekeeper.py to enhance data handling and model execution fidelity in dependency_analyst.py. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `d481fd` [7]: Uses `task_executor.py`: Instantiates the TaskExecutor class. _(Source: Import task_executor.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Analyzes project documentation components, organizes modules, critiques style against banned terms, and orchestrates feedback integration

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Organizes, aggregates, analyzes, and evaluates project documentation components [2]
- **`🔌 🔌 MapCritic.critique`**: Parses project map content into modules, analyzes each module's instructions, and appends critiques to list up to three [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper within __init__ method and calls run() function in map_critic.py. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `e3a269` [1]: Analyzes project documentation components, organizes modules, critiques style against banned terms, and orchestrates feedback integration _(Source: Synthesis (based on [3], [2]))_
> 🆔 `dfc021` [2]: Organizes, aggregates, analyzes, and evaluates project documentation components _(Source: class MapCritic)_
> 🆔 `294d9f` [3]: Parses project map content into modules, analyzes each module's instructions, and appends critiques to list up to three _(Source: 🔌 MapCritic.critique)_
> 🆔 `e30b04` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper within __init__ method and calls run() function in map_critic.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` Orchestrates the synthesis of modules into categorized groups, synthesizes each group, then synthesizes overall system architecture

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Organizes and categorizes modules into structured groups for systematic processing [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Aggregates modules into categorized groups based on processing order, synthesizes each group, then synthesizes overall system [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Analyzes and integrates module configurations using ModuleContext from summary_models.py in map_synthesizer.py. [4]
- **`llm_util.py`**: Uses `llm_util.py`: Invokes the chat_llm function to generate responses based on parsed input messages and constructed prompts, extracting content and handling exceptions as necessary for downstream processing in map_synthesizer.py.. [5]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Initializes and configures the SemanticGatekeeper instance within map_synthesizer.py to manage system configuration, define model execution parameters, and orchestrate prompt generation for language models.. [6]
- **`agent_config.py`**: Uses `agent_config.py`: Determines the model identifier for processing data within map_synthesizer.py using constants from agent_config.py. [7]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `15c2e3` [1]: Orchestrates the synthesis of modules into categorized groups, synthesizes each group, then synthesizes overall system architecture _(Source: Synthesis (based on [2], [3]))_
> 🆔 `16518b` [2]: Organizes and categorizes modules into structured groups for systematic processing _(Source: class MapSynthesizer)_
> 🆔 `c597ac` [3]: Aggregates modules into categorized groups based on processing order, synthesizes each group, then synthesizes overall system _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `eb4591` [4]: Uses `summary_models.py`: Analyzes and integrates module configurations using ModuleContext from summary_models.py in map_synthesizer.py. _(Source: Import summary_models.py)_
> 🆔 `ff7f98` [5]: Uses `llm_util.py`: Invokes the chat_llm function to generate responses based on parsed input messages and constructed prompts, extracting content and handling exceptions as necessary for downstream processing in map_synthesizer.py.. _(Source: Import llm_util.py)_
> 🆔 `60f444` [6]: Uses `semantic_gatekeeper.py`: Initializes and configures the SemanticGatekeeper instance within map_synthesizer.py to manage system configuration, define model execution parameters, and orchestrate prompt generation for language models.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `25f419` [7]: Uses `agent_config.py`: Determines the model identifier for processing data within map_synthesizer.py using constants from agent_config.py. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Organizes, processes, and renders context data into structured reports for downstream services

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Organizes and processes data for report generation [2]
- **`🔌 replace_ref`**: Parses text for reference patterns, substitutes them with unique identifiers stored in claim_map [3]
- **`🔌 sub`**: Manages claim references by assigning unique IDs, replacing refs in string with their corresponding ID [4]
- **`🔌 🔌 ReportRenderer.render`**: Collects context data, organizes by categories, renders module details, writes to output file [5]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Initializes summary model configuration by importing ModuleContext and instantiating the class with context_map and output_file parameters, invoking __init__ and _render_module methods.. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `79d616` [1]: Organizes, processes, and renders context data into structured reports for downstream services _(Source: Synthesis (based on [3], [5], [4], [2]))_
> 🆔 `da76a8` [2]: Organizes and processes data for report generation _(Source: class ReportRenderer)_
> 🆔 `637c6c` [3]: Parses text for reference patterns, substitutes them with unique identifiers stored in claim_map _(Source: replace_ref)_
> 🆔 `c714ba` [4]: Manages claim references by assigning unique IDs, replacing refs in string with their corresponding ID _(Source: sub)_
> 🆔 `83831d` [5]: Collects context data, organizes by categories, renders module details, writes to output file _(Source: 🔌 ReportRenderer.render)_
> 🆔 `fa66f4` [6]: Uses `summary_models.py`: Initializes summary model configuration by importing ModuleContext and instantiating the class with context_map and output_file parameters, invoking __init__ and _render_module methods.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Manages system configuration, defines model execution parameters, and orchestrates prompt generation for language models

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines a set containing disallowed adjectives for use in code [2]
- **`🔌 class SemanticGatekeeper`**: Organizes, analyzes, and structures data flow within the system [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Assembles final prompt, sends to LLM for analysis, parses response into JSON with specified key, critiques style against banned terms, verifies grounding if source provided, and returns formatted JSON description. [4]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Uses `llm_util.py`: Calls the `chat_llm` function from `llm_util.py`, passing in the `DEFAULT_MODEL` and either `messages` or `verify_prompt` to generate responses.. [5]
- **`agent_config.py`**: Uses `agent_config.py`: Defines and passes the model identifier to downstream functions for LLM interaction in semantic_gatekeeper.py. [6]

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

> 🆔 `e56834` [1]: Manages system configuration, defines model execution parameters, and orchestrates prompt generation for language models _(Source: Synthesis (based on [4], [3], [2]))_
> 🆔 `f35389` [2]: Defines a set containing disallowed adjectives for use in code _(Source: BANNED_ADJECTIVES)_
> 🆔 `b350d6` [3]: Organizes, analyzes, and structures data flow within the system _(Source: class SemanticGatekeeper)_
> 🆔 `a1e4e2` [4]: Assembles final prompt, sends to LLM for analysis, parses response into JSON with specified key, critiques style against banned terms, verifies grounding if source provided, and returns formatted JSON description. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `533ba0` [5]: Uses `llm_util.py`: Calls the `chat_llm` function from `llm_util.py`, passing in the `DEFAULT_MODEL` and either `messages` or `verify_prompt` to generate responses.. _(Source: Import llm_util.py)_
> 🆔 `ae1cf0` [6]: Uses `agent_config.py`: Defines and passes the model identifier to downstream functions for LLM interaction in semantic_gatekeeper.py. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` Orchestrates task execution, analyzes context, generates structured plans, delegates to underlying services, and synthesizes results

**Impact Analysis:** Changes to this module will affect: dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Handles the processing of gatekeeper responses and organizes execution flow [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Analyzes goal context to generate structured plan, executes sub-questions, gathers evidence, and summarizes intent as concise action verb. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper as gatekeeper and calls its run method within task_executor.py. [4]

### 👥 Used By (Downstream)
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `35b3be` [1]: Orchestrates task execution, analyzes context, generates structured plans, delegates to underlying services, and synthesizes results _(Source: Synthesis (based on [2], [3]))_
> 🆔 `ada7b1` [2]: Handles the processing of gatekeeper responses and organizes execution flow _(Source: class TaskExecutor)_
> 🆔 `b079d0` [3]: Analyzes goal context to generate structured plan, executes sub-questions, gathers evidence, and summarizes intent as concise action verb. _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `bd4820` [4]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper as gatekeeper and calls its run method within task_executor.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Provides parsing, prompting, and response generation functionality to downstream components like agent_core.py, map_synthesizer.py, and semantic_gatekeeper.py

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Parses input messages, constructs prompt, calls LLM interface to generate response, extracts content, handles exceptions [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f4d2c8` [1]: Provides parsing, prompting, and response generation functionality to downstream components like agent_core.py, map_synthesizer.py, and semantic_gatekeeper.py _(Source: Synthesis (based on [2]))_
> 🆔 `efe142` [2]: Parses input messages, constructs prompt, calls LLM interface to generate response, extracts content, handles exceptions _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Analyzes code structure, builds dependency graph using depth-first search

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Analyzes code structure, collects module data, records interactions, and captures entity details [2]
- **`🔌 class GraphAnalyzer`**: Collects, parses, and organizes project files and dependencies using depth-first search algorithm [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes class definition from current context and header stack [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Maintains current context stack by popping when leaving function definition [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Updates current statement attribute to None [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Collects annotated variable names and their source code for globals [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Captures global assignments from module node [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Records function call interactions in cross-module map [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Captures class name, parses source code, retrieves docstring, extracts bases, constructs header, stores entity data [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Captures function signature details, headers, docstrings, source code snippets, implementation status, and categorizes functions as methods or standalone based on context path. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Collects external module names from import node [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Collects external module names and relative import paths for ImportFrom nodes, updates state accordingly [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records interactions for name nodes [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Updates current statement reference within visitor [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds dependency graph using depth-first search, populates dependents dictionary, then returns the graph as JSON output. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `4e3c1e` [1]: Analyzes code structure, builds dependency graph using depth-first search _(Source: Synthesis (based on [10], [11], [3], [9], [15], [16], [14], [2], [7], [5], [12], [6], [4], [8], [13]))_
> 🆔 `57bf20` [2]: Analyzes code structure, collects module data, records interactions, and captures entity details _(Source: class CodeEntityVisitor)_
> 🆔 `1988e3` [3]: Collects, parses, and organizes project files and dependencies using depth-first search algorithm _(Source: class GraphAnalyzer)_
> 🆔 `bea5bd` [4]: Removes class definition from current context and header stack _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `91d05f` [5]: Maintains current context stack by popping when leaving function definition _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `ab60fa` [6]: Updates current statement attribute to None _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `6a1f01` [7]: Collects annotated variable names and their source code for globals _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `d703e4` [8]: Captures global assignments from module node _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `2a13c7` [9]: Records function call interactions in cross-module map _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `0f7084` [10]: Captures class name, parses source code, retrieves docstring, extracts bases, constructs header, stores entity data _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `0fb7a3` [11]: Captures function signature details, headers, docstrings, source code snippets, implementation status, and categorizes functions as methods or standalone based on context path. _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `a08b0b` [12]: Collects external module names from import node _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `fb5133` [13]: Collects external module names and relative import paths for ImportFrom nodes, updates state accordingly _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `51491a` [14]: Records interactions for name nodes _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `5013f1` [15]: Updates current statement reference within visitor _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `50db0d` [16]: Builds dependency graph using depth-first search, populates dependents dictionary, then returns the graph as JSON output. _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Encapsulates memory records as documents in Chroma database and defines query operations

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Manages memory records, retrieves and updates metadata [2]
- **`🔌 class MemoryInterface`**: Encapsulates memory data structure and defines query interface [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Generates unique ID, creates combined metadata, updates it with optional additional data, then adds memory record to Chroma collection [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Retrieves all memories, evaluates helpfulness and last used turn, deletes low-score or stale memories [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Updates memory metadata with last used turn [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Retrieves metadata for specified memory, updates its helpfulness value, and saves modified metadata to the database [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `e8f820` [1]: Encapsulates memory records as documents in Chroma database and defines query operations _(Source: Synthesis (based on [3], [5], [7], [2], [6], [4], [8]))_
> 🆔 `6298ae` [2]: Manages memory records, retrieves and updates metadata _(Source: class ChromaMemory)_
> 🆔 `29648e` [3]: Encapsulates memory data structure and defines query interface _(Source: class MemoryInterface)_
> 🆔 `96885f` [4]: Generates unique ID, creates combined metadata, updates it with optional additional data, then adds memory record to Chroma collection _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `31b226` [5]: Retrieves all memories, evaluates helpfulness and last used turn, deletes low-score or stale memories _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `79533b` [6]: Updates memory metadata with last used turn _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `348380` [7]: Retrieves metadata for specified memory, updates its helpfulness value, and saves modified metadata to the database _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Classifies modules based on their attributes, dependencies, and functionality using static analysis techniques

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Classifies modules based on their characteristics and relationships. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Determines module archetype by name, source code, entities, dependencies, functions, classes, and global assignments [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1af426` [1]: Classifies modules based on their attributes, dependencies, and functionality using static analysis techniques _(Source: Synthesis (based on [2], [3], [4]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `b7f885` [3]: Classifies modules based on their characteristics and relationships. _(Source: class ModuleClassifier)_
> 🆔 `dfb806` [4]: Determines module archetype by name, source code, entities, dependencies, functions, classes, and global assignments _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Analyzes context, identifies dependencies, synthesizes role based on usage patterns

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Analyzes module context, identifies dependencies, synthesizes role based on usage patterns [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyzes module context by checking for errors, performing component analysis, dependency analysis, systemic synthesis, and alert handling. [3]

### 🔗 Uses (Upstream)
- **`component_analyst.py`**: Uses `component_analyst.py`: Instantiates ComponentAnalyst from component_analyst module; Analyzes components by examining global variables, functions, and classes in specified module context using ComponentAnalyst class from component_analyst.py. [4]
- **`module_classifier.py`**: Uses `module_classifier.py`: Instantiates ModuleClassifier with module_name and data to classify modules based on their attributes, dependencies, and functionality using static analysis techniques from module_classifier.py; Creates an instance of ModuleClassifier to analyze and classify modules based on their attributes, dependencies, and functionality.. [5]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper for prompt assembly and LLM analysis execution.. [6]
- **`task_executor.py`**: Uses `task_executor.py`: Creates an instance of TaskExecutor by passing self.gatekeeper as the parameter to its constructor within module_contextualizer.py. [7]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext objects from summary_models.py by calling the constructor method __init__ with arguments such as file_path and graph_data, then employs the contextualize_module function to generate module context details.; Analyzes module context, generates unique identifiers using concatenated text and SHA1 hashing, sets module roles with associated claims from source modules, manages alerts related to analysis errors or incomplete implementations, and defines dependencies between modules through placeholders.. [8]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Instantiates an instance of DependencyAnalyst using gatekeeper and task_executor attributes. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ad8e43` [1]: Analyzes context, identifies dependencies, synthesizes role based on usage patterns _(Source: Synthesis (based on [2], [3]))_
> 🆔 `cc099f` [2]: Analyzes module context, identifies dependencies, synthesizes role based on usage patterns _(Source: class ModuleContextualizer)_
> 🆔 `df4695` [3]: Analyzes module context by checking for errors, performing component analysis, dependency analysis, systemic synthesis, and alert handling. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `7266d3` [4]: Uses `component_analyst.py`: Instantiates ComponentAnalyst from component_analyst module; Analyzes components by examining global variables, functions, and classes in specified module context using ComponentAnalyst class from component_analyst.py. _(Source: Import component_analyst.py)_
> 🆔 `529844` [5]: Uses `module_classifier.py`: Instantiates ModuleClassifier with module_name and data to classify modules based on their attributes, dependencies, and functionality using static analysis techniques from module_classifier.py; Creates an instance of ModuleClassifier to analyze and classify modules based on their attributes, dependencies, and functionality.. _(Source: Import module_classifier.py)_
> 🆔 `9f0a23` [6]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper for prompt assembly and LLM analysis execution.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `d0abac` [7]: Uses `task_executor.py`: Creates an instance of TaskExecutor by passing self.gatekeeper as the parameter to its constructor within module_contextualizer.py. _(Source: Import task_executor.py)_
> 🆔 `4c9a53` [8]: Uses `summary_models.py`: Instantiates ModuleContext objects from summary_models.py by calling the constructor method __init__ with arguments such as file_path and graph_data, then employs the contextualize_module function to generate module context details.; Analyzes module context, generates unique identifiers using concatenated text and SHA1 hashing, sets module roles with associated claims from source modules, manages alerts related to analysis errors or incomplete implementations, and defines dependencies between modules through placeholders.. _(Source: Import summary_models.py)_
> 🆔 `1630e3` [9]: Uses `dependency_analyst.py`: Instantiates an instance of DependencyAnalyst using gatekeeper and task_executor attributes. _(Source: Import dependency_analyst.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Represents structured summary of system components, stores relationships between modules, encapsulates module configurations, and defines the purpose and capabilities of each component

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Creates unique identifiers by combining text, reference, source module and computing SHA1 hash [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Manages module state, dependencies, public API, alerts, and claim placeholders through various methods [5]
- **`🔌 🔌 Claim.id`**: Creates unique identifier by concatenating text, reference, source module and computing SHA1 hash [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Collects alerts and appends them to internal list [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Adds dependency context to module by combining explanation and claim placeholders [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Manages dependent module contexts by storing provided explanation and placeholders in key_dependents dictionary [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds public API entry by merging description and placeholders, storing in dictionary with supporting claim IDs [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Combines module text with claim placeholders, updates module role state [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b0e0a0` [1]: Represents structured summary of system components, stores relationships between modules, encapsulates module configurations, and defines the purpose and capabilities of each component _(Source: Synthesis (based on [8], [3], [7], [10], [11], [4], [6], [2], [9], [5]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `43bd09` [3]: Creates unique identifiers by combining text, reference, source module and computing SHA1 hash _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `fe69d4` [5]: Manages module state, dependencies, public API, alerts, and claim placeholders through various methods _(Source: class ModuleContext)_
> 🆔 `cce842` [6]: Creates unique identifier by concatenating text, reference, source module and computing SHA1 hash _(Source: 🔌 Claim.id)_
> 🆔 `4c3dca` [7]: Collects alerts and appends them to internal list _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `3b0a7c` [8]: Adds dependency context to module by combining explanation and claim placeholders _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `dbd7bd` [9]: Manages dependent module contexts by storing provided explanation and placeholders in key_dependents dictionary _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `71ddaf` [10]: Adds public API entry by merging description and placeholders, storing in dictionary with supporting claim IDs _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `a07c66` [11]: Combines module text with claim placeholders, updates module role state _(Source: 🔌 ModuleContext.set_module_role)_
</details>

---
## 🔧 Configuration

## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Assigns maximum context length to 4096 characters [2]
- **`🔌 DEFAULT_MODEL`**: Assigns model identifier string to global variable for subsequent use in program [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `449512` [1]: Defines configuration constants. _(Source: Archetype)_
> 🆔 `eb1d4c` [2]: Assigns maximum context length to 4096 characters _(Source: CONTEXT_LIMIT)_
> 🆔 `8d9460` [3]: Assigns model identifier string to global variable for subsequent use in program _(Source: DEFAULT_MODEL)_
</details>

---