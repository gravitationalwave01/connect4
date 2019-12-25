import pygame
from Cell import Cell
from Drawer import Drawer
from Environment import Environment
from Player import HumanPlayer, AIPlayer
from enum import Enum

class GameMode(Enum):
    HUMAN_HUMAN = 0
    HUMAN_AI = 1
    AI_AI = 2

class Controller(object):
    def __init__(self, num_humans: int, board_w=7, board_h=7, num_to_win=4):
        self.env = Environment(board_w=board_w, board_h=board_h, num_to_win=num_to_win)
        if num_humans == 0:
            self.mode = GameMode.AI_AI
            self.player1 = AIPlayer()
            self.player2 = AIPlayer()
            self.use_gui = False
        elif num_humans == 1:
            self.mode = GameMode.HUMAN_AI
            self.player1 = HumanPlayer()
            self.player2 = AIPlayer()
            self.use_gui = True
        elif num_humans == 2:
            self.mode = GameMode.HUMAN_HUMAN
            self.player1 = HumanPlayer()
            self.player2 = HumanPlayer()
            self.use_gui = True
        else:
            raise ValueError(f'Number of human players must be 0, 1, or 2. You specified {num_humans}')

        if self.use_gui:
            pygame.init()
            self.drawer = Drawer()
            self.drawer.draw_board(self.env.b, pygame.Color('gray'))

    def _one_move(self):
        cur_state = self.env.get_state()
        if self.env.cur_player == Cell.RED:
            move = self.player1.move(cur_state)
        else:
            move = self.player2.move(cur_state)

        _ = self.env.take_action(move)  # result of the move is ignored

        if self.use_gui:
            col, row = self.env.last_move
            player = self.env.cur_player
            self.drawer.draw_cell(col, row, player, update=True)


    def play(self):
        while not self.env.is_game_over:
            self._one_move()

        # display game over
        if self.use_gui:
            winner = self.env.cur_player.name
            self.drawer.show_message(f'Congratulations! Player {winner} wins!')


if __name__ == "__main__":

    controller = Controller(num_humans=2)
    controller.play()
