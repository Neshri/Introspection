# Project Context Map

**Total Modules:** 15

## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` Orchestrates parsing of upstream logic using dataclasses, hashlib, re, typing

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, module_contextualizer.py, report_renderer.py [ref:e2197eadca6282f7dfac417f8cea648ca5f19d2b]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [ref:cdaf82fd4c021fa0a891dedd7d85fff3402f4bef]
- **`🔌 class Claim`**: Encapsulates unique identifiers for specific references [ref:9dece997f701a6b16940bdcf42c059591db28273]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [ref:b7729088a8954b42aeaaf067fb7b5ca6c1bcaf4c]
- **`🔌 class ModuleContext`**: Encapsulates module configuration, roles, dependencies, public API, and alerts, managing their relationships and interactions [ref:57c50e47613af2b850d343a7c4c81ddf00f58dfa]
- **`🔌 🔌 Claim.id`**: Generates unique identifier by combining text, reference, source module using SHA-1 hashing algorithm [ref:b9a17c01e7f031dbffc15da4bbead346c62e0be7]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds alert to alerts list [ref:5a75ac8d811175f2bec87ea7647b4a15846a35c7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Updates dependency context with full text containing explanation and claim IDs [ref:c455726b92f26b703e9fb2addfb0b1f5b70a9d3b]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds dependent context for a module path by combining explanation and placeholders from supporting claims, creating a new entry in key_dependents dictionary with text and claim IDs [ref:1020abc6096f2550ee34000a7542f66f71756cfa]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds public API entry by combining description and supporting claims into full text [ref:dc711f2a7ff4c734d1fffedfb2e951e43c7c3253]
- **`🔌 🔌 ModuleContext.set_module_role`**: Adds placeholders to text using supporting claims, then creates module role from modified text [ref:98d3fd5c99e11543a7fc88b5e8ead17ba17b2535]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `b9a17c`: Generates unique identifier by combining text, reference, source module using SHA-1 hashing algorithm _(Source: 🔌 Claim.id)_
> 🆔 `9dece9`: Encapsulates unique identifiers for specific references _(Source: class Claim)_
> 🆔 `b77290`: Data container for GroundedText records. _(Source: class GroundedText)_
> 🆔 `cdaf82`: Data container for Alert records. _(Source: class Alert)_
> 🆔 `98d3fd`: Adds placeholders to text using supporting claims, then creates module role from modified text _(Source: 🔌 ModuleContext.set_module_role)_
> 🆔 `c45572`: Updates dependency context with full text containing explanation and claim IDs _(Source: 🔌 ModuleContext.add_dependency_context)_
> 🆔 `1020ab`: Adds dependent context for a module path by combining explanation and placeholders from supporting claims, creating a new entry in key_dependents dictionary with text and claim IDs _(Source: 🔌 ModuleContext.add_dependent_context)_
> 🆔 `dc711f`: Adds public API entry by combining description and supporting claims into full text _(Source: 🔌 ModuleContext.add_public_api_entry)_
> 🆔 `5a75ac`: Adds alert to alerts list _(Source: 🔌 ModuleContext.add_alert)_
> 🆔 `57c50e`: Encapsulates module configuration, roles, dependencies, public API, and alerts, managing their relationships and interactions _(Source: class ModuleContext)_
> 🆔 `e2197e`: Orchestrates parsing of upstream logic using dataclasses, hashlib, re, typing _(Source: Synthesis)_
</details>

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` Processes input, verifies claims, and validates adherence to specified constraints using LLM integration

**Impact Analysis:** Changes to this module will affect: agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, module_contextualizer.py [ref:e978f117a7e8bad87624c8a6b19f0551328729da]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Creates a set containing words that should not be used in certain contexts [ref:4ea90f5b2214f8ebe511c02e1aeb8f968ff5f953]
- **`🔌 class SemanticGatekeeper`**: Provides feedback, verifies code correctness, critiques content quality, parses JSON safely, processes entire JSON string for analysis [ref:158ee76128c7df543d97fab66e1ece2da1424185]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: Constructs a prompt for LLM to generate JSON output [ref:18e04b3b1c812a78cf4e1e6318bdfe16a58aa042]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py`: Imports and utilizes the model identifier granite4 3b from a specified module within semantic_gatekeeper.py. [ref:55cde3909f2348a4e45d4fd028ee2823bf4db59e]
- **`llm_util.py`**: Uses `llm_util.py`: Calls process_user_input function from the imported module to handle user input and exceptions before sending to LLM model chat_llm.. [ref:d5603d8065d27c785d6cdbc695b7a77253ee0edb]

### 👥 Used By (Downstream)
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_critic.py`**
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `4ea90f`: Creates a set containing words that should not be used in certain contexts _(Source: BANNED_ADJECTIVES)_
> 🆔 `18e04b`: Constructs a prompt for LLM to generate JSON output _(Source: 🔌 SemanticGatekeeper.execute_with_feedback)_
> 🆔 `158ee7`: Provides feedback, verifies code correctness, critiques content quality, parses JSON safely, processes entire JSON string for analysis _(Source: class SemanticGatekeeper)_
> 🆔 `55cde3`: Uses `agent_config.py`: Imports and utilizes the model identifier granite4 3b from a specified module within semantic_gatekeeper.py. _(Source: Import agent_config.py)_
> 🆔 `d5603d`: Uses `llm_util.py`: Calls process_user_input function from the imported module to handle user input and exceptions before sending to LLM model chat_llm.. _(Source: Import llm_util.py)_
> 🆔 `e978f1`: Processes input, verifies claims, and validates adherence to specified constraints using LLM integration _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py [ref:449512ed434b04a04a62f74801a3cff91b4129f6]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Assigns an integer value to CONTEXT_LIMIT representing maximum context length [ref:44848c805cc44da4df28cc91ad8773ff15f2784d]
- **`🔌 DEFAULT_MODEL`**: Assigns string literal value granite4 3b to global variable specifying model identifier [ref:eb9a7060a5cc91be19cd3b95b62ca2a9758aa803]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `eb9a70`: Assigns string literal value granite4 3b to global variable specifying model identifier _(Source: DEFAULT_MODEL)_
> 🆔 `44848c`: Assigns an integer value to CONTEXT_LIMIT representing maximum context length _(Source: CONTEXT_LIMIT)_
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
**Role:** The module `report_renderer.py` Manages rendering process for generating reports based on project context data, delegating parsing tasks to upstream logic in summary_models.py

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [ref:379993bd81aea67804ca8193feb8de573107f345]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Manages the rendering process for generating reports based on project context data [ref:b02a8f22f85511e93914b96b19899c4742ca999c]
- **`🔌 🔌 ReportRenderer.render`**: Generates report file by rendering project context map details [ref:37eb20ac6a855a2938905687cdc6ca9481dea6ea]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Uses `summary_models.py`: report_renderer.py imports summary_models and uses GroundedText and Alert records to render reports based on module configuration and alerts.. [ref:ffe13db907f569bbda5bbd881f65978875654ce2]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `37eb20`: Generates report file by rendering project context map details _(Source: 🔌 ReportRenderer.render)_
> 🆔 `b02a8f`: Manages the rendering process for generating reports based on project context data _(Source: class ReportRenderer)_
> 🆔 `ffe13d`: Uses `summary_models.py`: report_renderer.py imports summary_models and uses GroundedText and Alert records to render reports based on module configuration and alerts.. _(Source: Import summary_models.py)_
> 🆔 `379993`: Manages rendering process for generating reports based on project context data, delegating parsing tasks to upstream logic in summary_models.py _(Source: Synthesis)_
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
**Role:** The module `map_critic.py` Analyzes project map content, extracting modules and critiquing each for instructions

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:9b5774b3bd49fc92c71af4d6a460692a4e19227d]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Organizes and maintains project structure information (⚠️ The code defines a MapCritic class to parse and critique project map content. It organizes information into modules by parsing the input string based on specific patterns. However, it does not explicitly maintain or update this structured information over time, nor does it provide mechanisms for organizing and maintaining the project structure beyond the initial parsing.) [ref:329698e2afc46774677e79c0d398512a38fbff90]
- **`🔌 🔌 MapCritic.critique`**: Parses project map content to extract modules, analyzes each module for instructions, and appends critiques as tuples to a list. [ref:290c68e6a40b75a1b29b51053ced3c49a8db39ce]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to provide feedback and verify code correctness on the content generated by LLM. [ref:e1179ca7669718bab220181750dd48493ea67040]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `290c68`: Parses project map content to extract modules, analyzes each module for instructions, and appends critiques as tuples to a list. _(Source: 🔌 MapCritic.critique)_
> 🆔 `329698`: Organizes and maintains project structure information (⚠️ The code defines a MapCritic class to parse and critique project map content. It organizes information into modules by parsing the input string based on specific patterns. However, it does not explicitly maintain or update this structured information over time, nor does it provide mechanisms for organizing and maintaining the project structure beyond the initial parsing.) _(Source: class MapCritic)_
> 🆔 `e1179c`: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to provide feedback and verify code correctness on the content generated by LLM. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `9b5774`: Analyzes project map content, extracting modules and critiquing each for instructions _(Source: Synthesis)_
</details>

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` Analyzes module components, generates skeleton code, orchestrates data lifecycle through ModuleContext managing upstream logic interactions securely

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:b712dd441800bbea5e063e0cedd0f4c7158da36b]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes module components, generates skeleton code, processes method summaries for structural role description [ref:b8d1109b50aa69c6a386b734ee78f70c0382e3f0]
- **`🔌 class SkeletonTransformer`**: Transforms and modifies code nodes by appending ellipsis expressions [ref:43c1630ba2fccc93a85c5ce9fb3872ea239aad3b]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes module components and generates working memory summary [ref:c485709f6a9d03e82be125f638581bc4d2da47c8]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Transforms source code into skeleton form by replacing function definitions with ellipsis, removing class docstrings, and appending pass statement if needed [ref:9e69a754aa276f24ced4e0d2f28a102dfa31c74c]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Replaces body content of async function definition node with ellipsis constant expression [ref:65098ccbf8ab2b430c1b3c5a9b2cd7595af3250d]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from class definition node and appends Pass if body becomes empty [ref:752f74ae95c41dd999e24a07a4687cc095f18c73]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Modifies function definition by appending ellipsis expression to its body [ref:ddce36e489339f94f6dc95cb4e0c989ab08413d9]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to create set of restricted words and generate prompt for LLM output. [ref:ac19e3ae2af474c916d75ff1e2319619d7a8c72f]
- **`summary_models.py`**: Uses `summary_models.py`: Imports and utilizes GroundedText and Alert records as Data containers to analyze component-related data, encapsulating module configuration, roles, dependencies, public API, and alerts.. [ref:a48d440d8d1eedfe303d0d55821efa15b436b73c]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c48570`: Analyzes module components and generates working memory summary _(Source: 🔌 ComponentAnalyst.analyze_components)_
> 🆔 `9e69a7`: Transforms source code into skeleton form by replacing function definitions with ellipsis, removing class docstrings, and appending pass statement if needed _(Source: 🔌 ComponentAnalyst.generate_module_skeleton)_
> 🆔 `b8d110`: Analyzes module components, generates skeleton code, processes method summaries for structural role description _(Source: class ComponentAnalyst)_
> 🆔 `ddce36`: Modifies function definition by appending ellipsis expression to its body _(Source: 🔌 SkeletonTransformer.visit_FunctionDef)_
> 🆔 `65098c`: Replaces body content of async function definition node with ellipsis constant expression _(Source: 🔌 SkeletonTransformer.visit_AsyncFunctionDef)_
> 🆔 `752f74`: Removes docstring from class definition node and appends Pass if body becomes empty _(Source: 🔌 SkeletonTransformer.visit_ClassDef)_
> 🆔 `43c163`: Transforms and modifies code nodes by appending ellipsis expressions _(Source: class SkeletonTransformer)_
> 🆔 `ac19e3`: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to create set of restricted words and generate prompt for LLM output. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `a48d44`: Uses `summary_models.py`: Imports and utilizes GroundedText and Alert records as Data containers to analyze component-related data, encapsulating module configuration, roles, dependencies, public API, and alerts.. _(Source: Import summary_models.py)_
> 🆔 `b712dd`: Analyzes module components, generates skeleton code, orchestrates data lifecycle through ModuleContext managing upstream logic interactions securely _(Source: Synthesis)_
</details>

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` Manages dependencies by initializing gatekeeper and analyzing usage context, encapsulating module configuration, roles, dependencies, public API, and alerts while interacting with semantic gatekeeper for feedback and validation.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [ref:0aaf12a46af6c4798bbe941e0c657dc1a37695c1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Manages dependencies by initializing gatekeeper and analyzing usage context [ref:40726de568d43959f31f00986c790dc6fdde8368]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes dependency imports to determine usage context [ref:0149497ae1fc2fa7d04a935969c5558b8769ec31]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Imports `semantic_gatekeeper.py`. [ref:c79af809dfdd33981d6ccc5f4b443df100463ad7]
- **`summary_models.py`**: Uses `summary_models.py`: Imports a module and utilizes its GroundedText, Alert records along with encapsulated configuration for managing relationships and interactions. [ref:a41b799e09400e650e133ff6b8e99893fd64e0f0]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `014949`: Analyzes dependency imports to determine usage context _(Source: 🔌 DependencyAnalyst.analyze_dependencies)_
> 🆔 `40726d`: Manages dependencies by initializing gatekeeper and analyzing usage context _(Source: class DependencyAnalyst)_
> 🆔 `c79af8`: Imports `semantic_gatekeeper.py`. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `a41b79`: Uses `summary_models.py`: Imports a module and utilizes its GroundedText, Alert records along with encapsulated configuration for managing relationships and interactions. _(Source: Import summary_models.py)_
> 🆔 `0aaf12`: Manages dependencies by initializing gatekeeper and analyzing usage context, encapsulating module configuration, roles, dependencies, public API, and alerts while interacting with semantic gatekeeper for feedback and validation. _(Source: Synthesis)_
</details>

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` Analyzes module context, synthesizes system-wide implications, and communicates relevant details through structured data containers like ModuleContext, Alert, and GroundedText.

**Impact Analysis:** Changes to this module will affect: agent_util.py [ref:f72abf3722c4056413b80b85626bfa5d646b405f]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Analyzes module structure, gathers upstream knowledge, synthesizes system-wide implications, and communicates relevant details [ref:3181460d09fa2dd30dcd0a3d97158fc56c238dec]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyzes module context, analyzes components and dependencies, performs systemic synthesis, and passes alerts based on critique instruction [ref:c3712ae15f4d5643ccba31340a0388a447c28e2f]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper function to create set of restricted words and generate prompt for LLM. [ref:9569bd2d9adcfb28234c3034f337cb1aaee2f6ab]
- **`module_classifier.py`**: Uses `module_classifier.py`: Calls ModuleClassifier to determine module archetype based on name, source code, entities, dependencies, functions, classes, and global variables.. [ref:6ee15f145e3960d52ec318aadb98aedd43737174]
- **`component_analyst.py`**: Uses `component_analyst.py`: Replaces body content of async function definition node with ellipsis constant expression; Calls ComponentAnalyst class to analyze module components and generate working memory summary. [ref:7ddd7d936efec2f605721f343893c82d24778b43]
- **`summary_models.py`**: Uses `summary_models.py`: Imports and utilizes GroundedText records for context within the module's operations.. [ref:0d2d3b40a12eaec31ffa533a7f201c4d0ba0d505]
- **`dependency_analyst.py`**: Imports `dependency_analyst.py`. [ref:a60f13a29ab6e9b23f6f55625fab16a89aa01575]

### 👥 Used By (Downstream)
- **`agent_util.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c3712a`: Analyzes module context, analyzes components and dependencies, performs systemic synthesis, and passes alerts based on critique instruction _(Source: 🔌 ModuleContextualizer.contextualize_module)_
> 🆔 `318146`: Analyzes module structure, gathers upstream knowledge, synthesizes system-wide implications, and communicates relevant details _(Source: class ModuleContextualizer)_
> 🆔 `9569bd`: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper function to create set of restricted words and generate prompt for LLM. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `6ee15f`: Uses `module_classifier.py`: Calls ModuleClassifier to determine module archetype based on name, source code, entities, dependencies, functions, classes, and global variables.. _(Source: Import module_classifier.py)_
> 🆔 `7ddd7d`: Uses `component_analyst.py`: Replaces body content of async function definition node with ellipsis constant expression; Calls ComponentAnalyst class to analyze module components and generate working memory summary. _(Source: Import component_analyst.py)_
> 🆔 `0d2d3b`: Uses `summary_models.py`: Imports and utilizes GroundedText records for context within the module's operations.. _(Source: Import summary_models.py)_
> 🆔 `a60f13`: Imports `dependency_analyst.py`. _(Source: Import dependency_analyst.py)_
> 🆔 `f72abf`: Analyzes module context, synthesizes system-wide implications, and communicates relevant details through structured data containers like ModuleContext, Alert, and GroundedText. _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` Orchestrates interaction between modules and state, managing alerts and summarizing context for project processing and execution

**Impact Analysis:** Changes to this module will affect: agent_core.py [ref:8a0dae87bced7f6c5282d58e968e5b3c14c8eeef]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Declares ProjectGraph as a dictionary mapping string keys to any values [ref:c4aec07bed5e78a3f5531df59eb03fad2c07c3b2]
- **`🔌 class ProjectSummarizer`**: Organizes, manages state, and computes processing order for project modules [ref:0bed41fd63af92013d43033f69579da30aefb6f0]
- **`🔌 project_pulse`**: Analyzes project structure and generates module contexts [ref:31e4a97f2958cb8511b54d24c8f5d837295e2f64]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Iteratively refines module contexts based on critiques and dependencies [ref:8587166e44c64399fc1a658825b9d6be9fb4b980]
- **`🔒 _create_module_context`**: Generates module context by contextualizing module using contextualizer [ref:14d2bf2e1bf40809bb8292e5c51e124306d026a9]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to prevent unwanted words and provide feedback. [ref:73654fbb5e676a4a3601c7aeef8e14d9e57b6927]
- **`module_contextualizer.py`**: Uses `module_contextualizer.py`: agent_util.py calls ModuleContextualizer to analyze module context and perform systemic synthesis.. [ref:6197051baddd9f09b9fb783d97d3fc229b79f5e6]
- **`report_renderer.py`**: Imports `report_renderer.py`. [ref:1c31637324d047bd4567e80499f5ff5619ad59d7]
- **`graph_analyzer.py`**: Uses `graph_analyzer.py`: imports a module and utilizes the interaction values captured for named function nodes; Calls GraphAnalyzer. [ref:e578d6c4685abcc57d449eea047bd4d4bf633515]
- **`map_critic.py`**: Imports `map_critic.py`. [ref:c54d03461bdbe40229c63bab2ba6ba1632087818]
- **`summary_models.py`**: Imports `summary_models.py`. [ref:0e8ce6fc6ba415b8374fa6adab75144ac1d3ad1b]

### 👥 Used By (Downstream)
- **`agent_core.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `c4aec0`: Declares ProjectGraph as a dictionary mapping string keys to any values _(Source: ProjectGraph)_
> 🆔 `14d2bf`: Generates module context by contextualizing module using contextualizer _(Source: _create_module_context)_
> 🆔 `31e4a9`: Analyzes project structure and generates module contexts _(Source: project_pulse)_
> 🆔 `858716`: Iteratively refines module contexts based on critiques and dependencies _(Source: 🔌 ProjectSummarizer.generate_contexts)_
> 🆔 `0bed41`: Organizes, manages state, and computes processing order for project modules _(Source: class ProjectSummarizer)_
> 🆔 `73654f`: Uses `semantic_gatekeeper.py`: Calls SemanticGatekeeper to prevent unwanted words and provide feedback. _(Source: Import semantic_gatekeeper.py)_
> 🆔 `619705`: Uses `module_contextualizer.py`: agent_util.py calls ModuleContextualizer to analyze module context and perform systemic synthesis.. _(Source: Import module_contextualizer.py)_
> 🆔 `1c3163`: Imports `report_renderer.py`. _(Source: Import report_renderer.py)_
> 🆔 `e578d6`: Uses `graph_analyzer.py`: imports a module and utilizes the interaction values captured for named function nodes; Calls GraphAnalyzer. _(Source: Import graph_analyzer.py)_
> 🆔 `c54d03`: Imports `map_critic.py`. _(Source: Import map_critic.py)_
> 🆔 `0e8ce6`: Imports `summary_models.py`. _(Source: Import summary_models.py)_
> 🆔 `8a0dae`: Orchestrates interaction between modules and state, managing alerts and summarizing context for project processing and execution _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` Orchestrates the crawling process by running the crawler agent, managing configurations, and integrating memory interfaces for context management and query operations while processing project-specific models and contexts.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [ref:640c95866728ea061b2a7cdd10430e0ac29a369a]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Manages execution flow and configuration parameters for project pulse crawler [ref:20eb846c5cb053788249cbba999f53dee851c3cc]
- **`🔌 🔌 CrawlerAgent.run`**: Prints running message then runs project pulse crawler [ref:1f056a69f4471fd20dd7851956b874b40defcbf7]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Uses `agent_config.py`: Imports and utilizes a specified context limit value defined elsewhere. [ref:ece0433481131669d8e40c902853251963dcc5d6]
- **`llm_util.py`**: Imports `llm_util.py`. [ref:8154323f40a1ca06e29bbcd9cd792149a6082cb5]
- **`report_renderer.py`**: Uses `report_renderer.py`: agent_core.py calls ReportRenderer to generate report file by rendering project context map details and managing the rendering process for reports based on project context data.. [ref:f271c82f25ba50cb1a113605bd07ad32a32da274]
- **`agent_util.py`**: Imports `agent_util.py`. [ref:d95bb586808b3d8220d8d19d3d2bfaeee1fe9349]
- **`memory_core.py`**: Uses `memory_core.py`: The module accesses functions/classes to generate unique identifiers, query stored information, update metadata with current context, manage deletion of infrequently used data based on usefulness metrics, and organize retrieval processes using ChromaMemory.. [ref:4e9589750237e8a8f18ff3c302087ef9ca157085]
- **`summary_models.py`**: Uses `summary_models.py`: Imports and uses the GroundedText records data container to store processed text information in its logic flow.. [ref:8801fcef8ad4cb99587ba92a666f290935861cb1]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `1f056a`: Prints running message then runs project pulse crawler _(Source: 🔌 CrawlerAgent.run)_
> 🆔 `20eb84`: Manages execution flow and configuration parameters for project pulse crawler _(Source: class CrawlerAgent)_
> 🆔 `ece043`: Uses `agent_config.py`: Imports and utilizes a specified context limit value defined elsewhere. _(Source: Import agent_config.py)_
> 🆔 `815432`: Imports `llm_util.py`. _(Source: Import llm_util.py)_
> 🆔 `f271c8`: Uses `report_renderer.py`: agent_core.py calls ReportRenderer to generate report file by rendering project context map details and managing the rendering process for reports based on project context data.. _(Source: Import report_renderer.py)_
> 🆔 `d95bb5`: Imports `agent_util.py`. _(Source: Import agent_util.py)_
> 🆔 `4e9589`: Uses `memory_core.py`: The module accesses functions/classes to generate unique identifiers, query stored information, update metadata with current context, manage deletion of infrequently used data based on usefulness metrics, and organize retrieval processes using ChromaMemory.. _(Source: Import memory_core.py)_
> 🆔 `8801fc`: Uses `summary_models.py`: Imports and uses the GroundedText records data container to store processed text information in its logic flow.. _(Source: Import summary_models.py)_
> 🆔 `640c95`: Orchestrates the crawling process by running the crawler agent, managing configurations, and integrating memory interfaces for context management and query operations while processing project-specific models and contexts. _(Source: Synthesis)_
</details>

---
## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` Orchestrates crawling process by parsing command line, delegating execution to CrawlerAgent, managing project pulse crawler flow [ref:ad351710369dcfe685d6221d1eaab88e3324e7e3]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 args`**: Parses command-line arguments using ArgumentParser and stores them in args variable for later use in main function [ref:afcb13ef5b75e551b14eb30302ee6a54ff063460]
- **`🔌 goal`**: Retrieves the goal argument parsed from command line arguments [ref:3100ea6c8cbe1088f002afcc1a3c821e93796e64]
- **`🔌 main`**: Searches target folder for _main.py files, creates CrawlerAgent instance, runs agent, logs completion [ref:f8b37167fa3e23ff696c733dd5ecd515a8e92a6a]
- **`🔌 parser`**: Creates an argument parser to handle command-line input options and descriptions for subsequent processing in main function [ref:703b919717986bdf598fa18e0b93b6c557a39964]
- **`🔌 result`**: Calls main function with goal and target folder arguments to process specified task. [ref:b2c138daae17eedc462e9180be0e32d36b4782bb]
- **`🔌 target_folder`**: Assigns the target folder argument to a variable for use in subsequent operations [ref:e000780c22c5dd0a254786a092c2b0457ad56ec9]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Uses `agent_core.py`: Imports and leverages Data to control project pulse crawler operations; Calls the specified CrawlerAgent class.. [ref:ca5f54d99f4f8fa2dd4618a35abe21b7a86133b5]

<details><summary><i>View Verification Claims</i></summary>

> 🆔 `703b91`: Creates an argument parser to handle command-line input options and descriptions for subsequent processing in main function _(Source: parser)_
> 🆔 `afcb13`: Parses command-line arguments using ArgumentParser and stores them in args variable for later use in main function _(Source: args)_
> 🆔 `3100ea`: Retrieves the goal argument parsed from command line arguments _(Source: goal)_
> 🆔 `e00078`: Assigns the target folder argument to a variable for use in subsequent operations _(Source: target_folder)_
> 🆔 `b2c138`: Calls main function with goal and target folder arguments to process specified task. _(Source: result)_
> 🆔 `f8b371`: Searches target folder for _main.py files, creates CrawlerAgent instance, runs agent, logs completion _(Source: main)_
> 🆔 `ca5f54`: Uses `agent_core.py`: Imports and leverages Data to control project pulse crawler operations; Calls the specified CrawlerAgent class.. _(Source: Import agent_core.py)_
> 🆔 `ad3517`: Orchestrates crawling process by parsing command line, delegating execution to CrawlerAgent, managing project pulse crawler flow _(Source: Synthesis)_
</details>

---