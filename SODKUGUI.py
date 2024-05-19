import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 540
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
FONT = pygame.font.SysFont('arial', 35)
LINE_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 255, 0)

# Sample Sudoku Puzzle
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Initialize the screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Sudoku')

# Helper function to draw grid lines
def draw_grid():
    for i in range(GRID_SIZE + 1):
        line_thickness = 1 if i % 3 != 0 else 3
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), line_thickness)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), line_thickness)

# Helper function to draw numbers
def draw_numbers():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if sudoku_board[row][col] != 0:
                text_surface = FONT.render(str(sudoku_board[row][col]), True, LINE_COLOR)
                screen.blit(text_surface, (col * CELL_SIZE + 15, row * CELL_SIZE + 10))

# Main loop
def main():
    selected = None
    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_grid()
        draw_numbers()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                selected = (y // CELL_SIZE, x // CELL_SIZE)
            elif event.type == pygame.KEYDOWN:
                if selected:
                    row, col = selected
                    if event.unicode.isdigit():
                        sudoku_board[row][col] = int(event.unicode)

        if selected:
            row, col = selected
            pygame.draw.rect(screen, SELECTED_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

        pygame.display.flip()

if __name__ == '__main__':
    main()
