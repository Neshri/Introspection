import logging
import os
import re
from .graph_analyzer import GraphAnalyzer
from .llm_util import chat_llm
from .agent_config import DEFAULT_MODEL
from .auditor_agent import run_duplication_auditor, run_completeness_auditor, run_service_auditor, run_dependency_grounding_auditor, run_grounding_auditor
from .writer_agent import generate_role_summary, generate_core_summary, generate_service_summary, generate_deps_summary

def _format_entities_for_prompt(entities: dict) -> str:
    """Formats the statically analyzed entities into a markdown string for the LLM prompt."""
    lines = []
    if not entities.get('functions') and not entities.get('classes'):
        return "No public API defined."
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

def _is_simple_constants_file(node: dict) -> bool:
    """Deterministically checks if a module is a simple constants/config file."""
    # A file is simple if it has no dependencies, no interactions, and no defined functions or classes.
    has_dependencies = bool(node.get('dependencies'))
    has_interactions = bool(node.get('interactions'))
    has_entities = bool(node.get('entities', {}).get('functions') or node.get('entities', {}).get('classes'))
    
    return not has_dependencies and not has_interactions and not has_entities

def _generate_simple_summary(file_name: str) -> str:
    """Generates a deterministic, template-based summary for simple config/constants files."""
    logging.info(f"[Orchestrator] Generating deterministic summary for simple file: {file_name}")
    return f"""### Summary for `{file_name}`
#### System-Level Role
This module serves as a configuration or constants file. It defines static values that are used by other modules in the project.
#### Core Responsibility
The primary purpose of this file is to centralize and define project-wide constants.
#### Dependency Interactions
This module has no direct interactions with other project modules or external libraries.
#### Service to Dependents
This module provides no callable services to dependents; it only provides constant values.
#### Potential Issues Detected
- None.
"""

def _summarize_module_recursively(path: str, graph: dict, module_summaries: dict):
    """
    Orchestrates the generation and auditing of a module summary.
    """
    if path in module_summaries:
        return

    node = graph.get(path)
    if not node or 'error' in node:
        file_name = os.path.basename(path)
        module_summaries[file_name] = f"### Summary for `{file_name}`\n\n**Error:** Failed during static analysis: {node.get('error', 'Unknown error')}"
        return
    
    for dep_path in node.get('dependencies', []):
        _summarize_module_recursively(dep_path, graph, module_summaries)

    file_name = node['file_name']
    
    # --- DETERMINISTIC PATH FOR SIMPLE FILES ---
    if _is_simple_constants_file(node):
        module_summaries[file_name] = _generate_simple_summary(file_name)
        return

    # --- LLM-BASED PATH FOR COMPLEX FILES ---
    logging.info(f"[Orchestrator] Generating LLM-based summary for: {file_name}")
    try:
        source_code = node.get('source_code', '')
        public_api = _format_entities_for_prompt(node.get('entities', {}))
        
        dependencies = [graph.get(p) for p in node.get('dependencies', [])]
        dependency_summaries_list = [
            f"**Summary of `{d['file_name']}`:**\n{module_summaries.get(d['file_name'], 'Summary not available.')}"
            for d in dependencies if d
        ]
        dependency_summaries_str = "\n---\n".join(dependency_summaries_list)

        source_code_context = f"**Full Source Code of `{file_name}`:**\n```python\n{source_code}\n```"
        api_context = f"**Statically Analyzed Public API of `{file_name}`:**\n{public_api}"
        
        role_summary = generate_role_summary(file_name, dependency_summaries_str, api_context)
        core_summary = generate_core_summary(file_name, source_code_context)
        service_summary = generate_service_summary(file_name, api_context)
        deps_summary = generate_deps_summary(node.get('interactions', []), node.get('external_imports', set()))

        MAX_ATTEMPTS = 3
        for attempt in range(MAX_ATTEMPTS):
            statically_detected_issues = [f"- {issue}" for issue in (
                [f"Function `{func['signature']}` is unimplemented." for func in node.get('entities', {}).get('functions', []) if func['is_unimplemented']] +
                [f"Method `{cls}.{m['signature']}` is unimplemented." for cls, meths in node.get('entities', {}).get('classes', {}).items() for m in meths if m['is_unimplemented']] +
                [f"TODO comment found: '{todo.strip()}'" for todo in node.get('todos', [])]
            )] or ["- None."]
            issues_summary = "\n".join(statically_detected_issues)
            
            draft_summary = f"### Summary for `{file_name}`\n#### System-Level Role\n{role_summary}\n#### Core Responsibility\n{core_summary}\n#### Dependency Interactions\n{deps_summary}\n#### Service to Dependents\n{service_summary}\n#### Potential Issues Detected\n{issues_summary}"

            if run_duplication_auditor(draft_summary) or run_completeness_auditor(draft_summary):
                raise Exception("Fatal draft error: Duplication or missing sections detected.")
            
            service_flawed, service_feedback = run_service_auditor(file_name, draft_summary, public_api)
            deps_grounding_flawed, deps_grounding_feedback = run_dependency_grounding_auditor(
                draft_summary, node.get('interactions', []), node.get('external_imports', set())
            )
            
            prose_grounding_flawed = False
            prose_grounding_feedback = ""
            if not service_flawed and not deps_grounding_flawed:
                prose_text = f"#### System-Level Role\n{role_summary}\n#### Core Responsibility\n{core_summary}"
                prose_grounding_flawed, prose_grounding_feedback = run_grounding_auditor(file_name, prose_text, source_code)

            # **CORRECTED CONTROL FLOW LOGIC**
            if not service_flawed and not deps_grounding_flawed and not prose_grounding_flawed:
                logging.info(f"--> Summary for {file_name}: All auditors passed on attempt {attempt + 1}.")
                module_summaries[file_name] = draft_summary.strip()
                return

            # --- REFINEMENT ACTIONS ---
            if prose_grounding_flawed:
                logging.warning(f"--> {file_name} | Attempt {attempt+1} | Prose Grounding Auditor FAILED: {prose_grounding_feedback}")
                role_summary = generate_role_summary(file_name, dependency_summaries_str, api_context)
                core_summary = generate_core_summary(file_name, source_code_context)
            
            if service_flawed:
                logging.warning(f"--> {file_name} | Attempt {attempt+1} | Service Auditor FAILED: {service_feedback}")
                prompt_service_refined = f"An auditor found a flaw in a previous draft of the 'Service to Dependents' section. Please fix it.\n\nAUDITOR FEEDBACK: {service_feedback}\n\n**Original Task:**\nYou are a software architect. Based ONLY on the Public API of `{file_name}`, create a bulleted list describing the service it provides.\n{api_context}\n\n**Revised Service to Dependents:**"
                service_summary = chat_llm(DEFAULT_MODEL, prompt_service_refined)

            if deps_grounding_flawed:
                logging.warning(f"--> {file_name} | Attempt {attempt+1} | Dependency Grounding FAILED: {deps_grounding_feedback}")
                deps_summary = generate_deps_summary(node.get('interactions', []), node.get('external_imports', set()))

        raise Exception(f"Failed to generate a valid summary for {file_name} after {MAX_ATTEMPTS} attempts.")

    except Exception as e:
        logging.error(f"Failed to generate a valid summary for {file_name}: {e}", exc_info=False)
        module_summaries[file_name] = f"### Summary for `{file_name}`\n\n**Error:** {e}"


def project_pulse(target_file_path: str) -> dict:
    """
    Analyzes a Python project starting from a target file, creates a dependency graph,
    and generates a summary for each module in the project.
    """
    if not os.path.isfile(target_file_path):
        logging.error(f"Error: Path '{target_file_path}' is not a valid file.")
        return {}
    
    analyzer = GraphAnalyzer(target_file_path)
    graph = analyzer.analyze()
    
    module_summaries = {}
    
    # Start the recursive summarization from the entry point
    _summarize_module_recursively(os.path.abspath(target_file_path), graph, module_summaries)
    
    return module_summaries