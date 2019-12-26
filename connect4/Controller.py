import pygame
from connect4.Cell import Cell
from connect4.Drawer import Drawer
from connect4.Environment import Environment
from connect4.player.RandomAIPlayer import RandomAIPlayer
from connect4.player.DeepQLearningPlayer import DeepQLearningPlayer
from connect4.player.HumanPlayer import HumanPlayer
from enum import Enum
import pickle
import os
import time

class GameMode(Enum):
    HUMAN_HUMAN = 0
    HUMAN_AI = 1
    AI_AI = 2

class Controller(object):
    def __init__(self, num_humans=2, board_w=7, board_h=7, num_to_win=4, num_games=1):
        self.env = Environment(board_w=board_w, board_h=board_h, num_to_win=num_to_win)
        self.num_games = num_games
        self.history = []
        if num_humans == 0:
            self.mode = GameMode.AI_AI
            self.player1 = RandomAIPlayer(num_cols=board_w)
            self.player2 = RandomAIPlayer(num_cols=board_w)
            self.use_gui = False
        elif num_humans == 1:
            self.mode = GameMode.HUMAN_AI
            self.player1 = HumanPlayer()
            self.player2 = DeepQLearningPlayer(num_cols=board_w)
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

    def play_one_game(self):
        while not self.env.is_game_over:
            self._one_move()

        # display game over
        if self.use_gui:
            winner = self.env.cur_player.name
            self.drawer.show_message(f'Congratulations! Player {winner} wins!')
            pygame.time.delay(2000)

    def play(self):
        for i in range(self.num_games):
            self.play_one_game()
            self.history += self.env.history
            self.env.reset()

            # reset the GUI
            if self.use_gui:
                self.drawer.draw_board(self.env.b, pygame.Color('gray'))
                self.drawer.clear_message()

        if self.mode == GameMode.AI_AI:
            fname = f'gamelog_{round(time.time())}.txt'
            fname = os.path.join('data', fname)
            with open(fname, 'wb') as f:
                pickle.dump(self.history, f)


if __name__ == "__main__":

    # controller = Controller(board_w=3, board_h=3, num_to_win=2, num_humans=0, num_games=4)
    controller = Controller(num_humans=1, num_games=1)
    controller.play()
