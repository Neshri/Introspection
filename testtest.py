def process_glimmer_string(input_string):
    # Step 1: Define helper functions
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    # Step 2: Initialize variables
    digits = [int(digit) for digit in input_string]
    output_digits = []

    # Step 3: Iterate through each index and apply the corresponding rule
    for index, current_digit in enumerate(digits):
        if is_prime(index):
            left_neighbor_value = 0 if index == 0 else digits[index - 1]
            new_digit = (current_digit + left_neighbor_value) % 10
        else:
            right_neighbor_value = 0 if index == len(digits) - 1 else digits[index + 1]
            new_digit = (current_digit - right_neighbor_value + 10) % 10

        output_digits.append(new_digit)

    # Step 4: Convert the list of digits back to a string
    output_string = "".join(str(digit) for digit in output_digits)

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