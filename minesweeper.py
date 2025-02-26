import pygame
import random
import sys
import time

# Initialise Pygame
pygame.init()

# Constants
TILE_SIZE = 40
GRID_SIZE = 10
NUM_MINES = 10
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE + 40  # Extra space for timer
FPS = 30

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialise screen
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

# Load sounds
try:
    tile_sound = pygame.mixer.Sound("tile.mp3")
    flag_sound = pygame.mixer.Sound("flag.mp3")
    gameover_sound = pygame.mixer.Sound("gameover.mp3")
    win_sound = pygame.mixer.Sound("win.mp3")
    start_sound = pygame.mixer.Sound("start.mp3")
except pygame.error as e:
    print(f"Error loading sounds: {e}")
    sys.exit(1)

class Button:
    def __init__(self, text, pos, size, callback):
        self.text = text
        self.pos = pos
        self.size = size
        self.callback = callback
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, 36)
        self.rendered_text = self.font.render(text, True, BLACK)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        screen.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

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
        """Generate mines at random positions on the board."""
        while len(self.mine_positions) < self.mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.mine_positions.add((x, y))

    def calculate_adjacent_mines(self):
        """Calculate the number of adjacent mines for each tile."""
        for x, y in self.mine_positions:
            self.board[x][y] = 'M'
            for i in range(max(0, x-1), min(self.size, x+2)):
                for j in range(max(0, y-1), min(self.size, y+2)):
                    if self.board[i][j] != 'M':
                        self.board[i][j] += 1

    def reveal_tile(self, x, y):
        """Reveal the tile at the given position."""
        if (x, y) in self.mine_positions:
            self.revealed.add((x, y))
            pygame.mixer.Sound.play(gameover_sound)
            return False
        if (x, y) not in self.revealed:
            self.revealed.add((x, y))
            pygame.mixer.Sound.play(tile_sound)
            if self.board[x][y] == 0:
                for i in range(max(0, x-1), min(self.size, x+2)):
                    for j in range(max(0, y-1), min(self.size, y+2)):
                        if (i, j) not in self.revealed:
                            self.reveal_tile(i, j)
        return True

    def place_flag(self, x, y):
        """Place or remove a flag at the given position."""
        if (x, y) in self.flags:
            self.flags.remove((x, y))
        else:
            self.flags.add((x, y))
        pygame.mixer.Sound.play(flag_sound)

    def check_win(self):
        """Check if the player has won the game."""
        return len(self.revealed) == self.size * self.size - self.mines

    def draw_board(self, reveal_all=False):
        """Draw the game board."""
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + 40, TILE_SIZE, TILE_SIZE)
                if (x, y) in self.revealed or reveal_all:
                    pygame.draw.rect(screen, GRAY, rect)
                    if self.board[x][y] == 'M':
                        screen.blit(bomb_image, (x * TILE_SIZE, y * TILE_SIZE + 40))
                    elif self.board[x][y] != 0:
                        text = font.render(str(self.board[x][y]), True, BLACK)
                        screen.blit(text, (x * TILE_SIZE + 10, y * TILE_SIZE + 45))
                else:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    if (x, y) in self.flags:
                        screen.blit(flag_image, (x * TILE_SIZE, y * TILE_SIZE + 40))
                pygame.draw.rect(screen, BLACK, rect, 1)

class Game:
    def __init__(self):
        self.menu_buttons = [
            Button("Start Game", (WIDTH // 2 - 100, HEIGHT // 2 - 50), (200, 50), self.start_game),
            Button("Quit", (WIDTH // 2 - 100, HEIGHT // 2 + 20), (200, 50), self.quit_game)
        ]
        self.state = "MENU"
        self.minesweeper = None

    def start_game(self):
        self.minesweeper = Minesweeper()
        self.state = "GAME"
        self.start_time = time.time()
        pygame.mixer.Sound.play(start_sound)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "MENU":
                        for button in self.menu_buttons:
                            if button.is_clicked(event.pos):
                                button.callback()
                    elif self.state == "GAME" and not self.minesweeper.check_win():
                        x, y = event.pos
                        x //= TILE_SIZE
                        y = (y - 40) // TILE_SIZE
                        if y < 0:
                            continue
                        if event.button == 1:  # Left click
                            if not self.minesweeper.reveal_tile(x, y):
                                self.state = "GAME_OVER"
                                print("Game Over! You hit a mine.")
                        elif event.button == 3:  # Right click
                            self.minesweeper.place_flag(x, y)

            screen.fill(WHITE)

            if self.state == "MENU":
                for button in self.menu_buttons:
                    button.draw(screen)
            elif self.state in ["GAME", "GAME_OVER"]:
                self.minesweeper.draw_board(reveal_all=(self.state == "GAME_OVER"))

                # Draw timer
                elapsed_time = int(time.time() - self.start_time)
                timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
                screen.blit(timer_text, (10, 10))

                if self.minesweeper.check_win():
                    self.state = "WIN"
                    pygame.mixer.Sound.play(win_sound)
                    print("Congratulations! You've revealed all safe tiles.")

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
