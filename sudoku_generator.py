
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



 def is_full(self):
        #Returns a Boolean value indicating whether the board is full or not.

    def update_board(self):
           # Updates the underlying 2D board with the values in all cells.
        # meant to update the board with the values that are entered (not sketched)?

    def find_empty(self):
            # Finds an empty cell and returns its row and col as a tuple(x, y).
            #do I need to continuously find empty cells
        for x in range(0, self.row_length):
            for y in range(0, self.row_length):
                if self.board[x][y] == 0:
                    return (x, y) #returning if a tuple


    def check_board(self):
            #Check whether the Sudoku board is solved correctly.






class Cell:
    def __init__(self, value, row, col, screen):
        #Constructor for the Cell class
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen

    def set_cell_value(self, value):
        #Setter for this cell’s value
        # set a cell value = after user presses enter
        #do i need a way to tell if user presses enter or not? - or in UI
        self.value = value

    def set_sketched_value(self, value):
        #Setter for this cell’s sketched value
        #sketched value = before the user presses enter
        self.value = value

    def draw(self): #Draws this cell, along with the value inside it.
        # how to draw cell? -
        if self.value != 0: # If this cell has a nonzero value, that value is displayed.
