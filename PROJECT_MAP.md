# Project Context Map

**Total Modules:** 15

## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Orchestrates data modeling processes, managing relationships between modules, roles, dependencies, API entries, and alerts through structured context management.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, module_contextualizer.py, report_renderer.py [ref:1b716c1452d4a21d91cbbaf5555d67e5db666379]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [ref:cdaf82fd4c021fa0a891dedd7d85fff3402f4bef]
- **`🔌 class Claim`**: Encapsulates unique identifier generation process for text, reference, and source module data [ref:728c0f788d41408bdb3c28a611620b3e2874f35e]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [ref:b7729088a8954b42aeaaf067fb7b5ca6c1bcaf4c]
- **`🔌 class ModuleContext`**: Manages structured data related to module instances, including explanations, supporting claims, dependencies, dependents, public API entries, and alerts associated with each instance. [ref:5e38ed6324285157fd7ba3a5b2f25d9fbcf63538]
- **`🔌 🔌 Claim.id`**: Generates unique identifier by hashing concatenated text, reference, and source module [ref:84c83725e0df1959ebc550649c4b0d55c2d4a488]
- **`🔌 🔌 ModuleContext.add_alert`**: Appends an alert to the alerts list [ref:8325d27ea4459752231859f585e88de6f0362ddb]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Combines explanation with placeholders and supporting claims to create grounded text for module dependencies [ref:5c6c4154f39ab093a759926125b8d7e4011b2c38]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds dependent context by combining explanation with placeholders from supporting claims and storing the resulting text in key_dependents dictionary. [ref:e31079cdb05f15fbe013426c3811de95456c0bb8]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds public API entry by attaching supporting claims to description [ref:54b95b6eadab8f58fa335a164aed9031527850f5]
- **`🔌 🔌 ModuleContext.set_module_role`**: Updates module role by adding supporting claims to text and storing in GroundedText [ref:06c151f8723a76f131dc87f8db321b5be723dd29]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `84c837`: Generates unique identifier by hashing concatenated text, reference, and source module _(Source: 🔌 Claim.id)_
> 🆔 `728c0f`: Encapsulates unique identifier generation process for text, reference, and source module data _(Source: class Claim)_
> 🆔 `b77290`: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `cdaf82`: Data container for Alert records. _(Source: class Alert)_
> 🆔 `06c151`: Updates module role by adding supporting claims to text and storing in GroundedText _(Source: 🔌 ModuleContext.set_module_role)_
> 🆔 `5c6c41`: Combines explanation with placeholders and supporting claims to create grounded text for module dependencies _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `e31079`: Adds dependent context by combining explanation with placeholders from supporting claims and storing the resulting text in key_dependents dictionary. _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `54b95b`: Adds public API entry by attaching supporting claims to description _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `8325d2`: Appends an alert to the alerts list _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `5e38ed`: Manages structured data related to module instances, including explanations, supporting claims, dependencies, dependents, public API entries, and alerts associated with each instance. _(Source: class ModuleContext)_
> 🆔 `1b716c`: Orchestrates data modeling processes, managing relationships between modules, roles, dependencies, API entries, and alerts through structured context management. _(Source: Synthesis)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Manages memory state, orchestrates secure processing of user input by routing through llm_util.py for parsing, ensuring upstream logic integration adheres to security standards

**Impact Analysis:** Changes to this module will affect: agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, module_contextualizer.py [ref:dc94ec8c3510fd07a6e3b4c24ae0a2fc40fb99f9]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines a set containing disallowed adjectives for use in code [ref:f35389f633e6a7172b69a3388fa45757ff21ba73]
- **`🔌 class SemanticGatekeeper`**: Organizes and controls access to structured data and messages [ref:d7db18e664cf67015a6a58c133ad38ed00318c9a]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Formats user input into system messages, generates response from LLM, critiques JSON validity and content style, verifies grounding if source provided, and returns final validated JSON with specified key or indicates failure [ref:403e7a08758fd1ff53ada8c2a0116ee5e9026c33]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Imports `agent_config.py`. [ref:e1a0411f6be9098116112284db26c3617b5e6386]
- **`llm_util.py`**: Uses `llm_util.py`: Calls a specific function from the imported module to manage user input handling and exception management for LLM model. [ref:d5ce7a67e57fadf838c9253d34de6f3746009caf]

### 👥 Used By (Downstream)
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_critic.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `f35389`: Defines a set containing disallowed adjectives for use in code _(Source: BANNED_ADJECTIVES)_
> 🆔 `403e7a`: Formats user input into system messages, generates response from LLM, critiques JSON validity and content style, verifies grounding if source provided, and returns final validated JSON with specified key or indicates failure _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `d7db18`: Organizes and controls access to structured data and messages _(Source: class SemanticGatekeeper)_
> 🆔 `e1a041`: Imports `agent_config.py`. _(Source: Import agent_config.py)_
> 🆔 `d5ce7a`: Uses `llm_util.py`: Calls a specific function from the imported module to manage user input handling and exception management for LLM model. _(Source: Import llm_util.py)_
> 🆔 `dc94ec`: Manages memory state, orchestrates secure processing of user input by routing through llm_util.py for parsing, ensuring upstream logic integration adheres to security standards _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [ref:449512ed434b04a04a62f74801a3cff91b4129f6]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Assigns maximum context length value to 2048 [ref:996907e92d601fc79485731eeb90a4a242afcee4]
- **`🔌 DEFAULT_MODEL`**: Assigns string value specifying Granite 3B model to global variable indicating preferred language model for tasks [ref:a8a0104e522e62069110332249f1438f3507e437]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a8a010`: Assigns string value specifying Granite 3B model to global variable indicating preferred language model for tasks _(Source: DEFAULT_MODEL)_
> 🆔 `996907`: Assigns maximum context length value to 2048 _(Source: CONTEXT_LIMIT)_
> 🆔 `449512`: Defines configuration constants. _(Source: Archetype)_
</details>

---
## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` Orchestrates parsing of user input into structured messages for LLM model, handling exceptions, and integrating with Ollama API without using hardcoded credentials or sensitive data.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [ref:6a1cb237ab187defa026fac30e0de0c922bd9aac]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Processes user input into messages for LLM model and handles exceptions [ref:a2f24f9844c5c54a482553113e1d9c3d7bc14023]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a2f24f`: Processes user input into messages for LLM model and handles exceptions _(Source: chat_llm)_
> 🆔 `6a1cb2`: Orchestrates parsing of user input into structured messages for LLM model, handling exceptions, and integrating with Ollama API without using hardcoded credentials or sensitive data. _(Source: Synthesis)_
</details>

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` Generates project context reports by aggregating GroundedText and Alert records, encapsulating report generation logic in ReportRenderer class

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [ref:1088ed4e4a8d1e814a5b6e8f00c082022a3b236a]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Encapsulates context data for project reports [ref:f2ad9b56a06380ec24256a1f8f1385a91dc39fba]
- **`🔌 🔌 ReportRenderer.render`**: Generates report file containing project context map details [ref:a255867044a6d8596594285fe8a2aa9928e5ad87]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: (Unverified) Calls generate_unique_id() function from summary_models.py to create unique identifier for text, reference, and source module data. [ref:26c4f3376992681a31399c406bfc01b3e5f3d56c]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a25586`: Generates report file containing project context map details _(Source: 🔌 ReportRenderer.render)_
> 🆔 `f2ad9b`: Encapsulates context data for project reports _(Source: class ReportRenderer)_
> 🆔 `26c4f3`: Uses `summary_models.py`: (Unverified) Calls generate_unique_id() function from summary_models.py to create unique identifier for text, reference, and source module data. _(Source: Import summary_models.py)_
> 🆔 `1088ed`: Generates project context reports by aggregating GroundedText and Alert records, encapsulating report generation logic in ReportRenderer class _(Source: Synthesis)_
</details>

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` Analyzes module structure, delegates parsing to upstream logic, determines archetype based on entities and dependencies, updates relevant records in ModuleArchetype system.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:a7482bbbc593e51527b1159e397b3771d2e2d13a]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [ref:a947722dc58c4984aaea3d4bb21713a64a0283ec]
- **`🔌 class ModuleClassifier`**: Manages module data, analyzes source code structure, and determines archetype based on entities and dependencies [ref:c546145f1076ca33fee77e66364b8959a1dde4d9]
- **`🔌 🔌 ModuleClassifier.classify`**: Determines module archetype based on name, source code, entities, dependencies, functions, classes, and global variables [ref:2c2d485d7e436d0f3778da29f34628c0dca6b340]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a94772`: Data container for ModuleArchetype records. _(Source: class ModuleArchetype)_
> 🆔 `2c2d48`: Determines module archetype based on name, source code, entities, dependencies, functions, classes, and global variables _(Source: 🔌 ModuleClassifier.classify)_
> 🆔 `c54614`: Manages module data, analyzes source code structure, and determines archetype based on entities and dependencies _(Source: class ModuleClassifier)_
> 🆔 `a7482b`: Analyzes module structure, delegates parsing to upstream logic, determines archetype based on entities and dependencies, updates relevant records in ModuleArchetype system. _(Source: Synthesis)_
</details>

---
## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` Analyzes code structure, identifies entities, and records interactions by parsing imports and function definitions

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:6d70a0bab54410cee504673340456ed16a043976]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Analyzes code structure, identifies entities, records module interactions [ref:2d8630ed7c85d42a408e3cee2e78e93d50a7bc04]
- **`🔌 class GraphAnalyzer`**: Manages the structure and dependencies within a project [ref:5bcd4adad3ee3c6b9f8f30eb163031ae8c32d849]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes current context from stack by popping it [ref:3fac96a795480d6f04fa9df1b62ef5dd13885953]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Removes context from stack when leaving function definition [ref:c86e255808006978b608f56424c0d992bd0f60ed]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Adds annotated assignment to global entities list [ref:fcdeef4f37a0475dc7042e0fe535fd4e283afe39]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Registers global variable assignments in entities list [ref:f1e255bd101461b3f5b8aec06978c07a1b9021c4]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Records interaction value from function node when it is a name [ref:ebaad9d86447974d4926a5936f7e2a01ef39a2c8]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Registers class details in entities dictionary [ref:e474017a85a479917eaab65acac3263987524f17]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Analyzes function definition node to determine if unimplemented or private [ref:ba8bc04ebeef5f0a5be024b8be2dcc7d3fdd2c6f]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Collects module names from import nodes and adds them to external imports set [ref:1c47a7d13b3f3861fbd49d72f02018b0e69cdb67]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes import statements to determine module names and file paths for relative imports [ref:cccd251b3c4e25c9ef92620d5299ca1135bdbc3e]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records interaction value when context condition is met (⚠️ The code records interaction value when context condition is met. However, it does not explicitly record an interaction value under the specified condition (self.current_context and self.current_context[-1] == node.value). Instead, it returns early without recording the interaction.) [ref:1d47a891517399cabedd5da5613cc3258cb034f0]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds graph depth-first search root path, populates dependents, and returns graph structure [ref:7c6a948893f9c09153b3a78094939ff4da3ee7e9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1c47a7`: Collects module names from import nodes and adds them to external imports set _(Source: 🔌 CodeEntityVisitor.visit_Import)_
> 🆔 `cccd25`: Analyzes import statements to determine module names and file paths for relative imports _(Source: 🔌 CodeEntityVisitor.visit_ImportFrom)_
> 🆔 `f1e255`: Registers global variable assignments in entities list _(Source: 🔌 CodeEntityVisitor.visit_Assign)_
> 🆔 `fcdeef`: Adds annotated assignment to global entities list _(Source: 🔌 CodeEntityVisitor.visit_AnnAssign)_
> 🆔 `e47401`: Registers class details in entities dictionary _(Source: 🔌 CodeEntityVisitor.visit_ClassDef)_
> 🆔 `3fac96`: Removes current context from stack by popping it _(Source: 🔌 CodeEntityVisitor.leave_ClassDef)_
> 🆔 `ba8bc0`: Analyzes function definition node to determine if unimplemented or private _(Source: 🔌 CodeEntityVisitor.visit_FunctionDef)_
> 🆔 `c86e25`: Removes context from stack when leaving function definition _(Source: 🔌 CodeEntityVisitor.leave_FunctionDef)_
> 🆔 `ebaad9`: Records interaction value from function node when it is a name _(Source: 🔌 CodeEntityVisitor.visit_Call)_
> 🆔 `1d47a8`: Records interaction value when context condition is met (⚠️ The code records interaction value when context condition is met. However, it does not explicitly record an interaction value under the specified condition (self.current_context and self.current_context[-1] == node.value). Instead, it returns early without recording the interaction.) _(Source: 🔌 CodeEntityVisitor.visit_Name)_
> 🆔 `2d8630`: Analyzes code structure, identifies entities, records module interactions _(Source: class CodeEntityVisitor)_
> 🆔 `7c6a94`: Builds graph depth-first search root path, populates dependents, and returns graph structure _(Source: 🔌 GraphAnalyzer.analyze)_
> 🆔 `5bcd4a`: Manages the structure and dependencies within a project _(Source: class GraphAnalyzer)_
> 🆔 `6d70a0`: Analyzes code structure, identifies entities, and records interactions by parsing imports and function definitions _(Source: Synthesis)_
</details>

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` Manages the lifecycle of memories, organizing them in Chroma database and updating their metadata based on query history and helpfulness ratings

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:02df603da82295233a25eb318da7c8199472bb85]

### 🚨 Alerts
- 🔴 **Incomplete**: Method not implemented `(Ref: def query_memory(self, query, current_turn=0, n_results=5):)`

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Organizes, manages, and retrieves data related to memories in the system [ref:5105a4eb080b9a28ad5b5986a5cee42ed7b415e0]
- **`🔌 class MemoryInterface`**: Encapsulates memory data structure and defines query operations (⚠️ The code defines a class `MemoryInterface` with an abstract method `query_memory`, but does not encapsulate any memory data structure or define how query operations should be implemented. The claim is too broad for the provided code.) [ref:e4e076cbe67caf2c46b06b130136b6db2b77b2a4]
- **`🔌 🔌 ChromaMemory.add_memory`**: Creates unique memory ID and combines metadata into structured format, then adds combined data to collection [ref:55a00c84486aa6f039a4e37444490c07e7dcdbcc]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Identifies memories for deletion based on usefulness and usage frequency then removes them [ref:02d165c0280cdce43b311180dc40e88e73d65e85]
- **`🔌 🔌 ChromaMemory.query_memory`**: Queries memory collection for specified query and updates metadata with current turn [ref:b8d1cf107185d8f8b57a2076ffc954a5872c2870]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Updates memory's helpfulness rating in database [ref:f7ca8f749942b21779a99be90ef29a5e66013e8c]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [ref:a118a7e568f2c463d1868b83e5ab35c1ced0bee2]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `a118a7`: Defines interface signature (Abstract). _(Source: 🔌 MemoryInterface.query_memory)_
> 🆔 `e4e076`: Encapsulates memory data structure and defines query operations (⚠️ The code defines a class `MemoryInterface` with an abstract method `query_memory`, but does not encapsulate any memory data structure or define how query operations should be implemented. The claim is too broad for the provided code.) _(Source: class MemoryInterface)_
> 🆔 `55a00c`: Creates unique memory ID and combines metadata into structured format, then adds combined data to collection _(Source: 🔌 ChromaMemory.add_memory)_
> 🆔 `b8d1cf`: Queries memory collection for specified query and updates metadata with current turn _(Source: 🔌 ChromaMemory.query_memory)_
> 🆔 `f7ca8f`: Updates memory's helpfulness rating in database _(Source: 🔌 ChromaMemory.update_helpfulness)_
> 🆔 `02d165`: Identifies memories for deletion based on usefulness and usage frequency then removes them _(Source: 🔌 ChromaMemory.cleanup_memories)_
> 🆔 `5105a4`: Organizes, manages, and retrieves data related to memories in the system _(Source: class ChromaMemory)_
> 🆔 `02df60`: Manages the lifecycle of memories, organizing them in Chroma database and updating their metadata based on query history and helpfulness ratings _(Source: Synthesis)_
</details>

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` Analyzes project structure, critiques documentation quality, and enforces style guidelines using banned adjectives from upstream state.

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:5f76e8dce3367145d3382d7b35efb6ad71a1b439]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Analyzes project structure, identifies modules, and critiques documentation quality [ref:063ee10ff7096266cbae8938ccbb0d773eec354e]
- **`🔌 🔌 MapCritic.critique`**: Analyzes modules to generate critiques for project [ref:b4d23b56b0c8a5d14801ff92233b3845a38a8264]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Importing a module containing a predefined set of prohibited words and utilizing this list to filter content. [ref:e154e39ffaf28b62318747e431a0fdb48d1c14c0]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b4d23b`: Analyzes modules to generate critiques for project _(Source: 🔌 MapCritic.critique)_
> 🆔 `063ee1`: Analyzes project structure, identifies modules, and critiques documentation quality _(Source: class MapCritic)_
> 🆔 `e154e3`: Uses `semantic_gatekeeper.py`: Importing a module containing a predefined set of prohibited words and utilizing this list to filter content. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `5f76e8`: Analyzes project structure, critiques documentation quality, and enforces style guidelines using banned adjectives from upstream state. _(Source: Synthesis)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes global code structure, deconstructs functions and classes, and generates modular skeletons for enhanced maintainability and adaptability through detailed component breakdowns.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:7408a6a711bceeca60574d71ccd17f0ac1ce4abb]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes and processes component definitions in specified module context [ref:3bbf114be7cf35c5eebb3133a90cbea948fb24a9]
- **`🔌 class SkeletonTransformer`**: Encapsulates logic for processing function, async function, and class definition nodes [ref:2fe7ed645a01f78e5aaafcd75789e6be42333921]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes global variables, functions, classes, and their interactions in a specified module context [ref:10f59d2fec916dff3a885dfd706a4a9e28224767]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Transforms source code by adding ellipsis placeholders to function and class definitions [ref:38a16b0d4992e70603ae0ed4ed4d99a12dd57898]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Mutates async function definition body to include ellipsis expression [ref:505140e252e84ed167b478809e21ccdccfbf6a19]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes first docstring line from class definition body [ref:4256d244818508273d2826621165a1186e75d312]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Modifies function node body to include ellipsis expression [ref:36ea7179a59444213dd1ce0c48335c430e9b8387]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Imports and uses a set of disallowed adjectives defined elsewhere for code analysis purposes; Calls SemanticGatekeeper to format user input, generate LLM response, critique JSON validity and content style, verify grounding if source provided, and return validated JSON or indicate failure. [ref:90543ecfa795eb530abb7c56525145b1d8bf9a68]
- **`summary_models.py`**: Uses `summary_models.py`: Imports and utilizes a data structure for GroundedText records. [ref:a68baede347498625851b193977ca9298371353d]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `10f59d`: Analyzes global variables, functions, classes, and their interactions in a specified module context _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `38a16b`: Transforms source code by adding ellipsis placeholders to function and class definitions _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `3bbf11`: Analyzes and processes component definitions in specified module context _(Source: class ComponentAnalyst)_
> 🆔 `36ea71`: Modifies function node body to include ellipsis expression _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `505140`: Mutates async function definition body to include ellipsis expression _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `4256d2`: Removes first docstring line from class definition body _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `2fe7ed`: Encapsulates logic for processing function, async function, and class definition nodes _(Source: class SkeletonTransformer)_
> 🆔 `90543e`: Uses `semantic_gatekeeper.py`: Imports and uses a set of disallowed adjectives defined elsewhere for code analysis purposes; Calls SemanticGatekeeper to format user input, generate LLM response, critique JSON validity and content style, verify grounding if source provided, and return validated JSON or indicate failure. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `a68bae`: Uses `summary_models.py`: Imports and utilizes a data structure for GroundedText records. _(Source: Import summary_models.py)_
> 🆔 `7408a6`: Analyzes global code structure, deconstructs functions and classes, and generates modular skeletons for enhanced maintainability and adaptability through detailed component breakdowns. _(Source: Synthesis)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Analyzes dependencies between modules and interactions, ensuring smooth integration and preventing conflicts.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:0439e0384b748da959c44a56ddb9d2fcf77c226d]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Captures the dependencies between modules [ref:f9c9fa7d6f41afd86dbb035233a11f3641a2f540]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes dependency imports and interactions between modules [ref:cd38bb292cc2dd952c4228e1bf3b39d4356fc7bb]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: dependency_analyst.py calls SemanticGatekeeper to format user input into system messages and generate response from LLM. [ref:6f33c55c905205621519bf49200776c089c3c8b1]
- **`summary_models.py`**: Uses `summary_models.py`: Calls the module's function for generating a unique identifier based on text, reference, and source data. [ref:c1ce994a64556769c1ffaee3204e7c5dc4ddab9e]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `cd38bb`: Analyzes dependency imports and interactions between modules _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `f9c9fa`: Captures the dependencies between modules _(Source: class DependencyAnalyst)_
> 🆔 `6f33c5`: Uses `semantic_gatekeeper.py`: dependency_analyst.py calls SemanticGatekeeper to format user input into system messages and generate response from LLM. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `c1ce99`: Uses `summary_models.py`: Calls the module's function for generating a unique identifier based on text, reference, and source data. _(Source: Import summary_models.py)_
> 🆔 `0439e0`: Analyzes dependencies between modules and interactions, ensuring smooth integration and preventing conflicts. _(Source: Synthesis)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Analyzes module context, synthesizes systemic critique based on instructions

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:4ed5008d83d24b1f2a4a91bb6d02cccd6a75e89b]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Analyzes module components, gathers contextual knowledge, and synthesizes detailed role description based on provided data and instructions [ref:8a8e714d85b5895362d3526ebdf19a8609faceb2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyzes module data, analyzes components and dependencies, synthesizes systemic critique based on instruction [ref:719976b721960b7dd68d1de78552e5058e16aa44]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Imports and uses the set of disallowed adjectives; Does module_contextualizer.py call SemanticGatekeeper's functions/classes?. [ref:03b1308cb4538461e3555365c2d38837f1dceaf0]
- **`module_classifier.py`**: Uses `module_classifier.py`: Exports Data; Calls ModuleClassifier to determine module archetype based on name, source code, entities, dependencies, functions, classes, and global variables.. [ref:80efbfdf06fd125846f586a8812f7c959edccc0b]
- **`component_analyst.py`**: Uses `component_analyst.py`: Calls ComponentAnalyst to analyze global variables, functions, classes, and their interactions in module context. [ref:1f5599e327893514b5ce20ce4e76d60fb6ae4a5b]
- **`summary_models.py`**: Uses `summary_models.py`: Imports and utilizes a data structure for grounded text entities; module_contextualizer.py calls a function to hash concatenated text, reference, and source module data, encapsulating this process for generating unique identifiers.. [ref:6c28f750b913a3a5f507b4cd0664c600121e315e]
- **`dependency_analyst.py`**: Uses `dependency_analyst.py`: Calls DependencyAnalyst to analyze dependency imports and interactions between modules. [ref:32c616861a8e4558b2bfd0bfde7d9152971d4555]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `719976`: Analyzes module data, analyzes components and dependencies, synthesizes systemic critique based on instruction _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `8a8e71`: Analyzes module components, gathers contextual knowledge, and synthesizes detailed role description based on provided data and instructions _(Source: class ModuleContextualizer)_
> 🆔 `03b130`: Uses `semantic_gatekeeper.py`: Imports and uses the set of disallowed adjectives; Does module_contextualizer.py call SemanticGatekeeper's functions/classes?. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `80efbf`: Uses `module_classifier.py`: Exports Data; Calls ModuleClassifier to determine module archetype based on name, source code, entities, dependencies, functions, classes, and global variables.. _(Source: Import module_classifier.py)_
> 🆔 `1f5599`: Uses `component_analyst.py`: Calls ComponentAnalyst to analyze global variables, functions, classes, and their interactions in module context. _(Source: Import component_analyst.py)_
> 🆔 `6c28f7`: Uses `summary_models.py`: Imports and utilizes a data structure for grounded text entities; module_contextualizer.py calls a function to hash concatenated text, reference, and source module data, encapsulating this process for generating unique identifiers.. _(Source: Import summary_models.py)_
> 🆔 `32c616`: Uses `dependency_analyst.py`: Calls DependencyAnalyst to analyze dependency imports and interactions between modules. _(Source: Import dependency_analyst.py)_
> 🆔 `4ed500`: Analyzes module context, synthesizes systemic critique based on instructions _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Orchestrates interaction management by delegating parsing logic from semantic_gatekeeper.py while managing code entity interactions through graph_analyzer.py, recording module-specific contexts and critiques to GroundedText instances.

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:e1eaa46466fca8f93523bce6ea33f81657125154]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns a dictionary data structure to store project information [ref:aa2b7ea668b7e9e865db55cb50ce7ff09ceb7079]
- **`🔌 class ProjectSummarizer`**: Manages project structure representation and processing logic [ref:b232d768ab93af88a32ee9785a9a2497853ce263]
- **`🔌 project_pulse`**: Analyzes project structure from root path [ref:8f19b0adf76dbca8ffb03aae022ce1395f743019]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Manages generating module contexts for project graph through iterative cycles, applying critiques and updating context hashes. [ref:d8dfeaf75d3fe24089187fe24b63caea49f04b2c]
- **`🔒 _create_module_context`**: Generates module context by contextualizing module path and graph data [ref:9295be24aa87c62bb91feb23d791511160c86176]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Imports and utilizes the predefined collection of unacceptable descriptors from a referenced module; SemanticGatekeeper is called by agent_util.py to format user input, generate LLM response, critique JSON validity and content style, verify grounding if source provided, and return validated JSON. [ref:3bd7147acf66a4a2fffefc5d3a8d1cf0b142674e]
- **`module_contextualizer.py`**: Imports `module_contextualizer.py`. [ref:3354661bd3d0f67b8e33db9dc3ae6e79a87ee97f]
- **`report_renderer.py`**: Imports `report_renderer.py`. [ref:1c31637324d047bd4567e80499f5ff5619ad59d7]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: Imports a module containing `graph_analyzer` and utilizes interaction values recorded for nodes based on their names.. [ref:164d2df74a3921920f9317fbc28ed7496ace9b0a]
- **`map_critic.py`**: Imports `map_critic.py`. [ref:c54d03461bdbe40229c63bab2ba6ba1632087818]
- **`summary_models.py`**: Imports `summary_models.py`. [ref:0e8ce6fc6ba415b8374fa6adab75144ac1d3ad1b]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `aa2b7e`: Assigns a dictionary data structure to store project information _(Source: ProjectGraph)_
> 🆔 `9295be`: Generates module context by contextualizing module path and graph data _(Source: _create_module_context)_
> 🆔 `8f19b0`: Analyzes project structure from root path _(Source: project_pulse)_
> 🆔 `d8dfea`: Manages generating module contexts for project graph through iterative cycles, applying critiques and updating context hashes. _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `b232d7`: Manages project structure representation and processing logic _(Source: class ProjectSummarizer)_
> 🆔 `3bd714`: Uses `semantic_gatekeeper.py`: Imports and utilizes the predefined collection of unacceptable descriptors from a referenced module; SemanticGatekeeper is called by agent_util.py to format user input, generate LLM response, critique JSON validity and content style, verify grounding if source provided, and return validated JSON. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `335466`: Imports `module_contextualizer.py`. _(Source: Import module_contextualizer.py)_
> 🆔 `1c3163`: Imports `report_renderer.py`. _(Source: Import report_renderer.py)_
> 🆔 `164d2d`: Uses `graph_analyzer.py`: Imports a module containing `graph_analyzer` and utilizes interaction values recorded for nodes based on their names.. _(Source: Import graph_analyzer.py)_
> 🆔 `c54d03`: Imports `map_critic.py`. _(Source: Import map_critic.py)_
> 🆔 `0e8ce6`: Imports `summary_models.py`. _(Source: Import summary_models.py)_
> 🆔 `e1eaa4`: Orchestrates interaction management by delegating parsing logic from semantic_gatekeeper.py while managing code entity interactions through graph_analyzer.py, recording module-specific contexts and critiques to GroundedText instances. _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Manages crawling process, stores project details, and renders reports using configured Granite 3B model and memory interface.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [ref:7e9f2e41d0729c5c39a4242d3ea81c8a332ad38e]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Manages the crawling process, stores project details, and renders reports [ref:c15c3b38aebc22d2154e5e2a4843d17ea497d398]
- **`🔌 🔌 CrawlerAgent.run`**: Prints running details, retrieves project map, renders report, cleans memory, and returns completion message [ref:6bbc3fe463593c762c1c0db7d592c36f48858c41]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py`: Imports and uses the specified language model value for tasks. [ref:dc85921085288338efb2f32ed0847a409f03e5a2]
- **`llm_util.py`**: Imports `llm_util.py`. [ref:8154323f40a1ca06e29bbcd9cd792149a6082cb5]
- **`report_renderer.py`**: Uses `report_renderer.py`: agent_core.py calls ReportRenderer to generate project context map report file and encapsulate context data for project reports. [ref:9401d77a33139e1978a761d7ab9e2ca833ab7174]
- **`agent_util.py`**: Imports `agent_util.py`. [ref:d95bb586808b3d8220d8d19d3d2bfaeee1fe9349]
- **`memory_core.py`**: Uses `memory_core.py`: Imports and utilizes an abstract class defining a memory interface with query methods. (⚠️ The code includes an abstract class `MemoryInterface` with a method `query_memory`, but it does not clearly define or encapsulate any memory data structure. The claim is partially supported by the presence of the abstract class and methods, but lacks evidence for full support.); Calls module's functionality to generate unique identifier and integrate metadata into structured format. [ref:3b77d0b7c481953d93e4ee93e7c388a8e62f4dc7]
- **`summary_models.py`**: Uses `summary_models.py`: The core module invokes functionalities from another module to create unique identifiers and grounded text by hashing combined data, updating roles with supporting claims, merging explanations with placeholders, and storing results.. [ref:e12b75ac02390c29e5952618e46b58ed5670fdd9]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `6bbc3f`: Prints running details, retrieves project map, renders report, cleans memory, and returns completion message _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `c15c3b`: Manages the crawling process, stores project details, and renders reports _(Source: class CrawlerAgent)_
> 🆔 `dc8592`: Uses `agent_config.py`: Imports and uses the specified language model value for tasks. _(Source: Import agent_config.py)_
> 🆔 `815432`: Imports `llm_util.py`. _(Source: Import llm_util.py)_
> 🆔 `9401d7`: Uses `report_renderer.py`: agent_core.py calls ReportRenderer to generate project context map report file and encapsulate context data for project reports. _(Source: Import report_renderer.py)_
> 🆔 `d95bb5`: Imports `agent_util.py`. _(Source: Import agent_util.py)_
> 🆔 `3b77d0`: Uses `memory_core.py`: Imports and utilizes an abstract class defining a memory interface with query methods. (⚠️ The code includes an abstract class `MemoryInterface` with a method `query_memory`, but it does not clearly define or encapsulate any memory data structure. The claim is partially supported by the presence of the abstract class and methods, but lacks evidence for full support.); Calls module's functionality to generate unique identifier and integrate metadata into structured format. _(Source: Import memory_core.py)_
> 🆔 `e12b75`: Uses `summary_models.py`: The core module invokes functionalities from another module to create unique identifiers and grounded text by hashing combined data, updating roles with supporting claims, merging explanations with placeholders, and storing results.. _(Source: Import summary_models.py)_
> 🆔 `7e9f2e`: Manages crawling process, stores project details, and renders reports using configured Granite 3B model and memory interface. _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates crawling process, delegates argument parsing, retrieves project root, instantiates CrawlerAgent, executes run method for goal processing [ref:db7326a24a3c336a29a16f3391735a698c1aac09]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Assigns parsed command line arguments to a variable for use in program execution [ref:6b91b0852ed90fd84399169d9dc85a4f6bb51a83]
- **`🔌 goal`**: Extracts goal argument from parsed command line arguments for further processing [ref:7161c5a33e4355b3dd22fd83d359033728e514d5]
- **`🔌 main`**: Retrieves project root, instantiates CrawlerAgent, runs agent with goal, completes execution [ref:0a12bc7e84a3730a3690a6c5309f04b95971bc9c]
- **`🔌 parser`**: Creates an argument parser to handle command line input for goal and target folder values. [ref:19ebfabd3455060ca82fdf0182dc79233be2fa99]
- **`🔌 result`**: Executes main function with goal and target folder arguments to process data [ref:d4e4d546cdbab3c0f2cd076b242ed36f747febe6]
- **`🔌 target_folder`**: Retrieves the target folder path from command line arguments and assigns it to variable [ref:0324637022873ac8e92fe20ed725ee8aa504b8b0]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Imports and uses the Data class from agent_core to manage crawling process, store project details, and render reports.; Calls export to handle various tasks including printing running details, retrieving project map, rendering report, cleaning memory and returning completion message. [ref:90b52948a869cbe8857483d0f9559d2abc7cd485]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `19ebfa`: Creates an argument parser to handle command line input for goal and target folder values. _(Source: parser)_
> 🆔 `6b91b0`: Assigns parsed command line arguments to a variable for use in program execution _(Source: args)_
> 🆔 `7161c5`: Extracts goal argument from parsed command line arguments for further processing _(Source: goal)_
> 🆔 `032463`: Retrieves the target folder path from command line arguments and assigns it to variable _(Source: target_folder)_
> 🆔 `d4e4d5`: Executes main function with goal and target folder arguments to process data _(Source: result)_
> 🆔 `0a12bc`: Retrieves project root, instantiates CrawlerAgent, runs agent with goal, completes execution _(Source: main)_
> 🆔 `90b529`: Uses `agent_core.py`: Imports and uses the Data class from agent_core to manage crawling process, store project details, and render reports.; Calls export to handle various tasks including printing running details, retrieving project map, rendering report, cleaning memory and returning completion message. _(Source: Import agent_core.py)_
> 🆔 `db7326`: Orchestrates crawling process, delegates argument parsing, retrieves project root, instantiates CrawlerAgent, executes run method for goal processing _(Source: Synthesis)_
</details>

---