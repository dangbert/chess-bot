from enum import Enum

# represents a chess piece
class Piece:
    def __init__(self, team, type):
        self._team = team
        self._type = type

    def __repr__(self):
        if self._team not in Team:
            raise ValueError("Invalid team: '" + str(self._team) + "'")
        if self._type not in Type:
            raise ValueError("Invalid type: '" + str(self._type) + "'")

        # (black pieces are printed with a '|' on either side)
        name = "  " if self._team == Team.WHITE else " |"
        if self._type == Type.PAWN:
            name += "P"
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
