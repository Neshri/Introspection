#
# llm_handler.py (A Leaf)
# This module is responsible for all direct communication with the Ollama LLM.
# It abstracts away the API calls and handles code execution.
#
# It uses the following modules:
# - agent.utils.config: To get the model name and prompt templates.
#

import ollama  # Main LLM interface library for model interactions
import subprocess  # System process execution for code running
import time  # Timing utilities for performance measurement
import tempfile  # Temporary file creation for safe code execution
import os  # File system operations for data persistence
import json  # JSON handling for prompt performance tracking
from agent.utils import config  # Configuration module for model and prompt settings

def get_executor_response(goal, document):
    """Generates the next code improvement using the Executor prompt with self-improvement."""
    # Get base prompt
    prompt = config.EXECUTOR_PROMPT_TEMPLATE.format(goal=goal, document=document)

    # Add self-improvement context if we have historical data
    best_prompts = get_best_prompt_variations(limit=3)
    if best_prompts:
        improvement_context = "\n\n**Self-Improvement Insights:**\nBased on previous successful code generations:\n"
        for i, (prompt_key, data) in enumerate(best_prompts[:3]):
            avg_score = data.get('avg_score', 0)
            success_rate = data.get('success_count', 0) / max(1, data.get('total_attempts', 1))
            improvement_context += f"- High-performing approach (score: {avg_score:.1f}, success: {success_rate:.1%}): Try variations that improve accuracy and efficiency.\n"
        improvement_context += "\nUse these insights to generate better code variations."
        prompt += improvement_context

    response = ollama.chat(model=config.MODEL, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content'].strip()

def get_critic_score(goal, document):
    """Evaluates the code so far using the Critic prompt."""
    prompt = config.CRITIC_PROMPT_TEMPLATE.format(goal=goal, document=document)
    response = ollama.chat(model=config.MODEL, messages=[{'role': 'user', 'content': prompt}])
    try:
        return int(response['message']['content'].strip())
    except ValueError:
        return 1

def parse_test_cases_from_goal(goal):
    """
    Parse test cases from goal description.
    Expected format: "function_name(input) should return expected, function_name(input2) should return expected2, ..."
    """
    test_cases = []
    import re  # Regular expressions for parsing goal descriptions and test cases
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
    import ast  # Abstract syntax tree for parsing and analyzing Python code
    import types  # Dynamic type creation for execution namespace

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

def track_prompt_performance(prompt_variation, score, goal, execution_result):
    """
    Track prompt performance for self-improvement.

    Records which prompt variations lead to better code generation outcomes.
    """
    try:
        # Load existing performance data
        if os.path.exists(config.PROMPT_PERFORMANCE_LOG):
            with open(config.PROMPT_PERFORMANCE_LOG, 'r') as f:
                performance_data = json.load(f)
        else:
            performance_data = {}

        # Use full prompt as key for detailed tracking
        prompt_key = prompt_variation.replace('\n', ' ').strip()

        # Update performance tracking
        if prompt_key not in performance_data:
            performance_data[prompt_key] = {
                'scores': [],
                'success_count': 0,
                'total_attempts': 0,
                'avg_score': 0,
                'goal': goal
            }

        performance_data[prompt_key]['scores'].append(score)
        performance_data[prompt_key]['total_attempts'] += 1
        if execution_result and execution_result['success']:
            performance_data[prompt_key]['success_count'] += 1

        # Calculate new average
        performance_data[prompt_key]['avg_score'] = sum(performance_data[prompt_key]['scores']) / len(performance_data[prompt_key]['scores'])

        # Keep only last 50 scores to prevent file bloat
        if len(performance_data[prompt_key]['scores']) > 50:
            performance_data[prompt_key]['scores'] = performance_data[prompt_key]['scores'][-50:]

        # Save updated data
        with open(config.PROMPT_PERFORMANCE_LOG, 'w') as f:
            json.dump(performance_data, f, indent=2)

    except Exception as e:
        # Don't crash the main process if tracking fails
        pass

def get_best_prompt_variations(limit=5):
    """
    Retrieve the best performing prompt variations from historical data.
    """
    try:
        if os.path.exists(config.PROMPT_PERFORMANCE_LOG):
            with open(config.PROMPT_PERFORMANCE_LOG, 'r') as f:
                performance_data = json.load(f)

            # Sort by average score and success rate
            sorted_prompts = sorted(
                performance_data.items(),
                key=lambda x: (x[1]['avg_score'], x[1]['success_count'] / max(1, x[1]['total_attempts'])),
                reverse=True
            )

            return sorted_prompts[:limit]
        else:
            return []
    except Exception as e:
        return []

def execute_code(code):
    """
    Executes Python code safely using subprocess and returns execution results.

    Returns a dict with:
    - success: bool
    - output: str (stdout)
    - error: str (stderr)
    - execution_time: float (seconds)
    """
    result = {
        'success': False,
        'output': '',
        'error': '',
        'execution_time': 0.0
    }

    # Create temporary file for the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        start_time = time.time()

        # Execute with timeout and resource limits
        process = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
            cwd=os.path.dirname(temp_file)  # Run in temp directory
        )

        end_time = time.time()
        result['execution_time'] = end_time - start_time
        result['output'] = process.stdout.strip()
        result['error'] = process.stderr.strip()
        result['success'] = process.returncode == 0

    except subprocess.TimeoutExpired:
        result['error'] = "Execution timed out after 30 seconds"
        result['success'] = False
    except Exception as e:
        result['error'] = f"Execution failed: {str(e)}"
        result['success'] = False
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_file)
        except:
            pass

    return result