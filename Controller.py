import pygame
import sys
from Board import Board
from Cell import Cell
from Drawer import Drawer

def process_key(event, b:Board):
    if event.key == pygame.K_1:
        col, row = b.move(0, cur_player)
    elif event.key == pygame.K_2:
        col, row = b.move(1, cur_player)
    elif event.key == pygame.K_3:
        col, row = b.move(2, cur_player)
    elif event.key == pygame.K_4:
        col, row = b.move(3, cur_player)
    elif event.key == pygame.K_5:
        col, row = b.move(4, cur_player)
    elif event.key == pygame.K_6:
        col, row = b.move(5, cur_player)
    elif event.key == pygame.K_7:
        col, row = b.move(6, cur_player)
    elif event.key == pygame.K_8:
        col, row = b.move(7, cur_player)
    elif event.key == pygame.K_9:
        col, row = b.move(8, cur_player)
    else:
        raise ValueError('Invalid key')

    return col, row


if __name__ == "__main__":

    pygame.init()

    board_h = 7
    board_w = 7

    b = Board(board_w, board_h, 4)
    drawer = Drawer()
    drawer.draw_board(b, pygame.Color('gray'))

    cur_player = Cell.BLACK
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                try:
                    col, row = process_key(event, b)
                except ValueError as e:
                    if 'Invalid key' in str(e) or 'Illegal move' in str(e):
                        drawer.show_message('Invalid move!')
                    continue
                drawer.draw_cell(col, row, cur_player, True)
                if b.check_winning_move(col, row):
                    winner = cur_player.name
                    drawer.show_message(f'Congratulations! Player {winner} wins!')

                # change current player
                if cur_player == Cell.BLACK:
                    cur_player = Cell.RED
                else:
                    cur_player = Cell.BLACK
