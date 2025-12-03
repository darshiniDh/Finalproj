import pygame
import math
import random
from sudoku_generator import SudokuGenerator, Cell, Board

WIDTH, HEIGHT = 660, 660


def draw_screen(screen, board):
    screen.fill((255, 255, 255))
    board.draw()
    button_font = pygame.font.SysFont('Arial', 24)
    button_y = 600 + 20
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


def initial_board(screen, diff):
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

    board = Board(600, 600, screen, diff)
    board.solution = solution

    for row in range(9):
        for col in range(9):
            cell_value = sudoku_board[row][col]
            cell = Cell(cell_value, row, col, screen)
            board.cells[row][col] = cell
            board.original_cell_values[row][col] = cell_value

    return board


def show_end_screen(screen, won=True):
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('Arial', 48)
    message = "Game Won!" if won else "Game Over :("
    color = (0, 200, 0) if won else (200, 0, 0)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(320, 200))
    screen.blit(text, text_rect)

    button_font = pygame.font.SysFont('Arial', 32)
    restart_button = pygame.Rect(180, 300, 120, 50)
    exit_button = pygame.Rect(340, 300, 120, 50)

    for button, text in [(restart_button, "Restart"), (exit_button, "Exit")]:
        pygame.draw.rect(screen, (100, 150, 200), button)
        pygame.draw.rect(screen, (0, 0, 0), button, 2)
        button_text = button_font.render(text, True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button.center)
        screen.blit(button_text, button_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if restart_button.collidepoint(pos):
                    return "restart"
                elif exit_button.collidepoint(pos):
                    return None


def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        reset_button = restart_button = exit_button = None

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
                        if reset_button and reset_button.collidepoint(mouse_pos):
                            board.reset_to_original()
                        elif restart_button and restart_button.collidepoint(mouse_pos):
                            game = "beg"
                            board = None
                        elif exit_button and exit_button.collidepoint(mouse_pos):
                            running = False
                        else:
                            clicked = board.click(mouse_pos[0], mouse_pos[1])
                            if clicked:
                                board.select(clicked[0], clicked[1])
                if event.type == pygame.KEYDOWN and game == "playing":
                    if board.selected_cell_position:
                        r, c = board.selected_cell_position
                        if event.key == pygame.K_LEFT:
                            board.select(r, max(0, c - 1))
                        elif event.key == pygame.K_RIGHT:
                            board.select(r, min(8, c + 1))
                        elif event.key == pygame.K_UP:
                            board.select(max(0, r - 1), c)
                        elif event.key == pygame.K_DOWN:
                            board.select(min(8, r + 1), c)
                        elif pygame.K_1 <= event.key <= pygame.K_9:
                            board.sketch(event.key - pygame.K_0)
                        elif event.key == pygame.K_RETURN:
                            cell = board.cells[r][c]
                            if cell.sketched_value != 0:
                                board.place_number(cell.sketched_value)
                        elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                            board.clear()

            if game == "beg":
                white = (255, 255, 255)
                black = (0, 0, 0)
                button_color = (100, 150, 200)

                font = pygame.font.SysFont('Arial', 48)
                button_font = pygame.font.SysFont('Arial', 32)

                text_welcome = font.render("Welcome to Sudoku", True, black)
                text_rect = text_welcome.get_rect()
                text_rect.center = (640 // 2, 512 // 4)

                text_select = font.render("Select Game Mode:", True, black)
                text_select_rect = text_select.get_rect()
                text_select_rect.center = (640 // 2, 512 // 2)

                screen.fill(white)
                screen.blit(text_welcome, text_rect)
                screen.blit(text_select, text_select_rect)

                for button, text in [(easy_button, "Easy"),
                                     (medium_button, "Medium"),
                                     (hard_button, "Hard")]:
                    pygame.draw.rect(screen, button_color, button)
                    pygame.draw.rect(screen, black, button, 2)
                    button_text = button_font.render(text, True, black)
                    button_text_rect = button_text.get_rect(center=button.center)
                    screen.blit(button_text, button_text_rect)
            elif game == "playing":
                reset_button, restart_button, exit_button = draw_screen(screen, board)
                if board.is_full():
                    if board.check_board():
                        result = show_end_screen(screen, won=True)
                    else:
                        result = show_end_screen(screen, won=False)
                    if result == "restart":
                        game = "beg"
                        board = None

            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()