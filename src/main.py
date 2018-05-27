from shesh_besh_gui import *


def main():
    g = Game()
    g.handle_board()

    a = g.board.slots
    for i in a:
        print i


if __name__ == "__main__":
    main()