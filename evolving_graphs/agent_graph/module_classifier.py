import ast
from typing import Dict, Any
from enum import Enum

class ModuleArchetype(Enum):
    CONFIGURATION = "Configuration"     
    DATA_MODEL = "Data Model"           
    UTILITY = "Utility"                 
    SERVICE = "Service"                 
    ENTRY_POINT = "Entry Point"              

class ModuleClassifier:
    def __init__(self, module_name: str, graph_data: Dict[str, Any]):
        self.module_name = module_name
        self.data = graph_data
        
    def classify(self) -> ModuleArchetype:
        if self.module_name.endswith("_main.py") or self.module_name == "__main__.py":
            return ModuleArchetype.ENTRY_POINT
        
        source = self.data.get('source_code', '')
        entities = self.data.get('entities', {})
        deps = len(self.data.get('dependencies', []))
        
        funcs = len(entities.get('functions', []))
        classes = len(entities.get('classes', {}))
        
        # Check for global assignments
        has_globals = False
        if source:
            try:
                for node in ast.parse(source).body:
                    if isinstance(node, (ast.Assign, ast.AnnAssign)):
                        has_globals = True
                        break
            except:
                pass

        # Check for "Behavior" (Public Methods)
        has_behavior = False
        classes_map = entities.get('classes', {})
        for class_name, class_data in classes_map.items():
            methods = class_data.get('methods', [])
            for method in methods:
                # Extract method name from signature "def name(...)"
                m_name = method['signature'].split('(')[0].replace('def ', '').strip()
                # If it's a public method (not starting with _), it's likely behavior
                if not m_name.startswith('_'):
                    has_behavior = True
                    break
            if has_behavior: break

        if deps == 0:
            if classes > 0:
                # If it has public methods, it's a Service (Logic), not just Data
                if has_behavior:
                    return ModuleArchetype.SERVICE
                return ModuleArchetype.DATA_MODEL
            
            if funcs > 0:
                return ModuleArchetype.UTILITY
                
            if has_globals:
                return ModuleArchetype.CONFIGURATION
                
            return ModuleArchetype.UTILITY # Fallback

        return ModuleArchetype.SERVICE

        return ModuleArchetype.SERVICE