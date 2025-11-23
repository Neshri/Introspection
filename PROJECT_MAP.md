# Project Context Map

**Total Modules:** 14

## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Analyzes structured data representing claims, such as text content and source module information, to extract relevant insights and dependencies.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, module_contextualizer.py, report_renderer.py [ref:278a6d68c045eafbb6720b3eab10145db119bd58]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [ref:cdaf82fd4c021fa0a891dedd7d85fff3402f4bef]
- **`🔌 class Claim`**: Manages structured data representing claims, including attributes such as text content, reference identifiers, and source module information [ref:2af21c57c076c61bfa3a26301ad5da171b9058ce]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [ref:b7729088a8954b42aeaaf067fb7b5ca6c1bcaf4c]
- **`🔌 class ModuleContext`**: Manages structural context for modules, storing file paths and text representations of module roles, dependencies, and public APIs, along with associated claims and alerts. [ref:57cb6eab39ca7aea43116e04a6afcdbdf6a2fb8f]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `2af21c`: Manages structured data representing claims, including attributes such as text content, reference identifiers, and source module information _(Source: class Claim)_
> 🆔 `b77290`: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `cdaf82`: Data container for Alert records. _(Source: class Alert)_
> 🆔 `57cb6e`: Manages structural context for modules, storing file paths and text representations of module roles, dependencies, and public APIs, along with associated claims and alerts. _(Source: class ModuleContext)_
> 🆔 `278a6d`: Analyzes structured data representing claims, such as text content and source module information, to extract relevant insights and dependencies. _(Source: Synthesis)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Enforces semantic validation protocols to ensure coherent information exchange within the system

**Impact Analysis:** Changes to this module will affect: component_analyst.py, dependency_analyst.py, module_contextualizer.py [ref:e0c3c8457924baf1f761f428ee9ed8818f501a08]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Enumerates undesirable adjectives for filtering in text processing [ref:245296f0051299ece373688693df7a38f13b79d8]
- **`🔌 class SemanticGatekeeper`**: Manages structural data coherence and enables controlled information exchange across system entities by enforcing semantic validation protocols. [ref:3362995bc2d25ccf64ad3e808e75b9c976f40878]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py` Imports configuration constants for setting maximum context length. [ref:81e88532b05045ef25747f002e0cbbb027429854]
- **`llm_util.py`**: Uses `llm_util.py` integrates essential functionality from llm utility module. [ref:86df4052a93d975f48275a0eb75b90710120feb7]

### 👥 Used By (Downstream)
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `245296`: Enumerates undesirable adjectives for filtering in text processing _(Source: BANNED_ADJECTIVES)_
> 🆔 `336299`: Manages structural data coherence and enables controlled information exchange across system entities by enforcing semantic validation protocols. _(Source: class SemanticGatekeeper)_
> 🆔 `81e885`: Uses `agent_config.py` Imports configuration constants for setting maximum context length. _(Source: Import agent_config.py)_
> 🆔 `86df40`: Uses `llm_util.py` integrates essential functionality from llm utility module. _(Source: Import llm_util.py)_
> 🆔 `e0c3c8`: Enforces semantic validation protocols to ensure coherent information exchange within the system _(Source: Synthesis)_
</details>

---
## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Manages interactions between user prompts and message history using an LLM wrapper

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [ref:8b483047ca8d33b90d0d0705ea4e42dba1f97b5a]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Wraps an LLM to handle user prompts and message history [ref:f0dfb4a169a94222147db1f930a074c0fe13f32c]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f0dfb4`: Wraps an LLM to handle user prompts and message history _(Source: chat_llm)_
> 🆔 `8b4830`: Manages interactions between user prompts and message history using an LLM wrapper _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [ref:449512ed434b04a04a62f74801a3cff91b4129f6]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Assign integer value setting maximum context length for model processing [ref:cf8009bb4858c5f9f46076bd48276968207fe6fa]
- **`🔌 DEFAULT_MODEL`**: Assign global default model identifier string specifying Granite4 3 billion parameter model variant. [ref:720b50054fbc4e6b83425aa3091cfdef6ccf8c03]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `720b50`: Assign global default model identifier string specifying Granite4 3 billion parameter model variant. _(Source: DEFAULT_MODEL)_
> 🆔 `cf8009`: Assign integer value setting maximum context length for model processing _(Source: CONTEXT_LIMIT)_
> 🆔 `449512`: Defines configuration constants. _(Source: Archetype)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Manages memories (⚠️ The code defines classes for managing memory resources but lacks actual implementation details. It declares a MemoryInterface class with an empty query_memory method and a ChromaMemory subclass which inherits from it. However, no specific functionality is provided to actually manage or store memories.)

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:e19c46b1437cee387f3f01ad21c7b45367b3e4c2]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Manages and stores memories with unique identifiers, metadata, and helpfulness scores [ref:bfbca55acbf4ae2c511d310d116d276a98df5999]
- **`🔌 class MemoryInterface`**: Manages access to system memory resources, encapsulating memory-related data and operations. (⚠️ The code only defines a class with a method that raises an exception without any actual implementation. It does not demonstrate access to system memory resources or encapsulate memory-related data and operations.) [ref:1c90fb45697111d7a849780604a12c44ffd15ddb]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1c90fb`: Manages access to system memory resources, encapsulating memory-related data and operations. (⚠️ The code only defines a class with a method that raises an exception without any actual implementation. It does not demonstrate access to system memory resources or encapsulate memory-related data and operations.) _(Source: class MemoryInterface)_
> 🆔 `bfbca5`: Manages and stores memories with unique identifiers, metadata, and helpfulness scores _(Source: class ChromaMemory)_
> 🆔 `e19c46`: Manages memories (⚠️ The code defines classes for managing memory resources but lacks actual implementation details. It declares a MemoryInterface class with an empty query_memory method and a ChromaMemory subclass which inherits from it. However, no specific functionality is provided to actually manage or store memories.) _(Source: Synthesis)_
</details>

---
## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Analyzes dependencies within Python projects using depth-first search algorithms and constructs an extensive dependency graph to identify TODO comments present in source code, while managing imports, assignments, function definitions, class structures, interactions between modules, recording annotations, and analyzing function bodies for specific logic handling.

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:f10f9fc43f1a5fd7dc48269ce938317e5e795f7f]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Manages and analyzes code entities, managing imports, assignments, function definitions, class structures, interactions between modules, recording annotations, analyzing function bodies for specific logic handling. [ref:0f96a9fc86550c59fff5b8165421742477785a99]
- **`🔌 class GraphAnalyzer`**: Manages and analyzes dependencies within Python projects, employing depth-first search algorithms to construct an extensive dependency graph detailing the relationships between entities and identifying TODO comments present in source code. [ref:2ae63b3bfbcb9d5c7ac870b4f215837b81916f6b]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `0f96a9`: Manages and analyzes code entities, managing imports, assignments, function definitions, class structures, interactions between modules, recording annotations, analyzing function bodies for specific logic handling. _(Source: class CodeEntityVisitor)_
> 🆔 `2ae63b`: Manages and analyzes dependencies within Python projects, employing depth-first search algorithms to construct an extensive dependency graph detailing the relationships between entities and identifying TODO comments present in source code. _(Source: class GraphAnalyzer)_
> 🆔 `f10f9f`: Analyzes dependencies within Python projects using depth-first search algorithms and constructs an extensive dependency graph to identify TODO comments present in source code, while managing imports, assignments, function definitions, class structures, interactions between modules, recording annotations, and analyzing function bodies for specific logic handling. _(Source: Synthesis)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Analyzes module characteristics using provided data

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:11a7c9518c11d288cd99b4097859f8ea479436af]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [ref:a947722dc58c4984aaea3d4bb21713a64a0283ec]
- **`🔌 class ModuleClassifier`**: Manages and analyzes module characteristics using provided data [ref:c3feb4756136f2030efba325c85bcae0e37af07c]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a94772`: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `c3feb4`: Manages and analyzes module characteristics using provided data _(Source: class ModuleClassifier)_
> 🆔 `11a7c9`: Analyzes module characteristics using provided data _(Source: Synthesis)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Manages generation of structured reports

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:a77927ccbd36f8a120b9d64c6e10548d424c92a3]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Manages and encapsulates the generation of structured reports, including module context, dependencies, alerts, public API entities, and dependents based on provided contexts. [ref:7bdaa50625b07a6a3fc3023fee14509b5fb68157]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py` Extracts structured data to render reports. [ref:a0ea818f70353cb8b1964b593ac7be86ab3a42f2]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `7bdaa5`: Manages and encapsulates the generation of structured reports, including module context, dependencies, alerts, public API entities, and dependents based on provided contexts. _(Source: class ReportRenderer)_
> 🆔 `a0ea81`: Uses `summary_models.py` Extracts structured data to render reports. _(Source: Import summary_models.py)_
> 🆔 `a77927`: Manages generation of structured reports _(Source: Synthesis)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Manages state and data related to module dependencies, including upstream module roles, exported values, and usage context for specified imports within the given module

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:36c0e745e3a7c211f3853425268988d8b8b64326]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Manages state and data related to module dependencies, including upstream module roles, exported values, and usage context for specified imports within the given module. [ref:2cd2ef03edafbe2cc80e792b394ce42373b96ad6]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py` Utilizes core functionality to enforce semantic validation protocols for system-wide information exchange.. [ref:2878acb6dbcbe586a658106e21b3fbd2da07ae0d]
- **`summary_models.py`**: Uses `summary_models.py` Extracts insights to analyze dependencies between modules. [ref:192cb5aa3252db943e7265977b4d1c3921be44b7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `2cd2ef`: Manages state and data related to module dependencies, including upstream module roles, exported values, and usage context for specified imports within the given module. _(Source: class DependencyAnalyst)_
> 🆔 `2878ac`: Uses `semantic_gatekeeper.py` Utilizes core functionality to enforce semantic validation protocols for system-wide information exchange.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `192cb5`: Uses `summary_models.py` Extracts insights to analyze dependencies between modules. _(Source: Import summary_models.py)_
> 🆔 `36c0e7`: Manages state and data related to module dependencies, including upstream module roles, exported values, and usage context for specified imports within the given module _(Source: Synthesis)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Manages and organizes component analysis within the system, handling logic extraction, module skeleton generation, and ensuring proper documentation for each analyzed component

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:986a12ef1d33e0990a6ebf2d47cb3b8e740ac64e]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Manages and organizes component analysis within the system, handling logic extraction, module skeleton generation, and ensuring proper documentation for each analyzed component. [ref:7763d4a5e94a157391e89fdafca4742f75f9c8d9]
- **`🔌 class SkeletonTransformer`**: Manages structural analysis of Python AST nodes, specifically handling function and class definitions by visiting them recursively and modifying their bodies [ref:9856b76c5ba88fe1140dcf3eb677dae65cb2ee3c]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py` Enforces semantic validation protocols to ensure coherent information exchange within system. [ref:ce311175ee60bbe4e024589024e4458c1293398b]
- **`summary_models.py`**: Uses `summary_models.py` Extract relevant insights dependencies. [ref:d0144b96b8e6bda73b0e586bcb1e75ec90a45a28]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `7763d4`: Manages and organizes component analysis within the system, handling logic extraction, module skeleton generation, and ensuring proper documentation for each analyzed component. _(Source: class ComponentAnalyst)_
> 🆔 `9856b7`: Manages structural analysis of Python AST nodes, specifically handling function and class definitions by visiting them recursively and modifying their bodies _(Source: class SkeletonTransformer)_
> 🆔 `ce3111`: Uses `semantic_gatekeeper.py` Enforces semantic validation protocols to ensure coherent information exchange within system. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `d0144b`: Uses `summary_models.py` Extract relevant insights dependencies. _(Source: Import summary_models.py)_
> 🆔 `986a12`: Manages and organizes component analysis within the system, handling logic extraction, module skeleton generation, and ensuring proper documentation for each analyzed component _(Source: Synthesis)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Manages detailed comprehension of module's context and dependencies, synthesizing system-wide usage patterns and upstream knowledge to define its role within the ecosystem

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:ba1d2f63c090d442aad7fea69786ac5dfd4c8d45]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Manages detailed comprehension of module's context and dependencies, synthesizing system-wide usage patterns and upstream knowledge to define its role within the ecosystem. [ref:f86256be4abb760704613ea6e9fdea2286353b37]

### 🔗 Uses (Upstream)
- **`module_classifier.py`**: Uses `module_classifier.py` imports to utilize classifier's functionality for contextual analysis. [ref:ea4ae3cfc61e177605e4e65a3556a3351323da94]
- **`summary_models.py`**: Uses `summary_models.py` Extracts relevant insights from structured data representing claims. [ref:e2160c466ead935124e08b30e77efda62cf9734a]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py` Leverages DependencyAnalyst for thorough dependency evaluation. [ref:1969427e182dd8649e4b792dc4183b6074b5b9d5]
- **`component_analyst.py`**: Uses `component_analyst.py` Imports and utilizes ModuleContextualizer for enhanced functionality. [ref:341a81d026850d12c0a64d538aa129044c09b92e]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py` Enrich contextualization functionality by leveraging semantic validation protocols. [ref:465a80f9640342a05dd0acd87ee854fbd1af79e6]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f86256`: Manages detailed comprehension of module's context and dependencies, synthesizing system-wide usage patterns and upstream knowledge to define its role within the ecosystem. _(Source: class ModuleContextualizer)_
> 🆔 `ea4ae3`: Uses `module_classifier.py` imports to utilize classifier's functionality for contextual analysis. _(Source: Import module_classifier.py)_
> 🆔 `e2160c`: Uses `summary_models.py` Extracts relevant insights from structured data representing claims. _(Source: Import summary_models.py)_
> 🆔 `196942`: Uses `dependency_analyst.py` Leverages DependencyAnalyst for thorough dependency evaluation. _(Source: Import dependency_analyst.py)_
> 🆔 `341a81`: Uses `component_analyst.py` Imports and utilizes ModuleContextualizer for enhanced functionality. _(Source: Import component_analyst.py)_
> 🆔 `465a80`: Uses `semantic_gatekeeper.py` Enrich contextualization functionality by leveraging semantic validation protocols. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `ba1d2f`: Manages detailed comprehension of module's context and dependencies, synthesizing system-wide usage patterns and upstream knowledge to define its role within the ecosystem _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Analyze project structure and dependencies using provided graph and context data to generate module processing order

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:b41370e5144fb69514846a40fa4b382971319f5c]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Defines a dictionary structure for project graph [ref:a540ac8ed7dd22294dd7ddf3aeec909db44cd0ea]
- **`🔌 class ProjectSummarizer`**: Manages project structure data and ensures proper module processing order through topological sorting. [ref:bdacb63b11d091ccfbefd98a34c6baaee10cb519]
- **`🔌 project_pulse`**: Analyzes a Python project and generates detailed module context map for each module [ref:426391b527d202a9739233f3ed97d28f9dd68793]
- **`🔒 _create_module_context`**: Generates and returns ModuleContext for specified module path using provided graph and dependency contexts [ref:5e5f2cb36358d2d485fe33b9790bc5ea0d0ec65b]

### 🔗 Uses (Upstream)
- **`graph_analyzer.py`**: Uses `graph_analyzer.py` Eliminates ambiguity by utilizing a detailed dependency analysis module to identify potential TODO items in source code structures. [ref:fb38ee2db20a5d97d6ed4988d2f726f7350c2984]
- **`summary_models.py`**: Uses `summary_models.py` utilizes extracted insights to process and analyze claims effectively. [ref:6d14a48df3f65bdbd51ddb0237e9331778c25413]
- **`module_contextualizer.py`**: Uses `module_contextualizer.py` (Unverified) Incorporates Advanced Contextualization Framework for Agent Utility Module. [ref:b5765701cba5c1383a6702beaa5277fb6929adb8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a540ac`: Defines a dictionary structure for project graph _(Source: ProjectGraph)_
> 🆔 `5e5f2c`: Generates and returns ModuleContext for specified module path using provided graph and dependency contexts _(Source: _create_module_context)_
> 🆔 `426391`: Analyzes a Python project and generates detailed module context map for each module _(Source: project_pulse)_
> 🆔 `bdacb6`: Manages project structure data and ensures proper module processing order through topological sorting. _(Source: class ProjectSummarizer)_
> 🆔 `fb38ee`: Uses `graph_analyzer.py` Eliminates ambiguity by utilizing a detailed dependency analysis module to identify potential TODO items in source code structures. _(Source: Import graph_analyzer.py)_
> 🆔 `6d14a4`: Uses `summary_models.py` utilizes extracted insights to process and analyze claims effectively. _(Source: Import summary_models.py)_
> 🆔 `b57657`: Uses `module_contextualizer.py` (Unverified) Incorporates Advanced Contextualization Framework for Agent Utility Module. _(Source: Import module_contextualizer.py)_
> 🆔 `b41370`: Analyze project structure and dependencies using provided graph and context data to generate module processing order _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Executes specified goals within target root directory while managing execution state and memory using CrawlerAgent

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [ref:e0c4e16beec72e28bad969e82dcf09e67747ae0c]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Manages execution state and memory for specified goal and target root directory [ref:3b8d5728fdecba3807aac16f19af158f3eb240e7]

### 🔗 Uses (Upstream)
- **`llm_util.py`**: Uses `llm_util.py` imports LLM wrapper to handle user prompts and message history. [ref:ee83c019a18051e2b396b24f920ef355029808b6]
- **`agent_config.py`**: Uses `agent_config.py` Requires configuration constants for proper operation. [ref:e3a9a67dc1f67fbaf20e97a0f1efbbb673adf676]
- **`report_renderer.py`**: Uses `report_renderer.py` Requires dependency for structured report generation. [ref:5ea2aef4a550749bfce4883c06b25ca30aa4026b]
- **`memory_core.py`**: Uses `memory_core.py` Clarify Requirement (⚠️ The code defines classes for managing memory resources but lacks actual implementation details. It declares a MemoryInterface class with an empty query_memory method and a ChromaMemory subclass which inherits from it. However, no specific functionality is provided to actually manage or store memories.). [ref:ab62dadffe84e6e552cc06640ed22d80db9bbf66]
- **`agent_util.py`**: Uses `agent_util.py` Analyze project structure and dependencies to generate module processing order using defined dictionary structure. [ref:0e3bb7c2cf8d59972d1a18c3dc15710094f623f7]
- **`summary_models.py`**: Uses `summary_models.py` Aggregates and processes structured data to derive actionable insights. [ref:cd18fb1b63503f99cca724e27de0202041868dbf]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `3b8d57`: Manages execution state and memory for specified goal and target root directory _(Source: class CrawlerAgent)_
> 🆔 `ee83c0`: Uses `llm_util.py` imports LLM wrapper to handle user prompts and message history. _(Source: Import llm_util.py)_
> 🆔 `e3a9a6`: Uses `agent_config.py` Requires configuration constants for proper operation. _(Source: Import agent_config.py)_
> 🆔 `5ea2ae`: Uses `report_renderer.py` Requires dependency for structured report generation. _(Source: Import report_renderer.py)_
> 🆔 `ab62da`: Uses `memory_core.py` Clarify Requirement (⚠️ The code defines classes for managing memory resources but lacks actual implementation details. It declares a MemoryInterface class with an empty query_memory method and a ChromaMemory subclass which inherits from it. However, no specific functionality is provided to actually manage or store memories.). _(Source: Import memory_core.py)_
> 🆔 `0e3bb7`: Uses `agent_util.py` Analyze project structure and dependencies to generate module processing order using defined dictionary structure. _(Source: Import agent_util.py)_
> 🆔 `cd18fb`: Uses `summary_models.py` Aggregates and processes structured data to derive actionable insights. _(Source: Import summary_models.py)_
> 🆔 `e0c4e1`: Executes specified goals within target root directory while managing execution state and memory using CrawlerAgent _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Extracts command line arguments to determine processing goal and target folder, then recursively searches the specified directory for Python scripts ending with _main.py [ref:7a1bf050ef47dae7f1ebcaec7dc83d61a6d5f51e]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Parses command line arguments and assigns values to variables for processing [ref:002681f4eba6a1a413202c5f2db5029ba26a89af]
- **`🔌 goal`**: Extract command line argument value for processing target folder (⚠️ The code snippet extracts a command line argument value but does not explicitly state it's for processing a target folder.) [ref:aafd6d1c83fb78565e106fd90c4004f78477ee8a]
- **`🔌 main`**: Recursively searches target folder for Python script ending in _main.py [ref:b43a935f24ae621ca8b061ab2e86a2c7b8692516]
- **`🔌 parser`**: Creates an ArgumentParser to parse command line arguments for main function [ref:6c85bf41475622a95196869dd79a2c2215a8bf02]
- **`🔌 result`**: The code parses command-line arguments using argparse to determine processing goal and target folder path, then invokes the main function with these parameters (⚠️ The code shows invocation of a function `main` with parameters `goal` and `target_folder`, suggesting these are passed to the function. However, there is no evidence provided in this snippet that command-line arguments are parsed using argparse or how these parameters are determined.) [ref:838d6566457ce51f4b25a992b93ac97c2c778977]
- **`🔌 target_folder`**: Extracts specified goal from provided command line arguments and utilizes it to set target directory for main function execution [ref:d3b8cec7a6ae3b13f0f86b741b4bd151fc9af232]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py` Imports required module to execute specified goals. [ref:e7d23965aa329157418e59ec77e8702b3cea752b]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `6c85bf`: Creates an ArgumentParser to parse command line arguments for main function _(Source: parser)_
> 🆔 `002681`: Parses command line arguments and assigns values to variables for processing _(Source: args)_
> 🆔 `aafd6d`: Extract command line argument value for processing target folder (⚠️ The code snippet extracts a command line argument value but does not explicitly state it's for processing a target folder.) _(Source: goal)_
> 🆔 `d3b8ce`: Extracts specified goal from provided command line arguments and utilizes it to set target directory for main function execution _(Source: target_folder)_
> 🆔 `838d65`: The code parses command-line arguments using argparse to determine processing goal and target folder path, then invokes the main function with these parameters (⚠️ The code shows invocation of a function `main` with parameters `goal` and `target_folder`, suggesting these are passed to the function. However, there is no evidence provided in this snippet that command-line arguments are parsed using argparse or how these parameters are determined.) _(Source: result)_
> 🆔 `b43a93`: Recursively searches target folder for Python script ending in _main.py _(Source: main)_
> 🆔 `e7d239`: Uses `agent_core.py` Imports required module to execute specified goals. _(Source: Import agent_core.py)_
> 🆔 `7a1bf0`: Extracts command line arguments to determine processing goal and target folder, then recursively searches the specified directory for Python scripts ending with _main.py _(Source: Synthesis)_
</details>

---