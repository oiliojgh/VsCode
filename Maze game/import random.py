import random

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 10
PACMAN = 'P'
GHOST = 'G'
COIN = 'C'
WALL = 'W'
EMPTY = ' '

# Initialize grid
grid = [[EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Add walls
wall_positions = [(0, 2), (1, 2), (2, 2), (3, 2), (5, 2), (6, 2), (7, 2), (8, 2)]
for x, y in wall_positions:
    grid[y][x] = WALL

# Add Pac-Man
pacman_x, pacman_y = 4, 4
grid[pacman_y][pacman_x] = PACMAN

# Add Ghost
ghost_x, ghost_y = 0, 0
grid[ghost_y][ghost_x] = GHOST

# Add coins
num_coins = 5
for _ in range(num_coins):
    coin_x, coin_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
    while grid[coin_y][coin_x] != EMPTY:
        coin_x, coin_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
    grid[coin_y][coin_x] = COIN

# Display grid
def display_grid():
    for row in grid:
        print(' '.join(row))

display_grid()