import math,random
import pygame
"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

Resources used: https://www.pygame.org/docs/ref/rect.html, GeeksforGeeks pygame functions documentation

"""

class SudokuGenerator():
    def __init__(self, row_length=9, removed_cells=0):
        self.row_length=row_length
        self.removed_cells=removed_cells
        self.board = []
        for i in range(row_length):
            row = []
            for j in range(row_length):
                row.append(0)
            self.board.append(row)
        self.box_length = 3

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        else:
            return True

    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start,row_start+3):
            for col in range(col_start,col_start+3):
                if self.board[row][col]==num:
                    return False
        return True

    def is_valid(self, row, col, num):
        box_row_beg = (row//3) * 3
        box_col_beg = (col// 3) * 3

        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(box_row_beg, box_col_beg, num))

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)

        num_index = 0
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                self.board[i][j] = nums[num_index]
                num_index += 1

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            row_i = random.randint(0, 8)
            col_i = random.randint(0, 8)
            if self.board[row_i][col_i] != 0:
                self.board[row_i][col_i] = 0
                removed += 1

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    solution = []
    for row in sudoku.get_board():
        solution.append(row[:])
    sudoku.remove_cells()
    puzzle = sudoku.get_board()
    return puzzle, solution

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def get_cell_value(self):
        return self.value

    def draw(self, board_width, total_columns):
        cell_size = board_width // total_columns
        x = self.col * cell_size
        y = self.row * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        if self.selected:
            pygame.draw.rect(self.screen, (220, 20, 60), rect, 3)
        if self.value != 0:
            font = pygame.font.SysFont('Arial', cell_size // 2)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, text.get_rect(center=rect.center))
        elif self.sketched_value != 0:
            font = pygame.font.SysFont('Arial', cell_size // 3)
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.total_rows = 9
        self.total_columns = 9
        self.selected_cell_position = None

        self.cells = []
        for row_index in range(self.total_rows):
            row_list = []
            for column_index in range(self.total_columns):
                row_list.append(None)
            self.cells.append(row_list)

        self.original_cell_values = []
        for row_index in range(self.total_rows):
            row_list = []
            for column_index in range(self.total_columns):
                row_list.append(0)
            self.original_cell_values.append(row_list)

        removed_map = {"easy": 30, "medium": 40, "hard": 50}
        if difficulty in removed_map:
            removed = removed_map[difficulty]
        else:
            removed = 40

        puzzle, solution = generate_sudoku(9, removed)
        self.solution = solution

        for r in range(self.total_rows):
            for c in range(self.total_columns):
                val = puzzle[r][c]
                cell = Cell(val, r, c, screen)
                self.cells[r][c] = cell
                self.original_cell_values[r][c] = val

    def draw(self):
        cell_size = self.width // self.total_columns
        for line_index in range(self.total_rows + 1):
            if line_index % 3 == 0:
                line_thickness = 3
            else:
                line_thickness = 1

            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, line_index * cell_size),
                             (self.width, line_index * cell_size),
                             line_thickness)

            pygame.draw.line(self.screen, (0, 0, 0),
                             (line_index * cell_size, 0),
                             (line_index * cell_size, self.height),
                             line_thickness)

        for row_index in range(self.total_rows):
            for column_index in range(self.total_columns):
                if self.cells[row_index][column_index]:
                    self.cells[row_index][column_index].draw(self.width, self.total_columns)

    def select(self, row_index, column_index):
        if 0 <= row_index < self.total_rows and 0 <= column_index < self.total_columns:
            if self.selected_cell_position:
                r, c = self.selected_cell_position
                self.cells[r][c].selected = False
            self.selected_cell_position = (row_index, column_index)
            self.cells[row_index][column_index].selected = True

    def click(self, x_position, y_position):
        cell_size = self.width // self.total_columns
        if x_position < self.width and y_position < self.height:
            row_index = y_position // cell_size
            column_index = x_position // cell_size
            return (row_index, column_index)
        return None

    def clear(self):
        if self.selected_cell_position:
            row_index, column_index = self.selected_cell_position
            if self.cells[row_index][column_index]:
                if self.original_cell_values[row_index][column_index] == 0:
                    self.cells[row_index][column_index].set_cell_value(0)
                    self.cells[row_index][column_index].set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell_position:
            row_index, column_index = self.selected_cell_position
            if self.cells[row_index][column_index]:
                self.cells[row_index][column_index].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell_position:
            row_index, column_index = self.selected_cell_position
            if self.cells[row_index][column_index]:
                if self.original_cell_values[row_index][column_index] == 0:
                    self.cells[row_index][column_index].set_cell_value(value)

    def reset_to_original(self):
        for row_index in range(self.total_rows):
            for column_index in range(self.total_columns):
                if self.cells[row_index][column_index]:
                    self.cells[row_index][column_index].set_cell_value(
                        self.original_cell_values[row_index][column_index])
                    self.cells[row_index][column_index].set_sketched_value(0)

    def is_full(self):
        for row_index in range(self.total_rows):
            for column_index in range(self.total_columns):
                if self.cells[row_index][column_index] and self.cells[row_index][column_index].get_cell_value() == 0:
                    return False
        return True

    def update_board(self):
        self.current_values = [
            [self.cells[row_index][column_index].get_cell_value()
             for column_index in range(self.total_columns)]
            for row_index in range(self.total_rows)
        ]

    def find_empty(self):
        for row_index in range(self.total_rows):
            for column_index in range(self.total_columns):
                if self.cells[row_index][column_index] and self.cells[row_index][column_index].get_cell_value() == 0:
                    return (row_index, column_index)
        return None

    def check_board(self):
        for row_index in range(self.total_rows):
            for column_index in range(self.total_columns):
                if self.cells[row_index][column_index].get_cell_value() != self.solution[row_index][column_index]:
                    return False
        return True


