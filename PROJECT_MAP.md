# Project Context Map

**Total Modules:** 15

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates parsing arguments and running main logic [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Interprets command-line arguments provided to the program and stores them in the args variable for further processing within the main function [2]
- **`🔌 goal`**: Assigns the value of goal argument to a variable for further processing in main function [3]
- **`🔌 main`**: Runs CrawlerAgent to process target folder based on goal parameter [4]
- **`🔌 parser`**: Creates an argument parser to handle command-line arguments for specifying goals and target folders, then passes these values to a main function to execute processing based on the provided goal and target folder path. [5]
- **`🔌 result`**: Calls main function with goal and target folder arguments to process specified task [6]
- **`🔌 target_folder`**: Assigns the target folder specified by user input to a variable for use in main function [7]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Imports a module containing logic and uses exported functions/classes such as CrawlerAgent for operations.. [8]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a02b94` [1]: Orchestrates parsing arguments and running main logic _(Source: Synthesis)_
> 🆔 `c45331` [2]: Interprets command-line arguments provided to the program and stores them in the args variable for further processing within the main function _(Source: args)_
> 🆔 `531f4b` [3]: Assigns the value of goal argument to a variable for further processing in main function _(Source: goal)_
> 🆔 `6e35b0` [4]: Runs CrawlerAgent to process target folder based on goal parameter _(Source: main)_
> 🆔 `28c6a2` [5]: Creates an argument parser to handle command-line arguments for specifying goals and target folders, then passes these values to a main function to execute processing based on the provided goal and target folder path. _(Source: parser)_
> 🆔 `36bd4e` [6]: Calls main function with goal and target folder arguments to process specified task _(Source: result)_
> 🆔 `0bc719` [7]: Assigns the target folder specified by user input to a variable for use in main function _(Source: target_folder)_
> 🆔 `fc9f33` [8]: Uses `agent_core.py`: Imports a module containing logic and uses exported functions/classes such as CrawlerAgent for operations.. _(Source: Import agent_core.py)_
</details>

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Manages crawling operations

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Manages crawling operations, manages memory for specific duration [2]
- **`🔌 🔌 CrawlerAgent.run`**: Prints crawler details, generates project map, renders report, cleans memory for 5 turns [3]

### 🔗 Uses (Upstream)
- **`agent_util.py`**: Imports `agent_util.py`. [4]
- **`memory_core.py`**: Uses `memory_core.py`: Imports and utilizes constants/types from module `agent_core.py` to define interface signature, retrieve metadata, update helpfulness value, and save updated metadata within its implementation. [5]
- **`llm_util.py`**: Uses `llm_util.py`: Calls chat_llm function to handle prompt processing and response generation. [6]
- **`agent_config.py`**: Uses `agent_config.py`: Exports Logic. [7]
- **`summary_models.py`**: Imports `summary_models.py`. [8]
- **`report_renderer.py`**: Imports `report_renderer.py`. [9]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8a2bce` [1]: Manages crawling operations _(Source: Synthesis)_
> 🆔 `01a437` [2]: Manages crawling operations, manages memory for specific duration _(Source: class CrawlerAgent)_
> 🆔 `be3899` [3]: Prints crawler details, generates project map, renders report, cleans memory for 5 turns _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `d95bb5` [4]: Imports `agent_util.py`. _(Source: Import agent_util.py)_
> 🆔 `636863` [5]: Uses `memory_core.py`: Imports and utilizes constants/types from module `agent_core.py` to define interface signature, retrieve metadata, update helpfulness value, and save updated metadata within its implementation. _(Source: Import memory_core.py)_
> 🆔 `b365d7` [6]: Uses `llm_util.py`: Calls chat_llm function to handle prompt processing and response generation. _(Source: Import llm_util.py)_
> 🆔 `dcfc98` [7]: Uses `agent_config.py`: Exports Logic. _(Source: Import agent_config.py)_
> 🆔 `dfcb1d` [8]: Imports `summary_models.py`. _(Source: Import summary_models.py)_
> 🆔 `8b28fd` [9]: Imports `report_renderer.py`. _(Source: Import report_renderer.py)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Analyzes interaction values and records function interactions

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Defines ProjectGraph as a dictionary capable of holding any type of values [2]
- **`🔌 class ProjectSummarizer`**: Organizes and processes project components, dependencies, and contexts iteratively [3]
- **`🔌 project_pulse`**: Verifies file existence, analyzes project structure using analyzer, generates module contexts for summarization [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Iteratively refines module contexts by generating new contexts based on updated source code, dependencies, and critiques, and caches unchanged paths after each cycle [5]
- **`🔒 _create_module_context`**: Generates module context by contextualizing module with critique instruction [6]

### 🔗 Uses (Upstream)
- **`graph_analyzer.py`**: Imports `graph_analyzer.py`. [7]
- **`module_contextualizer.py`**: Imports `module_contextualizer.py`. [8]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to process input prompt and generate JSON output. [9]
- **`summary_models.py`**: Imports `summary_models.py`. [10]
- **`map_critic.py`**: Imports `map_critic.py`. [11]
- **`report_renderer.py`**: Uses `report_renderer.py`: agent_util.py calls ReportRenderer to organize and write module documentation into output files.. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `95732b` [1]: Analyzes interaction values and records function interactions _(Source: Synthesis)_
> 🆔 `f8cc6a` [2]: Defines ProjectGraph as a dictionary capable of holding any type of values _(Source: ProjectGraph)_
> 🆔 `1f77d7` [3]: Organizes and processes project components, dependencies, and contexts iteratively _(Source: class ProjectSummarizer)_
> 🆔 `b5a7f9` [4]: Verifies file existence, analyzes project structure using analyzer, generates module contexts for summarization _(Source: project_pulse)_
> 🆔 `c3b49f` [5]: Iteratively refines module contexts by generating new contexts based on updated source code, dependencies, and critiques, and caches unchanged paths after each cycle _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `3b5bbe` [6]: Generates module context by contextualizing module with critique instruction _(Source: _create_module_context)_
> 🆔 `17eb3f` [7]: Imports `graph_analyzer.py`. _(Source: Import graph_analyzer.py)_
> 🆔 `335466` [8]: Imports `module_contextualizer.py`. _(Source: Import module_contextualizer.py)_
> 🆔 `dfc2da` [9]: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to process input prompt and generate JSON output. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `0e8ce6` [10]: Imports `summary_models.py`. _(Source: Import summary_models.py)_
> 🆔 `c54d03` [11]: Imports `map_critic.py`. _(Source: Import map_critic.py)_
> 🆔 `aaedae` [12]: Uses `report_renderer.py`: agent_util.py calls ReportRenderer to organize and write module documentation into output files.. _(Source: Import report_renderer.py)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes component structure, generates skeletons for code transformation, and synthesizes role descriptions without referencing the class directly.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes module components, generates skeleton code, synthesizes structural role description without referencing the class directly [2]
- **`🔌 class SkeletonTransformer`**: Manages transformation of function, class, and async function definitions by modifying their bodies or attributes [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes module components by extracting globals, functions, classes, and their interactions [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Transforms source code by adding ellipsis placeholder to function definitions [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Modifies async function definition by appending constant expression value to its body [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from class definition node and appends Pass if no body remains [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Modifies function definition node by appending expression to body [8]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Imports `semantic_gatekeeper.py`. [9]
- **`summary_models.py`**: Uses `summary_models.py`: Imports and utilizes the GroundedText and Alert data structures for handling textual information; Calls functions/classes for generating unique identifiers, encapsulating object identification based on attributes, adding supporting claims to text, creating grounded text modules, and storing module context.. [10]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `6667d9` [1]: Analyzes component structure, generates skeletons for code transformation, and synthesizes role descriptions without referencing the class directly. _(Source: Synthesis)_
> 🆔 `200d95` [2]: Analyzes module components, generates skeleton code, synthesizes structural role description without referencing the class directly _(Source: class ComponentAnalyst)_
> 🆔 `6ad0ee` [3]: Manages transformation of function, class, and async function definitions by modifying their bodies or attributes _(Source: class SkeletonTransformer)_
> 🆔 `dc3713` [4]: Analyzes module components by extracting globals, functions, classes, and their interactions _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `26e526` [5]: Transforms source code by adding ellipsis placeholder to function definitions _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `d1f2a7` [6]: Modifies async function definition by appending constant expression value to its body _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `40e662` [7]: Removes docstring from class definition node and appends Pass if no body remains _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `208553` [8]: Modifies function definition node by appending expression to body _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `c4adc2` [9]: Imports `semantic_gatekeeper.py`. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `560e8e` [10]: Uses `summary_models.py`: Imports and utilizes the GroundedText and Alert data structures for handling textual information; Calls functions/classes for generating unique identifiers, encapsulating object identification based on attributes, adding supporting claims to text, creating grounded text modules, and storing module context.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Analyzes dependency structure for modules

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Encapsulates semantic gatekeeping logic for dependency analysis [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Gathers dependency information for modules [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: dependency_analyst.py calls SemanticGatekeeper to process input prompt and generate JSON output with specified fields. [4]
- **`summary_models.py`**: Uses `summary_models.py`: Calls the `compute_unique_id` function to generate a unique identifier for objects based on specific attributes.. [5]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `fc0cbb` [1]: Analyzes dependency structure for modules _(Source: Synthesis)_
> 🆔 `6bc541` [2]: Encapsulates semantic gatekeeping logic for dependency analysis _(Source: class DependencyAnalyst)_
> 🆔 `c92cbe` [3]: Gathers dependency information for modules _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `16d9ff` [4]: Uses `semantic_gatekeeper.py`: dependency_analyst.py calls SemanticGatekeeper to process input prompt and generate JSON output with specified fields. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `ca9f42` [5]: Uses `summary_models.py`: Calls the `compute_unique_id` function to generate a unique identifier for objects based on specific attributes.. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Analyzes code structure and dependencies recursively

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Analyzes code structure and gathers entity information [2]
- **`🔌 class GraphAnalyzer`**: Encapsulates graph structure and dependencies for analysis [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes current context from stack by popping it [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Removes current context from stack when leaving function definition [5]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Collects annotated assignment information and adds to global entities list [6]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Collects global variable assignments from module code [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Records interaction value from function name in call node [8]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Appends class name to current context [9]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Collects function definition details and organizes into entities [10]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Collects module names from import aliases and adds them to external imports set [11]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes import from nodes to determine module names and paths [12]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records interaction value if not in current context or matches last context item [13]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds graph using depth-first search recursively [14]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ca838d` [1]: Analyzes code structure and dependencies recursively _(Source: Synthesis)_
> 🆔 `06e8c3` [2]: Analyzes code structure and gathers entity information _(Source: class CodeEntityVisitor)_
> 🆔 `750c69` [3]: Encapsulates graph structure and dependencies for analysis _(Source: class GraphAnalyzer)_
> 🆔 `3fac96` [4]: Removes current context from stack by popping it _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `94bc56` [5]: Removes current context from stack when leaving function definition _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `5c1e26` [6]: Collects annotated assignment information and adds to global entities list _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `a76157` [7]: Collects global variable assignments from module code _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `ab8344` [8]: Records interaction value from function name in call node _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `428015` [9]: Appends class name to current context _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `8edbc5` [10]: Collects function definition details and organizes into entities _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `1c3c16` [11]: Collects module names from import aliases and adds them to external imports set _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `954244` [12]: Analyzes import from nodes to determine module names and paths _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `55b5c8` [13]: Records interaction value if not in current context or matches last context item _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `d99ca3` [14]: Builds graph using depth-first search recursively _(Source: 🔌 GraphAnalyzer.analyze)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Analyzes project critiques and generates feedback

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Manages module critiques by parsing project map content and analyzing modules for specific flaws [2]
- **`🔌 🔌 MapCritic.critique`**: Manages module critiques by parsing project map content and analyzing modules to generate critiques [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: map_critic.py calls SemanticGatekeeper to process input data and generate safe JSON output. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `58ffe8` [1]: Analyzes project critiques and generates feedback _(Source: Synthesis)_
> 🆔 `87f164` [2]: Manages module critiques by parsing project map content and analyzing modules for specific flaws _(Source: class MapCritic)_
> 🆔 `f78dfc` [3]: Manages module critiques by parsing project map content and analyzing modules to generate critiques _(Source: 🔌 MapCritic.critique)_
> 🆔 `4e8ab2` [4]: Uses `semantic_gatekeeper.py`: map_critic.py calls SemanticGatekeeper to process input data and generate safe JSON output. _(Source: Import semantic_gatekeeper.py)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Manages querying, storing, updating, and cleaning memory data by utilizing a ChromaDB client connection

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Encapsulates a ChromaDB client connection and manages memory data [2]
- **`🔌 class MemoryInterface`**: Serves as an interface for querying memory data [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Creates unique memory ID, combines metadata fields into combined_metadata dictionary, updates collection with document text, embedding vector, and combined metadata [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Deletes memories based on helpfulness threshold and last usage turn [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Queries memory for specified query and updates metadata with current turn [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Retrieves metadata, updates helpfulness value, saves updated metadata [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `bdbebd` [1]: Manages querying, storing, updating, and cleaning memory data by utilizing a ChromaDB client connection _(Source: Synthesis)_
> 🆔 `aab1b5` [2]: Encapsulates a ChromaDB client connection and manages memory data _(Source: class ChromaMemory)_
> 🆔 `455d6d` [3]: Serves as an interface for querying memory data _(Source: class MemoryInterface)_
> 🆔 `72676a` [4]: Creates unique memory ID, combines metadata fields into combined_metadata dictionary, updates collection with document text, embedding vector, and combined metadata _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `16a891` [5]: Deletes memories based on helpfulness threshold and last usage turn _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `f3814c` [6]: Queries memory for specified query and updates metadata with current turn _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `eea90d` [7]: Retrieves metadata, updates helpfulness value, saves updated metadata _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `a118a7` [8]: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Analyzes module characteristics for classification

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Analyzes module characteristics and determines its archetype based on provided data [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Determines module archetype based on name, source code, entities, dependencies, functions, classes, and global variables [4]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a3b1b9` [1]: Analyzes module characteristics for classification _(Source: Synthesis)_
> 🆔 `a94772` [2]: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `d8a9af` [3]: Analyzes module characteristics and determines its archetype based on provided data _(Source: class ModuleClassifier)_
> 🆔 `2c2d48` [4]: Determines module archetype based on name, source code, entities, dependencies, functions, classes, and global variables _(Source: 🔌 ModuleClassifier.classify)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Analyzes components, synthesizes role definitions, and generates structured documentation for modules

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Analyzes module components, builds usage map based on dependencies, and synthesizes systemic role based on context [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Checks for errors, analyzes components and dependencies, performs systemic synthesis, passes alerts [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to process input and generate filtered JSON output.. [4]
- **`component_analyst.py`**: Uses `component_analyst.py`: Imports and modifies the async function definition by appending constant expression value to its body. [5]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Calls DependencyAnalyst class to gather dependency information for modules. [6]
- **`summary_models.py`**: Uses `summary_models.py`: Imports required data structures. [7]
- **`module_classifier.py`**: Uses `module_classifier.py`: Imports the specified file and utilizes its exported data container.. [8]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `aa6e71` [1]: Analyzes components, synthesizes role definitions, and generates structured documentation for modules _(Source: Synthesis)_
> 🆔 `2b1633` [2]: Analyzes module components, builds usage map based on dependencies, and synthesizes systemic role based on context _(Source: class ModuleContextualizer)_
> 🆔 `120a3f` [3]: Checks for errors, analyzes components and dependencies, performs systemic synthesis, passes alerts _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `fd2d49` [4]: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to process input and generate filtered JSON output.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `4895c9` [5]: Uses `component_analyst.py`: Imports and modifies the async function definition by appending constant expression value to its body. _(Source: Import component_analyst.py)_
> 🆔 `c04083` [6]: Uses `dependency_analyst.py`: Calls DependencyAnalyst class to gather dependency information for modules. _(Source: Import dependency_analyst.py)_
> 🆔 `aa3e99` [7]: Uses `summary_models.py`: Imports required data structures. _(Source: Import summary_models.py)_
> 🆔 `42ac13` [8]: Uses `module_classifier.py`: Imports the specified file and utilizes its exported data container.. _(Source: Import module_classifier.py)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Organizes, processes, and writes module documentation into output files

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Organizes, processes, and writes module documentation into output files [2]
- **`🔌 replace_ref`**: Replaces reference identifiers in text using mapping dictionary [3]
- **`🔌 sub`**: Maintains claim mapping using dictionary [4]
- **`🔌 🔌 ReportRenderer.render`**: Organizes and writes module documentation into output file [5]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: Imports and utilizes exported data types for report generation. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `10bb45` [1]: Organizes, processes, and writes module documentation into output files _(Source: Synthesis)_
> 🆔 `bf0c40` [2]: Organizes, processes, and writes module documentation into output files _(Source: class ReportRenderer)_
> 🆔 `466527` [3]: Replaces reference identifiers in text using mapping dictionary _(Source: replace_ref)_
> 🆔 `13a31a` [4]: Maintains claim mapping using dictionary _(Source: sub)_
> 🆔 `5fcba5` [5]: Organizes and writes module documentation into output file _(Source: 🔌 ReportRenderer.render)_
> 🆔 `d745cb` [6]: Uses `summary_models.py`: Imports and utilizes exported data types for report generation. _(Source: Import summary_models.py)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Processes input prompts, generates responses, and critiques content safety

**Impact Analysis:** Changes to this module will affect: agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Creates an immutable set containing disallowed descriptive words for use in filtering content. [2]
- **`🔌 class SemanticGatekeeper`**: Processes input data, generates JSON output, and ensures safety through parsing and critique [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Processes input prompt to generate JSON output with specified field [4]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Uses `llm_util.py`: Invokes a processing routine to handle messages and produce output. [5]
- **`agent_config.py`**: Uses `agent_config.py`: Imports and uses the configuration value for preferred language model to Granite4-3b from a module without directly referencing its name (⚠️ The code sets a configuration value for preferred language model to Granite4-3b without directly referencing its name. However, there is no clear evidence of the use or import of this specific model from another module.); semantic_gatekeeper.py calls functions or classes. [6]

### 👥 Used By (Downstream)
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_critic.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a829af` [1]: Processes input prompts, generates responses, and critiques content safety _(Source: Synthesis)_
> 🆔 `fea0ec` [2]: Creates an immutable set containing disallowed descriptive words for use in filtering content. _(Source: BANNED_ADJECTIVES)_
> 🆔 `02de91` [3]: Processes input data, generates JSON output, and ensures safety through parsing and critique _(Source: class SemanticGatekeeper)_
> 🆔 `f6f144` [4]: Processes input prompt to generate JSON output with specified field _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `5eaaf9` [5]: Uses `llm_util.py`: Invokes a processing routine to handle messages and produce output. _(Source: Import llm_util.py)_
> 🆔 `17517d` [6]: Uses `agent_config.py`: Imports and uses the configuration value for preferred language model to Granite4-3b from a module without directly referencing its name (⚠️ The code sets a configuration value for preferred language model to Granite4-3b without directly referencing its name. However, there is no clear evidence of the use or import of this specific model from another module.); semantic_gatekeeper.py calls functions or classes. _(Source: Import agent_config.py)_
</details>

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Manages summarization logic for text analysis workflows

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Encapsulates unique identifier generation for objects based on specific attributes [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Encapsulates module context details, manages claims and placeholders through explicit mapping algorithms, organizes role definitions by constructing GroundedText instances, and structures dependency and dependent contexts via aggregation functions [5]
- **`🔌 🔌 Claim.id`**: Computes unique identifier for object by concatenating text, reference, source module attributes into string, hashing it using SHA-1 algorithm [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Appends alert to list of alerts [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Collects module path explanation and supporting claims to create grounded text for dependency context. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds module context by combining explanation with supporting claims and storing in key_dependents [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds public API entry for an entity with description, placeholders, and claim IDs [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Adds supporting claims to text and creates GroundedText module role [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8f09a6` [1]: Manages summarization logic for text analysis workflows _(Source: Synthesis)_
> 🆔 `cdaf82` [2]: Data container for Alert records. _(Source: class Alert)_
> 🆔 `07f144` [3]: Encapsulates unique identifier generation for objects based on specific attributes _(Source: class Claim)_
> 🆔 `b77290` [4]: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `10495e` [5]: Encapsulates module context details, manages claims and placeholders through explicit mapping algorithms, organizes role definitions by constructing GroundedText instances, and structures dependency and dependent contexts via aggregation functions _(Source: class ModuleContext)_
> 🆔 `685e72` [6]: Computes unique identifier for object by concatenating text, reference, source module attributes into string, hashing it using SHA-1 algorithm _(Source: 🔌 Claim.id)_
> 🆔 `0f8c2e` [7]: Appends alert to list of alerts _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `75f6ec` [8]: Collects module path explanation and supporting claims to create grounded text for dependency context. _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `a67c85` [9]: Adds module context by combining explanation with supporting claims and storing in key_dependents _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `53c996` [10]: Adds public API entry for an entity with description, placeholders, and claim IDs _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `9cdf35` [11]: Adds supporting claims to text and creates GroundedText module role _(Source: 🔌 ModuleContext.set_module_role)_
</details>

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Provides functionality for input message handling and LLM response content generation

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Processes prompt or messages and generates LLM response content [2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `ccafed` [1]: Provides functionality for input message handling and LLM response content generation _(Source: Synthesis)_
> 🆔 `c23c11` [2]: Processes prompt or messages and generates LLM response content _(Source: chat_llm)_
</details>

---
## 🔧 Configuration

## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [1]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Sets global variable to specify maximum context length used in processing [2]
- **`🔌 DEFAULT_MODEL`**: Sets configuration value for preferred language model to Granite4-3b [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `449512` [1]: Defines configuration constants. _(Source: Archetype)_
> 🆔 `bab4b4` [2]: Sets global variable to specify maximum context length used in processing _(Source: CONTEXT_LIMIT)_
> 🆔 `84707f` [3]: Sets configuration value for preferred language model to Granite4-3b _(Source: DEFAULT_MODEL)_
</details>

---