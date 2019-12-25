import pygame
from abc import ABC

def process_key(event: pygame.event) -> int:
    '''
    Given a pygame event, determine whether the event is a keyboard number press
    If yes, return the number of the key
    If no, raise an exception
    '''
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


class Player(ABC):
    def __init__(self):
        self.is_human = False

    def move(self, game_state: str) -> int:
        pass

class HumanPlayer(Player):
    # TODO: this needs a lotta work
    #  - How should Player interact with the GUI? Should it at all?
    #  - How should Player interact with the keyboard? Should it?
    def __init__(self):
        super().__init__()
        self.is_human = True

    def move(self, game_state: str) -> int:
        # wait for human player to make a move
        move_accepted = False
        while not move_accepted:
            for event in pygame.event.get():
                if event.type != pygame.KEYDOWN:
                    continue

                try:
                    col = process_key(event)
                    move_accepted = True
                    break  # only process one valid move from user
                except ValueError as e:
                    # TODO: show an "illegal move" warning to the player
                    continue

        return col


class AIPlayer(Player):
    def __init__(self):
        super().__init__()
        self.is_human = False

    def move(self, game_state: str) -> int:
        return 0

