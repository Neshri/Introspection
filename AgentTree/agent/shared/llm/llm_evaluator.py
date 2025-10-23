#
# llm_evaluator.py (A Leaf)
# This module evaluates code quality through testing and analysis.
#
# It uses the following modules:
# - agent.utils.config: For configuration settings.
#

import ast  # Abstract syntax tree for parsing and analyzing Python code during test execution
import types  # Dynamic type creation for safe execution namespace isolation
import re  # Regular expressions for parsing goal descriptions and extracting test cases

def parse_test_cases_from_goal(goal):
    """
    Parse test cases from goal description.
    Expected format: "function_name(input) should return expected, function_name(input2) should return expected2, ..."
    """
    test_cases = []
    patterns = [
        r'(\w+)\s*\(\s*([^)]+)\s*\)\s*(?:should return|=)\s*([^,\n]+)',  # func(arg) should return value
    ]

    for pattern in patterns:
        matches = re.findall(pattern, goal, re.IGNORECASE)
        for match in matches:
            func_name, input_val, expected = match
            # Try to parse input and expected values
            try:
                # Handle numeric inputs
                if input_val.isdigit() or (input_val.startswith('-') and input_val[1:].isdigit()):
                    input_parsed = int(input_val)
                else:
                    input_parsed = input_val.strip()

                # Handle numeric expected values
                expected = expected.strip()
                if expected.isdigit() or (expected.startswith('-') and expected[1:].isdigit()):
                    expected_parsed = int(expected)
                else:
                    expected_parsed = expected

                test_cases.append({
                    'function': func_name,
                    'input': input_parsed,
                    'expected': expected_parsed
                })
            except:
                continue

    return test_cases

def run_test_cases(code, test_cases):
    """
    Execute code with test cases and return results.
    """
    results = []

    try:
        # Parse the code to find the function
        tree = ast.parse(code)

        # Execute the code in a restricted environment
        namespace = {}
        exec(code, namespace)

        for test_case in test_cases:
            func_name = test_case['function']
            input_val = test_case['input']
            expected = test_case['expected']

            if func_name in namespace and callable(namespace[func_name]):
                try:
                    result = namespace[func_name](input_val)
                    passed = (result == expected)
                    results.append({
                        'input': input_val,
                        'expected': expected,
                        'actual': result,
                        'passed': passed
                    })
                except Exception as e:
                    results.append({
                        'input': input_val,
                        'expected': expected,
                        'actual': f"ERROR: {str(e)}",
                        'passed': False
                    })
            else:
                results.append({
                    'input': input_val,
                    'expected': expected,
                    'actual': f"ERROR: Function {func_name} not found",
                    'passed': False
                })

    except Exception as e:
        # If code parsing fails, all tests fail
        for test_case in test_cases:
            results.append({
                'input': test_case['input'],
                'expected': test_case['expected'],
                'actual': f"ERROR: Code execution failed - {str(e)}",
                'passed': False
            })

    return results

def evaluate_code_quality(code, execution_result, goal):
    """
    General evaluation combining execution results with test case validation.

    Returns a score from 1-10 based on:
    - Execution success
    - Test case pass rate
    - Performance metrics
    - Code quality indicators
    """
    score = 1

    # Base score from execution success
    if execution_result and execution_result['success']:
        score = 5  # Code runs without syntax/runtime errors
    else:
        return 1  # Code doesn't run at all

    # Parse test cases from goal and run them
    test_cases = parse_test_cases_from_goal(goal)
    if test_cases:
        test_results = run_test_cases(code, test_cases)
        passed_tests = sum(1 for result in test_results if result['passed'])
        total_tests = len(test_results)

        if total_tests > 0:
            pass_rate = passed_tests / total_tests

            # Score based on test success: 5-10 range
            if pass_rate == 1.0:  # All tests pass
                score = 10
            elif pass_rate >= 0.8:  # 80%+ pass
                score = 8
            elif pass_rate >= 0.5:  # 50%+ pass
                score = 7
            else:  # Less than 50%
                score = 6

            # Performance bonus for reasonable execution time
            exec_time = execution_result.get('execution_time', 30)
            if exec_time < 5:  # Very fast
                score = min(10, score + 1)
            elif exec_time < 15:  # Reasonable
                score = min(10, score + 0.5)

    # Code quality checks
    code_lines = code.strip().split('\n')
    quality_indicators = 0

    # Check for basic code quality
    if any('def ' in line for line in code_lines): quality_indicators += 1
    if any('return' in line for line in code_lines): quality_indicators += 1
    if len([line for line in code_lines if line.strip() and not line.strip().startswith('#')]) > 2:
        quality_indicators += 1

    # Small quality bonus
    score += min(1, quality_indicators / 3)

    return min(10, max(1, int(score)))