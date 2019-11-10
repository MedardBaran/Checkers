from colorama import Fore, Back, Style
from model import EmptyField, Piece, King, Player

# todo: show id's only for next turn player. opponent should have 0's and [0]'s


def _empty_field_to_str(self):
    r = "   "

    if self.available:
        return Back.BLACK + r
    else:
        return Back.LIGHTWHITE_EX + r


def _piece_to_str(self):
    with_id = True
    id = self.id if with_id else "O"
    r = " " + id + " "

    if self.player == Player.red:
        return Back.BLACK + Fore.RED + r
    else:
        return Back.BLACK + Fore.WHITE + r


def _king_to_str(self):
    with_id = True
    id = self.id if with_id else "O"
    r = "[" + self.id + "]"

    if self.player == Player.red:
        return Back.BLACK + Fore.RED + r
    else:
        return Back.BLACK + Fore.WHITE + r


EmptyField.__str__ = _empty_field_to_str
Piece.__str__ = _piece_to_str
King.__str__ = _king_to_str


def print_board(board, selected=None, moves=None):
    """
    Print board. Show available moves if piece is selected.
    :param board: numpy board, 8 x 8
    :param selected: optional, tuple with item coordinates: (row, col)
    :param moves: optional, list of tuples with reachable fields: (row, col, name)
    :return: None.
    """

    for row in board:
        view = ""
        for field in row:
            print(field, end="")
        print(view + Style.RESET_ALL)


if __name__ == '__main__':
    a = Back.LIGHTWHITE_EX + Fore.RED + "back lightwhite fore red" + Style.RESET_ALL
    print(a)
