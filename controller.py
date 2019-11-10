from model import *
from terminalView import *
from itertools import cycle


class Controller:
    def __init__(self):
        self.game = Game()
        self.player_iterator = cycle([Player.red, Player.white])
        self._change_player()

    def start_game(self):
        self.dialog = Dialog()
        self.dialog.show_intro()

        while True:
            options = self.game.get_movable_pieces(self.current_player)
            self._print_board()
            piece, dest = self._get_next_move(options)
            self.game.move(piece, dest)
            # todo: check if player is obliged to do another move...
            # todo: check if endgame
            self._change_player()

    def _get_next_move(self, options):
        piece_addrs = list(options.keys())
        piece_ids = self.game._addr_to_id(piece_addrs)
        while True:
            piece_id = self.dialog.get_piece(piece_ids)
            piece = piece_ids[piece_id]
            self._print_board(piece_id, options[piece])
            dest = self.dialog.get_dest(options[piece])
            if dest == 0:
                continue
            else:
                return piece, dest

    def _change_player(self):
        self.current_player = next(self.player_iterator)

    def _print_board(self, selected=None, moves=None):
        print_board(self.game.get_board(), selected, moves)

    def _move(self, id, dest):
        self.game.move(id, dest)


class Dialog:
    def __init__(self):
        self.intro_msg = "Hello. Thats intro with tutorial."
        self.whose_turn_msg = ""
        self.select_piece_msg = "Please enter piece id you would like to move..."
        self.select_destination_msg = "Now please enter number with destination field or 0 to select different piece..."
        self.exit_confirmation_msg = "are you sure you want to exit?"

    def show_intro(self):
        print(self.intro_msg)

    def get_piece(self, available):
        while True:
            print(self.select_piece_msg)
            piece = input()
            if piece in available:
                return piece

    def get_dest(self, available):
        available[0] = 0
        while True:
            print(self.select_destination_msg)
            dest = int(input())
            if dest in available.keys():
                return available[dest]


# wyswietl intro, wyswietl plansze, zapytaj o nastepny ruch gracza...
# czekaj na wybor piona
# wyświetl plansze z dostępnymi ruchami dla tego pionka
# zapytaj o to ktory ruch uskutecznic, lub o powrot do poprzedniego pytania
# gdy wybrano ruch, wykonaj go i zmien gracza
# za każdym razem gdy uzytkownik cos pojebał -> spytaj jeszcze raz, bez wyświetlania planszy


if __name__ == '__main__':
    c = Controller()
    c._print_board()
    print("current player: ", c.current_player)
    c._change_player()
    print("current player: ", c.current_player)

    print("available moves for red b", c.game.get_possible_moves(c.game.board[5, 2]))
    c.game.move((5, 2), (4, 3))
    c._print_board()
