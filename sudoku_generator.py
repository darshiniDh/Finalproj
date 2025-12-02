
import math,random
import pygame
"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

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
                removed += 1#

    def generate_sudoku(size, removed):
        sudoku = SudokuGenerator(size, removed)
        sudoku.fill_values()
        board = sudoku.get_board()
        sudoku.remove_cells()
        board = sudoku.get_board()
        return board



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
                    self.cells[row_index][column_index].draw()

    def select(self, row_index, column_index):
        if 0 <= row_index < self.total_rows and 0 <= column_index < self.total_columns:
            self.selected_cell_position = (row_index, column_index)

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
        for row_index in range(self.total_rows):
            for column_index in range(self.total_columns):
                if self.cells[row_index][column_index]:
                    self.original_cell_values[row_index][column_index] = self

    def find_empty(self):
        for row_index in range(self.total_rows):
            for column_index in range(self.total_columns):
                if self.cells[row_index][column_index] and self.cells[row_index][column_index].get_cell_value() == 0:
                    return (row_index, column_index)
        return None

    def check_board(self):
        for row_index in range(self.total_rows):
            for column_index in range(self.total_columns):
                if self.cells[row_index][column_index].value != self.solution[row_index][column_index]:
                    return False
        return True

class Cell:
    def __init__(self, value, row, col, screen):
        #Constructor for the Cell class
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False

    def set_cell_value(self, value):
        #Setter for this cell’s value
        # set a cell value = after user presses enter
        #do i need a way to tell if user presses enter or not? - or in UI

        self.value = value

    def set_sketched_value(self, value):
        #Setter for this cell’s sketched value
        #make a sketched value vari. and assign sketched value
        self.sketched_value = value



    def draw(self): #Draws this cell, along with the value inside it.
        #anything draw is pygame
        # how to draw cell? - draw cell when user clicks the enter button
        red = (255, 0, 0) #selected cell is the red color
        green = (0, 255, 0) #placeholder cell color
        r = pygame.Rect(self.col, self.row, 640/81, 512/81) #use numbers for width and height
        if self.value != 0: # If this cell has a nonzero value, that value is displayed.
            pygame.draw.rect(self.screen, green, r)#rect. draw number

        elif self.sketched_value != 0: #user sketched an actual value
            pygame.draw.rect(self.screen, green, r)
        elif self.value == 0: #then just draw the cell
            pygame.draw.rect(self.screen, green, r)

        # if self.selected:
        #     pygame.draw.rect()

