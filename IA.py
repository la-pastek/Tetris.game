import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre de jeu
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Dimensions de la grille
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 0, 0)
]

# Formes de Tetris
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    draw_grid_lines(surface)


def draw_grid_lines(surface):
    """

    :param surface:
    :return:
    """
    for y in range(GRID_HEIGHT):
        pygame.draw.line(surface, WHITE, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))
    for x in range(GRID_WIDTH):
        pygame.draw.line(surface, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))

def draw_tetrimino(surface, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetrimino.color, ((tetrimino.x + x) * BLOCK_SIZE, (tetrimino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def valid_space(tetrimino, grid):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                if x + tetrimino.x < 0 or x + tetrimino.x >= GRID_WIDTH or y + tetrimino.y >= GRID_HEIGHT:
                    return False
                if grid[y + tetrimino.y][x + tetrimino.x] != BLACK:
                    return False
    return True

def clear_rows(grid, locked):
    increment = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        row = grid[y]
        if BLACK not in row:
            increment += 1
            ind = y
            for x in range(GRID_WIDTH):
                del locked[(x, y)]
    if increment > 0:
        for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + increment)
                locked[new_key] = locked.pop(key)
    return increment

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    locked_positions = {}
    grid = create_grid(locked_positions)
    logo = pygame.image.load("Logo.png")
    pygame.display.set_icon(logo)

    change_tetrimino = False
    current_tetrimino = Tetrimino(random.choice(SHAPES))
    next_tetrimino = Tetrimino(random.choice(SHAPES))
    fall_time = 0
    level_time = 0
    score = 0

    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.20

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetrimino.x -= 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.x += 1
                if event.key == pygame.K_RIGHT:
                    current_tetrimino.x += 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.x -= 1
                if event.key == pygame.K_DOWN:
                    current_tetrimino.y += 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.y -= 1
                if event.key == pygame.K_UP:
                    current_tetrimino.rotate()
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.rotate()
                        current_tetrimino.rotate()
                        current_tetrimino.rotate()

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_tetrimino.y += 1
            if not valid_space(current_tetrimino, grid) and current_tetrimino.y > 0:
                current_tetrimino.y -= 1
                change_tetrimino = True

        shape_pos = [(current_tetrimino.x + x, current_tetrimino.y + y) for y, row in enumerate(current_tetrimino.shape) for x, cell in enumerate(row) if cell]

        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_tetrimino.color

        if change_tetrimino:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_tetrimino.color
            current_tetrimino = next_tetrimino
            next_tetrimino = Tetrimino(random.choice(SHAPES))
            change_tetrimino = False
            score += clear_rows(grid, locked_positions) * 10

        draw_grid(screen, grid)
        draw_tetrimino(screen, current_tetrimino)
        pygame.display.update()

        if any(y <= 0 for (x, y) in locked_positions):
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()
