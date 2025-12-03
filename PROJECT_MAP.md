# Project Context Map

## 🏛️ System Architecture
The system is architecturally divided into distinct layers, each playing a crucial role in processing and managing data flow. At the heart of this architecture lies the Entry Point Layer, represented by agent_graph_main.py. This module acts as the central orchestrator, initiating the entire process by launching the CrawlerAgent. It sets the stage for how data will be handled throughout the system, ensuring that each subsequent step is executed in a controlled and synchronized manner.

---

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates data processing by initializing CrawlerAgent, invoking its execution flow, managing state data, synthesizing system summary, rendering reports, and cleaning memories [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Retrieves command-line arguments from ArgumentParser instance [2]
- **`🔌 goal`**: Assigns command line goal argument to local variable for further processing [3]
- **`🔌 main`**: Iterates through target folder's files, identifies main script, initializes CrawlerAgent, runs it, then reports completion [4]
- **`🔌 parser`**: Creates an argument parser for command-line input [5]
- **`🔌 result`**: Calls main function to process goal and target folder [6]
- **`🔌 target_folder`**: Assigns target folder argument to local variable for processing [7]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Executes CrawlerAgent to initiate memory cleanup and report generation processes.. [8]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ea11f8` [1]: Orchestrates data processing by initializing CrawlerAgent, invoking its execution flow, managing state data, synthesizing system summary, rendering reports, and cleaning memories _(Source: Synthesis)_
> 🆔 `e31ec8` [2]: Retrieves command-line arguments from ArgumentParser instance _(Source: args)_
> 🆔 `e0c95c` [3]: Assigns command line goal argument to local variable for further processing _(Source: goal)_
> 🆔 `8a5967` [4]: Iterates through target folder's files, identifies main script, initializes CrawlerAgent, runs it, then reports completion _(Source: main)_
> 🆔 `880c36` [5]: Creates an argument parser for command-line input _(Source: parser)_
> 🆔 `2b4862` [6]: Calls main function to process goal and target folder _(Source: result)_
> 🆔 `aa8b3e` [7]: Assigns target folder argument to local variable for processing _(Source: target_folder)_
> 🆔 `4f542b` [8]: Uses `agent_core.py`: Executes CrawlerAgent to initiate memory cleanup and report generation processes.. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Orchestrates memory cleanup, triggers report generation, synthesizes system summary, manages module contexts

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Manages state data processing workflow [2]
- **`🔌 🔌 CrawlerAgent.run`**: Manages CrawlerAgent's execution flow, initializes memory, retrieves project map and processing order, synthesizes system summary using gatekeeper and synthesizer, renders report renderer, cleans memories over five turns, and returns analysis completion response. [3]

### 🔗 Uses (Upstream)
- **`map_synthesizer.py`**: Uses `map_synthesizer.py`: Instantiates the MapSynthesizer class with the gatekeeper parameter to organize, aggregate, and summarize technical data into cohesive system narratives for agent_core.py. [4]
- **`agent_config.py`**: Imports `agent_config.py`. [5]
- **`memory_core.py`**: Uses `memory_core.py`: Instantiates ChromaMemory from memory_core.py and configures interaction with memory metadata and helpfulness values in agent_core.py; Instantiates and configures ChromaMemory from memory_core for agent operations, retrieves memory data, updates metadata based on helpfulness criteria, and cleans up unused memories as part of the agent's workflow.. [6]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates the ReportRenderer class in agent_core.py by calling its constructor and passing `project_map` and `system_summary` arguments.. [7]
- **`summary_models.py`**: Uses `summary_models.py`: Populates and manages the key_dependencies dictionary, ModuleContext instances, and public_api definitions within agent_core.py by aggregating explanation and claim placeholders from summary_models to construct full text outputs and define API endpoints.. [8]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper for structured response processing and validation in agent_core.py. [9]
- **`agent_util.py`**: Uses `agent_util.py`: Calls `project_pulse` function from `agent_core.py` within its run method, passing target root directory as argument to analyze project graph and return analysis results.. [10]
- **`llm_util.py`**: Uses `llm_util.py`: Invokes the `chat_llm` function from `llm_util.py`, passing in input parameters, then processes and strips LLM responses through downstream content filtering modules before returning the cleaned message to agent_core.. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `28fc7d` [1]: Orchestrates memory cleanup, triggers report generation, synthesizes system summary, manages module contexts _(Source: Synthesis)_
> 🆔 `94ef51` [2]: Manages state data processing workflow _(Source: class CrawlerAgent)_
> 🆔 `143edc` [3]: Manages CrawlerAgent's execution flow, initializes memory, retrieves project map and processing order, synthesizes system summary using gatekeeper and synthesizer, renders report renderer, cleans memories over five turns, and returns analysis completion response. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `15dc70` [4]: Uses `map_synthesizer.py`: Instantiates the MapSynthesizer class with the gatekeeper parameter to organize, aggregate, and summarize technical data into cohesive system narratives for agent_core.py. _(Source: Import map_synthesizer.py)_
> 🆔 `d23947` [5]: Imports `agent_config.py`. _(Source: Import agent_config.py)_
> 🆔 `00b890` [6]: Uses `memory_core.py`: Instantiates ChromaMemory from memory_core.py and configures interaction with memory metadata and helpfulness values in agent_core.py; Instantiates and configures ChromaMemory from memory_core for agent operations, retrieves memory data, updates metadata based on helpfulness criteria, and cleans up unused memories as part of the agent's workflow.. _(Source: Import memory_core.py)_
> 🆔 `60a145` [7]: Uses `report_renderer.py`: Instantiates the ReportRenderer class in agent_core.py by calling its constructor and passing `project_map` and `system_summary` arguments.. _(Source: Import report_renderer.py)_
> 🆔 `866703` [8]: Uses `summary_models.py`: Populates and manages the key_dependencies dictionary, ModuleContext instances, and public_api definitions within agent_core.py by aggregating explanation and claim placeholders from summary_models to construct full text outputs and define API endpoints.. _(Source: Import summary_models.py)_
> 🆔 `d3eb1c` [9]: Uses `semantic_gatekeeper.py`: Instantiates SemanticGatekeeper for structured response processing and validation in agent_core.py. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `e69d85` [10]: Uses `agent_util.py`: Calls `project_pulse` function from `agent_core.py` within its run method, passing target root directory as argument to analyze project graph and return analysis results.. _(Source: Import agent_util.py)_
> 🆔 `e5d2ff` [11]: Uses `llm_util.py`: Invokes the `chat_llm` function from `llm_util.py`, passing in input parameters, then processes and strips LLM responses through downstream content filtering modules before returning the cleaned message to agent_core.. _(Source: Import llm_util.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Orchestrates the execution of agent functions, manages dependencies between modules, generates structured reports from analysis results, and triggers downstream processing pipelines for actionable insights in real-time scenarios.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Declares ProjectGraph as a dictionary mapping string keys to any values [2]
- **`🔌 class ProjectSummarizer`**: Centralizes project dependencies, computes processing order, and generates module contexts [3]
- **`🔌 project_pulse`**: Validates file path, logs start message, analyzes project graph, summarizes contexts, and returns results [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Iteratively generates module contexts by refining paths, checking critiques, and updating cache [5]
- **`🔒 _create_module_context`**: Generates module context by contextualizing module using ModuleContextualizer [6]

### 🔗 Uses (Upstream)
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer and populates target_file_path parameter. [7]
- **`map_critic.py`**: Uses `map_critic.py`: Analyzes module content and critiques based on provided feedback. [8]
- **`report_renderer.py`**: Uses `report_renderer.py`: Instantiates the ReportRenderer class using contexts from agent_core.py and agent_util.py modules, specifying an output file path for report generation.. [9]
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: Analyzes module context to synthesize concise role description without referencing specific name. [10]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext and Claim objects from summary_models.py to manage module data, dependencies, context, alerts, and claims in agent_util.py; Constructs unique identifiers by combining relevant text, claims, and source module information, then hashing the combined string using a hashing algorithm. [11]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Initializes the SemanticGatekeeper instance to manage structured response construction and validation logic within agent_util.py.. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f24ade` [1]: Orchestrates the execution of agent functions, manages dependencies between modules, generates structured reports from analysis results, and triggers downstream processing pipelines for actionable insights in real-time scenarios. _(Source: Synthesis)_
> 🆔 `c4aec0` [2]: Declares ProjectGraph as a dictionary mapping string keys to any values _(Source: ProjectGraph)_
> 🆔 `2a5c65` [3]: Centralizes project dependencies, computes processing order, and generates module contexts _(Source: class ProjectSummarizer)_
> 🆔 `1d922f` [4]: Validates file path, logs start message, analyzes project graph, summarizes contexts, and returns results _(Source: project_pulse)_
> 🆔 `a2ec1a` [5]: Iteratively generates module contexts by refining paths, checking critiques, and updating cache _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `47bd06` [6]: Generates module context by contextualizing module using ModuleContextualizer _(Source: _create_module_context)_
> 🆔 `ea43f9` [7]: Uses `graph_analyzer.py`: Instantiates GraphAnalyzer and populates target_file_path parameter. _(Source: Import graph_analyzer.py)_
> 🆔 `918172` [8]: Uses `map_critic.py`: Analyzes module content and critiques based on provided feedback. _(Source: Import map_critic.py)_
> 🆔 `19b929` [9]: Uses `report_renderer.py`: Instantiates the ReportRenderer class using contexts from agent_core.py and agent_util.py modules, specifying an output file path for report generation.. _(Source: Import report_renderer.py)_
> 🆔 `a9abea` [10]: Uses `module_contextualizer.py`: Analyzes module context to synthesize concise role description without referencing specific name. _(Source: Import module_contextualizer.py)_
> 🆔 `4e6701` [11]: Uses `summary_models.py`: Instantiates ModuleContext and Claim objects from summary_models.py to manage module data, dependencies, context, alerts, and claims in agent_util.py; Constructs unique identifiers by combining relevant text, claims, and source module information, then hashing the combined string using a hashing algorithm. _(Source: Import summary_models.py)_
> 🆔 `de3b40` [12]: Uses `semantic_gatekeeper.py`: Initializes the SemanticGatekeeper instance to manage structured response construction and validation logic within agent_util.py.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes module structure, synthesizes role summaries of modules, generates code skeletons by transforming functions and classes into simplified forms

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes and interprets module structures, generating code skeletons for specified roles [2]
- **`🔌 class SkeletonTransformer`**: Transforms function, class, and async function nodes by modifying their bodies or docstrings [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Collects module information, analyzes global variables and functions for logic-only source code, identifies mechanisms, invariants, side effects, resolves dependencies, adds entries to context, and synthesizes class role summaries. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Parses source code into an AST, transforms functions to return ellipsis, modifies class definitions by removing docstrings and appending pass statement if needed, and then unparses the modified tree back to source code. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Creates new AST node with modified body containing an expression that yields Ellipsis constant [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from class definition, appends Pass if body empty [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Mutates FunctionDef node by adding Expr with Ellipsis constant to its body [8]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Analyzes and integrates module context, claims, and dependencies using ModuleContext and Claim from summary_models.py to process text inputs and generate summaries in component_analyst.py.; Analyzes components and constructs public API entries using ModuleContext and Claim classes from summary_models.py. [9]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Executes structured response validation and formatting tasks using SemanticGatekeeper class in component_analyst.py. [10]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f98151` [1]: Analyzes module structure, synthesizes role summaries of modules, generates code skeletons by transforming functions and classes into simplified forms _(Source: Synthesis)_
> 🆔 `2ae11b` [2]: Analyzes and interprets module structures, generating code skeletons for specified roles _(Source: class ComponentAnalyst)_
> 🆔 `6819f9` [3]: Transforms function, class, and async function nodes by modifying their bodies or docstrings _(Source: class SkeletonTransformer)_
> 🆔 `25a48f` [4]: Collects module information, analyzes global variables and functions for logic-only source code, identifies mechanisms, invariants, side effects, resolves dependencies, adds entries to context, and synthesizes class role summaries. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `759e0f` [5]: Parses source code into an AST, transforms functions to return ellipsis, modifies class definitions by removing docstrings and appending pass statement if needed, and then unparses the modified tree back to source code. _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `ea24f3` [6]: Creates new AST node with modified body containing an expression that yields Ellipsis constant _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `d49c36` [7]: Removes docstring from class definition, appends Pass if body empty _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `ba4954` [8]: Mutates FunctionDef node by adding Expr with Ellipsis constant to its body _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `62020d` [9]: Uses `summary_models.py`: Analyzes and integrates module context, claims, and dependencies using ModuleContext and Claim from summary_models.py to process text inputs and generate summaries in component_analyst.py.; Analyzes components and constructs public API entries using ModuleContext and Claim classes from summary_models.py. _(Source: Import summary_models.py)_
> 🆔 `498b43` [10]: Uses `semantic_gatekeeper.py`: Executes structured response validation and formatting tasks using SemanticGatekeeper class in component_analyst.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Analyzes dependencies between modules, invoking related functions to manage relationships and triggers updates in impacted components

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Establishes relationships between components, analyzes import usage patterns [2]
- **`🔌 clean_ref`**: Removes reference placeholders from text using regex pattern and trims whitespace [3]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes module dependencies by checking imports, used symbols, and related logic snippets. [4]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Constructs unique identifiers by combining relevant text, reference, source module data and applying hashing algorithms.; Analyzes dependencies, updates module context with explanations and claims from dependent modules, and manages public APIs for each module using ModuleContext and Claim objects.. [5]
- **`task_executor.py`**: Uses `task_executor.py`: Analyzes task execution dependencies and internal state variables to configure timeout settings for TaskExecutor in dependency_analyst.py; Instantiates TaskExecutor to enable task execution and interaction within dependency_analyst.py. [6]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Integrates SemanticGatekeeper to sanitize structured responses and enforce banned adjective filters in dependency_analyst.py. [7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `e62495` [1]: Analyzes dependencies between modules, invoking related functions to manage relationships and triggers updates in impacted components _(Source: Synthesis)_
> 🆔 `35ab89` [2]: Establishes relationships between components, analyzes import usage patterns _(Source: class DependencyAnalyst)_
> 🆔 `191d54` [3]: Removes reference placeholders from text using regex pattern and trims whitespace _(Source: clean_ref)_
> 🆔 `a59e60` [4]: Analyzes module dependencies by checking imports, used symbols, and related logic snippets. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `b45f97` [5]: Uses `summary_models.py`: Constructs unique identifiers by combining relevant text, reference, source module data and applying hashing algorithms.; Analyzes dependencies, updates module context with explanations and claims from dependent modules, and manages public APIs for each module using ModuleContext and Claim objects.. _(Source: Import summary_models.py)_
> 🆔 `b96219` [6]: Uses `task_executor.py`: Analyzes task execution dependencies and internal state variables to configure timeout settings for TaskExecutor in dependency_analyst.py; Instantiates TaskExecutor to enable task execution and interaction within dependency_analyst.py. _(Source: Import task_executor.py)_
> 🆔 `22a519` [7]: Uses `semantic_gatekeeper.py`: Integrates SemanticGatekeeper to sanitize structured responses and enforce banned adjective filters in dependency_analyst.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Orchestrates code analysis, builds project dependency graph, and extracts TODO comments

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Analyzes and organizes code structure, interactions, entities, and statements within a module. [2]
- **`🔌 class GraphAnalyzer`**: Analyzes project structure, builds dependency graph using DFS traversal, extracts TODO comments from source code, and populates dependents sets [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes current context from stack when exiting ClassDef node [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Removes current context and header from stack [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Clears current statement upon exiting SimpleStatementLine context [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Adds annotated assignment to global entities list [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Collects global variable assignments from module node [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Identifies function calls within code entity [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Pushes class name onto context stack, retrieves source code, docstring, bases, creates header string, pushes to header stack, updates entities dictionary, and resets current statement. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Records function signature, header, docstring, source code, implementation status, and privacy in entities [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Collects module names from imported aliases and adds them to external imports set [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Collects external module names, updates relative import set, maps imported names to file paths [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records name interactions if context present [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Updates current statement reference [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds project graph using DFS traversal, populates dependents dictionary [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `69c8f9` [1]: Orchestrates code analysis, builds project dependency graph, and extracts TODO comments _(Source: Synthesis)_
> 🆔 `535411` [2]: Analyzes and organizes code structure, interactions, entities, and statements within a module. _(Source: class CodeEntityVisitor)_
> 🆔 `7dcac4` [3]: Analyzes project structure, builds dependency graph using DFS traversal, extracts TODO comments from source code, and populates dependents sets _(Source: class GraphAnalyzer)_
> 🆔 `06e99b` [4]: Removes current context from stack when exiting ClassDef node _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `65360d` [5]: Removes current context and header from stack _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `5377a5` [6]: Clears current statement upon exiting SimpleStatementLine context _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `fcdeef` [7]: Adds annotated assignment to global entities list _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `a2bd71` [8]: Collects global variable assignments from module node _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `e265ff` [9]: Identifies function calls within code entity _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `83918d` [10]: Pushes class name onto context stack, retrieves source code, docstring, bases, creates header string, pushes to header stack, updates entities dictionary, and resets current statement. _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `9998b7` [11]: Records function signature, header, docstring, source code, implementation status, and privacy in entities _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `346510` [12]: Collects module names from imported aliases and adds them to external imports set _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `84f19c` [13]: Collects external module names, updates relative import set, maps imported names to file paths _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `b96b5f` [14]: Records name interactions if context present _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `12a88d` [15]: Updates current statement reference _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `e149b2` [16]: Builds project graph using DFS traversal, populates dependents dictionary _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Analyzes project documentation and critiques module content based on provided feedback

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Collects, organizes, and analyzes module content from project documentation [2]
- **`🔌 🔌 MapCritic.critique`**: Collects critiques for modules from project map content [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Constructs structured JSON output using SemanticGatekeeper for system instructions. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `65f889` [1]: Analyzes project documentation and critiques module content based on provided feedback _(Source: Synthesis)_
> 🆔 `3f4e42` [2]: Collects, organizes, and analyzes module content from project documentation _(Source: class MapCritic)_
> 🆔 `cabd98` [3]: Collects critiques for modules from project map content _(Source: 🔌 MapCritic.critique)_
> 🆔 `ffbb10` [4]: Uses `semantic_gatekeeper.py`: Constructs structured JSON output using SemanticGatekeeper for system instructions. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` Manages system architecture design, synthesizes module groups, and constructs summaries from technical data

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Organizes, aggregates, and summarizes technical data into cohesive system narratives [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Groups modules by archetype types, synthesizes each group, and constructs system summary [3]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Uses `llm_util.py`: Invokes the chat_llm function to handle LLM interactions, processing input messages, sending them for response generation, and stripping content before returning the output.. [4]
- **`agent_config.py`**: Imports `agent_config.py`. [5]
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates ModuleContext, passes group_name and modules to _synthesize_group method; Instantiates ModuleContext objects with contexts and processing_order parameters, integrating them into the synthesis process. [6]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Instructs `map_synthesizer.py` to apply structured response validation, error handling mechanisms, and formatting compliance enforced by the instantiated SemanticGatekeeper from `semantic_gatekeeper.py`, ensuring strict integration of user input with system instructions before proceeding downstream.. [7]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `851288` [1]: Manages system architecture design, synthesizes module groups, and constructs summaries from technical data _(Source: Synthesis)_
> 🆔 `d25dd3` [2]: Organizes, aggregates, and summarizes technical data into cohesive system narratives _(Source: class MapSynthesizer)_
> 🆔 `a7b396` [3]: Groups modules by archetype types, synthesizes each group, and constructs system summary _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `158f9f` [4]: Uses `llm_util.py`: Invokes the chat_llm function to handle LLM interactions, processing input messages, sending them for response generation, and stripping content before returning the output.. _(Source: Import llm_util.py)_
> 🆔 `24af77` [5]: Imports `agent_config.py`. _(Source: Import agent_config.py)_
> 🆔 `418b78` [6]: Uses `summary_models.py`: Instantiates ModuleContext, passes group_name and modules to _synthesize_group method; Instantiates ModuleContext objects with contexts and processing_order parameters, integrating them into the synthesis process. _(Source: Import summary_models.py)_
> 🆔 `4f800b` [7]: Uses `semantic_gatekeeper.py`: Instructs `map_synthesizer.py` to apply structured response validation, error handling mechanisms, and formatting compliance enforced by the instantiated SemanticGatekeeper from `semantic_gatekeeper.py`, ensuring strict integration of user input with system instructions before proceeding downstream.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Orchestrates memory management, analyzes helpfulness, retrieves memories by query, updates metadata, triggers cleanup of unused data

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Manages user memories, tracks helpfulness, updates memory metadata, and cleans up unused data [2]
- **`🔌 class MemoryInterface`**: Provides an interface for querying memory storage [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Creates unique identifier, merges metadata, updates collection [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Retrieves memories, evaluates helpfulness and last usage, deletes low utility or stale memories [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Retrieves memory results by query, updates last used turn for matching memories [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Retrieves memory metadata, updates helpfulness value, and saves modified metadata back to collection [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `265f3d` [1]: Orchestrates memory management, analyzes helpfulness, retrieves memories by query, updates metadata, triggers cleanup of unused data _(Source: Synthesis)_
> 🆔 `fb8ddc` [2]: Manages user memories, tracks helpfulness, updates memory metadata, and cleans up unused data _(Source: class ChromaMemory)_
> 🆔 `ead085` [3]: Provides an interface for querying memory storage _(Source: class MemoryInterface)_
> 🆔 `64f2af` [4]: Creates unique identifier, merges metadata, updates collection _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `ddb8aa` [5]: Retrieves memories, evaluates helpfulness and last usage, deletes low utility or stale memories _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `ba2240` [6]: Retrieves memory results by query, updates last used turn for matching memories _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `7a3b99` [7]: Retrieves memory metadata, updates helpfulness value, and saves modified metadata back to collection _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Determines module archetype, parses source code, analyzes entities and dependencies, and classifies modules into archetypes

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Encapsulates module data, parses source code for entities, analyzes dependencies and methods to determine archetype [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Determines module archetype based on name, source code analysis, entities, dependencies, and methods presence [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c44941` [1]: Determines module archetype, parses source code, analyzes entities and dependencies, and classifies modules into archetypes _(Source: Synthesis)_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `9da0ac` [3]: Encapsulates module data, parses source code for entities, analyzes dependencies and methods to determine archetype _(Source: class ModuleClassifier)_
> 🆔 `c9be24` [4]: Determines module archetype based on name, source code analysis, entities, dependencies, and methods presence _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Analyzes module context, synthesizes concise role description without referencing specific name

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Analyze module context, gather component information, synthesize concise role description without referencing specific name [2]
- **`🔌 clean_ref`**: Removes bracketed reference patterns from text using regex substitution [3]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyzes module context by gathering components, dependencies, and interactions [4]

### 🔗 Uses (Upstream)
- **`component_analyst.py`**: Uses `component_analyst.py`: Instantiates an instance of ComponentAnalyst, passing gatekeeping context to configure module analysis and role synthesis.; Analyzes module structure using ComponentAnalyst and synthesizes role summaries for module_contextualizer.py. [5]
- **`task_executor.py`**: Uses `task_executor.py`: Initializes an instance of TaskExecutor by passing the gatekeeper parameter to instantiate the task execution flow management.; Instantiates TaskExecutor with gatekeeper integration and invokes run() method for task execution flow management.. [6]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst class by passing gatekeeper and task_executor objects. [7]
- **`summary_models.py`**: Uses `summary_models.py`: Creates and configures ModuleContext instance, adds Alert records for incomplete implementations or errors, and sets module roles with claim information; Creates an instance of ModuleContext by passing file_path and dep_contexts arguments, adds alerts using add_alert method, and sets module role and claims using set_module_role and add_claims methods.. [8]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Initializes and configures the SemanticGatekeeper instance to manage structured response output, validation checks, and error handling for system instructions in module_contextualizer.py.. [9]
- **`module_classifier.py`**: Uses `module_classifier.py`: Initializes and configures the ModuleClassifier instance by passing self.module_name and self.data as keyword arguments to encapsulate module information in the ModuleArchetype data container.; Creates an instance of ModuleClassifier to analyze module name, source code entities, dependencies, and methods for determining the module archetype.. [10]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `3e521d` [1]: Analyzes module context, synthesizes concise role description without referencing specific name _(Source: Synthesis)_
> 🆔 `27371c` [2]: Analyze module context, gather component information, synthesize concise role description without referencing specific name _(Source: class ModuleContextualizer)_
> 🆔 `4d8635` [3]: Removes bracketed reference patterns from text using regex substitution _(Source: clean_ref)_
> 🆔 `a7c4cb` [4]: Analyzes module context by gathering components, dependencies, and interactions _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `f835ec` [5]: Uses `component_analyst.py`: Instantiates an instance of ComponentAnalyst, passing gatekeeping context to configure module analysis and role synthesis.; Analyzes module structure using ComponentAnalyst and synthesizes role summaries for module_contextualizer.py. _(Source: Import component_analyst.py)_
> 🆔 `4794bb` [6]: Uses `task_executor.py`: Initializes an instance of TaskExecutor by passing the gatekeeper parameter to instantiate the task execution flow management.; Instantiates TaskExecutor with gatekeeper integration and invokes run() method for task execution flow management.. _(Source: Import task_executor.py)_
> 🆔 `7bbfcf` [7]: Uses `dependency_analyst.py`: Instantiates DependencyAnalyst class by passing gatekeeper and task_executor objects. _(Source: Import dependency_analyst.py)_
> 🆔 `53beb6` [8]: Uses `summary_models.py`: Creates and configures ModuleContext instance, adds Alert records for incomplete implementations or errors, and sets module roles with claim information; Creates an instance of ModuleContext by passing file_path and dep_contexts arguments, adds alerts using add_alert method, and sets module role and claims using set_module_role and add_claims methods.. _(Source: Import summary_models.py)_
> 🆔 `c3ddd2` [9]: Uses `semantic_gatekeeper.py`: Initializes and configures the SemanticGatekeeper instance to manage structured response output, validation checks, and error handling for system instructions in module_contextualizer.py.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `48e737` [10]: Uses `module_classifier.py`: Initializes and configures the ModuleClassifier instance by passing self.module_name and self.data as keyword arguments to encapsulate module information in the ModuleArchetype data container.; Creates an instance of ModuleClassifier to analyze module name, source code entities, dependencies, and methods for determining the module archetype.. _(Source: Import module_classifier.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Generates structured reports from aggregated module contexts by collecting and organizing report sections

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Organizes and structures data for report generation [2]
- **`🔌 replace_ref`**: Replaces placeholders in text by generating unique numbers for each reference ID [3]
- **`🔌 sub`**: Maps reference IDs to sequential integers by checking existence in claim map [4]
- **`🔌 🔌 ReportRenderer.render`**: Collects module context data, organizes modules by archetype groups, generates presentation order for report sections [5]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Instantiates the ModuleContext class within report_renderer.py's constructor, passing context_map to initialize its properties and functions such as _render_module utilize it for processing.; Instantiates ModuleContext for context_map and output_file parameters. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `33773c` [1]: Generates structured reports from aggregated module contexts by collecting and organizing report sections _(Source: Synthesis)_
> 🆔 `0c3b99` [2]: Organizes and structures data for report generation _(Source: class ReportRenderer)_
> 🆔 `4fff06` [3]: Replaces placeholders in text by generating unique numbers for each reference ID _(Source: replace_ref)_
> 🆔 `1ad7f4` [4]: Maps reference IDs to sequential integers by checking existence in claim map _(Source: sub)_
> 🆔 `c82ac5` [5]: Collects module context data, organizes modules by archetype groups, generates presentation order for report sections _(Source: 🔌 ReportRenderer.render)_
> 🆔 `b0320d` [6]: Uses `summary_models.py`: Instantiates the ModuleContext class within report_renderer.py's constructor, passing context_map to initialize its properties and functions such as _render_module utilize it for processing.; Instantiates ModuleContext for context_map and output_file parameters. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Constructs detailed structured responses, manages complex interaction flow, orchestrates downstream components, and validates outputs before final delivery

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Assigns a set of disallowed adjectives to prevent their use in code [2]
- **`🔌 class SemanticGatekeeper`**: Constructs and manages structured response output for system instructions [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Constructs detailed response by combining user input with system instructions and parsing into structured JSON output, ensuring strict formatting compliance and handling potential errors through retry logic and validation checks. [4]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Uses `llm_util.py`: Transforms unprocessed LLM responses into sanitized formats using llm_util.py's parsing functions to prepare data for Semantic Gatekeeper processing, thereby optimizing downstream pipeline interactions.. [5]
- **`agent_config.py`**: Uses `agent_config.py`: Initializes configuration constants and sets model identifier for local logic usage.. [6]

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

> 🆔 `cc4f9b` [1]: Constructs detailed structured responses, manages complex interaction flow, orchestrates downstream components, and validates outputs before final delivery _(Source: Synthesis)_
> 🆔 `02aa04` [2]: Assigns a set of disallowed adjectives to prevent their use in code _(Source: BANNED_ADJECTIVES)_
> 🆔 `3ff71b` [3]: Constructs and manages structured response output for system instructions _(Source: class SemanticGatekeeper)_
> 🆔 `ff5c3d` [4]: Constructs detailed response by combining user input with system instructions and parsing into structured JSON output, ensuring strict formatting compliance and handling potential errors through retry logic and validation checks. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `601700` [5]: Uses `llm_util.py`: Transforms unprocessed LLM responses into sanitized formats using llm_util.py's parsing functions to prepare data for Semantic Gatekeeper processing, thereby optimizing downstream pipeline interactions.. _(Source: Import llm_util.py)_
> 🆔 `4a1944` [6]: Uses `agent_config.py`: Initializes configuration constants and sets model identifier for local logic usage.. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Analyzes text inputs, generates summaries using claim-based identifiers, orchestrates dependencies, and exports public APIs

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Constructs unique identifiers by combining relevant data fields and applying hashing algorithms [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Manages module data, dependencies, dependents, public API, alerts, and claims state. [5]
- **`🔌 🔌 Claim.id`**: Constructs unique identifier by combining text, reference, source module and hashing [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds alert to alerts list [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Aggregates explanation and claim placeholders, constructs full text, stores in key_dependencies dictionary [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds dependent context to ModuleContext by storing explanation and claims in key_dependents dictionary [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds public API entry by merging description and placeholders from supporting claims, storing in self.public_api dictionary. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Combines input text with placeholders from claims, updates module role state [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `9be1de` [1]: Analyzes text inputs, generates summaries using claim-based identifiers, orchestrates dependencies, and exports public APIs _(Source: Synthesis)_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `983168` [3]: Constructs unique identifiers by combining relevant data fields and applying hashing algorithms _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `1c71fb` [5]: Manages module data, dependencies, dependents, public API, alerts, and claims state. _(Source: class ModuleContext)_
> 🆔 `51ccb3` [6]: Constructs unique identifier by combining text, reference, source module and hashing _(Source: 🔌 Claim.id)_
> 🆔 `5a75ac` [7]: Adds alert to alerts list _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `e6e47e` [8]: Aggregates explanation and claim placeholders, constructs full text, stores in key_dependencies dictionary _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `59252c` [9]: Adds dependent context to ModuleContext by storing explanation and claims in key_dependents dictionary _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `9a084f` [10]: Adds public API entry by merging description and placeholders from supporting claims, storing in self.public_api dictionary. _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `86a7c6` [11]: Combines input text with placeholders from claims, updates module role state _(Source: 🔌 ModuleContext.set_module_role)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` Manages task execution flow

**Impact Analysis:** Changes to this module will affect: dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Encompasses internal state variables for managing task execution process [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Organizes task execution process [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Initializes SemanticGatekeeper instance for constructing structured responses and managing interaction flow in task_executor.py. [4]

### 👥 Used By (Downstream)
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `71a4ac` [1]: Manages task execution flow _(Source: Synthesis)_
> 🆔 `a05262` [2]: Encompasses internal state variables for managing task execution process _(Source: class TaskExecutor)_
> 🆔 `538a72` [3]: Organizes task execution process _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `579a05` [4]: Uses `semantic_gatekeeper.py`: Initializes SemanticGatekeeper instance for constructing structured responses and managing interaction flow in task_executor.py. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Provides LLM input parsing, response stripping, and content processing capabilities to agent_core.py, map_synthesizer.py, and semantic_gatekeeper.py for downstream use.

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Parses input messages and sends them to LLM for response, then strips content before returning [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `2cd6ac` [1]: Provides LLM input parsing, response stripping, and content processing capabilities to agent_core.py, map_synthesizer.py, and semantic_gatekeeper.py for downstream use. _(Source: Synthesis)_
> 🆔 `846a39` [2]: Parses input messages and sends them to LLM for response, then strips content before returning _(Source: chat_llm)_
</details>

---
## 🔧 Configuration

## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Assigns integer value 4096 to variable CONTEXT_LIMIT [2]
- **`🔌 DEFAULT_MODEL`**: Sets model identifier for use in local logic [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `449512` [1]: Defines configuration constants. _(Source: Archetype)_
> 🆔 `f49e9d` [2]: Assigns integer value 4096 to variable CONTEXT_LIMIT _(Source: CONTEXT_LIMIT)_
> 🆔 `f589a8` [3]: Sets model identifier for use in local logic _(Source: DEFAULT_MODEL)_
</details>

---