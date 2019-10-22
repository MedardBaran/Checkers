from colorama import Fore, Back, Style

def print_board(board, selected=None, moves=None):
    """
    Print game state showing available moves.
    :param board: numpy board, 8 x 8
    :param selected: optional, tuple with item coordinates: (row, col)
    :param moves: optional, list of tuples with reachable fields: (row, col, name)
    :return: None. Prints actual game state in the terminal.
    """
    def _field_to_str(s):
        s = str(s)
        r = ""
        if s == "None":
            r = Back.LIGHTWHITE_EX + "   "
        # elif field.addr in moves:
        #     pass
        # elif field.addr == selected:
        #     pass
        elif s == "    ":
            r = Back.BLACK + "   "
        elif s[1] == "0":
            r = Back.BLACK + Fore.RED + f"({s[2]})"
        elif s[1] == "1":
            r = Back.BLACK + Fore.WHITE + f"({s[2]})"
        return r

    for row in board:
        view = ""
        for field in row:
            view = view + _field_to_str(field)
        print(view + Style.RESET_ALL)


if __name__ == '__main__':
    a = Back.LIGHTWHITE_EX + Fore.RED + "back lightwhite fore red" + Style.RESET_ALL
    print(a)
