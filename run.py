#!/usr/bin/python3
from Board import Board, Type, Pos

def main():
    # TODO: keep track of all the past board positions (hash them)
    # to detect if a position is repeated 3 times (draw)
    board = Board()
    print(board)

    while 1:
        loc = getLoc("loc: ")                   # start location
        moves = board.getMoves(loc)
        print("Possible moves: " + str(moves))
        if len(moves) == 0:
            continue

        dest = getLoc("dest: ")                 # end location
        if board.isValidMove(loc, dest):
            print("valid move")
        else:
            print("invalid move")

# prompt for a valid Pos on the board
def getLoc(prompt):
    while 1:
        try:
            loc = Pos(input(prompt))
            if loc.isValid():
                return loc
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            continue

if __name__ == "__main__":
    main()
