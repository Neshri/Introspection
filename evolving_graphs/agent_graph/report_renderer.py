import os
import re
from typing import Dict, List
from .summary_models import ModuleContext

class ReportRenderer:
    def __init__(self, context_map: Dict[str, ModuleContext], output_file: str = "PROJECT_MAP.md", system_summary: str = ""):
        self.context_map = context_map
        self.output_file = output_file
        self.system_summary = system_summary
        self.claim_map = {} # Maps Claim ID -> Claim Object
        self.ref_counter = 1

    def render(self):
        """
        Organizes and writes module documentation into output file
        """
        lines = ["# Project Context Map", ""]
        
        if self.system_summary:
            lines.append("## 🏛️ System Architecture")
            lines.append(self.system_summary)
            lines.append("")
            lines.append("---")
            lines.append("")
            
        lines.append(f"**Total Modules:** {len(self.context_map)}")
        lines.append("")
        
        # 1. Calculate Reverse Dependencies (Who uses what?)
        # We allow this to be calculated dynamically to ensure accuracy
        module_dependents: Dict[str, set] = {k: set() for k in self.context_map}
        
        for name, ctx in self.context_map.items():
            for dep_path in ctx.key_dependencies:
                # Ensure we map the dependency back to the dependent
                if dep_path in module_dependents:
                    module_dependents[dep_path].add(name)
        
        # 2. Group by Archetype (Objective Truth Organization)
        # We want a logical flow: Entry -> Service -> Utility -> Data -> Config
        
        archetype_groups = {
            "Entry Point": [],
            "Service": [],
            "Utility": [],
            "Data Model": [],
            "Configuration": []
        }
        
        # Fallback for unknown archetypes
        others = []

        for path, ctx in self.context_map.items():
            arch = ctx.archetype
            if arch in archetype_groups:
                archetype_groups[arch].append(path)
            else:
                others.append(path)

        # Define the presentation order and icons
        presentation_order = [
            ("Entry Point", "🚀 Entry Points"),
            ("Service", "⚙️ Services"),
            ("Utility", "🛠️ Utilities"),
            ("Data Model", "📦 Data Models"),
            ("Configuration", "🔧 Configuration")
        ]

        # Render groups
        for arch_key, header in presentation_order:
            paths = archetype_groups.get(arch_key, [])
            if not paths: continue
            
            lines.append(f"## {header}")
            lines.append("")
            
            # Sort within group by name for consistency
            for path in sorted(paths):
                ctx = self.context_map[path]
                dependents = sorted(list(module_dependents.get(path, [])))
                lines.extend(self._render_module(ctx, dependents))
                lines.append("---")
        
        if others:
            lines.append("## 📂 Other Modules")
            lines.append("")
            for path in sorted(others):
                ctx = self.context_map[path]
                dependents = sorted(list(module_dependents.get(path, [])))
                lines.extend(self._render_module(ctx, dependents))
                lines.append("---")
        
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        print(f"Report generated: {os.path.abspath(self.output_file)}")

    def _render_module(self, ctx: ModuleContext, dependents: List[str]) -> List[str]:
        name = os.path.basename(ctx.file_path)
        lines = [f"## 📦 Module: `{name}`"]
        
        # Reference Management
        claim_map: Dict[str, int] = {}

        def replace_ref(text: str) -> str:
            def sub(match):
                ref_id = match.group(1)
                if ref_id not in claim_map:
                    claim_map[ref_id] = len(claim_map) + 1
                return f"[{claim_map[ref_id]}]"
            return re.sub(r"\[ref:([a-f0-9]+)\]", sub, text)

        # Role
        role_text = ctx.module_role.text if ctx.module_role.text else "_No role defined._"
        lines.append(f"**Role:** {replace_ref(role_text)}")
        lines.append("")

        # Alerts
        if ctx.alerts:
            lines.append("### 🚨 Alerts")
            for alert in ctx.alerts:
                icon = "🔴" if alert.category == "Incomplete" else "TODO" if alert.category == "TODO" else "⚠️"
                lines.append(f"- {icon} **{alert.category}**: {alert.description} `(Ref: {alert.reference})`")
            lines.append("")

        # Interface & Logic
        # Renamed to reflect that it now contains internal (🔒) logic
        if ctx.public_api:
            lines.append("### 🧩 Interface & Logic")
            
            # Sort alphabetically. 
            # Unicode: 🔌 (U+1F50C) < 🔒 (U+1F512)
            # This naturally puts Public (Plug) before Private (Lock)
            sorted_entities = sorted(ctx.public_api.items(), key=lambda x: x[0])
            
            for entity, g_text in sorted_entities:
                lines.append(f"- **`{entity}`**: {replace_ref(g_text.text)}")
            lines.append("")

        # Upstream Dependencies (What I use)
        if ctx.key_dependencies:
            lines.append("### 🔗 Uses (Upstream)")
            for dep, g_text in ctx.key_dependencies.items():
                dep_name = os.path.basename(dep)
                lines.append(f"- **`{dep_name}`**: {replace_ref(g_text.text)}")
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
        if claim_map:
            lines.append("<details><summary><i>View Verification Claims</i></summary>")
            lines.append("")
            
            # Sort by index
            sorted_claims = sorted(claim_map.items(), key=lambda x: x[1])
            
            for cid, index in sorted_claims:
                if cid in ctx.claims:
                    claim = ctx.claims[cid]
                    lines.append(f"> 🆔 `{cid[:6]}` [{index}]: {claim.text} _(Source: {replace_ref(claim.reference)})_")
                else:
                    lines.append(f"> 🆔 `{cid[:6]}` [{index}]: _Claim text missing_")
            
            lines.append("</details>")
            lines.append("")

        return lines