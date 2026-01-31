import pygame
import sys
import random
from gesture_control import get_direction, release  # your gesture functions

pygame.init()

# --- GRID SETTINGS ---
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

# --- COLORS ---
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

# --- PYGAME SCREEN SETUP ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Grid with Gesture Control")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- LOAD IMAGES ---
pacman_img = pygame.image.load("pacman.png").convert_alpha()
pellet_img = pygame.image.load("pellet.png").convert_alpha()
ghost_img = pygame.image.load("ghost (1).png").convert_alpha()
ghost2_img = pygame.image.load("ghost2.png").convert_alpha()  # second ghost image

pacman_img = pygame.transform.scale(pacman_img, (TILE_SIZE, TILE_SIZE))
pellet_img = pygame.transform.scale(pellet_img, ((TILE_SIZE // 2) + 6, TILE_SIZE // 2 - 4))
ghost_img = pygame.transform.scale(ghost_img, (TILE_SIZE, TILE_SIZE - 2))
ghost2_img = pygame.transform.scale(ghost2_img, (TILE_SIZE + 4, TILE_SIZE))

# --- MAP ---
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

ghosts = []
pellets = []

# --- INITIALIZE OBJECTS ---
def reset_game():
    global pacman_x, pacman_y, pellets, score, ghosts, ghost_timer, ghost_speed_multiplier
    pacman_x, pacman_y = 1, 1
    pellets[:] = [(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH) if grid[y][x] == 0]
    ghosts[:] = [
        {"x": 10, "y": 10, "dx": 1, "dy": 0, "img": ghost_img},   
        {"x": 15, "y": 7, "dx": 0, "dy": 1, "img": ghost2_img},  
    ]
    score = 0
    ghost_timer = 0
    ghost_speed_multiplier = 1

score = 0
ghost_speed_multiplier = 1
reset_game()

# --- START SCREEN ---
def show_start_screen():
    screen.fill(BLACK)
    title_text = font.render("PAC-MAN", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    screen.blit(pacman_img, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 32))
    screen.blit(ghost_img, (SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2 - 32))
    msg = font.render("Press any key to start", True, WHITE)
    screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2 + 80))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                release()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Show start screen before game loop
show_start_screen()
reset_game()

# --- DRAW FUNCTIONS ---
def draw_grid_background():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_grid_lines():
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRAY, (x*TILE_SIZE, 0), (x*TILE_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRAY, (0, y*TILE_SIZE), (SCREEN_WIDTH, y*TILE_SIZE))

def draw_pacman(x, y):
    screen.blit(pacman_img, (x * TILE_SIZE, y * TILE_SIZE))

def draw_pellets():
    for (px, py) in pellets:
        pellet_rect = pellet_img.get_rect(center=(px * TILE_SIZE + TILE_SIZE//2,
                                                  py * TILE_SIZE + TILE_SIZE//2))
        screen.blit(pellet_img, pellet_rect)

def draw_ghosts():
    for ghost in ghosts:
        screen.blit(ghost["img"], (ghost["x"] * TILE_SIZE, ghost["y"] * TILE_SIZE))

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def move_ghosts():
    global ghost_timer
    ghost_timer += 1
    if ghost_timer < max(1, 5 - ghost_speed_multiplier):
        return
    ghost_timer = 0
    for ghost in ghosts:
        new_x = ghost["x"] + ghost["dx"]
        new_y = ghost["y"] + ghost["dy"]
        if grid[new_y][new_x] == 0:
            ghost["x"] = new_x
            ghost["y"] = new_y
        else:
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            ghost["dx"], ghost["dy"] = random.choice(directions)

# --- MAIN LOOP ---
running = True
current_direction = None  # Pac-Man keeps moving in this direction

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- GESTURE INPUT ---
    direction = get_direction()
    if direction == 'quit':
        running = False
    elif direction in ['left', 'right', 'up', 'down']:
        current_direction = direction  # update only when new gesture comes

    # --- MOVE PACMAN CONSTANTLY ---
    if current_direction:
        new_x, new_y = pacman_x, pacman_y
        if current_direction == 'left':  new_x -= 1
        if current_direction == 'right': new_x += 1
        if current_direction == 'up':    new_y -= 1
        if current_direction == 'down':  new_y += 1

        # Only move if not hitting a wall
        if grid[new_y][new_x] == 0:
            pacman_x, pacman_y = new_x, new_y

    # --- PELLET COLLECTION ---
    if (pacman_x, pacman_y) in pellets:
        pellets.remove((pacman_x, pacman_y))
        score += 10

    if not pellets:
        pellets[:] = [(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH) if grid[y][x] == 0]
        ghost_speed_multiplier += 1

    move_ghosts()

    for ghost in ghosts:
        if pacman_x == ghost["x"] and pacman_y == ghost["y"]:
            screen.fill(BLACK)
            draw_score()
            msg1 = font.render("Game Over!", True, WHITE)
            msg2 = font.render("Press any key to restart", True, WHITE)
            screen.blit(msg1, (SCREEN_WIDTH//2 - msg1.get_width()//2, SCREEN_HEIGHT//2 - 40))
            screen.blit(msg2, (SCREEN_WIDTH//2 - msg2.get_width()//2, SCREEN_HEIGHT//2 + 10))
            pygame.display.flip()
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        waiting = False
                        running = False
                    if e.type == pygame.KEYDOWN:
                        reset_game()
                        current_direction = None
                        waiting = False
            break

    screen.fill(BLACK)
    draw_grid_background()
    draw_pellets()
    draw_pacman(pacman_x, pacman_y)
    draw_ghosts()
    draw_grid_lines()
    draw_score()

    pygame.display.flip()
    clock.tick(10)

release()  # release camera after quitting
pygame.quit()
sys.exit()
