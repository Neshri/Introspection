def process_glimmer_string(input_string):
    """
    Processes a string of digits according to the glimmer rule.

    Args:
        input_string: A string containing only digits.

    Returns:
        A string representing the transformed digits, or an error message if the input is invalid.
    """

    # Input Validation
    if not isinstance(input_string, str):
        return "Error: Input must be a string."

    if not all(char.isdigit() for char in input_string):
        return "Error: Input string must contain only digits."

    n = len(input_string)
    output_string = ""

    def is_prime(num):
        """Checks if a number is prime."""
        if num <= 1:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    for i in range(n):
        current_digit = int(input_string[i])

        if is_prime(i):
            # Growth Rule
            if i == 0:
                left_neighbor = 0
            else:
                left_neighbor = int(input_string[i - 1])

            new_digit = (current_digit + left_neighbor) % 10
        else:
            # Decay Rule
            if i == n - 1:
                right_neighbor = 0
            else:
                right_neighbor = int(input_string[i + 1])

            new_digit = (current_digit - right_neighbor + 10) % 10

        output_string += str(new_digit)

    return output_string

import unittest
class TestGlimmerString(unittest.TestCase):

    def test_example_from_prompt(self):
        """Tests the main example from the problem description."""
        self.assertEqual(process_glimmer_string("1428"), "7260")

    def test_simultaneous_update_is_critical(self):
        """Tests that all calculations use the original numbers."""
        # A naive sequential update would fail this test, producing "378".
        self.assertEqual(process_glimmer_string("181"), "379")

    def test_boundary_conditions(self):
        """Tests the 'missing neighbor is 0' rule at both ends."""
        # index 0 (non-prime): (1 - 1 + 10) % 10 -> 0
        # index 1 (non-prime): (1 - 0 + 10) % 10 -> 1
        self.assertEqual(process_glimmer_string("11"), "01")

    def test_prime_and_non_prime_logic(self):
        """Tests a longer string with a mix of prime and non-prime indices."""
        # i=0(np): (1-2+10)%10 -> 9
        # i=1(np): (2-3+10)%10 -> 9
        # i=2(p):  (3+2)%10 -> 5
        # i=3(p):  (4+3)%10 -> 7
        # i=4(np): (5-6+10)%10 -> 9
        # i=5(p):  (6+5)%10 -> 1
        self.assertEqual(process_glimmer_string("123456"), "995791")
        
    def test_single_digit_input(self):
        """Tests the simplest edge case."""
        # i=0(np): (5 - 0 + 10)%10 -> 5
        self.assertEqual(process_glimmer_string("5"), "5")
        
    def test_empty_string_input(self):
        """Tests that an empty input produces an empty output."""
        self.assertEqual(process_glimmer_string(""), "")

if __name__ == '__main__':
    unittest.main()