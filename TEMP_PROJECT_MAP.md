# Project Context Map

**Total Modules:** 16

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates crawling process [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Extracts command-line arguments using ArgumentParser and stores them in args variable for further processing. [2]
- **`🔌 goal`**: Retrieves value from command line arguments for further processing in main function [3]
- **`🔌 main`**: Runs crawler agent to analyze specified goal within target folder [4]
- **`🔌 parser`**: Creates an argument parser to define command line options for the program's execution. [5]
- **`🔌 result`**: Invokes main function with specified goal and target folder to process data [6]
- **`🔌 target_folder`**: Assigns the target folder value from command line arguments to a local variable for use in subsequent code execution [7]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Imports and employs various constants/types to manage goal configurations, target definitions, memory storage mechanisms, crawler setups, project layouts, synthesizer parameters, system summaries, report creation processes, and analysis completion notifications; Calls the CrawlerAgent class to initiate crawling with specific goals and target roots.. [8]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8fc8a1` [1]: Orchestrates crawling process _(Source: Synthesis)_
> 🆔 `d1580c` [2]: Extracts command-line arguments using ArgumentParser and stores them in args variable for further processing. _(Source: args)_
> 🆔 `20d32e` [3]: Retrieves value from command line arguments for further processing in main function _(Source: goal)_
> 🆔 `7b9f35` [4]: Runs crawler agent to analyze specified goal within target folder _(Source: main)_
> 🆔 `426cb8` [5]: Creates an argument parser to define command line options for the program's execution. _(Source: parser)_
> 🆔 `680892` [6]: Invokes main function with specified goal and target folder to process data _(Source: result)_
> 🆔 `300858` [7]: Assigns the target folder value from command line arguments to a local variable for use in subsequent code execution _(Source: target_folder)_
> 🆔 `65135d` [8]: Uses `agent_core.py`: Imports and employs various constants/types to manage goal configurations, target definitions, memory storage mechanisms, crawler setups, project layouts, synthesizer parameters, system summaries, report creation processes, and analysis completion notifications; Calls the CrawlerAgent class to initiate crawling with specific goals and target roots.. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Manages project structure and memory using CrawlingAgent

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Manages goal, target root, memory storage, crawler details, project map, synthesizer configuration, system summary, report rendering, and analysis completion message [2]
- **`🔌 🔌 CrawlerAgent.run`**: Prints crawler details, retrieves project map, creates synthesizer with gatekeeper, synthesizes system summary, renders report using renderer, cleans memory, and returns analysis completion message. [3]

### 🔗 Uses (Upstream)
- **`memory_core.py`**: Uses `memory_core.py`: Incorporates a module's capabilities for handling abstract interfaces and querying memory data; Calls functions/classes/logic from memory-related module via ChromaMemory to manage user-defined memories in agent_core.py.. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Extracts relevant data structures for further use within agent_core.py; Invokes functionality from Context module. [5]
- **`agent_config.py`**: Uses `agent_config.py`: Retrieves the specified model string from the imported module to set default usage within the system. [6]
- **`map_synthesizer.py`**: Uses `map_synthesizer.py`: Calls MapSynthesizer to process and synthesize module summaries while checking for presence, fidelity, and hallucinations.. [7]
- **`llm_util.py`**: Uses `llm_util.py`: Calls the `chat_llm` function to process user input for LLM chat session.. [8]
- **`agent_util.py`**: Uses `agent_util.py`: Calls the `project_pulse` function to initiate or interact with project dependencies and critiques logic. [9]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls or invokes functionality from an external module. [10]
- **`report_renderer.py`**: Uses `report_renderer.py`: Imports necessary module for processing text and using exported data to substitute references with unique identifiers; Calls the ReportRenderer class to encapsulate and organize report data and rendering logic.. [11]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `0a7558` [1]: Manages project structure and memory using CrawlingAgent _(Source: Synthesis)_
> 🆔 `8e6802` [2]: Manages goal, target root, memory storage, crawler details, project map, synthesizer configuration, system summary, report rendering, and analysis completion message _(Source: class CrawlerAgent)_
> 🆔 `9f865e` [3]: Prints crawler details, retrieves project map, creates synthesizer with gatekeeper, synthesizes system summary, renders report using renderer, cleans memory, and returns analysis completion message. _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `735fa7` [4]: Uses `memory_core.py`: Incorporates a module's capabilities for handling abstract interfaces and querying memory data; Calls functions/classes/logic from memory-related module via ChromaMemory to manage user-defined memories in agent_core.py.. _(Source: Import memory_core.py)_
> 🆔 `b19332` [5]: Uses `summary_models.py`: Extracts relevant data structures for further use within agent_core.py; Invokes functionality from Context module. _(Source: Import summary_models.py)_
> 🆔 `7f08f8` [6]: Uses `agent_config.py`: Retrieves the specified model string from the imported module to set default usage within the system. _(Source: Import agent_config.py)_
> 🆔 `2ce702` [7]: Uses `map_synthesizer.py`: Calls MapSynthesizer to process and synthesize module summaries while checking for presence, fidelity, and hallucinations.. _(Source: Import map_synthesizer.py)_
> 🆔 `e34dc2` [8]: Uses `llm_util.py`: Calls the `chat_llm` function to process user input for LLM chat session.. _(Source: Import llm_util.py)_
> 🆔 `5ed75f` [9]: Uses `agent_util.py`: Calls the `project_pulse` function to initiate or interact with project dependencies and critiques logic. _(Source: Import agent_util.py)_
> 🆔 `922e72` [10]: Uses `semantic_gatekeeper.py`: Calls or invokes functionality from an external module. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `c83578` [11]: Uses `report_renderer.py`: Imports necessary module for processing text and using exported data to substitute references with unique identifiers; Calls the ReportRenderer class to encapsulate and organize report data and rendering logic.. _(Source: Import report_renderer.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Analyzes interaction patterns between modules, identifies relationships, and orchestrates the flow of information within the system architecture.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns a dictionary to store project-related data and values using string keys and any type values [2]
- **`🔌 class ProjectSummarizer`**: Organizes project dependencies and critiques in topological order [3]
- **`🔌 project_pulse`**: Analyzes project graph and generates contexts [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Updates module contexts based on dependencies and critiques [5]
- **`🔒 _create_module_context`**: Contextualizes module using contextualizer and sets file path if missing [6]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Retrieves GroundedText and Alert records from a module containing these types for use in agent_util.py; Calls functions/classes/logic from referenced module to generate unique identifiers and support claims.. [7]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: Retrieves global variable assignments from module node source code to analyze graph structure and dependencies.; Calls the GraphAnalyzer class to analyze module dependencies and imports.. [8]
- **`map_critic.py`**: Uses `map_critic.py`: Calls a module/class/function from `agent_util.py` to extract and critique project map content and modules. [9]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to manage restricted words and format prompts for system messages. [10]
- **`report_renderer.py`**: Uses `report_renderer.py`: Imports a module containing code to replace references in text with unique identifiers and store mappings of original references to their new identifiers; Exports report rendering functionality and uses ReportRenderer class internally. [11]
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: Invokes functionality from another module to process data and analyze dependencies. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ad6623` [1]: Analyzes interaction patterns between modules, identifies relationships, and orchestrates the flow of information within the system architecture. _(Source: Synthesis)_
> 🆔 `568eab` [2]: Assigns a dictionary to store project-related data and values using string keys and any type values _(Source: ProjectGraph)_
> 🆔 `cb504a` [3]: Organizes project dependencies and critiques in topological order _(Source: class ProjectSummarizer)_
> 🆔 `cb786a` [4]: Analyzes project graph and generates contexts _(Source: project_pulse)_
> 🆔 `bbfc39` [5]: Updates module contexts based on dependencies and critiques _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `39d3be` [6]: Contextualizes module using contextualizer and sets file path if missing _(Source: _create_module_context)_
> 🆔 `d73344` [7]: Uses `summary_models.py`: Retrieves GroundedText and Alert records from a module containing these types for use in agent_util.py; Calls functions/classes/logic from referenced module to generate unique identifiers and support claims.. _(Source: Import summary_models.py)_
> 🆔 `3ccb7d` [8]: Uses `graph_analyzer.py`: Retrieves global variable assignments from module node source code to analyze graph structure and dependencies.; Calls the GraphAnalyzer class to analyze module dependencies and imports.. _(Source: Import graph_analyzer.py)_
> 🆔 `8d647d` [9]: Uses `map_critic.py`: Calls a module/class/function from `agent_util.py` to extract and critique project map content and modules. _(Source: Import map_critic.py)_
> 🆔 `2a49c1` [10]: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to manage restricted words and format prompts for system messages. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `28c0ee` [11]: Uses `report_renderer.py`: Imports a module containing code to replace references in text with unique identifiers and store mappings of original references to their new identifiers; Exports report rendering functionality and uses ReportRenderer class internally. _(Source: Import report_renderer.py)_
> 🆔 `191726` [12]: Uses `module_contextualizer.py`: Invokes functionality from another module to process data and analyze dependencies. _(Source: Import module_contextualizer.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes, synthesizes, and transforms code components for system integration

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes component structure, identifies global variables and code elements, synthesizes insights into module behavior [2]
- **`🔌 class SkeletonTransformer`**: Modifies function definition bodies, appends constants, and removes docstrings from class definitions [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes module components, identifies global constants, functions, classes, their mechanisms, side effects, and state mutations to provide detailed insights into code structure and behavior. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Transforms source code by adding ellipsis expressions to function and class definitions, removing docstrings from functions and appending Pass statement if body is empty [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Modifies async function node by appending constant value to body [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from class definition node body [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Modifies function definition body to include ellipsis expression [8]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls the SemanticGatekeeper class and its methods for managing restricted words, formatting prompts, and processing data as an intermediary. [9]
- **`summary_models.py`**: Uses `summary_models.py`: Extracts data containers of GroundedText and Alert records for processing within component_analyst.py; Calls or uses functions/classes/logic such as unique identifier computation, encapsulation of attributes, adding supporting claims to text, and dependency context creation.. [10]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c83f5d` [1]: Analyzes, synthesizes, and transforms code components for system integration _(Source: Synthesis)_
> 🆔 `68160d` [2]: Analyzes component structure, identifies global variables and code elements, synthesizes insights into module behavior _(Source: class ComponentAnalyst)_
> 🆔 `ee844e` [3]: Modifies function definition bodies, appends constants, and removes docstrings from class definitions _(Source: class SkeletonTransformer)_
> 🆔 `bedfae` [4]: Analyzes module components, identifies global constants, functions, classes, their mechanisms, side effects, and state mutations to provide detailed insights into code structure and behavior. _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `5ec093` [5]: Transforms source code by adding ellipsis expressions to function and class definitions, removing docstrings from functions and appending Pass statement if body is empty _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `fdeb4b` [6]: Modifies async function node by appending constant value to body _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `f19000` [7]: Removes docstring from class definition node body _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `e2c8f0` [8]: Modifies function definition body to include ellipsis expression _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `a09274` [9]: Uses `semantic_gatekeeper.py`: Calls the SemanticGatekeeper class and its methods for managing restricted words, formatting prompts, and processing data as an intermediary. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `46b1b6` [10]: Uses `summary_models.py`: Extracts data containers of GroundedText and Alert records for processing within component_analyst.py; Calls or uses functions/classes/logic such as unique identifier computation, encapsulation of attributes, adding supporting claims to text, and dependency context creation.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Analyzes dependencies for logical processing

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Analyzes data dependencies for logical analysis [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes dependencies to determine data and logic usage [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls the SemanticGatekeeper class to manage restricted words and format prompts as system messages for application usage. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Imports and incorporates data structures for text and alerts; Calls functions/classes/logic to compute unique identifiers, encapsulate attributes, add supporting claims, and create ModuleContext instances for dependency analysis.. [5]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `6b29e5` [1]: Analyzes dependencies for logical processing _(Source: Synthesis)_
> 🆔 `b88ada` [2]: Analyzes data dependencies for logical analysis _(Source: class DependencyAnalyst)_
> 🆔 `7d8464` [3]: Analyzes dependencies to determine data and logic usage _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `061b94` [4]: Uses `semantic_gatekeeper.py`: Calls the SemanticGatekeeper class to manage restricted words and format prompts as system messages for application usage. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `414f54` [5]: Uses `summary_models.py`: Imports and incorporates data structures for text and alerts; Calls functions/classes/logic to compute unique identifiers, encapsulate attributes, add supporting claims, and create ModuleContext instances for dependency analysis.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Analyzes Python code structure and dependencies

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Analyzes code structure, identifies entities, tracks import interactions [2]
- **`🔌 class GraphAnalyzer`**: Computes dependency graph and manages Python files in project [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes current context from stack [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Removes current context from stack when leaving function definition node [5]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Collects annotated assignment target names and sources, adds them to global entities list [6]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Collects global variable assignments from module node source code [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Records interaction between function name value and call node [8]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Processes class definition node by appending its name to current context stack [9]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Analyzes function definition to determine if it is unimplemented or private [10]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Collects module names from imported aliases and adds them to external imports set [11]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes import statements to identify external and relative imports, updating internal state accordingly [12]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records interactions based on node value without current context clash [13]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds graph depth-first search, populates dependents, and returns graph [14]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `264f89` [1]: Analyzes Python code structure and dependencies _(Source: Synthesis)_
> 🆔 `e9a1a4` [2]: Analyzes code structure, identifies entities, tracks import interactions _(Source: class CodeEntityVisitor)_
> 🆔 `3e1d71` [3]: Computes dependency graph and manages Python files in project _(Source: class GraphAnalyzer)_
> 🆔 `dc3717` [4]: Removes current context from stack _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `69574e` [5]: Removes current context from stack when leaving function definition node _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `2190d0` [6]: Collects annotated assignment target names and sources, adds them to global entities list _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `534053` [7]: Collects global variable assignments from module node source code _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `8b5a71` [8]: Records interaction between function name value and call node _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `a762aa` [9]: Processes class definition node by appending its name to current context stack _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `6056cb` [10]: Analyzes function definition to determine if it is unimplemented or private _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `346510` [11]: Collects module names from imported aliases and adds them to external imports set _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `08fd80` [12]: Analyzes import statements to identify external and relative imports, updating internal state accordingly _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `111d7e` [13]: Records interactions based on node value without current context clash _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `9e3c8f` [14]: Builds graph depth-first search, populates dependents, and returns graph _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Analyzes project documentation, extracts modules, and critiques descriptions

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Analyzes project documentation, extracts modules, and critiques specific descriptions [2]
- **`🔌 🔌 MapCritic.critique`**: Parses project map content to extract modules and analyze them for instructions, returning up to three critiques. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls functions within the imported module.. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `10eac7` [1]: Analyzes project documentation, extracts modules, and critiques descriptions _(Source: Synthesis)_
> 🆔 `424608` [2]: Analyzes project documentation, extracts modules, and critiques specific descriptions _(Source: class MapCritic)_
> 🆔 `974bba` [3]: Parses project map content to extract modules and analyze them for instructions, returning up to three critiques. _(Source: 🔌 MapCritic.critique)_
> 🆔 `b1df9c` [4]: Uses `semantic_gatekeeper.py`: Calls functions within the imported module.. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` Analyzes module presence, fidelity, and hallucinations while updating summaries

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Manages summary generation, checks module presence, fidelity, and hallucinations for integration [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Iterates through processing order, synthesizes module summaries, checks for presence, fidelity, and hallucinations, updates summary if successful [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls or uses functions/classes/logic from the imported module to manage restricted words, format prompts, and process data. [4]
- **`llm_util.py`**: Uses `llm_util.py`: Calls the chat_llm function to process user input for an LLM chat session.. [5]
- **`summary_models.py`**: Uses `summary_models.py`: Imports Data containers for GroundedText and Alert records to work with these types of data in the module; Calls or uses functions/classes/logic related to unique identifier generation, encapsulation of attributes, addition of supporting claims to text, combining explanation with claim placeholders for context storage.. [6]
- **`agent_config.py`**: Uses `agent_config.py`: Imports a module providing a Granite 3b model string constant and uses it as the default application setting. [7]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f2d26f` [1]: Analyzes module presence, fidelity, and hallucinations while updating summaries _(Source: Synthesis)_
> 🆔 `c45214` [2]: Manages summary generation, checks module presence, fidelity, and hallucinations for integration _(Source: class MapSynthesizer)_
> 🆔 `8d5a20` [3]: Iterates through processing order, synthesizes module summaries, checks for presence, fidelity, and hallucinations, updates summary if successful _(Source: 🔌 MapSynthesizer.synthesize)_
> 🆔 `0a7cfb` [4]: Uses `semantic_gatekeeper.py`: Calls or uses functions/classes/logic from the imported module to manage restricted words, format prompts, and process data. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `cdf0a2` [5]: Uses `llm_util.py`: Calls the chat_llm function to process user input for an LLM chat session.. _(Source: Import llm_util.py)_
> 🆔 `d19b86` [6]: Uses `summary_models.py`: Imports Data containers for GroundedText and Alert records to work with these types of data in the module; Calls or uses functions/classes/logic related to unique identifier generation, encapsulation of attributes, addition of supporting claims to text, combining explanation with claim placeholders for context storage.. _(Source: Import summary_models.py)_
> 🆔 `031b88` [7]: Uses `agent_config.py`: Imports a module providing a Granite 3b model string constant and uses it as the default application setting. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Manages user-defined memories by storing, organizing, retrieving, and updating their metadata and helpfulness scores

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Manages storage, organization, retrieval, and evaluation of user-defined memories [2]
- **`🔌 class MemoryInterface`**: Provides an interface for querying memory data (⚠️ The code defines a class MemoryInterface with an empty method query_memory. The comment suggests it's supposed to provide an interface for querying memory data, but the implementation is not provided.) [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Creates unique memory ID, combines metadata, updates collection [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Retrieves all memories from collection including metadata, identifies memories to delete based on low helpfulness or infrequent use, deletes identified memories [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Retrieves memory results for query and updates last used turn [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Retrieves metadata for specified memory ID and updates its helpfulness score [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `4051ef` [1]: Manages user-defined memories by storing, organizing, retrieving, and updating their metadata and helpfulness scores _(Source: Synthesis)_
> 🆔 `4eea59` [2]: Manages storage, organization, retrieval, and evaluation of user-defined memories _(Source: class ChromaMemory)_
> 🆔 `d2c24c` [3]: Provides an interface for querying memory data (⚠️ The code defines a class MemoryInterface with an empty method query_memory. The comment suggests it's supposed to provide an interface for querying memory data, but the implementation is not provided.) _(Source: class MemoryInterface)_
> 🆔 `9a9d6e` [4]: Creates unique memory ID, combines metadata, updates collection _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `34a78c` [5]: Retrieves all memories from collection including metadata, identifies memories to delete based on low helpfulness or infrequent use, deletes identified memories _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `c6e20d` [6]: Retrieves memory results for query and updates last used turn _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `45c56a` [7]: Retrieves metadata for specified memory ID and updates its helpfulness score _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Analyzes source code, entities, and dependencies to categorize modules accurately

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Manages module attributes, analyzes name and source code, identifies entities and dependencies, and determines appropriate archetype classification [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Determines module archetype by analyzing name, source code, entities, dependencies, and behavior to categorize as ENTRY_POINT, SERVICE, DATA_MODEL, UTILITY, or CONFIGURATION. [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1012c8` [1]: Analyzes source code, entities, and dependencies to categorize modules accurately _(Source: Synthesis)_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `12cc47` [3]: Manages module attributes, analyzes name and source code, identifies entities and dependencies, and determines appropriate archetype classification _(Source: class ModuleClassifier)_
> 🆔 `ab48de` [4]: Determines module archetype by analyzing name, source code, entities, dependencies, and behavior to categorize as ENTRY_POINT, SERVICE, DATA_MODEL, UTILITY, or CONFIGURATION. _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Manages context for modules, synthesizes systemic aspects from critiques

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Analyzes code dependencies, builds usage map, synthesizes module purpose based on systemic analysis, gathers external context, and generates role description for the module archetype. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Checks for errors in data, analyzes components and dependencies using analyzers, synthesizes systemic aspects based on critique instruction, passes alerts to context. [3]

### 🔗 Uses (Upstream)
- **`module_classifier.py`**: Uses `module_classifier.py`: Imports and uses Data container for ModuleArchetype records and determines module archetype by analyzing various attributes to categorize modules.; Identifies and categorizes software components based on their attributes and relationships to other parts of a system.. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Computes unique identifier by concatenating attributes and hashing. [5]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls the SemanticGatekeeper class to manage restricted words and format prompts for system messages. [6]
- **`component_analyst.py`**: Uses `component_analyst.py`: Imports and uses constants from exported data to analyze module components, global variables, and code elements for detailed insights into behavior; Calls the ComponentAnalyst class or function within module_contextualizer.py to apply contextual transformations to source code. [7]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Brings in an analytical component to scrutinize relationships between various components of the system. [8]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `419e64` [1]: Manages context for modules, synthesizes systemic aspects from critiques _(Source: Synthesis)_
> 🆔 `9da0b9` [2]: Analyzes code dependencies, builds usage map, synthesizes module purpose based on systemic analysis, gathers external context, and generates role description for the module archetype. _(Source: class ModuleContextualizer)_
> 🆔 `c3c428` [3]: Checks for errors in data, analyzes components and dependencies using analyzers, synthesizes systemic aspects based on critique instruction, passes alerts to context. _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `07aac9` [4]: Uses `module_classifier.py`: Imports and uses Data container for ModuleArchetype records and determines module archetype by analyzing various attributes to categorize modules.; Identifies and categorizes software components based on their attributes and relationships to other parts of a system.. _(Source: Import module_classifier.py)_
> 🆔 `2b273c` [5]: Uses `summary_models.py`: Computes unique identifier by concatenating attributes and hashing. _(Source: Import summary_models.py)_
> 🆔 `e316b7` [6]: Uses `semantic_gatekeeper.py`: Calls the SemanticGatekeeper class to manage restricted words and format prompts for system messages. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `21155b` [7]: Uses `component_analyst.py`: Imports and uses constants from exported data to analyze module components, global variables, and code elements for detailed insights into behavior; Calls the ComponentAnalyst class or function within module_contextualizer.py to apply contextual transformations to source code. _(Source: Import component_analyst.py)_
> 🆔 `0ac257` [8]: Uses `dependency_analyst.py`: Brings in an analytical component to scrutinize relationships between various components of the system. _(Source: Import dependency_analyst.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Manages report generation and rendering processing workflow

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Encapsulates and organizes report data and rendering logic [2]
- **`🔌 replace_ref`**: Replaces references in text with unique identifiers and stores mapping [3]
- **`🔌 sub`**: Maps unique identifiers to sequential numbers and returns formatted identifier [4]
- **`🔌 🔌 ReportRenderer.render`**: Generates a structured report file [5]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Interacts with defined functions/classes/logic from another module within report_renderer.py. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `534710` [1]: Manages report generation and rendering processing workflow _(Source: Synthesis)_
> 🆔 `f217ed` [2]: Encapsulates and organizes report data and rendering logic _(Source: class ReportRenderer)_
> 🆔 `b37537` [3]: Replaces references in text with unique identifiers and stores mapping _(Source: replace_ref)_
> 🆔 `1350b3` [4]: Maps unique identifiers to sequential numbers and returns formatted identifier _(Source: sub)_
> 🆔 `fec0fc` [5]: Generates a structured report file _(Source: 🔌 ReportRenderer.render)_
> 🆔 `bb4305` [6]: Uses `summary_models.py`: Interacts with defined functions/classes/logic from another module within report_renderer.py. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Manages restricted word processing and executes semantic feedback loops

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, map_synthesizer.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Manages a set of restricted words for application usage [2]
- **`🔌 class SemanticGatekeeper`**: Acts as an intermediary for processing, verifying, and parsing data [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Formats prompt into system message [4]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Uses `llm_util.py`: Calls the chat_llm function to process user input for an LLM chat session.. [5]
- **`agent_config.py`**: Uses `agent_config.py`: Incorporates predefined values from imported module to establish model usage defaults.. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_critic.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b9be3c` [1]: Manages restricted word processing and executes semantic feedback loops _(Source: Synthesis)_
> 🆔 `25d2f6` [2]: Manages a set of restricted words for application usage _(Source: BANNED_ADJECTIVES)_
> 🆔 `8506fc` [3]: Acts as an intermediary for processing, verifying, and parsing data _(Source: class SemanticGatekeeper)_
> 🆔 `ecaef8` [4]: Formats prompt into system message _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `44d5c7` [5]: Uses `llm_util.py`: Calls the chat_llm function to process user input for an LLM chat session.. _(Source: Import llm_util.py)_
> 🆔 `4bcf09` [6]: Uses `agent_config.py`: Incorporates predefined values from imported module to establish model usage defaults.. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Manages summarization models, generates concise text summaries, and integrates with external services for analysis and storage

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Encapsulates attributes and provides unique identifier generation [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Synthesizes structural role, encapsulates state data, and organizes method functionality [5]
- **`🔌 🔌 Claim.id`**: Computes unique identifier by concatenating attributes and hashing [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Appends alert to list of alerts [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Adds dependency context to module by combining explanation with placeholders from supporting claims and storing in key dependencies dictionary. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Combines explanation with claim placeholders to create full text for context storage [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds public API entity with description and supporting claims to dictionary [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Adds supporting claims to text and creates GroundedText instance [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `7732af` [1]: Manages summarization models, generates concise text summaries, and integrates with external services for analysis and storage _(Source: Synthesis)_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `b649f9` [3]: Encapsulates attributes and provides unique identifier generation _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `4ec0cb` [5]: Synthesizes structural role, encapsulates state data, and organizes method functionality _(Source: class ModuleContext)_
> 🆔 `4addb0` [6]: Computes unique identifier by concatenating attributes and hashing _(Source: 🔌 Claim.id)_
> 🆔 `0f8c2e` [7]: Appends alert to list of alerts _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `d5f63f` [8]: Adds dependency context to module by combining explanation with placeholders from supporting claims and storing in key dependencies dictionary. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `909025` [9]: Combines explanation with claim placeholders to create full text for context storage _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `24424f` [10]: Adds public API entity with description and supporting claims to dictionary _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `72d813` [11]: Adds supporting claims to text and creates GroundedText instance _(Source: 🔌 ModuleContext.set_module_role)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Processes user input for LLM chat session

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Processes user input for LLM chat session [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `aa294d` [1]: Processes user input for LLM chat session _(Source: Synthesis)_
> 🆔 `0974d2` [2]: Processes user input for LLM chat session _(Source: chat_llm)_
</details>

---
## 🔧 Configuration

## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, map_synthesizer.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Sets global variable to define maximum context length for processing [2]
- **`🔌 DEFAULT_MODEL`**: Assigns string value specifying Granite 3b model for default use in application [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`map_synthesizer.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `449512` [1]: Defines configuration constants. _(Source: Archetype)_
> 🆔 `d7c570` [2]: Sets global variable to define maximum context length for processing _(Source: CONTEXT_LIMIT)_
> 🆔 `8ec12d` [3]: Assigns string value specifying Granite 3b model for default use in application _(Source: DEFAULT_MODEL)_
</details>

---