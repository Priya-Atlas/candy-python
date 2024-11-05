import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
width, height = 400, 400
grid_size = 8
cell_size = width // grid_size
white = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Candy Crush")

# Initialize the grid
grid = [[random.randint(1, 3) for _ in range(grid_size)] for _ in range(grid_size)]
selected_candy = None

def handle_click(row, col):
    global selected_candy
    if selected_candy is None:
        selected_candy = (row, col)
    else:
        row1, col1 = selected_candy
        grid[row][col], grid[row1][col1] = grid[row1][col1], grid[row][col]
        selected_candy = None  # Reset selection after swap

def detect_match():
    matches = set()
    
    # Check for horizontal matches
    for row in range(grid_size):
        for col in range(grid_size - 2):  # Check only until the third last column
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.add((row, col))
                matches.add((row, col + 1))
                matches.add((row, col + 2))

    # Check for vertical matches
    for col in range(grid_size):
        for row in range(grid_size - 2):  # Check only until the third last row
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.add((row, col))
                matches.add((row + 1, col))
                matches.add((row + 2, col))

    return matches

def fill_empty_spaces():
    for col in range(grid_size):
        empty_count = sum(1 for row in range(grid_size) if grid[row][col] == 0)
        for row in range(grid_size - 1, -1, -1):
            if grid[row][col] == 0:
                for r in range(row, 0, -1):
                    grid[r][col] = grid[r - 1][col]
                grid[0][col] = random.randint(1, 3)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            col = event.pos[0] // cell_size
            row = event.pos[1] // cell_size
            if 0 <= row < grid_size and 0 <= col < grid_size:
                handle_click(row, col)

    screen.fill(white)

    # Draw the grid
    for row in range(grid_size):
        for col in range(grid_size):
            candy_type = grid[row][col]
            candy_color = (255, 0, 0) if candy_type == 1 else (0, 255, 0) if candy_type == 2 else (0, 0, 255)
            pygame.draw.rect(screen, candy_color, (col * cell_size, row * cell_size, cell_size, cell_size))

    matches = detect_match()
    for row, col in matches:
        grid[row][col] = 0  # Remove matched candies

    fill_empty_spaces()

    pygame.display.flip()

pygame.quit()


