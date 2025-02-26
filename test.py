import unittest
from minesweeper import Minesweeper

class TestMinesweeper(unittest.TestCase):
    def setUp(self):
        # This setup runs before each test case
        self.minesweeper = Minesweeper(size=5, mines=3)

    def test_generate_mines(self):
        """Test mine generation to ensure correct number of mines are placed."""
        self.minesweeper.generate_mines()
        self.assertEqual(len(self.minesweeper.mine_positions), self.minesweeper.mines)
        for x, y in self.minesweeper.mine_positions:
            self.assertEqual(self.minesweeper.board[x][y], 'M')

        def test_calculate_adjacent_mines(self):
            """Test adjacent mine calculation to ensure counts are correct."""
            # Manually place mines for predictable test results
            self.minesweeper.mine_positions = {(0, 0), (1, 1), (3, 3)}
            
            # Reset the board and calculate adjacent mines again
            self.minesweeper.board = [[0 for _ in range(self.minesweeper.size)] for _ in range(self.minesweeper.size)]
            self.minesweeper.calculate_adjacent_mines()

            # Expected board state after calculation
            expected_board = [
                ['M', 1, 0, 0, 0],
                [1, 'M', 1, 0, 0],
                [1, 1, 2, 1, 0],
                [0, 0, 1, 'M', 1],
                [0, 0, 1, 1, 1]
            ]

            for x in range(self.minesweeper.size):
                for y in range(self.minesweeper.size):
                    self.assertEqual(self.minesweeper.board[x][y], expected_board[x][y])

    def test_reveal_tile(self):
        """Test revealing tiles, including revealing a mine and safe tiles."""
        # Set a known mine position
        self.minesweeper.mine_positions = {(0, 0)}
        self.minesweeper.calculate_adjacent_mines()

        # Test revealing a safe tile
        result = self.minesweeper.reveal_tile(2, 2)
        self.assertTrue(result)
        self.assertIn((2, 2), self.minesweeper.revealed)

        # Test revealing a mine
        result = self.minesweeper.reveal_tile(0, 0)
        self.assertFalse(result)

    def test_place_flag(self):
        """Test placing and removing flags on tiles."""
        self.minesweeper.place_flag(1, 1)
        self.assertIn((1, 1), self.minesweeper.flags)
        
        self.minesweeper.place_flag(1, 1)
        self.assertNotIn((1, 1), self.minesweeper.flags)

    def test_check_win(self):
        """Test the win condition for the game."""
        # Simulate winning by flagging all mines
        self.minesweeper.mine_positions = {(0, 0), (1, 1)}
        self.minesweeper.flags = {(0, 0), (1, 1)}
        self.assertTrue(self.minesweeper.check_win())

        # Simulate winning by revealing all non-mine tiles
        self.minesweeper.revealed = {
            (x, y) for x in range(self.minesweeper.size) for y in range(self.minesweeper.size)
        }
        self.minesweeper.revealed.difference_update(self.minesweeper.mine_positions)
        self.assertTrue(self.minesweeper.check_win())

if __name__ == '__main__':
    unittest.main()
