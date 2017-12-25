from enum import Enum
from Board import Board

# represents a chess piece
class Piece:
    def __init__(self, team, type):
        self._team = team
        self._type = type
        # keep track of if each rook and the king have been moved yet
        if self._type == Type.ROOK or self._type == Type.KING:
            self._moved = False
        # track if a pawn just moved 2 positions (for en passant)
        if self._type == Type.PAWN:
            self._movedTwo = False

    def getTeam(self):
        return self._team

    def getType(self):
        return self._type

    def teamIs(self, t):
        return self._team == t

    def typeIs(self, t):
        return self._type == t

    def __repr__(self):
        if self._team not in Team:
            raise ValueError("Invalid team: '" + str(self._team) + "'")
        if self._type not in Type:
            raise ValueError("Invalid type: '" + str(self._type) + "'")

        # (black pieces are printed with a '|' on either side)
        name = "  " if self._team == Team.WHITE else " |"
        if self._type == Type.PAWN:
            name += "%"
        elif self._type == Type.KNIGHT:
            name += "N"
        elif self._type == Type.BISHOP:
            name += "B"
        elif self._type == Type.ROOK:
            name += "R"
        elif self._type == Type.QUEEN:
            name += "Q"
        elif self._type == Type.KING:
            name += "K"
        name += "  " if self._team == Team.WHITE else "| "
        return name

# team colors
class Team(Enum):
    WHITE  = 0
    BLACK  = 1

# types of pieces
class Type(Enum):
    PAWN   = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK   = 3
    QUEEN  = 4
    KING   = 5

# represents a position on the board
class Pos:
    # initialize with either 2 indices or one chess format string
    def __init__(self, x, y=None):
        if y != None:
            self.x = x
            self.y = y
        else:
            # initialize using a chess format string (e.g. "a2")
            self.x = ord(x[0]) - ord('a')
            self.y = int(x[1]) - 1

    # return true if this position is on the board
    def isValid(self):
        return 0 <= self.x and self.x <= 7 and 0 <= self.y and self.y <= 7

    # return a Pos with the given offset from this one
    def off(self, x, y):
        return Pos(self.x + x, self.y + y)

    # return the piece at this pos in the board
    # (assumes this pos is valid)
    def piece(self, board):
        return board._get(self)

    # print Pos objects as chess format strings (e.g. "a2")
    def __repr__(self):
        return chr(ord('a') + self.x) + str(self.y+1)

    # equality operator
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False
