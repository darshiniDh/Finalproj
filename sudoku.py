# Main function
import pygame
import math
import random
from sudoku_generator import SudokuGenerator, Cell, Board
def draw_screen(screen,board):
    screen.fill((255, 255, 255))
    board.draw()
    button_font = pygame.font.SysFont('Arial', 24)
    button_y = 512 + 20
    reset_button = pygame.Rect(50, button_y, 100, 40)
    restart_button = pygame.Rect(270, button_y, 100, 40)
    exit_button = pygame.Rect(490, button_y, 100, 40)
    for button, text in [(reset_button, "Reset"),
                         (restart_button, "Restart"),
                         (exit_button, "Exit")]:
        pygame.draw.rect(screen, (100, 150, 200), button)
        pygame.draw.rect(screen, (0, 0, 0), button, 2)
        button_text = button_font.render(text, True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button.center)
        screen.blit(button_text, button_text_rect)
    return reset_button, restart_button, exit_button

def initial_board(screen,diff):
    if diff == "easy":
        removed_cells = 30
    elif diff == "medium":
        removed_cells = 40
    else:
        removed_cells = 50
    sudoku_gener = SudokuGenerator(9, removed_cells)
    sudoku_gener.fill_values()
    solution = [row[:] for row in sudoku_gener.get_board()]
    sudoku_gener.remove_cells()
    sudoku_board = sudoku_gener.get_board()

    board = Board(512, 512, screen, diff)
    board.solution = solution

    for row in range(9):
        for col in range(9):
            cell_value = sudoku_board[row][col]
            cell = Cell(cell_value, row, col, screen)
            board.cells[row][col] = cell
            board.original_cell_values[row][col] = cell_value

    return board
def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((640, 640))
        pygame.display.set_caption("Sudoku")

        game = "beg"
        board = None
        diff = None

        button_width = 150
        button_height = 60
        button_spacing = 30
        button_y = 512 * 3 // 4

        easy_button = pygame.Rect(
            (640 // 2 - button_width - button_spacing - button_width // 2,
             button_y - button_height // 2,
             button_width,
             button_height)
        )
        medium_button = pygame.Rect(
            (640 // 2 - button_width // 2,
             button_y - button_height // 2,
             button_width,
             button_height)
        )
        hard_button = pygame.Rect(
            (640 // 2 + button_spacing + button_width // 2,
             button_y - button_height // 2,
             button_width,
             button_height)
        )
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if game == "beg":
                        if easy_button.collidepoint(mouse_pos):
                            diff = "easy"
                            board = initial_board(screen, diff)
                            game = "playing"
                        elif medium_button.collidepoint(mouse_pos):
                            diff = "medium"
                            board = initial_board(screen, diff)
                            game = "playing"
                        elif hard_button.collidepoint(mouse_pos):
                            diff = "hard"
                            board = initial_board(screen, diff)
                            game = "playing"

                    elif game == "playing":
                        if reset_button.collidepoint(mouse_pos):
                            board.reset_to_original()
                        elif restart_button.collidepoint(mouse_pos):
                            game = "beg"
                            board = None
                        elif exit_button.collidepoint(mouse_pos):
                            running = False
                        else:
                            clicked = board.click(mouse_pos[0], mouse_pos[1])
                            if clicked:
                                board.select(clicked[0], clicked[1])
            if game == "beg":

                white = (255, 255, 255)
                black = (0, 0, 0)
                button_color = (100, 150, 200)

                font = pygame.font.SysFont('Arial', 48)
                button_font = pygame.font.SysFont('Arial', 32)

                text_welcome = font.render("Welcome to Sudoku", True, black)
                text_rect = text_welcome.get_rect()
                text_rect.center = (640 // 2, 512 // 4)

                text_select = font.render("Select Game Mode", True, black)
                text_select_rect = text_select.get_rect()
                text_select_rect.center = (640 // 2, 512 // 2)

                screen.fill(white)
                screen.blit(text_welcome, text_rect)
                screen.blit(text_select, text_select_rect)

                mouse_pos = pygame.mouse.get_pos()

                for button, text in [(easy_button, "Easy"),
                                     (medium_button, "Medium"),
                                     (hard_button, "Hard")]:
                    color = button_color
                    pygame.draw.rect(screen, color, button)
                    pygame.draw.rect(screen, black, button, 2)  # Border

                    button_text = button_font.render(text, True, black)
                    button_text_rect = button_text.get_rect(center=button.center)
                    screen.blit(button_text, button_text_rect)
            elif game == "playing":
                reset_button, restart_button, exit_button = draw_screen(screen, board)
            pygame.display.flip()




    finally:
        pygame.quit()


if __name__ == "__main__":
    main()