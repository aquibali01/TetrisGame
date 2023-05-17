import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Define block shapes and colors
SHAPES = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1], [1, 1]],  # O-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1, 0], [0, 1, 1]],  # S-shape
    [[0, 1, 1], [1, 1, 0]],  # Z-shape
    [[1, 1, 1], [1, 0, 0]],  # J-shape
    [[1, 1, 1], [0, 0, 1]]  # L-shape
]
COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

# Define block dimensions
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = 10, 20
GRID_OFFSET_X = (WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_OFFSET_Y = HEIGHT - GRID_HEIGHT * BLOCK_SIZE - 50

# Define game variables
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5
score = 0
game_over = False

# Define functions

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(WIN, WHITE, (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_block(block, x, y, color):
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j]:
                pygame.draw.rect(WIN, color, (GRID_OFFSET_X + (x + j) * BLOCK_SIZE, GRID_OFFSET_Y + (y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(block, x, y):
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j] and (x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or grid[y + i][x + j]):
                return True
    return False

def merge_block(block, x, y):
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j]:
                grid[y + i][x + j] = 1

def remove_row(row):
    del grid[row]
    grid.insert(0, [0] * GRID_WIDTH)

def remove_complete_rows():
    global score
    rows_to_remove = []
    for i in range(GRID_HEIGHT):
        if all(grid[i]):
            rows_to_remove.append(i)
    for row in rows_to_remove:
        remove_row(row)
        score += 10 * GRID_WIDTH

def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    WIN.blit(text, (20, 20))

# Initialize the grid
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Initialize the current block
current_block = random.choice(SHAPES)
current_block_color = random.choice(COLORS)
current_block_x = GRID_WIDTH // 2 - len(current_block[0]) // 2
current_block_y = 0

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(current_block, current_block_x - 1, current_block_y):
                    current_block_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(current_block, current_block_x + 1, current_block_y):
                    current_block_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(current_block, current_block_x, current_block_y + 1):
                    current_block_y += 1
            elif event.key == pygame.K_UP:
                rotated_block = list(zip(*reversed(current_block)))
                if not check_collision(rotated_block, current_block_x, current_block_y):
                    current_block = rotated_block

    # Update block falling
    fall_time += clock.get_rawtime()
    if fall_time / 1000 >= fall_speed:
        if not check_collision(current_block, current_block_x, current_block_y + 1):
            current_block_y += 1
        else:
            merge_block(current_block, current_block_x, current_block_y)
            remove_complete_rows()
            current_block = random.choice(SHAPES)
            current_block_color = random.choice(COLORS)
            current_block_x = GRID_WIDTH // 2 - len(current_block[0]) // 2
            current_block_y = 0
            if check_collision(current_block, current_block_x, current_block_y):
                game_over = True

        fall_time = 0

    # Draw background
    WIN.fill(BLACK)

    # Draw grid and blocks
    draw_grid()
    draw_block(current_block, current_block_x, current_block_y, current_block_color)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j]:
                draw_block([[1]], j, i, WHITE)

    # Draw score
    draw_score()

    # Update the display
    pygame.display.update()
    clock.tick(60)

# Game over message
font = pygame.font.Font(None, 72)
text = font.render("Game Over", True, WHITE)
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
WIN.blit(text, text_rect)
pygame.display.update()

# Wait for a while before quitting
pygame.time.wait(3000)

# Quit the game
pygame.quit()
