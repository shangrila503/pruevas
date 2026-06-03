"""Apple Maze Monsters - a tiny beginner-friendly pygame game.

The game uses only simple colored shapes so it is easy to run and easy to
change. The green monster eats every red apple while avoiding brown ants.
"""

import random
import sys

import pygame

# -----------------------------
# Basic game settings
# -----------------------------
TILE_SIZE = 32
ROWS = 15
COLS = 19
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE + 50  # Extra space at the bottom for text.
FPS = 8  # A low FPS makes this grid game easier for beginners to follow.

# Colors are stored as RGB tuples: (red, green, blue).
BLACK = (0, 0, 0)
DARK_BLUE = (18, 35, 74)
WALL_BLUE = (45, 91, 186)
WHITE = (255, 255, 255)
GREEN = (66, 202, 91)
DARK_GREEN = (22, 120, 48)
RED = (235, 50, 55)
APPLE_LEAF = (45, 160, 55)
BROWN = (126, 74, 32)
TAN = (210, 150, 90)
YELLOW = (250, 220, 80)

# Messages shown when the game ends.
GAME_OVER_MESSAGE = "Game Over"
YOU_WIN_MESSAGE = "You Win!"

# The maze is a list of strings.
# # = wall, . = apple, P = player start, A = ant start, space = empty floor.
MAZE = [
    "###################",
    "#P....#.....#....A#",
    "#.###.#.###.#.###.#",
    "#.....#...#.#.....#",
    "###.#####.#.#####.#",
    "#...#.....#.....#.#",
    "#.###.###.###.###.#",
    "#.....#..A..#.....#",
    "#.###.###.###.###.#",
    "#.#.....#.....#...#",
    "#.#####.#.#####.###",
    "#.....#.#...#.....#",
    "#.###.#.###.#.###.#",
    "#A....#.....#.....#",
    "###################",
]


def grid_to_pixels(row, col):
    """Convert a maze row and column into the center point of that tile."""
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = row * TILE_SIZE + TILE_SIZE // 2
    return x, y


def load_level():
    """Read MAZE and create the starting positions for walls, apples, and actors."""
    walls = set()
    apples = set()
    player_position = None
    ant_positions = []

    for row, line in enumerate(MAZE):
        for col, symbol in enumerate(line):
            if symbol == "#":
                walls.add((row, col))
            elif symbol == ".":
                apples.add((row, col))
            elif symbol == "P":
                player_position = (row, col)
            elif symbol == "A":
                ant_positions.append((row, col))

    return walls, apples, player_position, ant_positions


def is_inside_maze(position):
    """Return True if a grid position is inside the maze area."""
    row, col = position
    return 0 <= row < ROWS and 0 <= col < COLS


def can_move(position, direction, walls):
    """Return True if a character can move one tile in the chosen direction."""
    row, col = position
    row_change, col_change = direction
    new_position = (row + row_change, col + col_change)

    # The next tile must be inside the maze and must not be a wall.
    return is_inside_maze(new_position) and new_position not in walls


def move_position(position, direction, walls):
    """Move one grid tile unless a wall blocks the way."""
    if can_move(position, direction, walls):
        row, col = position
        row_change, col_change = direction
        return (row + row_change, col + col_change)
    return position


def get_open_directions(position, walls):
    """Return every direction that is not blocked by a wall."""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [direction for direction in directions if can_move(position, direction, walls)]


def choose_ant_direction(ant_position, current_direction, walls):
    """Pick a simple direction for an ant.

    Ants keep walking forward when they can. If a wall blocks them, they choose
    a random open direction. This is intentionally simple for new programmers.
    """
    if can_move(ant_position, current_direction, walls):
        return current_direction

    possible_directions = get_open_directions(ant_position, walls)
    return random.choice(possible_directions) if possible_directions else (0, 0)


def make_starting_ant_directions(ant_positions, walls):
    """Give each ant a valid starting direction based on its maze tile."""
    ant_directions = []
    for ant_position in ant_positions:
        possible_directions = get_open_directions(ant_position, walls)
        ant_directions.append(
            random.choice(possible_directions) if possible_directions else (0, 0)
        )
    return ant_directions


def draw_maze(screen, walls, apples):
    """Draw the walls, floor, and apples."""
    screen.fill(BLACK)

    for row in range(ROWS):
        for col in range(COLS):
            tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (row, col) in walls:
                pygame.draw.rect(screen, WALL_BLUE, tile_rect)
                pygame.draw.rect(screen, DARK_BLUE, tile_rect, 2)
            else:
                pygame.draw.rect(screen, BLACK, tile_rect)

    for row, col in apples:
        x, y = grid_to_pixels(row, col)
        pygame.draw.circle(screen, RED, (x, y + 2), 9)
        pygame.draw.rect(screen, BROWN, (x - 1, y - 12, 3, 6))
        pygame.draw.ellipse(screen, APPLE_LEAF, (x + 1, y - 14, 8, 5))


def draw_player(screen, position):
    """Draw the cute green ball-shaped monster."""
    x, y = grid_to_pixels(*position)
    pygame.draw.circle(screen, GREEN, (x, y), 13)
    pygame.draw.circle(screen, DARK_GREEN, (x, y), 13, 2)

    # Eyes and a small smile make the monster friendly.
    pygame.draw.circle(screen, WHITE, (x - 5, y - 4), 3)
    pygame.draw.circle(screen, WHITE, (x + 5, y - 4), 3)
    pygame.draw.circle(screen, BLACK, (x - 5, y - 4), 1)
    pygame.draw.circle(screen, BLACK, (x + 5, y - 4), 1)
    pygame.draw.arc(screen, BLACK, (x - 6, y - 1, 12, 9), 0, 3.14, 2)


def draw_ant(screen, position):
    """Draw one small brown ant."""
    x, y = grid_to_pixels(*position)
    pygame.draw.ellipse(screen, BROWN, (x - 10, y - 6, 20, 12))
    pygame.draw.circle(screen, TAN, (x + 8, y), 5)

    # Tiny legs. Lines are enough for a simple beginner project.
    for leg_y in (-5, 0, 5):
        pygame.draw.line(screen, BROWN, (x - 4, y), (x - 13, y + leg_y), 2)
        pygame.draw.line(screen, BROWN, (x + 4, y), (x + 13, y + leg_y), 2)


def draw_status_bar(screen, font, score, message):
    """Draw the score and any win/lose message at the bottom of the screen."""
    bar_rect = pygame.Rect(0, ROWS * TILE_SIZE, SCREEN_WIDTH, 50)
    pygame.draw.rect(screen, DARK_BLUE, bar_rect)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (12, ROWS * TILE_SIZE + 14))

    if message:
        message_text = font.render(message, True, YELLOW)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, ROWS * TILE_SIZE + 25))
        screen.blit(message_text, message_rect)


def main():
    """Start pygame and run the main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Apple Maze Monsters")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    walls, apples, player_position, ant_positions = load_level()
    ant_directions = make_starting_ant_directions(ant_positions, walls)
    player_direction = (0, 0)
    score = 0
    game_message = ""
    game_finished = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_finished:
                if event.key == pygame.K_LEFT:
                    player_direction = (0, -1)
                elif event.key == pygame.K_RIGHT:
                    player_direction = (0, 1)
                elif event.key == pygame.K_UP:
                    player_direction = (-1, 0)
                elif event.key == pygame.K_DOWN:
                    player_direction = (1, 0)

        if not game_finished:
            player_position = move_position(player_position, player_direction, walls)

            # Eating an apple removes it from the set and adds to the score.
            if player_position in apples:
                apples.remove(player_position)
                score += 10

            # Check before ants move so walking onto an ant always ends the game.
            if player_position in ant_positions:
                game_message = GAME_OVER_MESSAGE
                game_finished = True
            elif not apples:
                game_message = YOU_WIN_MESSAGE
                game_finished = True
            else:
                for index, ant_position in enumerate(ant_positions):
                    ant_directions[index] = choose_ant_direction(
                        ant_position, ant_directions[index], walls
                    )
                    ant_positions[index] = move_position(
                        ant_position, ant_directions[index], walls
                    )

                # Check again after ants move so an ant can catch the player.
                if player_position in ant_positions:
                    game_message = GAME_OVER_MESSAGE
                    game_finished = True

        draw_maze(screen, walls, apples)
        draw_player(screen, player_position)
        for ant_position in ant_positions:
            draw_ant(screen, ant_position)
        draw_status_bar(screen, font, score, game_message)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
