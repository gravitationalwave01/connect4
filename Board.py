import numpy as np
from Cell import Cell

class Board:

    def __init__(self, width=7, height=7, num_to_win = 4):
        self.width = width
        self.height = height
        self.cells = np.full((width, height), Cell.EMPTY)
        self.num_to_win = num_to_win

    def find_top(self, col):

        for i, cell in enumerate(self.cells[col]):
            if cell == Cell.EMPTY:
                return i

        return self.height

    def move(self, col, color):

        if col >= self.width:
            raise ValueError('Illegal move')

        row = self.find_top(col)
        if row == self.height:
            raise ValueError('Illegal move')

        self.cells[col, row] = color

        return col, row

    def check_for_connect(self, arr, color):
        counter = 0
        for c in arr:
            if c == color:
                counter += 1
            if counter == self.num_to_win:
                return True
        return False

    def check_winning_move(self, col, row):
        '''Returns true if the cell identified has a winning combination'''
        winner = self.cells[col, row]

        # check up/down:
        if self.check_for_connect(self.cells[col, :], winner):
            return True

        # check left/right
        if self.check_for_connect(self.cells[:, row], winner):
            return True

        # check second diagonal
        if self.check_for_connect(np.diag(self.cells, k=row - col), winner):
            return True

        # check main diagonal
        if self.check_for_connect(np.diag(np.fliplr(self.cells), k=self.width-(col+row+1)), winner):
            return True

        return False

