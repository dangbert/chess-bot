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
            self._set(x, 1, Piece(Team.WHITE, Type.PAWN))
            self._set(x, 6, Piece(Team.BLACK, Type.PAWN))
        # set rest of pieces
        for y in [0, 7]:
            self._set(0, y, Piece(Team.BLACK if y else Team.WHITE, Type.ROOK))
            self._set(1, y, Piece(Team.BLACK if y else Team.WHITE, Type.KNIGHT))
            self._set(2, y, Piece(Team.BLACK if y else Team.WHITE, Type.BISHOP))
            self._set(3, y, Piece(Team.BLACK if y else Team.WHITE, Type.QUEEN))
            self._set(4, y, Piece(Team.BLACK if y else Team.WHITE, Type.KING))
            self._set(5, y, Piece(Team.BLACK if y else Team.WHITE, Type.BISHOP))
            self._set(6, y, Piece(Team.BLACK if y else Team.WHITE, Type.KNIGHT))
            self._set(7, y, Piece(Team.BLACK if y else Team.WHITE, Type.ROOK))

    # sets the desired square to the given Piece (object)
    def _set(self, x, y, piece):
        self._arr[x][y] = piece 

    # returns the piece in a given spot on the board (None if spot is empty)
    def _get(self, x, y):
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

    # convert a numerical coordinate to a string representing it
    @staticmethod
    def chessFormat(x, y):
        return chr(ord('a') + x) + str(y+1)

    # convert a chess coordinate to a numerical coordinate
    @staticmethod
    def compFormat(p):
        x = ord(p[0]) - ord('a')
        y = int(p[1]) - 1
        return (x, y)

    # returns true if the (current) player is in check
    def inCheck(self):
        pass

    # return true if a given position is on the board
    def isValidIndex(self, x, y):
        return 0 <= x and x <= 7 and 0 <= y and y <= 7

    # return true if a given position is valid and (either empty or contains an enemy piece)
    def isValidIndexCapture(self, x, y):
        return self.isValidIndex(x, y) and (self._arr[x][y] == None or self._arr[x][y]._team != self._turn)

    # return a list of positions that the piece
    # at the given position is allowed to move to
    # (taking check into account)
    def getMoves(self, loc):
        loc = self.compFormat(loc)
        x = loc[0]
        y = loc[1]
        print("translated to (" + str(x) + "," + str(y) + ")")
        # TODO: fix issues with checking if a spot is not None
        pos0 = Pos(x, y)
        moves = []
        piece = self._arr[x][y]
        if piece == None or self._turn != piece.getTeam():
            return [] # return empty list

        if piece.getType() == Type.PAWN:
            # sign for direction of travel
            s = (1 if piece.getTeam() == Team.WHITE else -1)
            # moving 2 positions forward
            if (s == 1 and y == 1) or (s == -1 and y == 6):
                self._addMove(moves, pos0, Pos(x, y+s*2))
            # moving 1 position forward
            self._addMove(moves, pos0, Pos(x, y+s*1))
            # attacking a piece
            if self.isValidIndex(x-1, y+s*1) and (self._arr[x-1][y+s*1] != None and self._arr[x-1][y+s*1]._team != self._turn):
                self._addMove(moves, pos0, Pos(x-1, y+s*1))
            if self.isValidIndex(x+1, y+s*1) and (self._arr[x+1][y+s*1] != None and self._arr[x+1][y+s*1]._team != self._turn):
                self._addMove(moves, pos0, Pos(x+1, y+s*1))

        if piece.getType() == Type.KNIGHT:
            for p in [(-2, -1), (-2, +1), (-1, -2), (-1, +2), (+2, -1), (+2, +1), (+1, -2), (+1, +2)]:
                if self.isValidIndexCapture(x+p[0], y+p[1]):
                    self._addMove(moves, pos0, Pos(x+p[0], y+p[1]))

        # (simply include the queen in the sections for the bishop and the rook)
        if piece.getType() == Type.BISHOP or piece.getType() == Type.QUEEN:
            for sx in [-1, 1]:                  # sign for x travel
                for sy in [-1, 1]:              # sign for y travel
                    i = 1                       # magnitude of travel
                    while self.isValidIndexCapture(x+sx*i, y+sy*i):
                        self._addMove(moves, pos0, Pos(x+sx*i, y+sy*i))
                        i += 1

        if piece.getType() == Type.ROOK or piece.getType() == Type.QUEEN:
            for s in [-1, 1]:                   # sign for travel direction
                # travel column:
                i = 1
                while self.isValidIndexCapture(x, y+s*i):
                    self._addMove(moves, pos0, Pos(x, y+s*i))
                    i += 1
                # travel row:
                i = 1
                while self.isValidIndexCapture(x+s*i, y):
                    self._addMove(moves, pos0, Pos(x+s*i, y))
                    i += 1

        if piece.getType() == Type.KING:
            for p in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                if self.isValidIndexCapture(x+p[0], y+p[1]):
                    self._addMove(moves, pos0, Pos(x+p[0], y+p[1]))
        return moves

    # add a move to the list if it's valid
    # (assumes provided indices are valid)
    def _addMove(self, moves, pos0, pos1):
        moves.append(pos1)
        # TODO: check if the king will be in check if the poice moves here
        # else add the move to the list
        #if self._isValidMove(pos0, pos1):

    # return true if moving the piece from (x0, y0) -> (x1, y1) is valid
    # (assumes that the given move would be valid if obstacles in between and check are disregarded)???
    def _isValidMove(self, pos0, pos1):
        # TODO: consider just calling my getMoves() and check that the provided index is in that list

        # check that resulting board wouldn't put you in check
        pass
