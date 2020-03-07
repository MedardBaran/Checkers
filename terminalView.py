from colorama import Fore, Back, Style
from model.items import EmptyField, Piece, King, Player, BoardMember


def _get_id(self, fields_with_id, standard_char):
    is_highlighted = self.addr in list(fields_with_id.keys())
    id = fields_with_id[self.addr] if is_highlighted else standard_char
    return id


def _empty_field_to_str(self, fields_with_id):
    r = " " + self._get_id(fields_with_id, standard_char=" ") + " "

    if self.addr in list(fields_with_id.keys()):
        r = " " + fields_with_id[self.addr] + " "
        return Back.LIGHTGREEN_EX + Fore.BLACK + r
    elif self.available:
        return Back.BLACK + r
    else:
        return Back.LIGHTWHITE_EX + r


def _piece_to_str(self, fields_with_id):
    r = " " + self._get_id(fields_with_id, standard_char="O") + " "

    if self.player == Player.red:
        return Back.BLACK + Fore.RED + r
    elif self.player == Player.white:
        return Back.BLACK + Fore.WHITE + r


def _king_to_str(self, fields_with_id):
    r = "{" + self._get_id(fields_with_id, standard_char="O") + "}"

    if self.player == Player.red:
        return Back.BLACK + Fore.RED + r
    elif self.player == Player.white:
        return Back.BLACK + Fore.WHITE + r


BoardMember._get_id = _get_id
EmptyField.to_str = _empty_field_to_str
Piece.to_str = _piece_to_str
King.to_str = _king_to_str


def print_board(board, fields_with_id):
    """
    Print board. Showing available choices.
    :param board: numpy board, 8 x 8
    :param fields_with_id: dictionary, key: addr, value: id.
                           Can be either EmptyField or Piece/King
    :return: None.
    """
    for row in board:
        for field in row:
            s = field.to_str(fields_with_id)
            print(s, end="")
        print("" + Style.RESET_ALL)
