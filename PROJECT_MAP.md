# Project Context Map

**Total Modules:** 14

## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` The module's business logic involves analyzing code structure and components, managing various data containers such as Claim, GroundedText, Alert, and ModuleContext, and computing SHA-1 hashes of strings composed by concatenating specific attributes like text, reference, and source_module. It also manages dependencies and public APIs related to these components.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, module_contextualizer.py, report_renderer.py [ref:8dfa1b56e436e9b1e5bf945034d3843c63668ab1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [ref:cdaf82fd4c021fa0a891dedd7d85fff3402f4bef]
- **`🔌 class Claim`**: The class manages and encapsulates text, reference, and source_module data attributes. It computes a SHA-1 hash of a string composed by concatenating these attributes using its id method. [ref:446395001562ad2672754a01e5832579383bbc1a]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [ref:b7729088a8954b42aeaaf067fb7b5ca6c1bcaf4c]
- **`🔌 class ModuleContext`**: Manages and encapsulates the structural role of various components, including file path, module role text, dependencies, dependents, public API, alerts, and claims. [ref:641713f02be44f77ae3263bfb73f4639a12f0d4c]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `446395`: The class manages and encapsulates text, reference, and source_module data attributes. It computes a SHA-1 hash of a string composed by concatenating these attributes using its id method. _(Source: class Claim)_
> 🆔 `b77290`: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `cdaf82`: Data container for Alert records. _(Source: class Alert)_
> 🆔 `641713`: Manages and encapsulates the structural role of various components, including file path, module role text, dependencies, dependents, public API, alerts, and claims. _(Source: class ModuleContext)_
> 🆔 `8dfa1b`: The module's business logic involves analyzing code structure and components, managing various data containers such as Claim, GroundedText, Alert, and ModuleContext, and computing SHA-1 hashes of strings composed by concatenating specific attributes like text, reference, and source_module. It also manages dependencies and public APIs related to these components. _(Source: Synthesis)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` The SemanticGatekeeper class is responsible for managing and encapsulating the states and data related to semantic analysis, such as parsed documents or text chunks, which are used for processing tasks like sentiment analysis, entity recognition, or topic modeling using a default model named 'granite4:3b'. It ensures that the context limit of 2048 tokens is not exceeded during these operations.

**Impact Analysis:** Changes to this module will affect: component_analyst.py, dependency_analyst.py, module_contextualizer.py [ref:22d1729331dafe77ee02dfb019d4878c9411c375]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Assigns a set of banned adjectives [ref:8c6d64a9018e557645eed18704250be6024f49bd]
- **`🔌 class SemanticGatekeeper`**: Manages and encapsulates the states and data related to semantic analysis, such as parsed documents or text chunks, which are used for processing tasks like sentiment analysis, entity recognition, or topic modeling. [ref:b29d500fff8591743f163aaff8cfaf4cffc907d9]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py` The `semantic_gatekeeper.py` module requires a dependency because it uses known exported values such as assigning string value 'granite4:3b' to DEFAULT_MODEL and integer value of 2048 to CONTEXT_LIMIT, both defined elsewhere (e.g., Configuration Module). This allows the module to access these constants for its functionality.. [ref:d2c47780d7954d3699d5269024cbe4153b0e7edc]
- **`llm_util.py`**: Uses `llm_util.py` The semantic_gatekeeper module requires access to utility functions, specifically those enabling response generation from language models based on given prompts and a selected model, necessitating dependency on another module.. [ref:b7e5daa650c64a13b6f87a08ae59cf0b5a76202b]

### 👥 Used By (Downstream)
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8c6d64`: Assigns a set of banned adjectives _(Source: BANNED_ADJECTIVES)_
> 🆔 `b29d50`: Manages and encapsulates the states and data related to semantic analysis, such as parsed documents or text chunks, which are used for processing tasks like sentiment analysis, entity recognition, or topic modeling. _(Source: class SemanticGatekeeper)_
> 🆔 `d2c477`: Uses `agent_config.py` The `semantic_gatekeeper.py` module requires a dependency because it uses known exported values such as assigning string value 'granite4:3b' to DEFAULT_MODEL and integer value of 2048 to CONTEXT_LIMIT, both defined elsewhere (e.g., Configuration Module). This allows the module to access these constants for its functionality.. _(Source: Import agent_config.py)_
> 🆔 `b7e5da`: Uses `llm_util.py` The semantic_gatekeeper module requires access to utility functions, specifically those enabling response generation from language models based on given prompts and a selected model, necessitating dependency on another module.. _(Source: Import llm_util.py)_
> 🆔 `22d172`: The SemanticGatekeeper class is responsible for managing and encapsulating the states and data related to semantic analysis, such as parsed documents or text chunks, which are used for processing tasks like sentiment analysis, entity recognition, or topic modeling using a default model named 'granite4:3b'. It ensures that the context limit of 2048 tokens is not exceeded during these operations. _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [ref:449512ed434b04a04a62f74801a3cff91b4129f6]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Assigns an integer value of 2048 to CONTEXT_LIMIT [ref:4df49e6489c89b9586188e089cd35deb64c861f7]
- **`🔌 DEFAULT_MODEL`**: Assigns string value 'granite4:3b' to DEFAULT_MODEL [ref:77daba3d409aa8d093633beb6d5798ad99ec294b]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `77daba`: Assigns string value 'granite4:3b' to DEFAULT_MODEL _(Source: DEFAULT_MODEL)_
> 🆔 `4df49e`: Assigns an integer value of 2048 to CONTEXT_LIMIT _(Source: CONTEXT_LIMIT)_
> 🆔 `449512`: Defines configuration constants. _(Source: Archetype)_
</details>

---
## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` The module is tasked with providing utility functions for implementing functionality to generate responses from language models, specifically focusing on the chat_llm function which attempts to generate outputs based on provided prompts using a specified model.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [ref:63625faf1ab67a1ac8b05a3e23676e773784aac8]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Attempts to chat using specified model and prompt, returning the response message content stripped of leading/trailing whitespace [ref:9ec7d259f6c0f41ffd29e2634a817158b8b6faa5]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `9ec7d2`: Attempts to chat using specified model and prompt, returning the response message content stripped of leading/trailing whitespace _(Source: chat_llm)_
> 🆔 `63625f`: The module is tasked with providing utility functions for implementing functionality to generate responses from language models, specifically focusing on the chat_llm function which attempts to generate outputs based on provided prompts using a specified model. _(Source: Synthesis)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` {'description': 'Analyzes code structure to classify modules into different archetypes based on their characteristics.', 'responsibilities': ['Manages and encapsulates module name, source code, entities, dependencies, and functions', 'Uses ModuleArchetype class as a data container for records', 'Applies specific business logic to determine the archetype of each module'], 'configurations': {'model_name': 'ModuleClassifier'}}

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:15752df2bb9de7a2958fd57527396076d75f542a]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [ref:a947722dc58c4984aaea3d4bb21713a64a0283ec]
- **`🔌 class ModuleClassifier`**: Manages and encapsulates module name, source code, entities, dependencies, and functions to classify modules into different archetypes based on their characteristics. [ref:3b93343cf8ab480d33a9d8279ea806207e350409]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a94772`: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `3b9334`: Manages and encapsulates module name, source code, entities, dependencies, and functions to classify modules into different archetypes based on their characteristics. _(Source: class ModuleClassifier)_
> 🆔 `15752d`: {'description': 'Analyzes code structure to classify modules into different archetypes based on their characteristics.', 'responsibilities': ['Manages and encapsulates module name, source code, entities, dependencies, and functions', 'Uses ModuleArchetype class as a data container for records', 'Applies specific business logic to determine the archetype of each module'], 'configurations': {'model_name': 'ModuleClassifier'}} _(Source: Synthesis)_
</details>

---
## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Analyzes code structure and dependencies, managing relationships between imports, assignments, function definitions, and classes within Python projects. It encapsulates the project's structural data, including its root path, root directory, all files, and a graph representation of dependencies, while tracking visited nodes during analysis.

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:155b2ea257079be8b430cedd256a547a4f8a52ef]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Manages and encapsulates the structural role of code entities in a Python project, including imports, assignments, function definitions, and classes, by tracking their relationships, interactions, and contexts through various visit methods. [ref:9267477845db26e8f9218e7f0cfd0c48e5dce317]
- **`🔌 class GraphAnalyzer`**: Manages and encapsulates the structural data of a project, including root path, project root, all project files, graph representation of dependencies, and visited nodes during analysis. [ref:aa221062c312f861516d590e5c0c69a64c566279]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `926747`: Manages and encapsulates the structural role of code entities in a Python project, including imports, assignments, function definitions, and classes, by tracking their relationships, interactions, and contexts through various visit methods. _(Source: class CodeEntityVisitor)_
> 🆔 `aa2210`: Manages and encapsulates the structural data of a project, including root path, project root, all project files, graph representation of dependencies, and visited nodes during analysis. _(Source: class GraphAnalyzer)_
> 🆔 `155b2e`: Analyzes code structure and dependencies, managing relationships between imports, assignments, function definitions, and classes within Python projects. It encapsulates the project's structural data, including its root path, root directory, all files, and a graph representation of dependencies, while tracking visited nodes during analysis. _(Source: Synthesis)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` {'business_logic': ['Analyzes code structure to identify memory resource operations such as allocation, storage, retrieval, modification, and deletion of data.', 'Defines classes `MemoryInterface` and `ChromaMemory` for encapsulating managing memory storage state tracking and utility functions.', "Provides a foundation for persistent client interaction with the system's memory resources."]}

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:b917a069b334cf5b5f15c628313895f030dc4fbc]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Encapsulates and manages memory storage, state tracking, and utility functions for persistent client interaction. [ref:11a543b0823136552b458c021de371fa44a9d225]
- **`🔌 class MemoryInterface`**: Encapsulates manages and supports memory resource operations such as allocation, storage, retrieval, modification, and deletion of data. (⚠️ The provided code only defines a class `MemoryInterface` with an empty method `query_memory` that raises NotImplementedError. This indicates the absence of actual implementation for managing and supporting memory resource operations such as allocation, storage, retrieval, modification, and deletion of data.) [ref:72a1bb0e5e80ce5b9f636da416e64fb9a1d1eed0]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `72a1bb`: Encapsulates manages and supports memory resource operations such as allocation, storage, retrieval, modification, and deletion of data. (⚠️ The provided code only defines a class `MemoryInterface` with an empty method `query_memory` that raises NotImplementedError. This indicates the absence of actual implementation for managing and supporting memory resource operations such as allocation, storage, retrieval, modification, and deletion of data.) _(Source: class MemoryInterface)_
> 🆔 `11a543`: Encapsulates and manages memory storage, state tracking, and utility functions for persistent client interaction. _(Source: class ChromaMemory)_
> 🆔 `b917a0`: {'business_logic': ['Analyzes code structure to identify memory resource operations such as allocation, storage, retrieval, modification, and deletion of data.', 'Defines classes `MemoryInterface` and `ChromaMemory` for encapsulating managing memory storage state tracking and utility functions.', "Provides a foundation for persistent client interaction with the system's memory resources."]} _(Source: Synthesis)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` The ReportRenderer is responsible for analyzing and encapsulating the rendering of report data, including project context map, module information, role descriptions, alerts, public API entities, key dependencies, and dependents. It utilizes provided contexts to generate output files that summarize these components effectively.

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:596826c9600bb9ff3c8bb33f7fe2561f12922ac7]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Manages and encapsulates the rendering of report data, including project context map, module information, role descriptions, alerts, public API entities, key dependencies, and dependents, from provided contexts into output files. [ref:8a4247d4e31784406b30055c3eb7a9b176653dc5]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py` The `report_renderer.py` needs this dependency because it uses a Known Exported Value from another module that provides essential data containers such as Claim, GroundedText, Alert, and ModuleContext necessary for rendering reports.. [ref:746a9e56ae74524e8ec0c936cc5b1b68481e36d7]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `8a4247`: Manages and encapsulates the rendering of report data, including project context map, module information, role descriptions, alerts, public API entities, key dependencies, and dependents, from provided contexts into output files. _(Source: class ReportRenderer)_
> 🆔 `746a9e`: Uses `summary_models.py` The `report_renderer.py` needs this dependency because it uses a Known Exported Value from another module that provides essential data containers such as Claim, GroundedText, Alert, and ModuleContext necessary for rendering reports.. _(Source: Import summary_models.py)_
> 🆔 `596826`: The ReportRenderer is responsible for analyzing and encapsulating the rendering of report data, including project context map, module information, role descriptions, alerts, public API entities, key dependencies, and dependents. It utilizes provided contexts to generate output files that summarize these components effectively. _(Source: Synthesis)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` {'description': 'Analyzes code structure and dependencies to determine the best way to implement new features or resolve issues.', 'responsibilities': ['Manages dependency analysis by encapsulating the gatekeeper instance', 'Owns dependencies and their context data', 'Constructs prompts for intent determination'], 'specific_configuration': {'model_name': '0674615bbd87ab7ea8b91bf42993de55bec693c5'}}

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:421a1037df946d07d21f8d860e4d15f587f55563]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Manages dependency analysis by encapsulating the gatekeeper instance, owning dependencies and their context data, and constructing prompts for intent determination. [ref:0674615bbd87ab7ea8b91bf42993de55bec693c5]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py` The `dependency_analyst.py` requires a module that manages and encapsulates states and data related to semantic analysis, such as parsed documents or text chunks, for processing tasks like sentiment analysis, entity recognition, or topic modeling using a default model named 'granite4:3b'. This dependency ensures that the context limit of 2048 tokens is not exceeded during these operations, enabling `dependency_analyst.py` to handle text data correctly and perform its functions effectively.. [ref:4c91bbd0344e6b20e8d50b26a4b407aee08c39f0]
- **`summary_models.py`**: Uses `summary_models.py` The `dependency_analyst.py` needs a dependency on a module that provides business logic for analyzing code structure and components, managing various data containers like Claim, GroundedText, Alert, and ModuleContext, computing SHA-1 hashes of strings composed by concatenating specific attributes such as text, reference, and source_module, and handling dependencies and public APIs related to these components.. [ref:44cb5828c6821407ab5b013547ba9a72ed67747a]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `067461`: Manages dependency analysis by encapsulating the gatekeeper instance, owning dependencies and their context data, and constructing prompts for intent determination. _(Source: class DependencyAnalyst)_
> 🆔 `4c91bb`: Uses `semantic_gatekeeper.py` The `dependency_analyst.py` requires a module that manages and encapsulates states and data related to semantic analysis, such as parsed documents or text chunks, for processing tasks like sentiment analysis, entity recognition, or topic modeling using a default model named 'granite4:3b'. This dependency ensures that the context limit of 2048 tokens is not exceeded during these operations, enabling `dependency_analyst.py` to handle text data correctly and perform its functions effectively.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `44cb58`: Uses `summary_models.py` The `dependency_analyst.py` needs a dependency on a module that provides business logic for analyzing code structure and components, managing various data containers like Claim, GroundedText, Alert, and ModuleContext, computing SHA-1 hashes of strings composed by concatenating specific attributes such as text, reference, and source_module, and handling dependencies and public APIs related to these components.. _(Source: Import summary_models.py)_
> 🆔 `421a10`: {'description': 'Analyzes code structure and dependencies to determine the best way to implement new features or resolve issues.', 'responsibilities': ['Manages dependency analysis by encapsulating the gatekeeper instance', 'Owns dependencies and their context data', 'Constructs prompts for intent determination'], 'specific_configuration': {'model_name': '0674615bbd87ab7ea8b91bf42993de55bec693c5'}} _(Source: Synthesis)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` {'business_logic': 'Analyzes code structure by parsing source code to encapsulate global variables, functions, and class methods within modules. It removes docstrings from the analyzed code and synthesizes structural role descriptions based on provided class names.', 'responsibility': 'Analyzes code structure...'}

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:f395aab20eec141a5031cf936c8a9a514777d4f8]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes and encapsulates global variables, functions, and class methods in modules by managing their logic through parsing source code, removing docstrings, and synthesizing structural role descriptions based on the provided class name. [ref:2d07f1f97e6978e9f9d97f014468d31a0b8c68a1]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py` The `component_analyst.py` requires a module to manage and encapsulate states and data related to semantic analysis, such as parsed documents or text chunks, for processing tasks like sentiment analysis, entity recognition, or topic modeling using a default model named 'granite4:3b'. This ensures the context limit of 2048 tokens is not exceeded during these operations.. [ref:af4dd84bebfbc1868f1780799ed2c7d168ea791a]
- **`summary_models.py`**: Uses `summary_models.py` The `component_analyst.py` module requires a dependency on another module that provides business logic for analyzing code structure and components, managing data containers such as Claim, GroundedText, Alert, and ModuleContext, and computing SHA-1 hashes of strings formed by concatenating specific attributes like text, reference, and source_module. This is essential for its functionality in handling dependencies and public APIs related to these components.. [ref:55ae4ffee49555e2af42551a25a97917f1c3c88a]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `2d07f1`: Analyzes and encapsulates global variables, functions, and class methods in modules by managing their logic through parsing source code, removing docstrings, and synthesizing structural role descriptions based on the provided class name. _(Source: class ComponentAnalyst)_
> 🆔 `af4dd8`: Uses `semantic_gatekeeper.py` The `component_analyst.py` requires a module to manage and encapsulate states and data related to semantic analysis, such as parsed documents or text chunks, for processing tasks like sentiment analysis, entity recognition, or topic modeling using a default model named 'granite4:3b'. This ensures the context limit of 2048 tokens is not exceeded during these operations.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `55ae4f`: Uses `summary_models.py` The `component_analyst.py` module requires a dependency on another module that provides business logic for analyzing code structure and components, managing data containers such as Claim, GroundedText, Alert, and ModuleContext, and computing SHA-1 hashes of strings formed by concatenating specific attributes like text, reference, and source_module. This is essential for its functionality in handling dependencies and public APIs related to these components.. _(Source: Import summary_models.py)_
> 🆔 `f395aa`: {'business_logic': 'Analyzes code structure by parsing source code to encapsulate global variables, functions, and class methods within modules. It removes docstrings from the analyzed code and synthesizes structural role descriptions based on provided class names.', 'responsibility': 'Analyzes code structure...'} _(Source: Synthesis)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` The ModuleContextualizer is responsible for analyzing and understanding the structure, dependencies, and usage patterns of module data within a system. It performs tasks such as error checking to ensure data integrity, mapping the usage of different components across modules, gathering knowledge about how various parts interact, passing alerts or notifications when issues are detected in downstream systems, and identifying any potential impacts on other parts of the system due to changes in this module's dependencies.

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:e5d2b5182b76a10b157ac66716e9a35f6eb7bde9]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Manages and encapsulates the contextual understanding of module data, its dependencies, and systemic synthesis through various mechanisms such as error checking, usage mapping, knowledge gathering, alert passing, and downstream dependency identification. [ref:75619b069172ad122dea3b94508f19510a73c86c]

### 🔗 Uses (Upstream)
- **`component_analyst.py`**: Uses `component_analyst.py` The `module_contextualizer.py` needs this dependency because it requires functionality from another module that analyzes and encapsulates global variables, functions, and class methods within modules, synthesizing structural role descriptions based on provided class names. This analysis is crucial for `module_contextualizer.py` to effectively perform its task.. [ref:ee2adbd15a6ff8947439bc6ad8c600bac73debc7]
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py` The module_contextualizer.py requires dependency to manage and encapsulate states and data related to semantic analysis, including parsed documents or text chunks used for processing tasks such as sentiment analysis, entity recognition, or topic modeling with a default model 'granite4:3b'. It ensures that operations do not exceed the context limit of 2048 tokens.. [ref:7b8e64f7aea06cae27aef2bfeb887e30fad2e767]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py` Analyze code structure and dependencies to determine the best way to implement new features or resolve issues in module_contextualizer.py. [ref:0227eb591930d1610b6c37afed0d6714c00a9a9b]
- **`module_classifier.py`**: Uses `module_classifier.py` The `module_contextualizer.py` requires the dependency on a component responsible for analyzing code structure, classifying modules into various archetypes based on their characteristics, managing and encapsulating module name, source code, entities, dependencies, and functions, as well as using ModuleArchetype class to store records and applying specific business logic to determine the archetype of each module.. [ref:c0acb59f24f0e04c315e208a1a7468c1c163c62b]
- **`summary_models.py`**: Uses `summary_models.py` The module_contextualizer.py requires a dependency because it uses Known Exported Values of various components such as Claim, GroundedText, Alert, and ModuleContext. These elements are essential for its business logic involving code structure analysis, managing dependencies, and computing SHA-1 hashes of strings formed by concatenating specific attributes.. [ref:e200b65458fd0a4e6b97f069ab8fbac6735fe7c9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `75619b`: Manages and encapsulates the contextual understanding of module data, its dependencies, and systemic synthesis through various mechanisms such as error checking, usage mapping, knowledge gathering, alert passing, and downstream dependency identification. _(Source: class ModuleContextualizer)_
> 🆔 `ee2adb`: Uses `component_analyst.py` The `module_contextualizer.py` needs this dependency because it requires functionality from another module that analyzes and encapsulates global variables, functions, and class methods within modules, synthesizing structural role descriptions based on provided class names. This analysis is crucial for `module_contextualizer.py` to effectively perform its task.. _(Source: Import component_analyst.py)_
> 🆔 `7b8e64`: Uses `semantic_gatekeeper.py` The module_contextualizer.py requires dependency to manage and encapsulate states and data related to semantic analysis, including parsed documents or text chunks used for processing tasks such as sentiment analysis, entity recognition, or topic modeling with a default model 'granite4:3b'. It ensures that operations do not exceed the context limit of 2048 tokens.. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `0227eb`: Uses `dependency_analyst.py` Analyze code structure and dependencies to determine the best way to implement new features or resolve issues in module_contextualizer.py. _(Source: Import dependency_analyst.py)_
> 🆔 `c0acb5`: Uses `module_classifier.py` The `module_contextualizer.py` requires the dependency on a component responsible for analyzing code structure, classifying modules into various archetypes based on their characteristics, managing and encapsulating module name, source code, entities, dependencies, and functions, as well as using ModuleArchetype class to store records and applying specific business logic to determine the archetype of each module.. _(Source: Import module_classifier.py)_
> 🆔 `e200b6`: Uses `summary_models.py` The module_contextualizer.py requires a dependency because it uses Known Exported Values of various components such as Claim, GroundedText, Alert, and ModuleContext. These elements are essential for its business logic involving code structure analysis, managing dependencies, and computing SHA-1 hashes of strings formed by concatenating specific attributes.. _(Source: Import summary_models.py)_
> 🆔 `e5d2b5`: The ModuleContextualizer is responsible for analyzing and understanding the structure, dependencies, and usage patterns of module data within a system. It performs tasks such as error checking to ensure data integrity, mapping the usage of different components across modules, gathering knowledge about how various parts interact, passing alerts or notifications when issues are detected in downstream systems, and identifying any potential impacts on other parts of the system due to changes in this module's dependencies. _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` The role is responsible for analyzing project structure and dependencies using a ProjectGraph, ModuleContextualizer for contextualizing modules based on paths and relationships, and GraphAnalyzer to determine topological order of elements. The module uses ProjectSummarizer to manage processing by updating contexts according to dependencies.

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:1275a1c8ce4d43c5070d3f2a68055b286f293090]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns a dictionary type variable named ProjectGraph which maps string keys to any value. [ref:fa59e67fd1677a4f4804b5c65d6834614203594d]
- **`🔌 class ProjectSummarizer`**: Manages and encapsulates the processing order of project-related data, initializes an instance by assigning graph and max_cycles attributes, computes topological order, updates module contexts based on dependencies, and returns updated contexts. [ref:93ef324fd31e37ed448fa4f3dfff9086a85652c5]
- **`🔌 project_pulse`**: Checks if target file path exists, logs information about starting project analysis, creates GraphAnalyzer instance, analyzes project graph, generates contexts using ProjectSummarizer, logs completion of context map generation, and returns the final contexts. [ref:c7aa78ac0b3e4b5f2ba387e643ecbe73d353972f]
- **`🔒 _create_module_context`**: Assigns path and graph arguments to ModuleContextualizer, calls contextualize_module method, assigns file_path attribute if not set, returns context [ref:0c79e166c0f14783c7dcbc435c43a1c240cd8eea]

### 🔗 Uses (Upstream)
- **`module_contextualizer.py`**: Uses `module_contextualizer.py` (Unverified) The `agent_util.py` necessitates dependence on `module_contextualizer.py` due to its utilization of contextual analysis functionalities inherent within that dependency. This facilitates execution of robust error validation procedures, mapping of component usage across modules, aggregation of insights into interaction patterns among various system components, and identification of potential downstream effects resulting from alterations in module dependencies. The direct implementation of the contextual analysis class within `agent_util.py` underscores its explicit reliance on the capabilities provided by the aforementioned dependency.. [ref:e68fd18c60cf4dcefe71a1f0e2badb08cbf4243a]
- **`summary_models.py`**: Uses `summary_models.py` The `agent_util.py` module requires a dependency on a module that provides business logic for analyzing code structure and components, managing data containers like Claim, GroundedText, Alert, and ModuleContext, computing SHA-1 hashes of strings formed by concatenating attributes such as text, reference, and source_module, and handling dependencies and public APIs related to these components.. [ref:39739294bf304a6b0dde99c62baaafe84cd4804b]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py` The module responsible for analyzing code structure and dependencies is required by `agent_util.py` to effectively manage relationships between imports, assignments, function definitions, and classes within Python projects.. [ref:c47d8f28a9f39e15387eb7f61e1178c233a5d1b8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `fa59e6`: Assigns a dictionary type variable named ProjectGraph which maps string keys to any value. _(Source: ProjectGraph)_
> 🆔 `0c79e1`: Assigns path and graph arguments to ModuleContextualizer, calls contextualize_module method, assigns file_path attribute if not set, returns context _(Source: _create_module_context)_
> 🆔 `c7aa78`: Checks if target file path exists, logs information about starting project analysis, creates GraphAnalyzer instance, analyzes project graph, generates contexts using ProjectSummarizer, logs completion of context map generation, and returns the final contexts. _(Source: project_pulse)_
> 🆔 `93ef32`: Manages and encapsulates the processing order of project-related data, initializes an instance by assigning graph and max_cycles attributes, computes topological order, updates module contexts based on dependencies, and returns updated contexts. _(Source: class ProjectSummarizer)_
> 🆔 `e68fd1`: Uses `module_contextualizer.py` (Unverified) The `agent_util.py` necessitates dependence on `module_contextualizer.py` due to its utilization of contextual analysis functionalities inherent within that dependency. This facilitates execution of robust error validation procedures, mapping of component usage across modules, aggregation of insights into interaction patterns among various system components, and identification of potential downstream effects resulting from alterations in module dependencies. The direct implementation of the contextual analysis class within `agent_util.py` underscores its explicit reliance on the capabilities provided by the aforementioned dependency.. _(Source: Import module_contextualizer.py)_
> 🆔 `397392`: Uses `summary_models.py` The `agent_util.py` module requires a dependency on a module that provides business logic for analyzing code structure and components, managing data containers like Claim, GroundedText, Alert, and ModuleContext, computing SHA-1 hashes of strings formed by concatenating attributes such as text, reference, and source_module, and handling dependencies and public APIs related to these components.. _(Source: Import summary_models.py)_
> 🆔 `c47d8f`: Uses `graph_analyzer.py` The module responsible for analyzing code structure and dependencies is required by `agent_util.py` to effectively manage relationships between imports, assignments, function definitions, and classes within Python projects.. _(Source: Import graph_analyzer.py)_
> 🆔 `1275a1`: The role is responsible for analyzing project structure and dependencies using a ProjectGraph, ModuleContextualizer for contextualizing modules based on paths and relationships, and GraphAnalyzer to determine topological order of elements. The module uses ProjectSummarizer to manage processing by updating contexts according to dependencies. _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` The High-Level Purpose of the module that serves as a core service for managing and executing crawling tasks on web projects involves encapsulating various functionalities such as initializing attributes like goal and target_root, creating a memory instance for data storage during each operation, and printing progress messages. It includes running main operations like obtaining the project map, setting up the renderer, and updating memory across multiple turns. The module leverages configurations from `agent_config.py`, including DEFAULT_MODEL set to 'granite4:3b' and CONTEXT_LIMIT set to 2048, as well as using the MemoryInterface class for managing data storage operations.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [ref:9188f8e069449615c8a4ed6631edf9a3203de4ab]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Encapsulates and manages the overall process of crawling and rendering web projects, including initializing attributes such as goal and target_root, creating a memory instance for storing data during each turn, printing messages to indicate progress, running the main operations like getting the project map, initializing the renderer, and updating memory for multiple turns. [ref:f4de653d34e638c566ef9f3ac8d8c3604f489790]

### 🔗 Uses (Upstream)
- **`report_renderer.py`**: Uses `report_renderer.py` The `agent_core.py` requires a dependency on the module responsible for analyzing and encapsulating rendering of report data, which includes various components such as project context map, module information, role descriptions, alerts, public API entities, key dependencies, and dependents. This functionality allows `agent_core.py` to generate output files that effectively summarize these components.. [ref:e35c9e7503a6713a21cf2f9fc92520adaabea737]
- **`agent_util.py`**: Uses `agent_util.py` The `agent_core.py` requires this dependency to utilize ProjectGraph for analyzing project structure and dependencies, as well as for contextualizing modules based on paths and relationships using ModuleContextualizer.. [ref:1cd06fd9ce5dc0f86ee1cc383a94fffe4fb9412f]
- **`agent_config.py`**: Uses `agent_config.py` The `agent_core.py` module requires this dependency as it utilizes configuration constants defined in another module (referred to as [CONFIG_MODULE]). Specifically, it assigns the string value 'granite4:3b' to DEFAULT_MODEL and an integer value of 2048 to CONTEXT_LIMIT, both of which are exported values from [CONFIG_MODULE].. [ref:7f9626d0e89a979c09f03f302e01d3e1fcadae4d]
- **`memory_core.py`**: Uses `memory_core.py` The dependency on `agent_core.py` relies on classes such as `MemoryInterface` and `ChromaMemory`, which encapsulate management of resource operations including allocation, storage, retrieval, modification, and deletion of data. This allows for persistent client interaction with the system's memory resources.. [ref:37d0d6f13ab62fe3a25fe61c7cfd5302c75952ef]
- **`llm_util.py`**: Uses `llm_util.py` The `agent_core.py` module needs the dependency on the utility module, which exports the `chat_llm` function to generate responses based on provided prompts using a specified model for language models.. [ref:e341d5d73be7b441498e7ec9d3f5052e4da3e17a]
- **`summary_models.py`**: Uses `summary_models.py` The `agent_core.py` needs this dependency to leverage its business logic for analyzing code structure and components, handling various data containers such as Claim, GroundedText, Alert, and ModuleContext, computing SHA-1 hashes of strings composed by specific attributes concatenation, and managing dependencies and public APIs related to these components.. [ref:ded5934a0beff48010d7e5150382bbc534d6ab13]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f4de65`: Encapsulates and manages the overall process of crawling and rendering web projects, including initializing attributes such as goal and target_root, creating a memory instance for storing data during each turn, printing messages to indicate progress, running the main operations like getting the project map, initializing the renderer, and updating memory for multiple turns. _(Source: class CrawlerAgent)_
> 🆔 `e35c9e`: Uses `report_renderer.py` The `agent_core.py` requires a dependency on the module responsible for analyzing and encapsulating rendering of report data, which includes various components such as project context map, module information, role descriptions, alerts, public API entities, key dependencies, and dependents. This functionality allows `agent_core.py` to generate output files that effectively summarize these components.. _(Source: Import report_renderer.py)_
> 🆔 `1cd06f`: Uses `agent_util.py` The `agent_core.py` requires this dependency to utilize ProjectGraph for analyzing project structure and dependencies, as well as for contextualizing modules based on paths and relationships using ModuleContextualizer.. _(Source: Import agent_util.py)_
> 🆔 `7f9626`: Uses `agent_config.py` The `agent_core.py` module requires this dependency as it utilizes configuration constants defined in another module (referred to as [CONFIG_MODULE]). Specifically, it assigns the string value 'granite4:3b' to DEFAULT_MODEL and an integer value of 2048 to CONTEXT_LIMIT, both of which are exported values from [CONFIG_MODULE].. _(Source: Import agent_config.py)_
> 🆔 `37d0d6`: Uses `memory_core.py` The dependency on `agent_core.py` relies on classes such as `MemoryInterface` and `ChromaMemory`, which encapsulate management of resource operations including allocation, storage, retrieval, modification, and deletion of data. This allows for persistent client interaction with the system's memory resources.. _(Source: Import memory_core.py)_
> 🆔 `e341d5`: Uses `llm_util.py` The `agent_core.py` module needs the dependency on the utility module, which exports the `chat_llm` function to generate responses based on provided prompts using a specified model for language models.. _(Source: Import llm_util.py)_
> 🆔 `ded593`: Uses `summary_models.py` The `agent_core.py` needs this dependency to leverage its business logic for analyzing code structure and components, handling various data containers such as Claim, GroundedText, Alert, and ModuleContext, computing SHA-1 hashes of strings composed by specific attributes concatenation, and managing dependencies and public APIs related to these components.. _(Source: Import summary_models.py)_
> 🆔 `9188f8`: The High-Level Purpose of the module that serves as a core service for managing and executing crawling tasks on web projects involves encapsulating various functionalities such as initializing attributes like goal and target_root, creating a memory instance for data storage during each operation, and printing progress messages. It includes running main operations like obtaining the project map, setting up the renderer, and updating memory across multiple turns. The module leverages configurations from `agent_config.py`, including DEFAULT_MODEL set to 'granite4:3b' and CONTEXT_LIMIT set to 2048, as well as using the MemoryInterface class for managing data storage operations. _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` This module acts as the primary entry point for executing the main functionality of an application that deals with analyzing code structure. It parses command-line arguments using an ArgumentParser object and assigns specific values to variables like goal and target_folder. Subsequently, it invokes a function named 'main' which searches for a particular file in the specified folder, creates an instance of CrawlerAgent with the goal and found file path, runs the agent, and returns a completion message. [ref:1c6884fb45af11a71080a7df05b903f3047640b9]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Assigns X, Calls Y (⚠️ The code assigns values to 'args' by parsing command line arguments and then calls a function (Y) on it. However, the specific operations performed in Y are not shown.) [ref:29c0c4d53e37253da3a8e096838c2f999ac8f34a]
- **`🔌 goal`**: Assigns value of `goal` from parsed arguments [ref:02bcfdf8ddb29d2e8d5650b48b66d41d32d7d3a1]
- **`🔌 main`**: The function searches for a file ending with '_file.py' in the specified target folder, creates an instance of CrawlerAgent with the goal and found file path, runs the agent, and returns a completion message. [ref:18ad98c89cfb6695c2871529c047312e14e35f56]
- **`🔌 parser`**: Assigns an ArgumentParser object for parsing command-line arguments. [ref:b39e376d84e389698a762e5a56e77de56ef8c4c6]
- **`🔌 result`**: Calls main function with goal and target_folder arguments [ref:eb82b3d7429b4c52fa1d95ce2d4c0d2947193b8e]
- **`🔌 target_folder`**: Assigns target_folder from args using parser.parse_args() (⚠️ The provided code snippet only assigns `target_folder` from `args`, but there's no indication of using a parser to parse the arguments. The claim suggests that `parser.parse_args()` is used, which isn't shown in this snippet.) [ref:1457a8233495f54f3c0f12c4479d7865f28a7aec]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py` The module agent_graph_main.py requires a dependency due to its need for functionalities like initializing attributes, creating data storage instances, obtaining project maps, setting up renderers, and updating memory across multiple turns. These services are crucial for effectively managing and executing crawling tasks.. [ref:65645c91b9b2927afc306f9f3400c50a2e43eb7f]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b39e37`: Assigns an ArgumentParser object for parsing command-line arguments. _(Source: parser)_
> 🆔 `29c0c4`: Assigns X, Calls Y (⚠️ The code assigns values to 'args' by parsing command line arguments and then calls a function (Y) on it. However, the specific operations performed in Y are not shown.) _(Source: args)_
> 🆔 `02bcfd`: Assigns value of `goal` from parsed arguments _(Source: goal)_
> 🆔 `1457a8`: Assigns target_folder from args using parser.parse_args() (⚠️ The provided code snippet only assigns `target_folder` from `args`, but there's no indication of using a parser to parse the arguments. The claim suggests that `parser.parse_args()` is used, which isn't shown in this snippet.) _(Source: target_folder)_
> 🆔 `eb82b3`: Calls main function with goal and target_folder arguments _(Source: result)_
> 🆔 `18ad98`: The function searches for a file ending with '_file.py' in the specified target folder, creates an instance of CrawlerAgent with the goal and found file path, runs the agent, and returns a completion message. _(Source: main)_
> 🆔 `65645c`: Uses `agent_core.py` The module agent_graph_main.py requires a dependency due to its need for functionalities like initializing attributes, creating data storage instances, obtaining project maps, setting up renderers, and updating memory across multiple turns. These services are crucial for effectively managing and executing crawling tasks.. _(Source: Import agent_core.py)_
> 🆔 `1c6884`: This module acts as the primary entry point for executing the main functionality of an application that deals with analyzing code structure. It parses command-line arguments using an ArgumentParser object and assigns specific values to variables like goal and target_folder. Subsequently, it invokes a function named 'main' which searches for a particular file in the specified folder, creates an instance of CrawlerAgent with the goal and found file path, runs the agent, and returns a completion message. _(Source: Synthesis)_
</details>

---