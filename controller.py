from model import *


class Game:
    def __init__(self):
        self.board = Board()
        self.next_turn = Player.white


