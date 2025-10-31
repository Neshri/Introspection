# Reality-Grounded Code Agent Architecture

## What the LLM Actually Needs

The LLM doesn't need "enhanced reasoning" or "multi-stage pipelines" - it needs **reality checks** to prevent hallucination and **grounding** to avoid getting stuck. The core problems the current architecture fails to solve:

### 1. Hallucination Prevention
- **Problem**: LLM generates plans for files/functions that don't exist
- **Solution**: Pre-validate ALL file/function references against actual codebase
- **Implementation**: Build complete file/function/class inventory upfront

### 2. Getting Unstuck
- **Problem**: LLM gets stuck in loops trying impossible operations
- **Solution**: Clear success/failure signals with actionable next steps
- **Implementation**: Reality checks before each planning step

### 3. Context Management
- **Problem**: LLM loses track of what it's already done/changed
- **Solution**: Maintain running state of codebase changes
- **Implementation**: Track modifications and validate against current state

### 4. Actionable Planning
- **Problem**: Plans are too abstract or reference non-existent things
- **Solution**: Ground all planning in concrete file/function/class names
- **Implementation**: Require specific file references for all objectives

## Core Requirements

### Grounding First
```python
# Before ANY planning, build complete reality map:
reality_map = {
    'files': ['agent_core.py', 'intelligence_plan_generator.py', ...],
    'functions': {'agent_core.py': ['set_goal', 'run_with_agent', ...]},
    'classes': {'agent_core.py': ['Agent'], ...},
    'imports': {'agent_core.py': ['re', 'time', 'typing', ...]},
    'dependencies': {'agent_core.py': ['intelligence_project_scout.py'], ...}
}
```

### Reality-Checked Planning
```python
# EVERY planning step must validate against reality:
def validate_objective(objective: str, reality_map: dict) -> bool:
    # Extract file/function references from objective
    # Check they exist in reality_map
    # Return True only if grounded in actual code
```

### State-Aware Execution
```python
# Track what has actually changed:
execution_state = {
    'modified_files': set(),
    'new_functions': [],
    'changed_dependencies': [],
    'current_reality': reality_map.copy()
}
```

## Minimal Viable Reality-Grounded Architecture

### The Real Problems (From User Feedback)
1. **Context Limits**: Current architecture doesn't respect LLM context limits
2. **Over-Specific Planning**: Plans fail because they're too specific about non-existent details
3. **Test Cheating**: Architecture allows bypassing real validation

### Minimal Solution: Context-Limited Grounded Planning

#### 1. Context-Bound Reality Map
```python
class ContextBoundRealityMap:
    """Reality map that fits within LLM context limits."""

    MAX_CONTEXT_TOKENS = 2048  # From config.CONTEXT_LIMIT

    def build_bounded_map(self, backpack: List[Dict]) -> BoundedRealityMap:
        """Build reality map that fits in context window."""
        # Only include most relevant files/functions
        # Prioritize recently modified and goal-relevant code
        # Summarize when necessary to fit context
```

#### 2. Bounded Objective Validation
```python
class BoundedValidator:
    """Validates objectives against bounded reality."""

    def validate_within_bounds(self, objective: str, bounded_map: BoundedRealityMap) -> BoundedValidation:
        """Validate objective against what's actually in context."""
        # Check if objective references items in the bounded map
        # Reject if references items not in current context
        # Suggest context expansion if needed
```

#### 3. Context-Aware Planning Loop
```python
class ContextAwarePlanner:
    """Plans within context bounds with validation."""

    def plan_within_context(self, goal: str, bounded_map: BoundedRealityMap) -> ContextPlan:
        """Generate plan that works within given context bounds."""

        # Phase 1: Generate initial plan
        raw_plan = self._generate_bounded_plan(goal, bounded_map)

        # Phase 2: Validate against bounded reality
        validated_plan = self._validate_against_bounds(raw_plan, bounded_map)

        # Phase 3: If validation fails, expand context or simplify plan
        if not validated_plan.is_fully_valid:
            return self._handle_validation_failure(validated_plan, bounded_map)

        return validated_plan
```

### Context Management Strategy

1. **Initial Context**: Start with minimal relevant code
2. **Progressive Expansion**: Add more context only when needed
3. **Validation First**: Check if plan works before expanding
4. **Concrete References**: Require specific file/function names that exist

### Anti-Cheating Measures

1. **Real File Validation**: All file references must exist in actual backpack
2. **Context Enforcement**: Cannot reference code not in current context
3. **Progressive Disclosure**: Context expands based on real needs, not assumptions
4. **Validation Logging**: Track what was validated and how

### Implementation Approach

1. Extract minimal reality mapping from existing ASTAnalyzer
2. Add context bounds checking
3. Implement bounded validation
4. Create context-aware planning loop
5. Add anti-cheating validation

This solves the core issues: respects context limits, prevents over-specific planning that fails, and cannot be cheated because it validates against real code.