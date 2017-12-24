#!/usr/bin/python3
from Board import Board, Type

# TODO: keep track of all the past board positions (hash them)
# to detect if a position is repeated 3 times (draw)
board = Board()
print(board)
while 1:
    loc = input("pos: ")
    moves = board.getMoves(loc)
    print(moves)
