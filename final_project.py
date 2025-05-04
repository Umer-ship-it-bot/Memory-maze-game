import pygame
import random
import sys

# --- Constants ---
BOARD_SIZE = 8
TILE_SIZE = 80
WINDOW_SIZE = BOARD_SIZE * TILE_SIZE
FPS = 60
NUM_TRAPS = 10
NUM_BONUSES = 5
MAX_TRAPS = 3

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

# --- Classes ---
class Tile:
    def __init__(self):
        self.type = "path"  # "trap", "bonus", "goal"
        self.revealed = False
        self.temp_reveal = False

class Player:
    def __init__(self, name, color, pos):
        self.name = name
        self.color = color
        self.position = pos
        self.checkpoint = pos
        self.memory_tokens = 2
        self.trap_count = 0
        self.active = True

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Memory Maze")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)

        self.board = [[Tile() for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.players = [
            Player("Player 1", BLUE, (0, 0)),
            Player("Player 2", RED, (BOARD_SIZE - 1, BOARD_SIZE - 1))
        ]
        self.goal = (BOARD_SIZE // 2, BOARD_SIZE // 2)
        self.board[self.goal[0]][self.goal[1]].type = "goal"
        self.turn = 0
        self.running = True
        self.winner = None

        self.place_items()

    def place_items(self):
        self.place_items_type("trap", NUM_TRAPS)
        self.place_items_type("bonus", NUM_BONUSES)

    def place_items_type(self, item_type, count):
        placed = 0
        while placed < count:
            x, y = random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)
            if self.board[x][y].type == "path" and (x, y) != self.goal:
                self.board[x][y].type = item_type
                placed += 1

    def draw_board(self):
        self.screen.fill(GRAY)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tile = self.board[i][j]

                # Draw revealed or temp-revealed tile
                if tile.revealed or tile.temp_reveal:
                    if tile.type == "trap":
                        pygame.draw.rect(self.screen, RED, rect)
                    elif tile.type == "bonus":
                        pygame.draw.rect(self.screen, YELLOW, rect)
                    elif tile.type == "goal":
                        pygame.draw.rect(self.screen, GREEN, rect)
                    else:
                        pygame.draw.rect(self.screen, WHITE, rect)
                else:
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)

        # Draw players
        for player in self.players:
            if player.active:
                x, y = player.position
                center = (y*TILE_SIZE + TILE_SIZE//2, x*TILE_SIZE + TILE_SIZE//2)
                pygame.draw.circle(self.screen, player.color, center, TILE_SIZE//4)

    def display_info(self):
        pygame.draw.rect(self.screen, WHITE, (0, WINDOW_SIZE, WINDOW_SIZE, 100))
        current = self.players[self.turn % len(self.players)]
        info = f"{current.name}'s Turn | Tokens: {current.memory_tokens} | Traps Hit: {current.trap_count}"
        text = self.font.render(info, True, BLACK)
        self.screen.blit(text, (10, WINDOW_SIZE + 20))

        if self.winner:
            win_text = self.font.render(f"🎉 {self.winner.name} wins! Press R to replay or Q to quit.", True, PURPLE)
            self.screen.blit(win_text, (10, WINDOW_SIZE + 60))

    def move(self, dx, dy):
        current = self.players[self.turn % len(self.players)]
        if not current.active or self.winner:
            return
        x, y = current.position
        nx, ny = x + dx, y + dy

        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            tile = self.board[nx][ny]
            tile.revealed = True

            if tile.type == "trap":
                current.trap_count += 1
                if current.trap_count >= MAX_TRAPS:
                    current.active = False
                    print(f"{current.name} is eliminated!")
                    self.winner = self.players[(self.turn + 1) % len(self.players)]  # Other player wins
                else:
                    current.position = current.checkpoint
            elif tile.type == "bonus":
                current.memory_tokens += 1
                current.position = (nx, ny)
                current.checkpoint = current.position
            else:
                current.position = (nx, ny)
                steps = abs(current.position[0] - current.checkpoint[0]) + abs(current.position[1] - current.checkpoint[1])
                if steps % 4 == 0:
                    current.checkpoint = current.position

            if (nx, ny) == self.goal:
                self.winner = current

            self.clear_temp_tiles()
            self.turn += 1
            self.check_game_over()

    def check_game_over(self):
        active_players = [p for p in self.players if p.active]
        if len(active_players) == 1:
            self.winner = active_players[0]

    def clear_temp_tiles(self):
        for row in self.board:
            for tile in row:
                tile.temp_reveal = False

    def use_token(self):
        current = self.players[self.turn % len(self.players)]
        if current.memory_tokens <= 0 or not current.active:
            return

        x, y = current.position
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    self.board[nx][ny].temp_reveal = True
        current.memory_tokens -= 1

    def reset(self):
        self.__init__()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if self.winner:
                        if event.key == pygame.K_r:
                            self.reset()
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        continue

                    if event.key == pygame.K_UP:
                        self.move(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move(1, 0)
                    elif event.key == pygame.K_LEFT:
                        self.move(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        self.move(0, 1)
                    elif event.key == pygame.K_SPACE:
                        self.use_token()

            self.draw_board()
            self.display_info()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

# --- Run Game ---
if __name__ == "__main__":
    game = Game()
    game.run()
