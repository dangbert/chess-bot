#!/usr/bin/python3
from Board import Board, Type, Pos

# TODO: keep track of all the past board positions (hash them)
# to detect if a position is repeated 3 times (draw)
board = Board()
print(board)
while 1:
    while 1:
        try:
            loc = Pos(input("loc: "))
            break
        except:
            loc = Pos(input("loc: "))

    moves = board.getMoves(loc)
    print("Possible moves: " + str(moves))
    if len(moves) == 0:
        continue

    dest = Pos(input("dest: "))
    if board.isValidMove(loc, dest):
        print("valid move")
    else:
        print("invalid move")
