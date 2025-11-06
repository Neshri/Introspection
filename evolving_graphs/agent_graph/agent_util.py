import logging
import os
from .graph_analyzer import GraphAnalyzer
from .llm_util import chat_llm
from .agent_config import DEFAULT_MODEL

def _format_entities_for_prompt(entities: dict) -> str:
    # This helper can now live inside agent_util as it's only used here.
    lines = []
    if not entities.get('functions') and not entities.get('classes'): return "No public API defined."
    if entities.get('functions'):
        lines.append("Public Functions:")
        for func in entities['functions']:
            unimplemented_tag = " # UNIMPLEMENTED" if func['is_unimplemented'] else ""
            lines.append(f"- `{func['signature']}`{unimplemented_tag}")
    if entities.get('classes'):
        lines.append("\nClasses:")
        for class_name, methods in entities['classes'].items():
            lines.append(f"- class {class_name}:")
            for method in methods:
                unimplemented_tag = " # UNIMPLEMENTED" if method['is_unimplemented'] else ""
                lines.append(f"  - `{method['signature']}`{unimplemented_tag}")
    return "\n".join(lines)

def _format_interactions_for_prompt(interactions: list) -> str:
    if not interactions: return "None."
    return "\n".join([f"- Context `{call['context']}` uses symbol `{call['target_module']}.{call['symbol']}`" for call in interactions])

def project_pulse(target_file_path: str) -> dict:
    """
    Generates a diagnostic, contextually consistent summary for all modules in a dependency graph.
    """
    if not os.path.isfile(target_file_path):
        logging.error(f"Error: Path '{target_file_path}' is not a valid file.")
        return {}

    # --- PASS 1: DETERMINISTIC STATIC ANALYSIS ---
    analyzer = GraphAnalyzer(target_file_path)
    graph = analyzer.analyze()
    
    # --- PASS 2: CONTEXTUAL PROSE GENERATION ---
    logging.info("--- Starting Pass 2: Contextual Prose Generation ---")
    
    processed_modules = list(analyzer.visited)
    module_summaries = {}

    for path in processed_modules:
        node = graph.get(path)
        if not node or 'error' in node:
            file_name = os.path.basename(path) if node else "Unknown"
            error_message = node['error'] if node and 'error' in node else "Node not found in graph."
            module_summaries[file_name] = f"### Summary for `{file_name}`\n\n**Error:** Failed during static analysis: {error_message}"
            continue
        
        file_name = node['file_name']
        try:
            # Build the factual context string from our reliable analysis
            dependencies = [graph.get(p) for p in node.get('dependencies', [])]
            dependents = [graph.get(p) for p in node.get('dependents', [])]
            deps_str = "\n".join([f"- `{d['file_name']}`" for d in dependencies if d]) or "None."
            dependents_str = "\n".join([f"- `{d['file_name']}`" for d in dependents if d]) or "None."

            context_string = f"""
**Full Source Code of `{file_name}`:**
```python
{node.get('source_code', '')}
```

**Statically Analyzed Public API:**
{_format_entities_for_prompt(node.get('entities', {}))}

**Verified Cross-Module Interactions:**
{_format_interactions_for_prompt(node.get('interactions', []))}

**It USES these modules (Dependencies):**
{deps_str}

**It is USED BY these modules (Dependents):**
{dependents_str}
"""
            
            # Build the deterministic list of issues
            statically_detected_issues = []
            for func in node.get('entities', {}).get('functions', []):
                if func['is_unimplemented']: statically_detected_issues.append(f"Function `{func['signature']}` is unimplemented.")
            for class_name, methods in node.get('entities', {}).get('classes', {}).items():
                for method in methods:
                    if method['is_unimplemented']: statically_detected_issues.append(f"Method `{class_name}.{method['signature']}` is unimplemented.")
            for todo in node.get('todos', []):
                statically_detected_issues.append(f"TODO comment found: '{todo.strip()}'")

            # The final, simple prompt
            prompt = f"""
You are an expert software architect. Your task is to synthesize all available information into a single, comprehensive, and accurate summary for the module `{file_name}`.

**CONTEXT:**
{context_string}

**Statically Detected Issues:**
{("- " + "\n- ".join(statically_detected_issues)) if statically_detected_issues else "None."}

**INSTRUCTIONS:**
Based on all the context above, produce a final summary in the following Markdown format.
- Your primary focus is explaining this module's role in the context of the larger system.
- For "Potential Issues Detected", ONLY report the "Statically Detected Issues" provided above. Do not invent problems.

**OUTPUT FORMAT:**
### Summary for `{file_name}`
**Core Responsibility:** (A single sentence that defines the module's primary purpose.)

**Dependency Interactions:**
- **`dependency_name.py`**: (A short, specific explanation of HOW and WHY this module uses this dependency.)

**Service to Dependents:**
(A short explanation of the service or functionality this module provides to the modules that import it.)

**Potential Issues Detected:**
- (A bulleted list of the statically detected issues.)
"""
            logging.info(f"[ProseGenerator] Generating summary for: {file_name}")
            final_summary = chat_llm(DEFAULT_MODEL, prompt)
            module_summaries[file_name] = final_summary
        except Exception as e:
            logging.error(f"Failed to generate summary for {file_name}: {e}", exc_info=True)
            module_summaries[file_name] = f"### Summary for `{file_name}`\n\n**Error:** An unexpected error occurred during prose generation."
            
    return module_summaries