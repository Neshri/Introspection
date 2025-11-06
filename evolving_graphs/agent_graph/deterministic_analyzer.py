
import os

class DeterministicAnalyzer:
    def format_analysis_for_prompt(self, node: dict, graph: dict) -> str:
        """Formats all statically gathered facts into a single string for the final prompt."""
        
        file_name = node['file_name']
        
        # Format API
        api_str = self._format_entities(node.get('entities', {}))

        # Format interactions
        interactions_str = self._format_interactions(node.get('interactions', []))

        # Format neighbors
        dependencies = [graph.get(p) for p in node.get('dependencies', [])]
        dependents = [graph.get(p) for p in node.get('dependents', [])]
        
        deps_str = "\n".join([f"- `{d['file_name']}`" for d in dependencies if d]) or "None."
        dependents_str = "\n".join([f"- `{d['file_name']}`" for d in dependents if d]) or "None."

        return f"""
**Full Source Code of `{file_name}`:**
```python
{node.get('source_code', '')}
```

**Statically Analyzed Public API:**
{api_str}

**Verified Cross-Module Interactions:**
{interactions_str}

**It USES these modules (Dependencies):**
{deps_str}

**It is USED BY these modules (Dependents):**
{dependents_str}
"""

    def get_entry_point_context(self, entry_point_node: dict) -> str:
        """
        NEW: Creates a high-level context string focused only on the application's entry point.
        """
        file_name = entry_point_node['file_name']
        dependencies = [os.path.basename(p) for p in entry_point_node.get('dependencies', [])]

        return f"""
**Entry Point Source Code (`{file_name}`):**
```python
{entry_point_node.get('source_code', '')}
```

**Direct Imports:**
{', '.join(dependencies) if dependencies else "None."}
"""

    def _format_entities(self, entities: dict) -> str:
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

    def _format_interactions(self, interactions: list) -> str:
        if not interactions: return "None."
        return "\n".join([f"- Context `{call['context']}` uses symbol `{call['target_module']}.{call['symbol']}`" for call in interactions])