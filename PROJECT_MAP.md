# Project Context Map

**Total Modules:** 11

## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` defines data structures including: class Claim, class GroundedText, class Alert.

**Used By:** agent_core.py, agent_util.py, module_contextualizer.py, report_renderer.py [ref:52f41aa295e1f547f8f023754f265011812789bc]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Stores structured data for Alert. *(Used by: module_contextualizer.py)* [ref:eaa1bfcc935fc43df0e67de1e3800473777cffd6]
- **`🔌 class Claim`**: processes specified logic *(Used by: agent_util.py, module_contextualizer.py)* [ref:1e6d394cb5e0aada3f9c2dfd1e08b9cada6ef97b]
- **`🔌 class GroundedText`**: Stores structured data for GroundedText. [ref:9d9728e474af4ded69554b06a3af9582b413f883]
- **`🔌 class ModuleContext`**: determine the module's role *(Used by: agent_core.py, agent_util.py, module_contextualizer.py, report_renderer.py)* [ref:c5d5dfa4bde3af8a25c5aee2492627be8a469349]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1e6d39`: processes specified logic *(Used by: agent_util.py, module_contextualizer.py)* _(Source: class Claim)_
> 🆔 `9d9728`: Stores structured data for GroundedText. _(Source: class GroundedText)_
> 🆔 `eaa1bf`: Stores structured data for Alert. *(Used by: module_contextualizer.py)* _(Source: class Alert)_
> 🆔 `c5d5df`: determine the module's role *(Used by: agent_core.py, agent_util.py, module_contextualizer.py, report_renderer.py)* _(Source: class ModuleContext)_
> 🆔 `52f41a`: The module `summary_models.py` defines data structures including: class Claim, class GroundedText, class Alert. _(Source: Archetype Analysis)_
</details>

---
## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Provides utility functions for handling and interacting with language models in agent_core.py and semantic_gatekeeper.py.

**Used By:** agent_core.py, semantic_gatekeeper.py [ref:cd28daab6529bf3ff920e029a8b45473c5d9b9a5]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: execute function *(Used by: agent_core.py, semantic_gatekeeper.py)* [ref:c688e9cf0c71a84931edde1b6fe2538a19e58301]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c688e9`: execute function *(Used by: agent_core.py, semantic_gatekeeper.py)* _(Source: def chat_llm(model: str, prompt: str) -> str:)_
> 🆔 `cd28da`: The module `llm_util.py` Provides utility functions for handling and interacting with language models in agent_core.py and semantic_gatekeeper.py.

**Used By:** agent_core.py, semantic_gatekeeper.py _(Source: Recursive Synthesis)_
</details>

---
## 📦 Module: `agent_config.py`
**Role:** The module `agent_config.py` defines configuration constants and settings.

**Used By:** agent_core.py, semantic_gatekeeper.py [ref:03a911d8181bd52b977a17d2297c4abb5a522075]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: assign integer *(Used by: agent_core.py)* [ref:028ea422f912cb1a1ef3e9e3506853fc80776064]
- **`🔌 DEFAULT_MODEL`**: assign string constant *(Used by: agent_core.py, semantic_gatekeeper.py)* [ref:95d162592bae620cbf638ed5e0ac095049c21dc9]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `95d162`: assign string constant *(Used by: agent_core.py, semantic_gatekeeper.py)* _(Source: DEFAULT_MODEL = ...)_
> 🆔 `028ea4`: assign integer *(Used by: agent_core.py)* _(Source: CONTEXT_LIMIT = ...)_
> 🆔 `03a911`: The module `agent_config.py` defines configuration constants and settings. _(Source: Archetype Analysis)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` defines data structures including: class MemoryInterface, class ChromaMemory.

**Used By:** agent_core.py [ref:0e490f3264dce846ed0af5c207e21e8aa72f9655]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Monitors memory for user interactions and updates the system accordingly. *(Used by: agent_core.py)* [ref:530a289435b15dfe9f73be39b1e03fe840c3a905]
- **`🔌 class MemoryInterface`**: queries memory [ref:e17dacbf48e002d2bd4689e21d3cc8e646fac7ac]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `e17dac`: queries memory _(Source: class MemoryInterface)_
> 🆔 `530a28`: Monitors memory for user interactions and updates the system accordingly. *(Used by: agent_core.py)* _(Source: class ChromaMemory)_
> 🆔 `0e490f`: The module `memory_core.py` defines data structures including: class MemoryInterface, class ChromaMemory. _(Source: Archetype Analysis)_
</details>

---
## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` defines data structures including: class CodeEntityVisitor, class GraphAnalyzer.

**Used By:** agent_util.py [ref:934f27fa0926bb2467180535a98ac71e5186781a]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: processes import node [ref:46ed72201340549e3c77b01566ea2917bd264e36]
- **`🔌 class GraphAnalyzer`**: Determines the function's purpose. *(Used by: agent_util.py)* [ref:083e503941d65a9ba60afcf5f8010c929eebc82d]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `46ed72`: processes import node _(Source: class CodeEntityVisitor)_
> 🆔 `083e50`: Determines the function's purpose. *(Used by: agent_util.py)* _(Source: class GraphAnalyzer)_
> 🆔 `934f27`: The module `graph_analyzer.py` defines data structures including: class CodeEntityVisitor, class GraphAnalyzer. _(Source: Archetype Analysis)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` generates report file for downstream consumption

**Used By:** agent_core.py [ref:19677fd76f8627db84f6c480ddb0d2d79b3e26d5]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: generates report file *(Used by: agent_core.py)* [ref:c1f3e413260dc10a58873382bbe9a6b887fcbd67]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py` to provide data structures. [ref:a1c804f955fce1197451d68a5037ba153aadfe8c]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c1f3e4`: generates report file *(Used by: agent_core.py)* _(Source: class ReportRenderer)_
> 🆔 `a1c804`: Uses `summary_models.py` to provide data structures. _(Source: Import summary_models.py)_
> 🆔 `19677f`: The module `report_renderer.py` generates report file for downstream consumption

**Used By:** agent_core.py _(Source: Recursive Synthesis)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` The SemanticGatekeeper module analyzes and optimizes code operations using language model utilities, while filtering out banned adjectives.

**Used By:** module_contextualizer.py [ref:ed94ddea85cd49bf89129c22796c340384707357]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: optimize operations [ref:9ce5a8398e2afd026418cdef20dfe0aeb71288e2]
- **`🔌 class SemanticGatekeeper`**: analyzes code *(Used by: module_contextualizer.py)* [ref:49179157480d1522e7257cb9d154d5d6165165c9]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py` to define configuration. [ref:d0df2868c9a95a075c069df2b98b29a8979eb471]
- **`llm_util.py`**: Uses `llm_util.py` to handle language models. [ref:1798194d7e7f5d058d7458d18e2f492468e38ac9]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `9ce5a8`: optimize operations _(Source: BANNED_ADJECTIVES: Set[str] = ...)_
> 🆔 `491791`: analyzes code *(Used by: module_contextualizer.py)* _(Source: class SemanticGatekeeper)_
> 🆔 `d0df28`: Uses `agent_config.py` to define configuration. _(Source: Import agent_config.py)_
> 🆔 `179819`: Uses `llm_util.py` to handle language models. _(Source: Import llm_util.py)_
> 🆔 `ed94dd`: The module `semantic_gatekeeper.py` The SemanticGatekeeper module analyzes and optimizes code operations using language model utilities, while filtering out banned adjectives.

**Used By:** module_contextualizer.py _(Source: Recursive Synthesis)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Analyzes and synthesizes the role of a class by examining its data components, code mechanisms, and dependencies

**Used By:** agent_util.py [ref:d0413a0f865d952be0cb42957b37a42ac998bfb0]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Stores structured data for ModuleArchetype. [ref:f71cbfd490513e44c14215b3def898b543f4614d]
- **`🔌 class ModuleClassifier`**: classifies code modules [ref:86214445561cb8ad727a2587bf9d723ff5bf14bb]
- **`🔌 class ModuleContextualizer`**: Analyzes and synthesizes the role of a class by examining its data components, code mechanisms, and dependencies. *(Used by: agent_util.py)* [ref:0473391101bc66ed21ec3d11bfc04f0c9a62b0f9]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py` to analyze and optimize code operations. [ref:7ceb2e5374b1e1e33160649599316247d9cc85cc]
- **`summary_models.py`**: Uses `summary_models.py` to define data structures. [ref:fe4438ed1e90f8fe5f6b095fa21c4be255e01a6b]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f71cbf`: Stores structured data for ModuleArchetype. _(Source: class ModuleArchetype)_
> 🆔 `862144`: classifies code modules _(Source: class ModuleClassifier)_
> 🆔 `047339`: Analyzes and synthesizes the role of a class by examining its data components, code mechanisms, and dependencies. *(Used by: agent_util.py)* _(Source: class ModuleContextualizer)_
> 🆔 `7ceb2e`: Uses `semantic_gatekeeper.py` to analyze and optimize code operations. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `fe4438`: Uses `summary_models.py` to define data structures. _(Source: Import summary_models.py)_
> 🆔 `d0413a`: The module `module_contextualizer.py` Analyzes and synthesizes the role of a class by examining its data components, code mechanisms, and dependencies

**Used By:** agent_util.py _(Source: Recursive Synthesis)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Analyzes and synthesizes project context, generates module contexts, and summarizes the project using contextual analysis tools.

**Used By:** agent_core.py [ref:66d658cf37e58d9f2e67a9aaeac772a47d64eb68]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: analyze code [ref:67618b546e88ea690a2ed1119059ce7795456a20]
- **`🔌 class ProjectSummarizer`**: summarizes the project [ref:f1494872f3ca8ddc4fa6f9e2f0a8bb0a35af38a4]
- **`🔌 project_pulse`**: analyze project context *(Used by: agent_core.py)* [ref:ea3272e65daa9ae2717caa6eb36d7d73a52dd4cc]
- **`🔒 _create_module_context`**: generate module context [ref:36f3b67e711ee553e46d8cf9ba34b1bbbef2fe29]

### 🔗 Uses (Upstream)
- **`module_contextualizer.py`**: Uses `module_contextualizer.py` to analyze and synthesize. [ref:e15bfde83ccfffe442862b4b20f2e26d2af4ea4a]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py` to analyze graph. [ref:a62ef2a438ccb0cff6557446c1c5ebf74f4eda9f]
- **`summary_models.py`**: Uses `summary_models.py` to define data structures. [ref:036c055ea96f135d02f11ee3a48d2ba89e32df2c]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `67618b`: analyze code _(Source: ProjectGraph = ...)_
> 🆔 `36f3b6`: generate module context _(Source: def _create_module_context(path: str, graph: ProjectGraph, dep_contexts: Dict[str, ModuleContext]) -> ModuleContext:)_
> 🆔 `ea3272`: analyze project context *(Used by: agent_core.py)* _(Source: def project_pulse(target_file_path: str) -> Dict[str, ModuleContext]:)_
> 🆔 `f14948`: summarizes the project _(Source: class ProjectSummarizer)_
> 🆔 `e15bfd`: Uses `module_contextualizer.py` to analyze and synthesize. _(Source: Import module_contextualizer.py)_
> 🆔 `a62ef2`: Uses `graph_analyzer.py` to analyze graph. _(Source: Import graph_analyzer.py)_
> 🆔 `036c05`: Uses `summary_models.py` to define data structures. _(Source: Import summary_models.py)_
> 🆔 `66d658`: The module `agent_util.py` Analyzes and synthesizes project context, generates module contexts, and summarizes the project using contextual analysis tools.

**Used By:** agent_core.py _(Source: Recursive Synthesis)_
</details>

---
## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` The module defines and manages the behavior of agents, utilizing various tools for memory management, language model interaction, report generation, context analysis, configuration handling, and claim summarization.

**Used By:** agent_graph_main.py [ref:5b8002c7b78f8b65a0c989172991a689a2336829]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: initializes an agent object *(Used by: agent_graph_main.py)* [ref:cd0ca868da560f006d6cae08f6e4c81d5908697f]

### 🔗 Uses (Upstream)
- **`memory_core.py`**: Uses `memory_core.py` to define data structures. [ref:1f95a8a6b00430283376ae1b09343071aa809620]
- **`llm_util.py`**: Uses `llm_util.py` to process natural language. [ref:593fc2c507326badc66c7b0c13ed22aa377aeb24]
- **`report_renderer.py`**: Uses `report_renderer.py` to generate report. [ref:bfa366ab8bfd3e505de3242b347a851eb512995c]
- **`agent_util.py`**: Uses `agent_util.py` to summarize project. [ref:04a90a901071efc66604a76287118145afb1f462]
- **`agent_config.py`**: Uses `agent_config.py` to define configuration constants and settings. [ref:87b46c2fd22aebe0fbdf4aa5dfef69425178a947]
- **`summary_models.py`**: Uses `summary_models.py` to provide service. [ref:216d3750f3d4700dcd4a9110f7b65d49b9a594c3]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `cd0ca8`: initializes an agent object *(Used by: agent_graph_main.py)* _(Source: class CrawlerAgent)_
> 🆔 `1f95a8`: Uses `memory_core.py` to define data structures. _(Source: Import memory_core.py)_
> 🆔 `593fc2`: Uses `llm_util.py` to process natural language. _(Source: Import llm_util.py)_
> 🆔 `bfa366`: Uses `report_renderer.py` to generate report. _(Source: Import report_renderer.py)_
> 🆔 `04a90a`: Uses `agent_util.py` to summarize project. _(Source: Import agent_util.py)_
> 🆔 `87b46c`: Uses `agent_config.py` to define configuration constants and settings. _(Source: Import agent_config.py)_
> 🆔 `216d37`: Uses `summary_models.py` to provide service. _(Source: Import summary_models.py)_
> 🆔 `5b8002`: The module `agent_core.py` The module defines and manages the behavior of agents, utilizing various tools for memory management, language model interaction, report generation, context analysis, configuration handling, and claim summarization.

**Used By:** agent_graph_main.py _(Source: Recursive Synthesis)_
</details>

---
## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` The agent_core.py module defines and manages the behavior of agents, utilizing various tools for memory management, language model interaction, report generation, context analysis, configuration handling, and claim summarization. [ref:1268fb3462e983cd74a9ff4cac2a1a994be71c0e]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: parse arguments [ref:0d899a350b41c5ac329b7a34ccc51eeba168bfc7]
- **`🔌 goal`**: retrieve value [ref:e2a1a2fe9ee8e3aa6d4979a269703822c1b8e37e]
- **`🔌 main`**: initialize agent [ref:538ac364f4cc52cafb6b82ca9f4cb08a886cd1f6]
- **`🔌 parser`**: generate argument handler [ref:36ecea2bb6a59e67a2bc1120bc6e322e6cd7ae97]
- **`🔌 result`**: execute main function [ref:30ff25f71795c49ac1bdc5a170b4396ece090beb]
- **`🔌 target_folder`**: assign target folder [ref:2ab08466fc45d752db6b755d53e042093d00916d]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py` to define and manage. [ref:4ec7e7dec9d78c540351abfb773d22a1a2297bde]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `36ecea`: generate argument handler _(Source: parser = ...)_
> 🆔 `0d899a`: parse arguments _(Source: args = ...)_
> 🆔 `e2a1a2`: retrieve value _(Source: goal = ...)_
> 🆔 `2ab084`: assign target folder _(Source: target_folder = ...)_
> 🆔 `30ff25`: execute main function _(Source: result = ...)_
> 🆔 `538ac3`: initialize agent _(Source: def main(goal: str, target_folder: str) -> str:)_
> 🆔 `4ec7e7`: Uses `agent_core.py` to define and manage. _(Source: Import agent_core.py)_
> 🆔 `1268fb`: The module `agent_graph_main.py` The agent_core.py module defines and manages the behavior of agents, utilizing various tools for memory management, language model interaction, report generation, context analysis, configuration handling, and claim summarization. _(Source: Recursive Synthesis)_
</details>

---