from abc import ABC

class Player(ABC):
    def __init__(self):
        self.is_human = False

    def move(self, game_state: str) -> int:
        pass
