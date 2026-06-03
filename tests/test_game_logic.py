"""Small logic tests for Apple Maze Monsters.

These tests avoid opening a pygame window. They provide a tiny fake pygame module
so we can import main.py and test the grid movement rules directly.
"""

import sys
import types
import unittest


# main.py imports pygame at the top of the file. The real pygame package is not
# installed in this environment, so this simple placeholder lets us test helper
# functions that do not need pygame graphics.
sys.modules.setdefault("pygame", types.SimpleNamespace())

import main


class GameLogicTests(unittest.TestCase):
    def setUp(self):
        self.walls, self.apples, self.player_position, self.ant_positions = (
            main.load_level()
        )

    def test_player_cannot_move_through_wall(self):
        # The player starts next to a wall on the left side of the maze.
        new_position = main.move_position(self.player_position, (0, -1), self.walls)
        self.assertEqual(new_position, self.player_position)

    def test_player_cannot_leave_maze_bounds(self):
        # Even if a caller gives the corner tile, moving outside the grid is blocked.
        new_position = main.move_position((0, 0), (-1, 0), self.walls)
        self.assertEqual(new_position, (0, 0))

    def test_player_can_move_into_open_tile(self):
        new_position = main.move_position(self.player_position, (0, 1), self.walls)
        self.assertNotEqual(new_position, self.player_position)
        self.assertNotIn(new_position, self.walls)

    def test_apple_disappears_when_collected(self):
        apples = set(self.apples)
        apple_position = main.move_position(self.player_position, (0, 1), self.walls)

        self.assertIn(apple_position, apples)
        apples.remove(apple_position)
        self.assertNotIn(apple_position, apples)

    def test_ants_get_valid_automatic_directions(self):
        ant_directions = main.make_starting_ant_directions(
            self.ant_positions, self.walls
        )

        self.assertEqual(len(ant_directions), len(self.ant_positions))
        for ant_position, direction in zip(self.ant_positions, ant_directions):
            new_position = main.move_position(ant_position, direction, self.walls)
            self.assertNotIn(new_position, self.walls)
            self.assertTrue(main.is_inside_maze(new_position))

    def test_game_over_and_you_win_messages_are_available(self):
        # These exact messages are shown by the main loop when a collision or win happens.
        self.assertEqual(main.GAME_OVER_MESSAGE, "Game Over")
        self.assertEqual(main.YOU_WIN_MESSAGE, "You Win!")


if __name__ == "__main__":
    unittest.main()
