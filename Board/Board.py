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
        self._lastMoved = None
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
        count = 0
        name = "\t  a    b    c    d    e    f    g    h\n\n"
        for y in range(7, -1, -1):
            count += 1
            name += "      " + str(y + 1) + "\t"
            for x in range(8):
                count += 1
                if self._arr[x][y] != None:
                    name += str(self._arr[x][y])
                else:
                    name += ("  ~  " if count % 2 == 0 else "  -  ")
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

        if piece.getType() == Type.PAWN:
            # sign for direction of travel
            s = (1 if piece.getTeam() == Team.WHITE else -1)
            # moving 1 or 2 positions forward
            if self._arr[x][y+s*1] == None:
                self._addMove(moves, p0, Pos(x, y+s*1))
                if (s == 1 and y == 1) or (s == -1 and y == 6) and self._arr[x][y+s*2] == None:
                    self._addMove(moves, p0, Pos(x, y+s*2))
            # attacking a piece
            for k in [-1, 1]:
                p1 = p0.off(k, s*1)
                if p1.isValid():
                    if p1.piece(self) != None:
                        if not p1.piece(self).teamIs(self._turn):
                            self._addMove(moves, p0, p1)
                    else: # en passant
                        piece2 = p0.off(k, 0).piece(self)
                        if piece2 != None and piece2.typeIs(Type.PAWN) and piece2._movedTwo == True:
                            self._addMove(moves, p0, p1)

        if piece.getType() == Type.KNIGHT:
            for k in [(-2, -1), (-2, +1), (-1, -2), (-1, +2), (+2, -1), (+2, +1), (+1, -2), (+1, +2)]:
                p1 = p0.off(k[0], k[1])
                if self.isValidCapture(p1):
                    self._addMove(moves, p0, p1)


        # (simply include the queen in the sections for the bishop and the rook)
        if piece.getType() == Type.BISHOP or piece.getType() == Type.QUEEN:
            for sx in [-1, 1]:                  # sign for x travel
                for sy in [-1, 1]:              # sign for y travel
                    i = 1                       # magnitude of travel
                    while self.isValidCapture(p0.off(sx*i, sy*i)):
                        self._addMove(moves, p0, p0.off(sx*i, sy*i))
                        if p0.off(sx*i, sy*i).piece(self) != None:
                            break               # stop after we reach an enemy piece
                        i += 1

        # TODO: consider replacing isValidCapture()
        #       with a (bigger) function that can be used by the BISHOP and ROOK sections
        #       (perhaps pass the function the pattern that's being used?)
        if piece.getType() == Type.ROOK or piece.getType() == Type.QUEEN:
            for s in [-1, 1]:                   # sign for travel direction
                # travel column:
                i = 1
                while self.isValidCapture(p0.off(0, s*i)):
                    self._addMove(moves, p0, p0.off(0, s*i))
                    if p0.off(0, s*i).piece(self) != None:
                        break                   # stop after we reach an enemy piece
                    i += 1
                # travel row:
                i = 1
                while self.isValidCapture(p0.off(s*i, 0)):
                    self._addMove(moves, p0, p0.off(s*i, 0))
                    if p0.off(s*i, 0).piece(self) != None:
                        break                   # stop after we reach an enemy piece
                    i += 1

        # TODO: take castling into account
        if piece.getType() == Type.KING:
            for k in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                p1 = p0.off(k[0], k[1])
                if self.isValidCapture(p1):
                    self._addMove(moves, p0, p1)
        return moves

    # add a move to a provided list if it's valid
    # (assumes provided indices are valid)
    def _addMove(self, moves, p0, p1):
        if not self._inCheck(p0, p1):
            moves.append(p1)

    def makeMove(self, p0, p1):
        if self.isValidMove(p0, p1):
            if self._lastMoved != None and self._lastMoved.piece(self).typeIs(Type.PAWN):
                self._lastMoved.piece(self)._movedTwo = False
            if p0.piece(self).typeIs(Type.PAWN) and p1.piece(self) == None and p0.x != p1.x:
                # remove enemy pawn if en passant is being done
                self._set(Pos(p1.x, p0.y), None)

            self._set(p1, self._get(p0))
            self._set(p0, None)
            self._turn = (Team.WHITE if self._turn == Team.BLACK else Team.BLACK)
            self._lastMoved = p1
            if p1.piece(self).typeIs(Type.PAWN) and (p0.off(0, 2) == p1 or p0.off(0, -2) == p1):
                self._lastMoved.piece(self)._movedTwo = True
            return True
        return False

    # return true if moving the piece from (x0, y0) -> (x1, y1) is valid
    # (assumes that the given move would be valid if obstacles in between and check are disregarded)
    def isValidMove(self, p0, p1):
        moves = self.getMoves(p0)               # list of Pos objects
        if p1 not in moves:
            return False
        return True
