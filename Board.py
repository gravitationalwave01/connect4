import numpy as np
from Cell import Cell

class Board:

    def __init__(self, width=7, height=7, num_to_win = 4):
        self.width = width
        self.height = height
        self.cells = np.full((width, height), Cell.EMPTY)
        self.num_to_win = num_to_win

    def find_top(self, col):
        '''
        For a given column, returns the index of the topmost empty cell
        '''
        for i, cell in enumerate(self.cells[col]):
            if cell != Cell.EMPTY:
                return i - 1

        return self.height - 1

    def move(self, col, color):
        '''
        Updates the col column of the Board with the passed in color
        Raises ValueError if the column specified is already full (illegal move)
        '''
        if col >= self.width:
            raise ValueError('Illegal move')

        row = self.find_top(col)
        if row == -1:
            raise ValueError('Illegal move')

        self.cells[col, row] = color

        return col, row

    def check_for_connect(self, arr, color):
        '''
        For a given array, returns True if the array contains a winning streak (4 in a row) for the given color
        Returns False otherwise
        '''
        counter = 0
        for c in arr:
            if c == color:
                counter += 1
            else:
                counter = 0
            if counter == self.num_to_win:
                return True
        return False

    def check_winning_move(self, col, row):
        '''
        For a given cell, returns True if the cell is part of a winning combination
        Returns False otherwise
        '''
        winner = self.cells[col, row]

        # check up/down:
        if self.check_for_connect(self.cells[col, :], winner):
            print('up-down found a win!!')
            return True

        # check left/right
        if self.check_for_connect(self.cells[:, row], winner):
            print('left-right found a win!!')
            return True

        # check second diagonal
        if self.check_for_connect(np.diag(self.cells, k=row - col), winner):
            print(f'second diag found a win!! {np.diag(self.cells, k=row - col)}')
            return True

        # check main diagonal
        if self.check_for_connect(np.diag(np.fliplr(self.cells), k=self.width-(col+row+1)), winner):
            print(f'first diag found a win!! {np.diag(np.fliplr(self.cells), k=self.width-(col+row+1))}')
            return True

        return False

