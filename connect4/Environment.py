from Board import Board
from Cell import Cell
from typing import Tuple

class Environment(object):
    '''
    Class that serves as an interface that Players use to interact with the Board
    Environment manages which player is currently active, manages when the game is over,
        manages hwo the board state is represented to players, etc.
    '''

    def __init__(self, board_w=7, board_h=7, num_to_win=4):
        self.b = Board(board_w, board_h, num_to_win=num_to_win)
        self.cur_player = Cell.RED
        self.num_actions = board_w
        self.is_game_over = False
        self.num_moves: int = 0
        self.last_move = None  # last move in game (col, row)
        self.history = []  # history will be a list of tuples (state, action, reward)

    def get_num_cells(self) -> int:
        return self.b.get_num_cells()

    def reset(self) -> None:
        h, w, ntw = self.b.height, self.b.width, self.b.num_to_win
        self.b = Board(width=w, height=h, num_to_win=ntw)
        self.cur_player = Cell.RED
        self.is_game_over = False
        self.num_moves = 0
        self.last_move = None
        self.history = []

    def _actually_take_action(self, col: int) -> float:
        '''
        Moves the current player into the column specified by 'col'
        Returns the score of the last move: -1 if illegal, 1 if winning, 0 otherwise
        '''
        state = self.get_state()

        try:
            row = self.b.move(col, self.cur_player)
        except ValueError:  # illegal moves cause game over
            self.is_game_over = True
            return -1
        self.last_move = (col, row)

        # change current player
        self.cur_player = Cell.RED if self.cur_player == Cell.BLACK else Cell.BLACK
        self.num_moves += 1

        # check if any legal moves remain
        if self.num_moves >= self.get_num_cells():
            self.is_game_over = True

        if self.b.check_winning_move(col, row):
            self.is_game_over = True
            return 1

        return 0

    def take_action(self, col: int) -> float:
        '''
        Moves the current player into the specified column.
        Also records history for the move
        Returns the reward for making such a move
        '''
        state = self.get_state()
        reward = self._actually_take_action(col)
        self.history.append((state, col, reward))
        return reward

    def get_state(self) -> str:
        '''
        Board's __str__ method returns a string of 0s 1s and 2s (for empty, red, black cells as per the Cell enum)
        This method converts such a string to Es, Ms, and Ys which stand for Empty, My cells, and Your cells
        '''

        board_str = str(self.b)
        if self.cur_player == Cell.BLACK:
            board_str = board_str.replace(str(Cell.BLACK.value), 'M')  # Mine
            board_str = board_str.replace(str(Cell.RED.value), 'Y')    # Yours
            board_str = board_str.replace(str(Cell.EMPTY.value), 'E')  # Empty
        else:
            board_str = board_str.replace(str(Cell.RED.value), 'M')    # Mine
            board_str = board_str.replace(str(Cell.BLACK.value), 'Y')  # Yours
            board_str = board_str.replace(str(Cell.EMPTY.value), 'E')  # Empty
        return board_str
