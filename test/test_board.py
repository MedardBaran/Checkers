from test.board_gen import *

# todo: pytests of everything!!!!
"""
        ; f01;    ; f03;    ; f05;    ; f07
     f10;    ; f12;    ; f14;    ; f16;
        ; f21;    ; f23;    ; f25;    ; f27
     f30;    ; f32;    ; f34;    ; f36;
        ; f41;    ; f43;    ; f45;    ; f47
     f50;    ; f52;    ; f54;    ; f56;
        ; f61;    ; f63;    ; f65;    ; f67
     f70;    ; f72;    ; f74;    ; f76;
     """


def multimoves_calculation():
    return BoardLayout(f12='wK', f23='rP', f45='rP', f43='rP', f70='rP', f21='rP', f07='wP', f16='rP')


def upgrade_test():
    return BoardLayout(f54='wP', f12='rP', f63='rP', f36='rP')


def end_game():
    return BoardLayout(f23='wP', f34='rP')


def sort_moves():
    return BoardLayout(f34='wK', f76='rP')


if __name__ == '__main__':
    layout = multimoves_calculation()
    start_test_scenario(layout)
