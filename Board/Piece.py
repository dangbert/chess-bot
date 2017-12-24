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
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        x = chr(ord('a') + self.x)
        y = self.y + 1
        #return Board.chessFormat(self.x, self.y)
        return "(" + str(self.x) + "," + str(self.y) + ")"
