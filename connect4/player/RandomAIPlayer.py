from Player import Player
import numpy as np

class RandomAIPlayer(Player):
    '''
    Contains logic for an AI that moves randomly
    '''
    def __init__(self, num_cols):
        self.num_actions = num_cols

    def move(self, state: str) -> int:
        return np.random.randint(0, self.num_actions)
