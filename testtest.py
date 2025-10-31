
import unittest
def simulate_gridbot(initial_state, instructions):
  """
  Simulates a gridbot on a 10x10 grid.
  If the robot is out of bounds, the move is ignored, and the robot remains in its current position,
  continuing with the next instruction.
  Args:
  initial_state: A tuple (x, y, direction) representing the robot's initial state.
  instructions: A string of instructions ('R', 'L', 'F').
  Returns:
  A tuple (x, y, direction) representing the robot's final state.
  """
  x, y, direction = initial_state
  for instruction in instructions:
    if instruction == 'R':
      if direction == 'N':
        direction = 'E'
      elif direction == 'E':
        direction = 'S'
      elif direction == 'S':
        direction = 'W'
      elif direction == 'W':
        direction = 'N'
    elif instruction == 'L':
      if direction == 'N':
        direction = 'W'
      elif direction == 'E':
        direction = 'N'
      elif direction == 'S':
        direction = 'E'
      elif direction == 'W':
        direction = 'S'
    elif instruction == 'F':
      if x >= 0 and x <= 9 and y >= 0 and y <= 9:
        if direction == 'N':
          y += 1
        elif direction == 'E':
          x += 1
        elif direction == 'S':
          y -= 1
        elif direction == 'W':
          x -= 1
      else:
        # Move is out of bounds, ignore it and continue
        pass  # No return statement here
    else:
      # Invalid instruction, ignore it and continue
      pass # No return statement here
  return (x, y, direction)


class TestGridBot(unittest.TestCase):

    def test_simple_movement(self):
        """Tests a basic instruction set that stays on the board."""
        self.assertEqual(simulate_gridbot((0, 0, 'N'), "RFF"), (2, 0, 'E'))

    def test_complex_path(self):
        """Tests a more complex path with multiple turns."""
        self.assertEqual(simulate_gridbot((5, 5, 'W'), "LFFRFF"), (3, 3, 'W'))

    def test_ignore_move_off_east_boundary(self):
        """CRITICAL TEST: Checks if a move off the East edge is ignored."""
        # Expected: Stays at x=9. Actual (Buggy): Moves to x=10.
        self.assertEqual(simulate_gridbot((9, 5, 'E'), "F"), (9, 5, 'E'))

    def test_ignore_move_off_north_boundary(self):
        """CRITICAL TEST: Checks if a move off the North edge is ignored."""
        # Expected: Stays at y=9. Actual (Buggy): Moves to y=10.
        self.assertEqual(simulate_gridbot((5, 9, 'N'), "F"), (5, 9, 'N'))

    def test_ignore_move_off_west_boundary(self):
        """CRITICAL TEST: Checks if a move off the West edge is ignored."""
        # Expected: Stays at x=0. Actual (Buggy): Moves to x=-1.
        self.assertEqual(simulate_gridbot((0, 5, 'W'), "F"), (0, 5, 'W'))

    def test_ignore_move_off_south_boundary(self):
        """CRITICAL TEST: Checks if a move off the South edge is ignored."""
        # Expected: Stays at y=0. Actual (Buggy): Moves to y=-1.
        self.assertEqual(simulate_gridbot((5, 0, 'S'), "F"), (5, 0, 'S'))
        
    def test_path_with_ignored_moves(self):
        """Tests a path where some moves should be ignored."""
        # Starts at (0, 9, 'N'). 'F' ignored. 'L' -> (0, 9, 'W'). 'F' ignored.
        self.assertEqual(simulate_gridbot((0, 9, 'N'), "FLF"), (0, 9, 'W'))

if __name__ == '__main__':
    unittest.main()