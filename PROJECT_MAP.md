# Project Context Map

## 🏛️ System Architecture
The system architecture is built on the Configuration layer, which defines constants crucial for the system's operation, particularly those in agent_config.py that influence downstream modules such as agent_core.py and semantic_gatekeeper.py. These configuration settings serve as the blueprint for how data flows through the system, setting the stage for application logic to process and utilize this information effectively. The Data Model layer represents a repository of role, dependencies, dependents, API, alerts, and claims of various modules within the software project, providing critical context for the Service layer to generate accurate project context map reports.

---

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates the initialization and execution of CrawlerAgent to process the main script in the specified target folder [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 main`**: Initializes CrawlerAgent, runs it to process the main script, and returns completion message. [2]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Instantiates CrawlerAgent with goal and target root. [3]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `00cbd0` [1]: Orchestrates the initialization and execution of CrawlerAgent to process the main script in the specified target folder _(Source: Synthesis (based on [2]))_
> 🆔 `008281` [2]: Initializes CrawlerAgent, runs it to process the main script, and returns completion message. _(Source: main)_
> 🆔 `45b813` [3]: Instantiates CrawlerAgent with goal and target root. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Orchestrates crawling of project maps, synthesizes system summaries, renders reports, and manages memory cleanup through defined methods and components.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Summarizes project map, synthesizes system summary, renders report, and cleans memories. [2]
- **`🔌 🔌 CrawlerAgent.run`**: Runs the CrawlerAgent by initializing memory, retrieving project map and processing order, synthesizing system summary, rendering report, cleaning memories for 5 turns, and returning analysis complete message. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Instantiates class from `summary_models.py`. [4]
- **`memory_core.py`**: Instantiates class ChromaMemory. [5]
- **`llm_util.py`**: Imports `chat_llm` from `llm_util`. [6]
- **`agent_config.py`**: Imports constants from agent_config. [7]
- **`report_renderer.py`**: Instantiates ReportRenderer class. [8]
- **`agent_util.py`**: Calls project_pulse function. [9]
- **`map_synthesizer.py`**: Instantiates MapSynthesizer class. [10]
- **`semantic_gatekeeper.py`**: Instantiates SemanticGatekeeper class. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a0b5ea` [1]: Orchestrates crawling of project maps, synthesizes system summaries, renders reports, and manages memory cleanup through defined methods and components. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `88f92d` [2]: Summarizes project map, synthesizes system summary, renders report, and cleans memories. _(Source: class CrawlerAgent)_
> 🆔 `ffea72` [3]: Runs the CrawlerAgent by initializing memory, retrieving project map and processing order, synthesizing system summary, rendering report, cleaning memories for 5 turns, and returning analysis complete message. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `0b224f` [4]: Instantiates class from `summary_models.py`. _(Source: Import summary_models.py)_
> 🆔 `33c4c2` [5]: Instantiates class ChromaMemory. _(Source: Import memory_core.py)_
> 🆔 `f683eb` [6]: Imports `chat_llm` from `llm_util`. _(Source: Import llm_util.py)_
> 🆔 `64549a` [7]: Imports constants from agent_config. _(Source: Import agent_config.py)_
> 🆔 `7b9009` [8]: Instantiates ReportRenderer class. _(Source: Import report_renderer.py)_
> 🆔 `3799a7` [9]: Calls project_pulse function. _(Source: Import agent_util.py)_
> 🆔 `a12483` [10]: Instantiates MapSynthesizer class. _(Source: Import map_synthesizer.py)_
> 🆔 `ec4f8b` [11]: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Orchestrates the integration of external services and APIs within the agent framework, coordinating their invocation based on predefined triggers and context requirements.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns a dictionary to the variable ProjectGraph. [2]
- **`🔌 class ProjectSummarizer`**: Initializes instance by assigning provided graph, setting default max_cycles, creating empty contexts dictionary, and computing topological order. [3]
- **`🔌 project_pulse`**: Creates a dependency graph, summarizes it, generates contexts and processing order for the project. [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Computes module contexts for each path in the project graph, updating them based on dependencies and critique instructions if available. [5]
- **`🔒 _create_module_context`**: Creates module context by instantiating ModuleContextualizer, contextualizing the module, handling file path assignment, and returning ModuleContext. [6]

### 🔗 Uses (Upstream)
- **`graph_analyzer.py`**: Instantiates GraphAnalyzer class. [7]
- **`summary_models.py`**: Instantiates ModuleContext class. [8]
- **`map_critic.py`**: Instantiates MapCritic with gatekeeper. [9]
- **`module_contextualizer.py`**: Instantiates ModuleContextualizer class. [10]
- **`report_renderer.py`**: Instantiates ReportRenderer class. [11]
- **`semantic_gatekeeper.py`**: Instantiates SemanticGatekeeper class. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `32a1e6` [1]: Orchestrates the integration of external services and APIs within the agent framework, coordinating their invocation based on predefined triggers and context requirements. _(Source: Synthesis (based on [5], [2], [4], [6], [3]))_
> 🆔 `56e610` [2]: Assigns a dictionary to the variable ProjectGraph. _(Source: ProjectGraph)_
> 🆔 `cae5d5` [3]: Initializes instance by assigning provided graph, setting default max_cycles, creating empty contexts dictionary, and computing topological order. _(Source: class ProjectSummarizer)_
> 🆔 `8cfe85` [4]: Creates a dependency graph, summarizes it, generates contexts and processing order for the project. _(Source: project_pulse)_
> 🆔 `114ce6` [5]: Computes module contexts for each path in the project graph, updating them based on dependencies and critique instructions if available. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `8f33c3` [6]: Creates module context by instantiating ModuleContextualizer, contextualizing the module, handling file path assignment, and returning ModuleContext. _(Source: _create_module_context)_
> 🆔 `336648` [7]: Instantiates GraphAnalyzer class. _(Source: Import graph_analyzer.py)_
> 🆔 `45488d` [8]: Instantiates ModuleContext class. _(Source: Import summary_models.py)_
> 🆔 `75498a` [9]: Instantiates MapCritic with gatekeeper. _(Source: Import map_critic.py)_
> 🆔 `891c6a` [10]: Instantiates ModuleContextualizer class. _(Source: Import module_contextualizer.py)_
> 🆔 `81cbd1` [11]: Instantiates ReportRenderer class. _(Source: Import report_renderer.py)_
> 🆔 `b41390` [12]: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes the systemic role of defined components by parsing provided context and synthesizing their responsibilities.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Initializes an instance of the ComponentAnalyst class by assigning provided gatekeeper and task_executor objects to instance attributes. [2]
- **`🔌 class SkeletonTransformer`**: Removes docstrings from function, async function, and class definitions and ensures classes have an empty body handle by adding `Pass()`. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes the behavior of `analyze_components` function, identifies global constants and functions defined in provided module, analyzes their mechanisms, interactions, dependencies, and class state definitions to summarize each component's role and functionality. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Transforms the abstract syntax tree of provided source code using `SkeletonTransformer`, then returns the modified code as a string. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Removes docstring from AsyncFunctionDef and visits the node. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from node and adds `Pass()` if body is empty, then visits children. [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Removes docstring from function definition and visits node recursively. [8]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Instantiates TaskExecutor class. [9]
- **`summary_models.py`**: Instantiates class. [10]
- **`semantic_gatekeeper.py`**: Instantiates SemanticGatekeeper class. [11]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8a5157` [1]: Analyzes the systemic role of defined components by parsing provided context and synthesizing their responsibilities. _(Source: Synthesis (based on [6], [5], [3], [7], [2], [4], [8]))_
> 🆔 `d13953` [2]: Initializes an instance of the ComponentAnalyst class by assigning provided gatekeeper and task_executor objects to instance attributes. _(Source: class ComponentAnalyst)_
> 🆔 `46ae70` [3]: Removes docstrings from function, async function, and class definitions and ensures classes have an empty body handle by adding `Pass()`. _(Source: class SkeletonTransformer)_
> 🆔 `ec9ae2` [4]: Analyzes the behavior of `analyze_components` function, identifies global constants and functions defined in provided module, analyzes their mechanisms, interactions, dependencies, and class state definitions to summarize each component's role and functionality. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `328442` [5]: Transforms the abstract syntax tree of provided source code using `SkeletonTransformer`, then returns the modified code as a string. _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `2dc0fd` [6]: Removes docstring from AsyncFunctionDef and visits the node. _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `649c1d` [7]: Removes docstring from node and adds `Pass()` if body is empty, then visits children. _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `ee9524` [8]: Removes docstring from function definition and visits node recursively. _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `40c4c2` [9]: Instantiates TaskExecutor class. _(Source: Import task_executor.py)_
> 🆔 `2e80be` [10]: Instantiates class. _(Source: Import summary_models.py)_
> 🆔 `31cab0` [11]: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Defines a service that analyzes module dependencies to describe their role and impact on functionality.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Analyzes module dependencies to describe their role and impact on functionality. [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes upstream context for used symbols and usage snippets of specified dependency, describing its role and impact on the module's functionality. [3]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Instantiates class. [4]
- **`summary_models.py`**: Analyzes dependencies in `analyze_dependencies`. [5]
- **`semantic_gatekeeper.py`**: Instantiates SemanticGatekeeper class. [6]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `32f057` [1]: Defines a service that analyzes module dependencies to describe their role and impact on functionality. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `19e519` [2]: Analyzes module dependencies to describe their role and impact on functionality. _(Source: class DependencyAnalyst)_
> 🆔 `1c4d8c` [3]: Analyzes upstream context for used symbols and usage snippets of specified dependency, describing its role and impact on the module's functionality. _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `fbc2bb` [4]: Instantiates class. _(Source: Import task_executor.py)_
> 🆔 `2c80fc` [5]: Analyzes dependencies in `analyze_dependencies`. _(Source: Import summary_models.py)_
> 🆔 `7b3431` [6]: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Defines and coordinates an analysis process that extracts project modules from documentation content and generates critiques for each module up to three, focusing on specific description errors related to definitions, constants, and dependencies.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Analyzes project map content, extracts modules, and generates critiques for each module up to three. [2]
- **`🔌 🔌 MapCritic.critique`**: Analyzes project map content, extracts modules, and generates critiques for each module up to three. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Instantiates SemanticGatekeeper class. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d90b23` [1]: Defines and coordinates an analysis process that extracts project modules from documentation content and generates critiques for each module up to three, focusing on specific description errors related to definitions, constants, and dependencies. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `9d5d48` [2]: Analyzes project map content, extracts modules, and generates critiques for each module up to three. _(Source: class MapCritic)_
> 🆔 `c0d722` [3]: Analyzes project map content, extracts modules, and generates critiques for each module up to three. _(Source: 🔌 MapCritic.critique)_
> 🆔 `a9b808` [4]: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` The Map Synthesizer module processes specified contexts and processing order to synthesize a functional summary of each layer group (Entry Point, Service, Utility, Data Model, Configuration) based on module roles and interactions.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Initializes an instance by storing the provided gatekeeper in its gatekeeper attribute. [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Processes specified contexts and processing order, categorizes modules into groups (Entry Point, Service, Utility, Data Model, Configuration) based on archetype, synthesizes summaries for each group, and returns a synthesized system representation. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Instantiates SemanticGatekeeper class. [4]
- **`summary_models.py`**: Calls function `_synthesize_group`. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ff902a` [1]: The Map Synthesizer module processes specified contexts and processing order to synthesize a functional summary of each layer group (Entry Point, Service, Utility, Data Model, Configuration) based on module roles and interactions. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `1eadb9` [2]: Initializes an instance by storing the provided gatekeeper in its gatekeeper attribute. _(Source: class MapSynthesizer)_
> 🆔 `f75974` [3]: Processes specified contexts and processing order, categorizes modules into groups (Entry Point, Service, Utility, Data Model, Configuration) based on archetype, synthesizes summaries for each group, and returns a synthesized system representation. _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `edd598` [4]: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `0d4ca7` [5]: Calls function `_synthesize_group`. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Orchestrates the generation of project context map reports by rendering module details, dependencies, and categorizing them into archetype groups while managing references and claims.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Initializes attributes including `context_map`, `output_file`, `system_summary`, an empty `claim_map`, and sets `ref_counter` to 1. [2]
- **`🔌 🔌 ReportRenderer.render`**: Generates project context map report by rendering module details, dependencies, and categorizing them into archetype groups. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Instantiates class ModuleContext. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `9af7d6` [1]: Orchestrates the generation of project context map reports by rendering module details, dependencies, and categorizing them into archetype groups while managing references and claims. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `4967c6` [2]: Initializes attributes including `context_map`, `output_file`, `system_summary`, an empty `claim_map`, and sets `ref_counter` to 1. _(Source: class ReportRenderer)_
> 🆔 `bd5303` [3]: Generates project context map report by rendering module details, dependencies, and categorizing them into archetype groups. _(Source: 🔌 ReportRenderer.render)_
> 🆔 `5ba0f1` [4]: Instantiates class ModuleContext. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Analyzes LLM outputs for policy compliance and contextual relevance before passing them to downstream services.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines global constant `BANNED_ADJECTIVES`. [2]
- **`🔌 class SemanticGatekeeper`**: Summarizes the responsibility of Class SemanticGatekeeper, detailing its methods for executing LLM responses, verifying code accuracy, critiquing content for policy compliance, extracting balanced JSON data, parsing safe JSON structures, and parsing entire JSON dictionaries. [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Executes the `execute_with_feedback` method, which prompts an LLM to generate a response based on provided inputs and returns the specified key from the JSON output if `expect_json` is True. [4]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Calls chat_llm function from llm_util module. [5]
- **`agent_config.py`**: Instantiates class. [6]

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

> 🆔 `4df7c4` [1]: Analyzes LLM outputs for policy compliance and contextual relevance before passing them to downstream services. _(Source: Synthesis (based on [4], [2], [3]))_
> 🆔 `4d3df2` [2]: Defines global constant `BANNED_ADJECTIVES`. _(Source: BANNED_ADJECTIVES)_
> 🆔 `86dc28` [3]: Summarizes the responsibility of Class SemanticGatekeeper, detailing its methods for executing LLM responses, verifying code accuracy, critiquing content for policy compliance, extracting balanced JSON data, parsing safe JSON structures, and parsing entire JSON dictionaries. _(Source: class SemanticGatekeeper)_
> 🆔 `10ab14` [4]: Executes the `execute_with_feedback` method, which prompts an LLM to generate a response based on provided inputs and returns the specified key from the JSON output if `expect_json` is True. _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `fc9012` [5]: Calls chat_llm function from llm_util module. _(Source: Import llm_util.py)_
> 🆔 `89caeb` [6]: Instantiates class. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` Manages orchestration of complex tasks and coordinates execution flow within the system.

**Impact Analysis:** Changes to this module will affect: component_analyst.py, dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Summarizes responsibility of TaskExecutor class, initializes attributes via __init__, and executes goal loop to refine answer based on feedback. [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Attempts to execute the specified goal by calling `_run_goal_loop`, logs start and error, returns result or generic failure message. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Instantiates SemanticGatekeeper class. [4]

### 👥 Used By (Downstream)
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `3fc0e9` [1]: Manages orchestration of complex tasks and coordinates execution flow within the system. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `6ef306` [2]: Summarizes responsibility of TaskExecutor class, initializes attributes via __init__, and executes goal loop to refine answer based on feedback. _(Source: class TaskExecutor)_
> 🆔 `94d53c` [3]: Attempts to execute the specified goal by calling `_run_goal_loop`, logs start and error, returns result or generic failure message. _(Source: 🔌 TaskExecutor.solve_complex_task)_
> 🆔 `89a8a0` [4]: Instantiates SemanticGatekeeper class. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Defines a function that defines and offers a utility for converting user prompts into messages to be processed by an LLM model and returns the formatted response content.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Converts user prompt to messages and sends them to the specified LLM model, returning the processed response content. [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d05354` [1]: Defines a function that defines and offers a utility for converting user prompts into messages to be processed by an LLM model and returns the formatted response content. _(Source: Synthesis (based on [2]))_
> 🆔 `f27f60` [2]: Converts user prompt to messages and sends them to the specified LLM model, returning the processed response content. _(Source: chat_llm)_
</details>

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Defines and builds a dependency graph representing the structure of Python modules in a project by analyzing imports, function definitions, class definitions, assignments, annotations, and call interactions.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Traverses and analyzes Python code structure, collecting imports, assignments, annotations, function definitions, class definitions, and call interactions. [2]
- **`🔌 class GraphAnalyzer`**: Analyzes Python project structure to build and populate a dependency graph, identifies TODO comments, and handles errors during recursive file parsing. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes the current class definition from context and header stack. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Removes the current context from the stack and pops the header when leaving a function definition node, updating state accordingly. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Clears the current statement by setting it to None. [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Collects annotation assignment information and stores it in the entities dictionary for globals, including name, source code, signature, and privacy status. [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Collects global variable assignments from the module node and stores their names, source code snippets, default signatures, and privacy status as private. [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Analyzes call nodes and records interactions for the function being called if it is a simple name, storing the node in `self._record_interaction`. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Registers class definition by appending its name to context, retrieving source code, docstring, bases, and storing them in the `classes` dictionary. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Analyzes function definition, generates signature and header, extracts docstring, determines if unimplemented or private, stores component data in entities dictionary, identifies methods within classes. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Analyzes each imported module name, retrieves the corresponding code for the module node, and adds the resolved module names to `external_imports`. [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes and records external imports, computes module names based on import paths, resolves potential file paths, checks for existing project files, handles directory imports, and updates import mappings accordingly. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Analyzes `cst.Name` nodes, records interactions if context is non-empty and last context matches node value, then calls `_record_interaction`. [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Updates the current_statement attribute to the provided node in the visit_SimpleStatementLine method of CodeEntityVisitor class. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds and populates the dependency graph of Python files in the project. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `02be1c` [1]: Defines and builds a dependency graph representing the structure of Python modules in a project by analyzing imports, function definitions, class definitions, assignments, annotations, and call interactions. _(Source: Synthesis (based on [7], [16], [5], [9], [12], [13], [10], [2], [14], [3], [6], [8], [4], [15], [11]))_
> 🆔 `3d5660` [2]: Traverses and analyzes Python code structure, collecting imports, assignments, annotations, function definitions, class definitions, and call interactions. _(Source: class CodeEntityVisitor)_
> 🆔 `6e407e` [3]: Analyzes Python project structure to build and populate a dependency graph, identifies TODO comments, and handles errors during recursive file parsing. _(Source: class GraphAnalyzer)_
> 🆔 `814978` [4]: Removes the current class definition from context and header stack. _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `0b0174` [5]: Removes the current context from the stack and pops the header when leaving a function definition node, updating state accordingly. _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `70c968` [6]: Clears the current statement by setting it to None. _(Source: 🔌 CodeEntityVisitor.leave_SimpleStatementLine)_
> 🆔 `046683` [7]: Collects annotation assignment information and stores it in the entities dictionary for globals, including name, source code, signature, and privacy status. _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `7b34d4` [8]: Collects global variable assignments from the module node and stores their names, source code snippets, default signatures, and privacy status as private. _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `11d4ee` [9]: Analyzes call nodes and records interactions for the function being called if it is a simple name, storing the node in `self._record_interaction`. _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `35dec5` [10]: Registers class definition by appending its name to context, retrieving source code, docstring, bases, and storing them in the `classes` dictionary. _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `baf944` [11]: Analyzes function definition, generates signature and header, extracts docstring, determines if unimplemented or private, stores component data in entities dictionary, identifies methods within classes. _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `1e80c7` [12]: Analyzes each imported module name, retrieves the corresponding code for the module node, and adds the resolved module names to `external_imports`. _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `2e3f45` [13]: Analyzes and records external imports, computes module names based on import paths, resolves potential file paths, checks for existing project files, handles directory imports, and updates import mappings accordingly. _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `54db3a` [14]: Analyzes `cst.Name` nodes, records interactions if context is non-empty and last context matches node value, then calls `_record_interaction`. _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `9a3afe` [15]: Updates the current_statement attribute to the provided node in the visit_SimpleStatementLine method of CodeEntityVisitor class. _(Source: 🔌 CodeEntityVisitor.visit_SimpleStatementLine)_
> 🆔 `06978a` [16]: Builds and populates the dependency graph of Python files in the project. _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Defines an interface for querying and managing memory collections in ChromaDB, including adding memories with metadata, querying based on queries and turns, updating helpfulness, and cleaning up low-quality memories.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Manages interaction with ChromaDB, initializing client and collection, adding memories, querying based on queries and turns, updating helpfulness, and cleaning up low-quality memories. [2]
- **`🔌 class MemoryInterface`**: Defines interface for querying memory. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Adds a new memory to the ChromaDB collection with unique ID, combined metadata including turn_added and helpfulness, and provided text and embedding. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Identifies and removes low-quality memories based on helpfulness threshold and last used turn, deleting specified memory IDs from the collection. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Queries the memory collection for documents matching the given query, updates the last used turn of each document metadata based on current_turn, and returns the results including ids, documents, metadatas, and distances. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Updates the `helpfulness` value of a specified memory in the Chroma database. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `2b3eab` [1]: Defines an interface for querying and managing memory collections in ChromaDB, including adding memories with metadata, querying based on queries and turns, updating helpfulness, and cleaning up low-quality memories. _(Source: Synthesis (based on [3], [2], [4], [6], [8], [7], [5]))_
> 🆔 `222e7d` [2]: Manages interaction with ChromaDB, initializing client and collection, adding memories, querying based on queries and turns, updating helpfulness, and cleaning up low-quality memories. _(Source: class ChromaMemory)_
> 🆔 `08e1a1` [3]: Defines interface for querying memory. _(Source: class MemoryInterface)_
> 🆔 `4a6044` [4]: Adds a new memory to the ChromaDB collection with unique ID, combined metadata including turn_added and helpfulness, and provided text and embedding. _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `edc5cf` [5]: Identifies and removes low-quality memories based on helpfulness threshold and last used turn, deleting specified memory IDs from the collection. _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `8d69e7` [6]: Queries the memory collection for documents matching the given query, updates the last used turn of each document metadata based on current_turn, and returns the results including ids, documents, metadatas, and distances. _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `bc508f` [7]: Updates the `helpfulness` value of a specified memory in the Chroma database. _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Defines a system that analyzes and classifies modules based on their names, source code structure, dependencies, and other metadata to determine their archetype such as ENTRY_POINT, DATA_MODEL, CONFIGURATION, SERVICE, or UTILITY.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Initializes instance with provided module name and graph data. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Analyzes module based on name, source code structure, and dependencies to determine archetype such as ENTRY_POINT, DATA_MODEL, CONFIGURATION, SERVICE, or UTILITY. [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a73e11` [1]: Defines a system that analyzes and classifies modules based on their names, source code structure, dependencies, and other metadata to determine their archetype such as ENTRY_POINT, DATA_MODEL, CONFIGURATION, SERVICE, or UTILITY. _(Source: Synthesis (based on [4], [3], [2]))_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `a0c438` [3]: Initializes instance with provided module name and graph data. _(Source: class ModuleClassifier)_
> 🆔 `51d099` [4]: Analyzes module based on name, source code structure, and dependencies to determine archetype such as ENTRY_POINT, DATA_MODEL, CONFIGURATION, SERVICE, or UTILITY. _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Defines a system for contextualizing and synthesizing module information by analyzing source code structure and generating descriptive roles.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Inits dependencies and initializes module state by setting up file path, graph data, context, gatekeeper, task executor, classifier, archetype, component analyst, dependency analyst, and usage map. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Executes an analysis pipeline on the module, updating working memory and alerts based on components and dependencies, then applies systemic synthesis to critique instruction. [3]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Instantiates class `TaskExecutor`. [4]
- **`module_classifier.py`**: Instantiates ModuleClassifier. [5]
- **`summary_models.py`**: Instantiates summary_models class. [6]
- **`dependency_analyst.py`**: Instantiates class DependencyAnalyst. [7]
- **`component_analyst.py`**: Instantiates ComponentAnalyst. [8]
- **`semantic_gatekeeper.py`**: Instantiates SemanticGatekeeper. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a7e782` [1]: Defines a system for contextualizing and synthesizing module information by analyzing source code structure and generating descriptive roles. _(Source: Synthesis (based on [2], [3]))_
> 🆔 `061080` [2]: Inits dependencies and initializes module state by setting up file path, graph data, context, gatekeeper, task executor, classifier, archetype, component analyst, dependency analyst, and usage map. _(Source: class ModuleContextualizer)_
> 🆔 `9e93ab` [3]: Executes an analysis pipeline on the module, updating working memory and alerts based on components and dependencies, then applies systemic synthesis to critique instruction. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `c664a2` [4]: Instantiates class `TaskExecutor`. _(Source: Import task_executor.py)_
> 🆔 `083c27` [5]: Instantiates ModuleClassifier. _(Source: Import module_classifier.py)_
> 🆔 `dd783b` [6]: Instantiates summary_models class. _(Source: Import summary_models.py)_
> 🆔 `2a63da` [7]: Instantiates class DependencyAnalyst. _(Source: Import dependency_analyst.py)_
> 🆔 `5f8925` [8]: Instantiates ComponentAnalyst. _(Source: Import component_analyst.py)_
> 🆔 `480c13` [9]: Instantiates SemanticGatekeeper. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Defines a system for encapsulating and representing the role, dependencies, dependents, public API, alerts, and claims of various modules within a software project.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Computes SHA1 hash of unique string formed by concatenating `text`, `reference`, and `source_module`. [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Initializes default attributes for file path, archetype, module role, dependencies, dependents, public API, alerts, and claims. [5]
- **`🔌 🔌 Claim.id`**: Computes SHA1 hash of unique string formed by concatenating `text`, `reference`, and `source_module`. [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds an alert to the alerts list. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Adds dependency context to module by combining explanation and supporting claims, storing in `key_dependencies` dictionary. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds dependent context to the module, storing the combined explanation and placeholders in `key_dependents` dictionary with supporting claim IDs. [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds an entry to the public API dictionary for a given entity, combining description and placeholders from supporting claims. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Updates module role by appending provided text and placeholders to existing role, storing claim IDs. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `d67c20` [1]: Defines a system for encapsulating and representing the role, dependencies, dependents, public API, alerts, and claims of various modules within a software project. _(Source: Synthesis (based on [9], [5], [8], [4], [2], [3], [11], [10], [6], [7]))_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `d73662` [3]: Computes SHA1 hash of unique string formed by concatenating `text`, `reference`, and `source_module`. _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `9ad09d` [5]: Initializes default attributes for file path, archetype, module role, dependencies, dependents, public API, alerts, and claims. _(Source: class ModuleContext)_
> 🆔 `f70c6b` [6]: Computes SHA1 hash of unique string formed by concatenating `text`, `reference`, and `source_module`. _(Source: 🔌 Claim.id)_
> 🆔 `fd2ffa` [7]: Adds an alert to the alerts list. _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `ae04ae` [8]: Adds dependency context to module by combining explanation and supporting claims, storing in `key_dependencies` dictionary. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `4dbf7c` [9]: Adds dependent context to the module, storing the combined explanation and placeholders in `key_dependents` dictionary with supporting claim IDs. _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `e9dbab` [10]: Adds an entry to the public API dictionary for a given entity, combining description and placeholders from supporting claims. _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `daa122` [11]: Updates module role by appending provided text and placeholders to existing role, storing claim IDs. _(Source: 🔌 ModuleContext.set_module_role)_
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