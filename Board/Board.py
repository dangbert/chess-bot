from Board.Piece import *

# represents a chess board
class Board:
    def __init__(self):
        # each spot on the board holds a Piece or None (if empty)
        self.reset()

    # reset chess board (new game)
    def reset(self):
        self._arr = [[None for x in range(8)] for y in range(8)]
        self._turn = Team.WHITE                 # white's turn
        self._wCastle = True                    # white can still castle
        self._bCastle = True                    # black can still castle

        # set pawns
        for x in range(8):
            self._arr[x][1] = Piece(Team.WHITE, Type.PAWN)
            self._arr[x][6] = Piece(Team.BLACK, Type.PAWN)
        # set rest of pieces
        for y in [0, 7]:
            self._arr[0][y] = Piece(Team.BLACK if y else Team.WHITE, Type.ROOK)
            self._arr[1][y] = Piece(Team.BLACK if y else Team.WHITE, Type.KNIGHT)
            self._arr[2][y] = Piece(Team.BLACK if y else Team.WHITE, Type.BISHOP)
            self._arr[3][y] = Piece(Team.BLACK if y else Team.WHITE, Type.QUEEN)
            self._arr[4][y] = Piece(Team.BLACK if y else Team.WHITE, Type.KING)
            self._arr[5][y] = Piece(Team.BLACK if y else Team.WHITE, Type.BISHOP)
            self._arr[6][y] = Piece(Team.BLACK if y else Team.WHITE, Type.KNIGHT)
            self._arr[7][y] = Piece(Team.BLACK if y else Team.WHITE, Type.ROOK)

    # sets the desired square to the given Piece (object)
    def set(self, x, y, piece):
        self._arr[x][y] = piece 

    # returns the piece in a given spot on the board (None if spot is empty)
    def get(self, x, y):
        return self._arr[x][y]

    def __repr__(self):
        name = "\t  a\t  b\t  c\t  d\t  e\t  f\t  g\t  h\t\n\n"
        for y in range(7, -1, -1):
            name += "      " + str(y + 1) + "\t"
            for x in range(8):
                if self._arr[x][y] != None:
                    name += str(self._arr[x][y])
                else:
                    name += "  -  "
                name += "\t"
            name += "\n"
        name += "\n      Turn: " + ("white\n" if self._turn == Team.WHITE else "black\n")
        return name
