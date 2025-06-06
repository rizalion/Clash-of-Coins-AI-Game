import pygame
import random

# Initialize
pygame.init()
GRID_SIZE = 12
CELL_SIZE = 60
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE

SCORE_HEIGHT = 80
screen = pygame.display.set_mode((WIDTH, HEIGHT + SCORE_HEIGHT))
pygame.display.set_caption("Clash of Coins")

# Fonts and Music
font = pygame.font.SysFont("comicsansms", 28, bold=True)
big_font = pygame.font.SysFont("comicsansms", 40, bold=True)

# Load and play music (looped)
pygame.mixer.music.load("background_music.mp3")  # Replace with path to your music file
pygame.mixer.music.play(-1)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_TRANSPARENT = (30, 30, 30, 180)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Game State
player_pos = [0, 0]
agent_pos = [GRID_SIZE - 1, GRID_SIZE - 1]
coins, walls = [], []
player_score = 0
agent_score = 0
game_over = False
game_started = False

ai_move_counter = 0
ai_move_delay = 2

def is_accessible(start, coins, walls):
    queue = [start]
    visited = {tuple(start)}
    reachable = set()

    while queue:
        x, y = queue.pop(0)
        if [x, y] in coins:
            reachable.add(tuple([x, y]))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and
                    [nx, ny] not in walls and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append([nx, ny])
    return len(reachable) == len(coins)

def generate_level():
    global coins, walls
    while True:
        coins, walls = [], []

        # Generate coins
        for _ in range(10):
            while True:
                pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
                if pos not in [player_pos, agent_pos] and pos not in walls and pos not in coins:
                    coins.append(pos)
                    break

        # Generate walls (15%)
        for _ in range(int(GRID_SIZE * GRID_SIZE * 0.15)):
            while True:
                pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
                if pos not in coins and pos not in [player_pos, agent_pos] and pos not in walls:
                    walls.append(pos)
                    break

        if is_accessible(player_pos, coins, walls) and is_accessible(agent_pos, coins, walls):
            break

class AIAgent:
    def __init__(self):
        self.path = []

    def find_path(self, start, target, walls):
        queue = [[start]]
        visited = set()
        while queue:
            path = queue.pop(0)
            x, y = path[-1]
            if [x, y] == target:
                return path[1:]
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and
                        [nx, ny] not in walls and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(path + [[nx, ny]])
        return []

agent = AIAgent()
generate_level()
clock = pygame.time.Clock()

def render_text_with_background(text, font, color, background_color, pos):
    text_surf = font.render(text, True, color)
    background = pygame.Surface((text_surf.get_width()+20, text_surf.get_height()+10), pygame.SRCALPHA)
    background.fill(background_color)
    background.blit(text_surf, (10, 5))
    screen.blit(background, pos)

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (20, 20, 20), (0, 0, WIDTH, SCORE_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (0, SCORE_HEIGHT, WIDTH, HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started and event.type == pygame.KEYDOWN:
            game_started = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            player_pos = [0, 0]
            agent_pos = [GRID_SIZE - 1, GRID_SIZE - 1]
            player_score = 0
            agent_score = 0
            game_over = False
            generate_level()

    if not game_started:
        title = big_font.render("💰 Clash of Coins 💰", True, BLUE)
        sub = font.render("Press Any Key to Begin!", True, RED)
        screen.fill((180, 220, 255))
        pygame.draw.circle(screen, (255, 255, 102), (WIDTH//2, HEIGHT//2 - 120), 100)
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
        screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))
    else:
        if not game_over:
            keys = pygame.key.get_pressed()
            new_pos = player_pos.copy()
            if keys[pygame.K_UP] and [player_pos[0], player_pos[1]-1] not in walls and player_pos[1] > 0:
                new_pos[1] -= 1
            if keys[pygame.K_DOWN] and [player_pos[0], player_pos[1]+1] not in walls and player_pos[1] < GRID_SIZE-1:
                new_pos[1] += 1
            if keys[pygame.K_LEFT] and [player_pos[0]-1, player_pos[1]] not in walls and player_pos[0] > 0:
                new_pos[0] -= 1
            if keys[pygame.K_RIGHT] and [player_pos[0]+1, player_pos[1]] not in walls and player_pos[0] < GRID_SIZE-1:
                new_pos[0] += 1
            if new_pos != player_pos:
                player_pos = new_pos

            if coins and ai_move_counter == 0:
                nearest_coin = min(coins, key=lambda c: abs(c[0]-agent_pos[0]) + abs(c[1]-agent_pos[1]))
                path = agent.find_path(agent_pos, nearest_coin, walls)
                if path:
                    agent_pos = path[0]
                if agent_pos == nearest_coin:
                    coins.remove(agent_pos)
                    agent_score += 1
            ai_move_counter = (ai_move_counter + 1) % ai_move_delay

            if player_pos in coins:
                coins.remove(player_pos)
                player_score += 1

            if not coins:
                game_over = True

        # Grid and objects (Adjusted for SCORE_HEIGHT)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE + SCORE_HEIGHT, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)

        for wall in walls:
            pygame.draw.rect(screen, BLACK,
                             (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE + SCORE_HEIGHT, CELL_SIZE, CELL_SIZE))

        for coin in coins:
            pygame.draw.circle(screen, YELLOW,
                               (coin[0]*CELL_SIZE + CELL_SIZE//2, coin[1]*CELL_SIZE + SCORE_HEIGHT + CELL_SIZE//2),
                               CELL_SIZE//4)

        pygame.draw.rect(screen, GREEN,
                         (player_pos[0]*CELL_SIZE, player_pos[1]*CELL_SIZE + SCORE_HEIGHT, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED,
                         (agent_pos[0]*CELL_SIZE, agent_pos[1]*CELL_SIZE + SCORE_HEIGHT, CELL_SIZE, CELL_SIZE))

        render_text_with_background(f"🏀 Player: {player_score}  |  AI: {agent_score}", font, WHITE, (60, 60, 60, 180), (10, 20))
        if game_over:
            msg = "YOU WIN!" if player_score > agent_score else "AI WINS!" if agent_score > player_score else "DRAW!"
            color = GREEN if msg == "YOU WIN!" else RED if msg == "AI WINS!" else BLUE
            render_text_with_background(f"{msg} - Press R to restart", font, color, DARK_TRANSPARENT, (WIDTH//2 - 180, HEIGHT//2 - 20))

    pygame.display.flip()
    clock.tick(8)

pygame.quit()
