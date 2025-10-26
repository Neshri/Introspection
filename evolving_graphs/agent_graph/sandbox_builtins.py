"""
sandbox_builtins.py - Safe builtins configuration for sandboxed code execution.
"""

# Custom safe builtins - block dangerous modules and functions
SAFE_BUILTINS = {
    # Safe built-ins
    'print': print,
    'len': len,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
    'range': range,
    'enumerate': enumerate,
    'zip': zip,
    'sorted': sorted,
    'min': min,
    'max': max,
    'sum': sum,
    'abs': abs,
    'round': round,
    'type': type,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'repr': repr,
    'Exception': Exception,
    'ValueError': ValueError,
    'TypeError': TypeError,
    'IndexError': IndexError,
    'KeyError': KeyError,
    'AttributeError': AttributeError,
    'None': None,
    'True': True,
    'False': False,
    # Math operations
    '__import__': __import__,  # Will be restricted further
}


def _setup_safe_builtins():
    """Set up custom builtins that block dangerous modules."""
    def safe_import(name, *args, **kwargs):
        blocked_modules = {
            'os', 'sys', 'subprocess', 'importlib', 'builtins',
            'eval', 'exec', 'open', 'file', 'input'
        }
        if name in blocked_modules:
            raise ImportError(f"Import of '{name}' is blocked for security")
        return __import__(name, *args, **kwargs)

    SAFE_BUILTINS['__import__'] = safe_import
    return SAFE_BUILTINS