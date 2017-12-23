from Board.Piece import *

# represents a chess board
class Board:
    def __init__(self):
        # each spot on the board holds a Piece or None (if empty)
        self.arr = [[None for x in range(8)] for y in range(8)]
        self.reset()

    # reset chess board (new game)
    def reset(self):
        self.turn = Team.WHITE                  # white's turn
        self.w_castled = False                  # white hasn't castled
        self.b_castled = False                  # black hasn't castled

        # set pawns
        for x in range(8):
            self.arr[x][1] = Piece(Team.WHITE, Type.PAWN)
            self.arr[x][6] = Piece(Team.BLACK, Type.PAWN)
        # set rest of pieces
        for y in [0, 7]:
            self.arr[0][y] = Piece(Team.BLACK if y else Team.WHITE, Type.ROOK)
            self.arr[1][y] = Piece(Team.BLACK if y else Team.WHITE, Type.KNIGHT)
            self.arr[2][y] = Piece(Team.BLACK if y else Team.WHITE, Type.BISHOP)
            self.arr[3][y] = Piece(Team.BLACK if y else Team.WHITE, Type.QUEEN)
            self.arr[4][y] = Piece(Team.BLACK if y else Team.WHITE, Type.KING)
            self.arr[5][y] = Piece(Team.BLACK if y else Team.WHITE, Type.BISHOP)
            self.arr[6][y] = Piece(Team.BLACK if y else Team.WHITE, Type.KNIGHT)
            self.arr[7][y] = Piece(Team.BLACK if y else Team.WHITE, Type.ROOK)

    # sets the desired square to the given Piece (object)
    def set(self, x, y, piece):
        self.arr[x][y] = piece 

    # returns the value of a given spot on the board
    def get(self, x, y):
        return self.arr[x][y]

    def __repr__(self):
        name = "\t  a\t  b\t  c\t  d\t  e\t  f\t  g\t  h\t\n\n"
        for y in range(7, -1, -1):
            name += "      " + str(y + 1) + "\t"
            for x in range(8):
                if self.arr[x][y] != None:
                    name += str(self.arr[x][y])
                else:
                    name += "  -  "
                name += "\t"
            name += "\n"
        name += "\n      Turn: " + ("white\n" if self.turn == Team.WHITE else "black\n")
        return name
