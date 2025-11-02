"""
Logic Expression Evaluator and Truth Table Generator
====================================================
Provides tools for parsing, evaluating, and visualizing Boolean expressions.
Generates complete truth tables for user-defined logic circuits.

Author: Digital Logic Educational Project
"""

import sys
import os
from typing import List, Dict, Tuple
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logic_gates import LogicGates


class LogicExpressionParser:
    """
    Parses and evaluates Boolean logic expressions.

    Supported operators (precedence high to low):
    1. NOT (!, ~)
    2. AND (&, AND)
    3. OR (|, OR)
    4. XOR (^, XOR)

    Example expressions:
    - "A AND B"
    - "(A OR B) AND NOT C"
    - "A XOR B"
    - "(A AND B) OR (C AND D)"
    """

    def __init__(self):
        """Initialize the parser with operator definitions."""
        self.operators = {
            'NOT': {'precedence': 3, 'unary': True},
            '!': {'precedence': 3, 'unary': True},
            '~': {'precedence': 3, 'unary': True},
            'AND': {'precedence': 2, 'unary': False},
            '&': {'precedence': 2, 'unary': False},
            'OR': {'precedence': 1, 'unary': False},
            '|': {'precedence': 1, 'unary': False},
            'XOR': {'precedence': 1, 'unary': False},
            '^': {'precedence': 1, 'unary': False},
        }

    def tokenize(self, expression: str) -> List[str]:
        """
        Convert expression string into tokens.

        Args:
            expression: Boolean expression string

        Returns:
            List[str]: List of tokens (variables, operators, parentheses)
        """
        # Replace word operators with symbols for easier parsing
        expr = expression.upper()
        expr = expr.replace('AND', '&')
        expr = expr.replace('OR', '|')
        expr = expr.replace('XOR', '^')
        expr = expr.replace('NOT', '!')

        # Tokenize using regex
        # Matches: variables (letters), operators (&|^!~), parentheses, numbers
        tokens = re.findall(r'[A-Z]+|[&|^!~()]|\d+', expr)

        return tokens

    def extract_variables(self, tokens: List[str]) -> List[str]:
        """
        Extract unique variables from token list.

        Args:
            tokens: List of tokens

        Returns:
            List[str]: Sorted list of unique variables
        """
        variables = set()
        for token in tokens:
            if token.isalpha() and token not in self.operators:
                variables.add(token)

        return sorted(list(variables))

    def infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Convert infix notation to postfix (Reverse Polish Notation).

        Uses Shunting Yard Algorithm:
        1. Scan tokens left to right
        2. If operand: add to output
        3. If operator: pop stack while top has higher/equal precedence
        4. If '(': push to stack
        5. If ')': pop until matching '('

        Example:
        Infix: A & B | C
        Postfix: A B & C |

        Args:
            tokens: List of tokens in infix notation

        Returns:
            List[str]: Tokens in postfix notation
        """
        output = []
        operator_stack = []

        for token in tokens:
            # If variable or number, add to output
            if token.isalnum():
                output.append(token)

            # If left parenthesis, push to stack
            elif token == '(':
                operator_stack.append(token)

            # If right parenthesis, pop until matching left paren
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # Remove '('

            # If operator
            elif token in self.operators:
                # Pop operators with higher or equal precedence
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.operators and
                       self.operators[operator_stack[-1]]['precedence'] >=
                       self.operators[token]['precedence']):
                    output.append(operator_stack.pop())
                operator_stack.append(token)

        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())

        return output

    def evaluate_postfix(self, postfix: List[str],
                         variable_values: Dict[str, int]) -> int:
        """
        Evaluate postfix expression with given variable values.

        Algorithm:
        1. For each token:
           - If operand: push to stack
           - If operator: pop operands, apply operation, push result
        2. Final stack value is result

        Args:
            postfix: Expression in postfix notation
            variable_values: Dictionary mapping variables to values (0 or 1)

        Returns:
            int: Evaluation result (0 or 1)
        """
        stack = []

        for token in postfix:
            # If variable, get its value
            if token.isalpha():
                stack.append(variable_values.get(token, 0))

            # If number
            elif token.isdigit():
                stack.append(int(token))

            # If operator
            elif token in self.operators:
                if self.operators[token]['unary']:
                    # Unary operator (NOT)
                    if stack:
                        operand = stack.pop()
                        result = LogicGates.NOT(operand)
                        stack.append(result)
                else:
                    # Binary operator
                    if len(stack) >= 2:
                        b = stack.pop()
                        a = stack.pop()

                        if token in ['&', 'AND']:
                            result = LogicGates.AND(a, b)
                        elif token in ['|', 'OR']:
                            result = LogicGates.OR(a, b)
                        elif token in ['^', 'XOR']:
                            result = LogicGates.XOR(a, b)

                        stack.append(result)

        return stack[0] if stack else 0

    def evaluate(self, expression: str,
                 variable_values: Dict[str, int]) -> int:
        """
        Evaluate Boolean expression with given variable values.

        Args:
            expression: Boolean expression string
            variable_values: Variable assignments

        Returns:
            int: Evaluation result (0 or 1)
        """
        tokens = self.tokenize(expression)
        postfix = self.infix_to_postfix(tokens)
        return self.evaluate_postfix(postfix, variable_values)

    def generate_truth_table(self, expression: str) -> Dict:
        """
        Generate complete truth table for expression.

        Args:
            expression: Boolean expression string

        Returns:
            dict: Truth table with variables, combinations, and results
        """
        tokens = self.tokenize(expression)
        variables = self.extract_variables(tokens)

        if not variables:
            return {
                'variables': [],
                'rows': [],
                'error': 'No variables found in expression'
            }

        # Generate all possible input combinations
        num_vars = len(variables)
        num_combinations = 2 ** num_vars

        rows = []
        for i in range(num_combinations):
            # Create variable assignment for this row
            variable_values = {}
            row_inputs = []

            for j, var in enumerate(variables):
                # Extract bit value for this variable
                bit_value = (i >> (num_vars - 1 - j)) & 1
                variable_values[var] = bit_value
                row_inputs.append(bit_value)

            # Evaluate expression
            try:
                result = self.evaluate(expression, variable_values)
                rows.append({
                    'inputs': row_inputs,
                    'output': result,
                    'binary_index': format(i, f'0{num_vars}b')
                })
            except Exception as e:
                return {
                    'variables': variables,
                    'rows': [],
                    'error': f'Evaluation error: {str(e)}'
                }

        return {
            'variables': variables,
            'rows': rows,
            'expression': expression,
            'num_combinations': num_combinations
        }

    def format_truth_table(self, truth_table: Dict) -> str:
        """
        Format truth table as readable string.

        Args:
            truth_table: Truth table dictionary from generate_truth_table

        Returns:
            str: Formatted truth table string
        """
        if 'error' in truth_table:
            return f"ERROR: {truth_table['error']}"

        variables = truth_table['variables']
        rows = truth_table['rows']
        expression = truth_table.get('expression', '')

        # Build header
        output = f"\nTruth Table for: {expression}\n"
        output += "=" * (len(expression) + 18) + "\n\n"

        # Column headers
        header = " | ".join(variables) + " | OUT"
        output += header + "\n"
        output += "-" * len(header) + "\n"

        # Rows
        for row in rows:
            row_str = " | ".join(str(val) for val in row['inputs'])
            row_str += f" |  {row['output']}"
            output += row_str + "\n"

        return output


class CircuitSimulator:
    """
    Simulates custom logic circuits with step-by-step execution.
    """

    def __init__(self):
        """Initialize circuit simulator."""
        self.parser = LogicExpressionParser()
        self.execution_trace = []

    def simulate_step_by_step(self, expression: str,
                              variable_values: Dict[str, int]) -> List[Dict]:
        """
        Simulate circuit execution with detailed steps.

        Args:
            expression: Boolean expression
            variable_values: Variable assignments

        Returns:
            List[Dict]: Step-by-step execution trace
        """
        self.execution_trace = []

        # Parse expression
        tokens = self.parser.tokenize(expression)
        postfix = self.parser.infix_to_postfix(tokens)

        self.execution_trace.append({
            'step': 'Parse',
            'description': 'Convert to postfix notation',
            'data': {
                'infix': tokens,
                'postfix': postfix
            }
        })

        # Evaluate with tracing
        stack = []
        step_num = 1

        for token in postfix:
            if token.isalpha():
                value = variable_values.get(token, 0)
                stack.append(value)
                self.execution_trace.append({
                    'step': f'Step {step_num}',
                    'description': f'Load variable {token}',
                    'data': {
                        'variable': token,
                        'value': value,
                        'stack': stack.copy()
                    }
                })
                step_num += 1

            elif token in self.parser.operators:
                if self.parser.operators[token]['unary']:
                    if stack:
                        operand = stack.pop()
                        result = LogicGates.NOT(operand)
                        stack.append(result)
                        self.execution_trace.append({
                            'step': f'Step {step_num}',
                            'description': f'Apply NOT',
                            'data': {
                                'operation': 'NOT',
                                'operand': operand,
                                'result': result,
                                'stack': stack.copy()
                            }
                        })
                        step_num += 1
                else:
                    if len(stack) >= 2:
                        b = stack.pop()
                        a = stack.pop()

                        if token in ['&', 'AND']:
                            result = LogicGates.AND(a, b)
                            op_name = 'AND'
                        elif token in ['|', 'OR']:
                            result = LogicGates.OR(a, b)
                            op_name = 'OR'
                        elif token in ['^', 'XOR']:
                            result = LogicGates.XOR(a, b)
                            op_name = 'XOR'

                        stack.append(result)
                        self.execution_trace.append({
                            'step': f'Step {step_num}',
                            'description': f'Apply {op_name}',
                            'data': {
                                'operation': op_name,
                                'operand_a': a,
                                'operand_b': b,
                                'result': result,
                                'stack': stack.copy()
                            }
                        })
                        step_num += 1

        final_result = stack[0] if stack else 0
        self.execution_trace.append({
            'step': 'Final',
            'description': 'Circuit output',
            'data': {
                'output': final_result
            }
        })

        return self.execution_trace


# Test suite
if __name__ == "__main__":
    print("=" * 70)
    print("LOGIC EXPRESSION EVALUATOR TEST SUITE")
    print("=" * 70)

    parser = LogicExpressionParser()

    # Test 1: Simple expression
    print("\n1. SIMPLE EXPRESSION TEST: A AND B")
    expr = "A AND B"
    truth_table = parser.generate_truth_table(expr)
    print(parser.format_truth_table(truth_table))

    # Test 2: Complex expression
    print("\n2. COMPLEX EXPRESSION: (A OR B) AND NOT C")
    expr = "(A OR B) AND NOT C"
    truth_table = parser.generate_truth_table(expr)
    print(parser.format_truth_table(truth_table))

    # Test 3: XOR expression
    print("\n3. XOR EXPRESSION: A XOR B")
    expr = "A XOR B"
    truth_table = parser.generate_truth_table(expr)
    print(parser.format_truth_table(truth_table))

    # Test 4: Step-by-step simulation
    print("\n4. STEP-BY-STEP SIMULATION: (A AND B) OR C")
    simulator = CircuitSimulator()
    expr = "(A AND B) OR C"
    values = {'A': 1, 'B': 1, 'C': 0}

    print(f"Expression: {expr}")
    print(f"Inputs: A={values['A']}, B={values['B']}, C={values['C']}")
    print("\nExecution Trace:")

    trace = simulator.simulate_step_by_step(expr, values)
    for entry in trace:
        print(f"\n{entry['step']}: {entry['description']}")
        if 'stack' in entry['data']:
            print(f"  Stack: {entry['data']['stack']}")

    print("\n" + "=" * 70)
    print("All logic designer tests completed!")
    print("=" * 70)