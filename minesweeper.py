import pygame
import random
import sys


pygame.init()

# Constants
TILE_SIZE = 40
GRID_SIZE = 10
NUM_MINES = 10
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE
FPS = 30


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

# Load font
font = pygame.font.Font(None, 36)

# Load images
try:
    bomb_image = pygame.image.load("bomb.png")
    flag_image = pygame.image.load("flag.png")
    bomb_image = pygame.transform.scale(bomb_image, (TILE_SIZE, TILE_SIZE))
    flag_image = pygame.transform.scale(flag_image, (TILE_SIZE, TILE_SIZE))
except pygame.error as e:
    print(f"Error loading images: {e}")
    sys.exit(1)

class Minesweeper:
    def __init__(self, size=GRID_SIZE, mines=NUM_MINES):
        self.size = size
        self.mines = mines
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.mine_positions = set()
        self.revealed = set()
        self.flags = set()
        self.generate_mines()
        self.calculate_adjacent_mines()

    def generate_mines(self):
        while len(self.mine_positions) < self.mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.mine_positions.add((x, y))

    def calculate_adjacent_mines(self):
        for x, y in self.mine_positions:
            self.board[x][y] = 'M'
            for i in range(max(0, x-1), min(self.size, x+2)):
                for j in range(max(0, y-1), min(self.size, y+2)):
                    if self.board[i][j] != 'M':
                        self.board[i][j] += 1

    def reveal_tile(self, x, y):
        if (x, y) in self.mine_positions:
            self.revealed.add((x, y))
            return False
        if (x, y) not in self.revealed:
            self.revealed.add((x, y))
            if self.board[x][y] == 0:
                for i in range(max(0, x-1), min(self.size, x+2)):
                    for j in range(max(0, y-1), min(self.size, y+2)):
                        if (i, j) not in self.revealed:
                            self.reveal_tile(i, j)
        return True

    def place_flag(self, x, y):
        if (x, y) in self.flags:
            self.flags.remove((x, y))
        else:
            self.flags.add((x, y))

    def check_win(self):
        return len(self.revealed) == self.size * self.size - self.mines

    def draw_board(self, reveal_all=False):
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if (x, y) in self.revealed or reveal_all:
                    pygame.draw.rect(screen, GRAY, rect)
                    if self.board[x][y] == 'M':
                        screen.blit(bomb_image, (x * TILE_SIZE, y * TILE_SIZE))
                    elif self.board[x][y] != 0:
                        text = font.render(str(self.board[x][y]), True, BLACK)
                        screen.blit(text, (x * TILE_SIZE + 10, y * TILE_SIZE + 5))
                else:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    if (x, y) in self.flags:
                        screen.blit(flag_image, (x * TILE_SIZE, y * TILE_SIZE))
                pygame.draw.rect(screen, BLACK, rect, 1)

def main():
    game = Minesweeper()
    running = True
    game_over = False
    win = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                x //= TILE_SIZE
                y //= TILE_SIZE
                if event.button == 1:  # Left click
                    if not game.reveal_tile(x, y):
                        game_over = True
                        print("Game Over! You hit a mine.")
                elif event.button == 3:  # Right click
                    game.place_flag(x, y)

        if game.check_win():
            game_over = True
            win = True
            print("Congratulations! You've revealed all safe tiles.")

        screen.fill(WHITE)
        game.draw_board(reveal_all=game_over)
        pygame.display.flip()
        clock.tick(FPS)

    if win:
        print("You win!")
    else:
        print("Game Over! You hit a mine.")
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
