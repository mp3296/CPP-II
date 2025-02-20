import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 32
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 24
WIDTH, HEIGHT = 640, 480
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Initialize font
pygame.font.init()
font = pygame.font.Font(None, FONT_SIZE)

# Maze generation using Recursive Backtracking with more elaborate paths
def generate_maze(rows, cols):
    maze = [['W' for _ in range(cols)] for _ in range(rows)]
    stack = [(0, random.randint(0, rows - 1))]
    maze[stack[0][1]][0] = ' '

    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 'W':
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(y + ny) // 2][(x + nx) // 2] = ' '
            maze[ny][nx] = ' '
            stack.append((nx, ny))
        else:
            stack.pop()

    # Add more complexity by creating additional random paths
    for _ in range(rows * cols // 4):
        x, y = random.randint(0, cols - 1), random.randint(0, rows - 1)
        if maze[y][x] == 'W':
            maze[y][x] = ' '

    # Create multiple entry points on the left side
    for i in range(0, rows, rows // 4):
        maze[i][0] = ' '

    # Ensure only one exit point on the right side
    exit_row = random.randint(0, rows - 1)
    maze[exit_row][cols - 1] = 'E'
    return maze, exit_row

# Initialize game variables
level = 1
player_x, player_y = 0, random.randint(0, ROWS - 1)
remaining_time = 60  # in seconds
win = False
running = True

# Generate the first maze
maze, exit_row = generate_maze(ROWS, COLS)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and maze[player_y][player_x + 1] != 'W':
                player_x += 1
            elif event.key == pygame.K_LEFT and maze[player_y][player_x - 1] != 'W':
                player_x -= 1
            elif event.key == pygame.K_UP and maze[player_y - 1][player_x] != 'W':
                player_y -= 1
            elif event.key == pygame.K_DOWN and maze[player_y + 1][player_x] != 'W':
                player_y += 1

    if maze[player_y][player_x] == 'E':
        level += 1
        player_x, player_y = 0, random.randint(0, ROWS - 1)
        remaining_time = 60
        maze, exit_row = generate_maze(ROWS, COLS)

    if remaining_time <= 0:
        running = False

    screen.fill(BLACK)

    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 'W':
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == ' ':
                pygame.draw.rect(screen, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 'E':
                pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.draw.rect(screen, GREEN, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Render and display the timer and level
    timer_text = font.render(f'Time: {int(remaining_time)}', True, WHITE)
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(timer_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(FPS)

    # Decrease the remaining time
    remaining_time -= 1 / FPS

pygame.quit()

if win:
    print("You win!")
else:
    print("Time's up! You lose.")
sys.exit()