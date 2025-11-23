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

        if classes > 0 and funcs == 0 and deps == 0:
            return ModuleArchetype.DATA_MODEL
        
        if classes == 0 and funcs > 0 and deps == 0:
            return ModuleArchetype.UTILITY

        if deps == 0:
            if funcs == 0 and classes == 0 and has_globals:
                return ModuleArchetype.CONFIGURATION
            if classes > 0:
                return ModuleArchetype.DATA_MODEL
            return ModuleArchetype.UTILITY

        return ModuleArchetype.SERVICE