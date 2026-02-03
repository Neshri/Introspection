# Project Context Map

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` orchestrates scanning of target folder to locate specific files, initializes CrawlerAgent with specified goal and root path, runs the agent to process memory, project map, order, create gatekeeper and executor, synthesize results into system summary, render report, clean memories for five turns, and returns completion response. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 main`**: Scans `target_folder` recursively to locate the file ending in `_main.py`, initializes `CrawlerAgent` with the goal and target root path, runs the agent which processes memory, project map, order, creates gatekeeper and executor, synthesizes results into system summary, renders report, cleans memories for five turns, and returns completion response. [2]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Orchestrates project analysis by setting up the crawler, managing memory and agents, synthesizing results into a summary report, and ensuring system cleanup. [3]

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` orchestrates analysis by retrieving project map and processing order, creating synthesizer and executor, generating system summary, rendering report, cleaning memories for five turns, and returning analysis complete response.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Initializes CrawlerAgent with goal and target root, creates ChromaMemory instance, and prints initialization message. [2]
- **`🔌 🔌 CrawlerAgent.run`**: Runs the CrawlerAgent by initializing memory, retrieving project map and processing order, creating gatekeeper and executor, synthesizing results into system summary, rendering report, cleaning memories for five turns, and returning analysis completion response. [3]

### 🔗 Uses (Upstream)
- **`map_synthesizer.py`**: Orchestrates synthesis of technical architecture narratives from module contexts and supporting components using defined goal in agent_core.py. [4]
- **`semantic_gatekeeper.py`**: Validates and critiques LLM-generated output by constructing prompts, sending them to an LLM, validating the critique, verifying grounding against specified sources, handling errors after multiple attempts, extracting balanced JSON substrings, parsing JSON safely, and returning or logging errors. [5]
- **`agent_util.py`**: Analyzes target file path to build project graph and generates summarizer contexts and processing order for integrated components in `agent_core.py`. [6]
- **`memory_core.py`**: Manages and organizes memory records in `agent_core.py`, enabling the system to track and utilize contextual information by generating unique identifiers, storing metadata, querying memories based on text inputs, updating helpfulness scores, and automatically purging low-quality or unused memories. [7]
- **`llm_util.py`**: Formats and truncates text inputs to ensure they fit within the specified context limits for LLM interactions, preserving critical information. [8]
- **`report_renderer.py`**: Organizes modules into context maps and verification proofs for specified files, orchestrating the generation of documentation by delegating tasks to other components. [9]
- **`task_executor.py`**: Orchestrates task management by initializing SemanticGatekeeper, executing complex tasks, parsing responses, verifying grounding and relevance, auditing accuracy, refining vague answers, and solving goals through goal loops. [10]
- **`agent_config.py`**: Defines constants for model and context limits to configure agent behavior. [11]
- **`summary_models.py`**: Orchestrates summarization and contextual analysis of module roles, dependencies, APIs, alerts, and claims by defining classes to encapsulate these components and managing their relationships through methods that update the ModuleContext instance. [12]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` analyzes and coordinates the execution of agent-based operations within the system, ensuring integration and performance optimization across integrated components.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns a dictionary literal to the variable `ProjectGraph`. [2]
- **`🔌 class ProjectSummarizer`**: Initializes an instance by setting the graph, max_cycles, contexts dictionary, and processing order based on topological sorting. [3]
- **`🔌 project_pulse`**: Analyzes the target file path to build a project graph, generates summarizer contexts and processing order based on the graph. [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Computes module contexts for each path in the project graph, considering dependencies and critiques, and returns updated contexts and processing order. [5]
- **`🔒 _create_module_context`**: Generates module context by creating an instance of ModuleContextualizer, contextualizing the module with critique instruction, setting file path if not present, and returning the ModuleContext. [6]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Orchesters data validation, grounding verification, and error handling for LLM-generated output. [7]
- **`map_critic.py`**: Analyzes project modules and returns critiques for up to three modules, identifying specific flaws in documentation and guiding improvements. [8]
- **`report_renderer.py`**: Organizes project documentation by archetype and exports detailed reports to specified files. [9]
- **`module_contextualizer.py`**: Analyzes module context by examining components, dependencies, and critiques to populate alerts and guide further processing. [10]
- **`graph_analyzer.py`**: Analyzes Python code structure to construct and populate a dependency graph representing imports, assignments, function definitions, classes, and their interactions. [11]
- **`summary_models.py`**: Orchestrates summarization and contextual analysis of module roles, dependencies, APIs, alerts, and claims by encapsulating these components in classes and managing their relationships through methods. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` orchestrates the parsing and transformation of source code into an abstract syntax tree (AST), removes docstrings and replaces function bodies with pass statements, generates module skeletons, analyzes components for logic and mechanisms, synthesizes class roles, adds entries to module contexts, resolves dependency contexts, and handles alerts and warnings.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Initializes instance by assigning provided gatekeeper and task_executor attributes to class attributes. [2]
- **`🔌 class SkeletonTransformer`**: Transforms AST nodes by removing docstrings and replacing bodies with `Pass()` when `strip_bodies` is True. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Describes the purpose and behavior of the method. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Parses source code into an AST, applies a SkeletonTransformer to generate module skeleton structure, and unparses the modified tree back to source code. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Removes docstring from the node and replaces body with [ast.Pass()] if strip_bodies is True, then recursively visits child nodes. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from node, replaces empty body with `ast.Pass()`, and recursively visits child nodes. [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Removes docstring from function node and replaces body with `Pass()` if strip_bodies is True. [8]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Orchestrates task management by initializing SemanticGatekeeper, executing complex tasks, parsing responses, verifying grounding and relevance, auditing accuracy, refining vague answers, and solving goals through goal loops. [9]
- **`semantic_gatekeeper.py`**: Orchestrates semantic validation and grounding of LLM-generated text, ensuring accuracy against specified sources. [10]
- **`summary_models.py`**: Orchestrates summarization and contextual analysis of module roles, dependencies, public APIs, alerts, and claims by managing relationships through ModuleContext instance. [11]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` analyzes dependencies and coordinates contextual information for modules.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Initializes gatekeeper and task_executor attributes. [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes upstream API usage of imported dependency and generates explanations based on symbol usage, interactions, and archetype guidance. [3]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Orchestrates task management by initializing SemanticGatekeeper, executing complex tasks, parsing responses, verifying grounding and relevance, auditing accuracy, refining vague answers, and solving goals through goal loops. [4]
- **`semantic_gatekeeper.py`**: Validates, critiques, and grounds LLM output through the SemanticGatekeeper class while coordinating interaction with other services like TaskExecutor. [5]
- **`module_classifier.py`**: Analyzes module properties to categorize based on dependencies and code structure, informing downstream analysis in `dependency_analyst.py`. [6]
- **`summary_models.py`**: Orchestrates summarization and contextual analysis of module roles, dependencies, public APIs, alerts, and claims by managing relationships through methods that update ModuleContext. [7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` provides critiques

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Initializes an instance by setting the gatekeeper attribute. Parses project map content, analyzes each module, and returns critiques for up to three modules. Parses project map content to extract modules and their descriptions, returning a dictionary mapping module names to concatenated header and body text. Verifies module documentation for specific flaws and returns appropriate audit result or instruction. [2]
- **`🔌 🔌 MapCritic.critique`**: Parses project map content, analyzes each module, and returns critiques for up to three modules. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Validates and critiques LLM output, verifies grounding against specified sources, handles errors after multiple attempts using `SemanticGatekeeper` class. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` orchestrates the synthesis of technical architecture narratives from module contexts and supporting components using a defined goal.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Initializes an instance of MapSynthesizer, storing the provided task_executor. [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Identifies anchors, gathers component details including role, archetype, API points, and dependencies from contexts, determines supporting cast based on processing order, and runs grounded synthesis. [3]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Orchestrates task management by initializing SemanticGatekeeper, executing complex tasks, parsing responses, verifying grounding and relevance, auditing accuracy, refining vague answers, and solving goals through goal loops. [4]
- **`summary_models.py`**: Orchesters summarization and contextual analysis of module roles, dependencies, public APIs, alerts, and claims by defining classes to encapsulate these components and managing their relationships through methods that update the ModuleContext instance. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` orchestrates the generation of project context maps and verification proofs by organizing modules based on their archetypes and exporting detailed documentation to specified files.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Initializes attributes including context_map, output_file, verification_file, system_summary, an empty claim_map, and sets ref_counter to 1. [2]
- **`🔌 🔌 ReportRenderer.render`**: Generates a project context map and verification proof, organizing modules by archetype and outputting to specified files. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Aggregates and organizes module role, dependencies, context, public API, alerts, and claims for structured reporting. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` defines

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines global constant `BANNED_ADJECTIVES`. [2]
- **`🔌 class SemanticGatekeeper`**: The SemanticGatekeeper class is responsible for processing input text through an LLM, validating and critiquing the output, verifying grounding against specified sources, handling errors after multiple attempts, extracting balanced JSON substrings, parsing JSON safely, and parsing whole JSON sections. [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: The function constructs a prompt, sends it to an LLM, validates and critiques the output, verifies grounding against specified sources, and returns or logs errors after exhausting attempts. [4]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Configures the default model for semantic gatekeeper processing to ensure consistent natural language understanding and response generation across all interactions. [5]
- **`llm_util.py`**: Formats prompts and truncates texts to ensure context length is appropriate while preserving critical information in LLM interactions. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_critic.py`**
- **`module_contextualizer.py`**
- **`task_executor.py`**

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` orchestrates task management by initializing SemanticGatekeeper, executing complex tasks, parsing responses, verifying grounding and relevance, auditing accuracy, refining vague answers, and solving goals through goal loops.

**Impact Analysis:** Changes to this module will affect: agent_core.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Manages execution of tasks, initializes SemanticGatekeeper and sets max_retries to 5, handles goal loops using gatekeeper, parses responses, verifies grounding and relevance, audits accuracy and refines vague answers. [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Commences task, logs start with goal and log label, truncates context data, attempts to run goal loop using `gatekeeper` from `TaskExecutor`, handles exceptions by logging error details, returns failure message on crash. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Orchesters semantic validation, grounding checks, and error handling for LLM-generated output in task execution flow. [4]
- **`llm_util.py`**: Formats LLM interaction prompts and truncates long texts to fit within token limits while preserving first and last halves of the string. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` defines utility functions that format input prompts for LLM interactions and truncate long texts to specified context limits while preserving first and last halves of the string.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Transforms input prompt or messages into appropriate format and generates response using specified model. [2]
- **`🔌 truncate_context`**: Truncates long text to specified maximum characters, preserving first and last half of the string, and adds truncation indicator in between. [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**
- **`task_executor.py`**

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` defines and analyzes the dependency graph of Python code by traversing the code structure, identifying entities such as imports, assignments, function definitions, classes, and their interactions, and populating a detailed graph dictionary representing these relationships.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Traverses Python code structure, identifies and records entities such as imports, assignments, function definitions, classes, and their interactions. [2]
- **`🔌 class GraphAnalyzer`**: Initializes class attributes including root path, project root directory, Python files list, empty graph structure, and visited nodes set. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes the current context and header stack from the visitor when leaving a class definition node, effectively popping the relevant elements from the internal state. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Updates current context and header stack by popping elements when leaving a FunctionDef node. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Clears the current statement by setting it to None when leaving a SimpleStatementLine node. [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Processes an assignment statement, checking if it's a global variable declaration and storing its name, source code, type annotation, line number, end line number in the `globals` list within entities. [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Processes an `Assign` node, extracts target variable names as globals, retrieves source code and metadata for each global, and populates the entities dictionary. [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Analyzes call nodes, recording interactions for named function calls. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Traverses class definition node, updating context stack and entity dictionary with class source code, docstring, bases, line numbers, and initializing methods list. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Analyzes function definition node, extracts signature, header, docstring, and component data, determines if method or standalone function, and updates entities list for functions and classes. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Iterates over import aliases in an `Import` node, retrieves the module name for each alias using `module_node.code_for_node`, and adds the module names to `external_imports` set. [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes and records imports from other modules or directories, updating external and relative import sets and mapping local names to file paths. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records name interactions and updates cross module interactions for the given node value if context is set. [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Updates the current statement to the provided node. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds dependency graph using DFS, populates dependents, and returns the graph dictionary. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` defines a system for encapsulating and managing memory records using Chroma database, enabling the addition of memories with unique IDs and metadata, querying based on text queries, updating helpfulness scores, and automatically cleaning up unused or low-quality memories.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Initializes a Chroma client, retrieves or creates a 'memories' collection, adds memories with metadata, queries memories based on criteria, updates helpfulness scores, and cleans up low-quality or unused memories. [2]
- **`🔌 class MemoryInterface`**: Defines interface signature for querying memory. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Creates a unique memory ID, combines metadata fields into one dictionary, updates it if additional metadata is provided, and adds the document to the Chroma collection. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Deletes memories from the collection if their helpfulness score is below 0.3 or they haven't been used in over 50 turns. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Retrieves memory records matching the query, updates the last used turn for each retrieved record, and returns the results. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Updates the helpfulness score of a specified memory in the collection. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` classifies modules based on name, dependencies, and source code

**Impact Analysis:** Changes to this module will affect: dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Initializes the ModuleClassifier by setting `module_name` and `data` attributes. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Classifies the module based on its name, dependencies, entities, and source code to determine if it is an entry point, data model, configuration, utility, or service. [4]

### 👥 Used By (Downstream)
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` orchestrates the analysis of module context by analyzing components, dependencies, populating alerts, and processing critique instruction.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Initializes ModuleContextualizer by setting up file path, graph data, dependency contexts, and analysis components including gatekeeper, task executor, classifier, archetype determination, component analyst, dependency analyst, and usage map. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyzes module context by analyzing components, dependencies, populating alerts, and processing critique instruction. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Validates, critiques, grounds, and safely parses LLM output in structured formats before returning or logging errors. [4]
- **`module_classifier.py`**: Classifies modules based on name, dependencies, and source code to determine their role (entry point, data model, configuration, utility, or service) within the system. [5]
- **`component_analyst.py`**: Transforms source code into an abstract syntax tree (AST), generates module skeletons, analyzes components for logic and mechanisms, synthesizes class roles, resolves dependency contexts, and handles alerts and warnings. [6]
- **`dependency_analyst.py`**: Analyzes dependencies and contextual information for modules in module_contextualizer.py to inform architectural decisions and ensure maintainability. [7]
- **`task_executor.py`**: Orchestrates task management by initializing SemanticGatekeeper, executing complex tasks, parsing responses, verifying grounding and relevance, auditing accuracy, refining vague answers, and solving goals through goal loops. [8]
- **`summary_models.py`**: Orchesters summarization and contextual analysis of module roles, dependencies, public APIs, alerts, and claims by defining classes to encapsulate these components and managing their relationships through methods that update the ModuleContext instance. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` orchestrates the summarization and contextual analysis of module roles, dependencies, public APIs, alerts, and claims by defining classes to encapsulate these components and managing their relationships through methods that update the ModuleContext instance.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Computes SHA1 hash of concatenated string representation. [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Initializes ModuleContext instance by setting attributes such as file_path, archetype, module_role, key_dependencies, key_dependents, public_api, alerts, and claims. [5]
- **`🔌 🔌 Claim.id`**: Computes SHA1 hash of concatenated string representation. [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds an alert to the list of alerts in `ModuleContext` by appending it to `self.alerts`. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Adds dependency context by combining explanation and supporting claims, storing in `key_dependencies` dictionary. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds dependent context by combining explanation and supporting claims, then storing in `key_dependents` dictionary. [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds an entry to the public API dictionary, combining description and placeholders from supporting claims. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Sets the module's role by concatenating provided text with placeholders and claim IDs, storing the result in `module_role`. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

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

---