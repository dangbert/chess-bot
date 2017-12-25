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
            self._set(Pos(x,1), Piece(Team.WHITE, Type.PAWN))
            self._set(Pos(x,6), Piece(Team.BLACK, Type.PAWN))
        # set rest of pieces
        for y in [0, 7]:
            self._set(Pos(0,y), Piece(Team.BLACK if y else Team.WHITE, Type.ROOK))
            self._set(Pos(1,y), Piece(Team.BLACK if y else Team.WHITE, Type.KNIGHT))
            self._set(Pos(2,y), Piece(Team.BLACK if y else Team.WHITE, Type.BISHOP))
            self._set(Pos(3,y), Piece(Team.BLACK if y else Team.WHITE, Type.QUEEN))
            self._set(Pos(4,y), Piece(Team.BLACK if y else Team.WHITE, Type.KING))
            self._set(Pos(5,y), Piece(Team.BLACK if y else Team.WHITE, Type.BISHOP))
            self._set(Pos(6,y), Piece(Team.BLACK if y else Team.WHITE, Type.KNIGHT))
            self._set(Pos(7,y), Piece(Team.BLACK if y else Team.WHITE, Type.ROOK))

    # sets the desired position to the given Piece (object)
    def _set(self, p, piece):
        self._arr[p.x][p.y] = piece 

    # returns the piece in a given spot on the board (None if spot is empty)
    def _get(self, p):
        return self._arr[p.x][p.y]

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

    # returns true if the (current) player is in check
    # or would be in check if the given move is made
    def _inCheck(self, p0, p1):
        return False # TODO: implement

    # return true if a given position is valid and (either empty or contains an enemy piece)
    def isValidCapture(self, p):
        return p.isValid() and (self._arr[p.x][p.y] == None or self._arr[p.x][p.y]._team != self._turn)

    # return a list of positions that the piece
    # at the given position is allowed to move to
    # (taking check into account)
    def getMoves(self, p0):
        x = p0.x
        y = p0.y
        moves = []
        piece = self._arr[x][y]
        if piece == None or self._turn != piece.getTeam():
            return [] # return empty list

        # TODO: fix problem allowing pawn to attack vertically
        # TODO: fix problem not allowing en passant
        if piece.getType() == Type.PAWN:
            # sign for direction of travel
            s = (1 if piece.getTeam() == Team.WHITE else -1)
            # moving 2 positions forward
            if (s == 1 and y == 1) or (s == -1 and y == 6):
                self._addMove(moves, p0, Pos(x, y+s*2))
            # moving 1 position forward
            self._addMove(moves, p0, Pos(x, y+s*1))
            # attacking a piece
            if Pos(x-1, y+s*1).isValid() and (self._arr[x-1][y+s*1] != None
                    and self._arr[x-1][y+s*1]._team != self._turn):
                self._addMove(moves, p0, Pos(x-1, y+s*1))
            if Pos(x+1, y+s*1).isValid() and (self._arr[x+1][y+s*1] != None
                    and self._arr[x+1][y+s*1]._team != self._turn):
                self._addMove(moves, p0, Pos(x+1, y+s*1))

        if piece.getType() == Type.KNIGHT:
            for k in [(-2, -1), (-2, +1), (-1, -2), (-1, +2), (+2, -1), (+2, +1), (+1, -2), (+1, +2)]:
                if self.isValidCapture(Pos(x+k[0], y+k[1])):
                    self._addMove(moves, p0, Pos(x+k[0], y+k[1]))

        # (simply include the queen in the sections for the bishop and the rook)
        # TODO: fix bug where it lets you move diagonally past an enemy piece
        if piece.getType() == Type.BISHOP or piece.getType() == Type.QUEEN:
            for sx in [-1, 1]:                  # sign for x travel
                for sy in [-1, 1]:              # sign for y travel
                    i = 1                       # magnitude of travel
                    while self.isValidCapture(Pos(x+sx*i, y+sy*i)):
                        self._addMove(moves, p0, Pos(x+sx*i, y+sy*i))
                        i += 1

        # TODO: fix problem allowing a rook to move past an enemy piece
        if piece.getType() == Type.ROOK or piece.getType() == Type.QUEEN:
            for s in [-1, 1]:                   # sign for travel direction
                # travel column:
                i = 1
                while self.isValidCapture(Pos(x, y+s*i)):
                    self._addMove(moves, p0, Pos(x, y+s*i))
                    i += 1
                # travel row:
                i = 1
                while self.isValidCapture(Pos(x+s*i, y)):
                    self._addMove(moves, p0, Pos(x+s*i, y))
                    i += 1

        if piece.getType() == Type.KING:
            for k in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                if self.isValidCapture(Pos(x+k[0], y+k[1])):
                    self._addMove(moves, p0, Pos(x+k[0], y+k[1]))
        return moves

    # add a move to a provided list if it's valid
    # (assumes provided indices are valid)
    def _addMove(self, moves, p0, p1):
        if not self._inCheck(p0, p1):
            moves.append(p1)

    def makeMove(self, p0, p1):
        # TODO: consider en passent (update pawn val)
        if self.isValidMove(p0, p1):
            self._set(p1, self._get(p0))
            self._set(p0, None)
            self._turn = (Team.WHITE if self._turn == Team.BLACK else Team.BLACK)
            return True
        return False

    # return true if moving the piece from (x0, y0) -> (x1, y1) is valid
    # (assumes that the given move would be valid if obstacles in between and check are disregarded)
    def isValidMove(self, p0, p1):
        moves = self.getMoves(p0)               # list of Pos objects
        if p1 not in moves:
            return False
        return True
