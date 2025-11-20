import os
from typing import Dict, List
from .summary_models import ModuleContext

class ReportRenderer:
    def __init__(self, contexts: Dict[str, ModuleContext], output_file: str = "PROJECT_MAP.md"):
        self.contexts = contexts
        self.output_file = output_file

    def render(self):
        lines = ["# Project Context Map", "", f"**Total Modules:** {len(self.contexts)}", ""]
        
        # 1. Calculate Reverse Dependencies (Who uses what?)
        # We allow this to be calculated dynamically to ensure accuracy
        module_dependents: Dict[str, set] = {k: set() for k in self.contexts}
        
        for name, ctx in self.contexts.items():
            for dep_path in ctx.key_dependencies:
                # Ensure we map the dependency back to the dependent
                if dep_path in module_dependents:
                    module_dependents[dep_path].add(name)
        
        # 2. Sort by "Impact Score" (Number of Dependents)
        # Central modules (highly used) appear first
        sorted_paths = sorted(
            self.contexts.keys(), 
            key=lambda p: len(module_dependents.get(p, [])), 
            reverse=True
        )

        for path in sorted_paths:
            ctx = self.contexts[path]
            dependents = sorted(list(module_dependents.get(path, [])))
            lines.extend(self._render_module(ctx, dependents))
            lines.append("---")
        
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        print(f"Report generated: {os.path.abspath(self.output_file)}")

    def _render_module(self, ctx: ModuleContext, dependents: List[str]) -> List[str]:
        name = os.path.basename(ctx.file_path)
        lines = [f"## 📦 Module: `{name}`"]
        
        # Role
        role_text = ctx.module_role.text if ctx.module_role.text else "_No role defined._"
        lines.append(f"**Role:** {role_text}")
        lines.append("")

        # Alerts
        if ctx.alerts:
            lines.append("### 🚨 Alerts")
            for alert in ctx.alerts:
                icon = "🔴" if alert.category == "Incomplete" else "TODO" if alert.category == "TODO" else "⚠️"
                lines.append(f"- {icon} **{alert.category}**: {alert.description} `(Ref: {alert.reference})`")
            lines.append("")

        # Interface & Components
        # Renamed to reflect that it now contains internal (🔒) logic
        if ctx.public_api:
            lines.append("### 🧩 Interface & Logic")
            
            # Sort alphabetically. 
            # Unicode: 🔌 (U+1F50C) < 🔒 (U+1F512)
            # This naturally puts Public (Plug) before Private (Lock)
            sorted_entities = sorted(ctx.public_api.items(), key=lambda x: x[0])
            
            for entity, g_text in sorted_entities:
                lines.append(f"- **`{entity}`**: {g_text.text}")
            lines.append("")

        # Upstream Dependencies (What I use)
        if ctx.key_dependencies:
            lines.append("### 🔗 Uses (Upstream)")
            for dep, g_text in ctx.key_dependencies.items():
                dep_name = os.path.basename(dep)
                lines.append(f"- **`{dep_name}`**: {g_text.text}")
            lines.append("")

        # Downstream Dependents (Who uses me)
        # Vital for Impact Analysis
        if dependents:
            lines.append("### 👥 Used By (Downstream)")
            for dep_path in dependents:
                dep_name = os.path.basename(dep_path)
                lines.append(f"- **`{dep_name}`**")
            lines.append("")

        # Claims (Verification)
        if ctx.claims:
            lines.append("<details><summary><i>View Verification Claims</i></summary>")
            lines.append("")
            for cid, claim in ctx.claims.items():
                lines.append(f"> 🆔 `{cid[:6]}`: {claim.text} _(Source: {claim.reference})_")
            lines.append("</details>")
            lines.append("")

        return lines