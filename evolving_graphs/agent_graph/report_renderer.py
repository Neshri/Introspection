import os
import re
from typing import Dict, List, Tuple
from .summary_models import ModuleContext

class ReportRenderer:
    def __init__(self, context_map: Dict[str, ModuleContext], output_file: str = "PROJECT_MAP.md", verification_file: str = "PROJECT_VERIFICATION.md", system_summary: str = ""):
        self.context_map = context_map
        self.output_file = output_file
        self.verification_file = verification_file
        self.system_summary = system_summary
        self.claim_map = {} # Maps Claim ID -> Claim Object
        self.ref_counter = 1

    def render(self):
        """
        Organizes and writes module documentation into output file
        """
        # Line buffers for both files
        map_lines = ["# Project Context Map", ""]
        verif_lines = ["# Project Verification Proof", "", "This document contains the AST-derived evidence and line ranges for all architectural claims.", ""]
        
        if self.system_summary:
            map_lines.append("## 🏛️ System Architecture")
            map_lines.append(self.system_summary)
            map_lines.append("")
            map_lines.append("---")
            map_lines.append("")
            
        map_lines.append(f"**Total Modules:** {len(self.context_map)}")
        map_lines.append("")
        
        # 1. Calculate Reverse Dependencies
        module_dependents: Dict[str, set] = {k: set() for k in self.context_map}
        for name, ctx in self.context_map.items():
            for dep_path in ctx.key_dependencies:
                if dep_path in module_dependents:
                    module_dependents[dep_path].add(name)
        
        # 2. Group by Archetype
        archetype_groups = {
            "Entry Point": [], "Service": [], "Utility": [], "Data Model": [], "Configuration": []
        }
        others = []

        for path, ctx in self.context_map.items():
            arch = ctx.archetype
            if arch in archetype_groups:
                archetype_groups[arch].append(path)
            else:
                others.append(path)

        presentation_order = [
            ("Entry Point", "🚀 Entry Points"),
            ("Service", "⚙️ Services"),
            ("Utility", "🛠️ Utilities"),
            ("Data Model", "📦 Data Models"),
            ("Configuration", "🔧 Configuration")
        ]
        presentation_order.append(("Other", "📂 Other Modules"))

        # Render groups
        for arch_key, header in presentation_order:
            if arch_key == "Other":
                paths = others
            else:
                paths = archetype_groups.get(arch_key, [])
            
            if not paths: continue
            
            map_lines.append(f"## {header}")
            map_lines.append("")
            
            for path in sorted(paths):
                ctx = self.context_map[path]
                dependents = sorted(list(module_dependents.get(path, [])))
                m_map, m_verif = self._render_module(ctx, dependents)
                map_lines.extend(m_map)
                map_lines.append("---")
                verif_lines.extend(m_verif)
                verif_lines.append("---")
        
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(map_lines))
        
        with open(self.verification_file, "w", encoding="utf-8") as f:
            f.write("\n".join(verif_lines))
        
        print(f"Report generated: {os.path.abspath(self.output_file)}")
        print(f"Verification proof generated: {os.path.abspath(self.verification_file)}")

    def _render_module(self, ctx: ModuleContext, dependents: List[str]) -> Tuple[List[str], List[str]]:
        name = os.path.basename(ctx.file_path)
        map_lines = [f"## 📦 Module: `{name}`"]
        verif_lines = [f"## 📦 Verification: `{name}`"]
        
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
        map_lines.append(f"**Role:** {replace_ref(role_text)}")
        map_lines.append("")

        # Alerts
        if ctx.alerts:
            map_lines.append("### 🚨 Alerts")
            for alert in ctx.alerts:
                icon = "🔴" if alert.category == "Incomplete" else "TODO" if alert.category == "TODO" else "⚠️"
                map_lines.append(f"- {icon} **{alert.category}**: {alert.description} `(Ref: {alert.reference})`")
            map_lines.append("")

        # Interface & Logic
        if ctx.public_api:
            map_lines.append("### 🧩 Interface & Logic")
            # Sort alphabetically. Unicode: 🔌 (U+1F50C) < 🔒 (U+1F512)
            sorted_entities = sorted(ctx.public_api.items(), key=lambda x: x[0])
            for entity, g_text in sorted_entities:
                map_lines.append(f"- **`{entity}`**: {replace_ref(g_text.text)}")
            map_lines.append("")

        # Upstream Dependencies
        if ctx.key_dependencies:
            map_lines.append("### 🔗 Uses (Upstream)")
            for dep, g_text in ctx.key_dependencies.items():
                dep_name = os.path.basename(dep)
                map_lines.append(f"- **`{dep_name}`**: {replace_ref(g_text.text)}")
            map_lines.append("")

        # Downstream Dependents
        if dependents:
            map_lines.append("### 👥 Used By (Downstream)")
            for dep_path in dependents:
                dep_name = os.path.basename(dep_path)
                map_lines.append(f"- **`{dep_name}`**")
            map_lines.append("")

        # Claims (Verification) - Only in verif_lines
        if claim_map:
            verif_lines.append("### 🆔 Verification Claims")
            verif_lines.append("")
            sorted_claims = sorted(claim_map.items(), key=lambda x: x[1])
            
            for cid, index in sorted_claims:
                if cid in ctx.claims:
                    claim = ctx.claims[cid]
                    verif_lines.append(f"> 🆔 `{cid[:6]}` [{index}]: {claim.text} _(Source: {replace_ref(claim.reference)})_")
                    if claim.evidence_snippet:
                        verif_lines.append(f">   - **Evidence (L{claim.line_range[0]}-{claim.line_range[1]}):**")
                        snippet_lines = claim.evidence_snippet.strip().split('\n')
                        verif_lines.append(f">     ```python")
                        for s_line in snippet_lines:
                            verif_lines.append(f">     {s_line}")
                        verif_lines.append(f">     ```")
                else:
                    verif_lines.append(f"> 🆔 `{cid[:6]}` [{index}]: _Claim text missing_")
            verif_lines.append("")

        return map_lines, verif_lines