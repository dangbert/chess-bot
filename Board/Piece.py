from enum import Enum

# represents a chess piece
class Piece:
    def __init__(self, team, type):
        self.team = team
        self.type = type

    def __repr__(self):
        if self.team not in Team:
            raise ValueError("Invalid team: '" + str(self.team) + "'")
        if self.type not in Type:
            raise ValueError("Invalid type: '" + str(self.type) + "'")

        # (black pieces are printed with a '|' on either side)
        name = "  " if self.team == Team.WHITE else " |"
        if self.type == Type.PAWN:
            name += "P"
        elif self.type == Type.KNIGHT:
            name += "N"
        elif self.type == Type.BISHOP:
            name += "B"
        elif self.type == Type.ROOK:
            name += "R"
        elif self.type == Type.QUEEN:
            name += "Q"
        elif self.type == Type.KING:
            name += "K"
        name += "  " if self.team == Team.WHITE else "| "
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
