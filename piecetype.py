class Piece():
    def setColor(self, color):
        self.color = color

    def isMoveLegal(self, currPos, movePos):
        pass

class Pawn(Piece):
    # (0, 1) means "stay at x-axis, move one up at y-axis"
    def __init__(self):
        self.movementPattern = [(0, 1)] 
        self.bounded = True
        self.symbol = 'P'

class Knight(Piece):
    def __init__(self):
        self.movementPattern = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        self.bounded = True
        self.symbol = 'N'

class Queen(Piece):
    def __init__(self):
        self.movementPattern = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.bounded = False
        self.symbol = 'Q'

class Bishop(Piece):
    def __init__(self):
        self.movementPattern = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        self.bounded = False
        self.symbol = 'B'

class Rook(Piece):
    def __init__(self):
        self.movementPattern = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.bounded = False
        self.symbol = 'R'

class King(Piece):
    def __init__(self):
        self.movementPattern = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.bounded = True
        self.symbol = 'K'

