import pygame
import sys
import random
from gesture_control import get_direction, release
from screens import show_start_screen, show_game_over

# ================= HIGH SCORE =================
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_high_score()

# ================= PYGAME INIT =================
pygame.init()

TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gesture Controlled Pac-Man")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# ================= LOAD IMAGES =================
pacman_img = pygame.transform.scale(
    pygame.image.load("pacman_PNG87.png").convert_alpha(),
    (TILE_SIZE, TILE_SIZE)
)

pellet_img = pygame.transform.scale(
    pygame.image.load("pellete.png").convert_alpha(),
    (TILE_SIZE//2 + 6, TILE_SIZE//2 - 4)
)

ghost_img = pygame.transform.scale(
    pygame.image.load("monster.png").convert_alpha(),
    (TILE_SIZE, TILE_SIZE - 2)
)

ghost2_img = pygame.transform.scale(
    pygame.image.load("redmonster.png").convert_alpha(),
    (TILE_SIZE + 4, TILE_SIZE)
)

# ================= MAP =================
grid = [
 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1],
 [1,0,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,1],
 [1,0,1,0,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
 [1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
 [1,1,1,1,1,0,1,1,0,0,0,1,1,1,0,1,1,1,1,1],
 [1,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,1,1],
 [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1],
 [1,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1],
 [1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1],
 [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
 [1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# ================= GAME OBJECTS =================
ghosts = []
pellets = []

def reset_game():
    global pacman_x, pacman_y, pellets, score, ghosts
    pacman_x, pacman_y = 1, 1
    pellets = [(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH) if grid[y][x] == 0]
    ghosts = [
        {"x": 10, "y": 10, "dx": 1, "dy": 0, "img": ghost_img},
        {"x": 15, "y": 7, "dx": 0, "dy": 1, "img": ghost2_img}
    ]
    score = 0

# ================= DRAW FUNCTIONS =================
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_grid_lines():
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRAY, (x*TILE_SIZE, 0), (x*TILE_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRAY, (0, y*TILE_SIZE), (SCREEN_WIDTH, y*TILE_SIZE))

def draw_pellets():
    for px, py in pellets:
        rect = pellet_img.get_rect(center=(px*TILE_SIZE + TILE_SIZE//2,
                                           py*TILE_SIZE + TILE_SIZE//2))
        screen.blit(pellet_img, rect)

def draw_score():
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"High Score: {high_score}", True, WHITE), (10, 40))

def move_ghosts():
    for ghost in ghosts:
        nx, ny = ghost["x"] + ghost["dx"], ghost["y"] + ghost["dy"]
        if grid[ny][nx] == 0:
            ghost["x"], ghost["y"] = nx, ny
        else:
            ghost["dx"], ghost["dy"] = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

# ================= START GAME =================
show_start_screen(screen, font, release)
reset_game()

current_direction = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    direction = get_direction()
    if direction == 'quit':
        running = False
    elif direction in ['left', 'right', 'up', 'down']:
        current_direction = direction

    if current_direction:
        nx, ny = pacman_x, pacman_y
        if current_direction == 'left':  nx -= 1
        if current_direction == 'right': nx += 1
        if current_direction == 'up':    ny -= 1
        if current_direction == 'down':  ny += 1
        if grid[ny][nx] == 0:
            pacman_x, pacman_y = nx, ny

    if (pacman_x, pacman_y) in pellets:
        pellets.remove((pacman_x, pacman_y))
        score += 10

    move_ghosts()

    for ghost in ghosts:
        if pacman_x == ghost["x"] and pacman_y == ghost["y"]:
            high_score = show_game_over(
                screen, font, score, high_score,
                save_high_score, reset_game, release
            )
            current_direction = None
            break

    screen.fill(BLACK)
    draw_grid()
    draw_pellets()
    screen.blit(pacman_img, (pacman_x*TILE_SIZE, pacman_y*TILE_SIZE))
    for g in ghosts:
        screen.blit(g["img"], (g["x"]*TILE_SIZE, g["y"]*TILE_SIZE))
    draw_grid_lines()
    draw_score()

    pygame.display.flip()
    clock.tick(10)

release()
pygame.quit()
sys.exit()
