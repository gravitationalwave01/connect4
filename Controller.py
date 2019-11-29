import pygame
import sys
from Board import Board
from Cell import Cell
from Drawer import Drawer
from AI import DummyAI, QLearningAI
import pickle
import time
import os
from copy import deepcopy

def process_key(event):
    if event.key == pygame.K_1:
        return 0
    if event.key == pygame.K_2:
        return 1
    if event.key == pygame.K_3:
        return 2
    if event.key == pygame.K_4:
        return 3
    if event.key == pygame.K_5:
        return 4
    if event.key == pygame.K_6:
        return 5
    if event.key == pygame.K_7:
        return 6
    if event.key == pygame.K_8:
        return 7
    if event.key == pygame.K_9:
        return 8

    raise ValueError('Invalid key')




if __name__ == "__main__":

    pygame.init()
    use_ai = True
    train = True
    load_saved = True

    board_h = 7
    board_w = 7

    b = Board(board_w, board_h, 4)
    drawer = Drawer()
    drawer.draw_board(b, pygame.Color('gray'))

    cur_player = Cell.BLACK

    game_active = True

    if use_ai:
        if load_saved:
            # get most recent version of model, based on filename
            files = os.listdir('data/')
            stamps = [int(fname.split('_')[1][:-4]) for fname in files]
            newest_model_fname = f'qlearning_{max(stamps)}.pkl'
            with open('data/'+newest_model_fname, 'rb') as f:
                ai = pickle.load(f)
        else:
            ai = QLearningAI(b)

    if train:
        second_ai = deepcopy(ai)

    counter = 0
    while game_active:
        print(f'making move {counter}')
        counter+=1
        time.sleep(0.5)
        col = None
        ai_turn = use_ai and cur_player == Cell.RED
        if ai_turn:
            col = ai.move(b)
        elif train:
            col = second_ai.move(b)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type != pygame.KEYDOWN:
                    continue

                try:
                    col = process_key(event)
                    break  # only process one valid move from user
                except ValueError as e:
                    drawer.show_message(f'{str(e)}')
                    continue

        if col is None:
            continue

        try:
            row = b.move(col, cur_player)
        except ValueError as e:
            drawer.show_message(f'{str(e)}')
            if ai_turn:
                ai.update(b, win=False, illegal=True)
            continue

        drawer.draw_cell(col, row, cur_player, True)
        game_won = b.check_winning_move(col, row)
        if ai_turn:
            ai.update(b, win=game_won, illegal=False)

        if game_won:
            winner = cur_player.name
            drawer.show_message(f'Congratulations! Player {winner} wins!')
            game_active = False

            # save model
            stamp = int(time.time())
            fname = f'qlearning_{stamp}.pkl'
            with open('data/' + fname, 'wb') as f:
                pickle.dump(ai, f)

        # change current player
        if cur_player == Cell.BLACK:
            cur_player = Cell.RED
        else:
            cur_player = Cell.BLACK
