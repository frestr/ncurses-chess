
UNICODE = True

class Piece():
    def setAttributes(self, movementPattern, bounded, symbol):
        self.movementPattern = movementPattern
        self.bounded = bounded
        self.symbol = symbol

    def setColor(self, color):
        self.color = color

    def isMoveLegal(self, currPos, movePos):
        return True

class Pawn(Piece):
    # (0, 1) means "stay at x-axis, move one up at y-axis"
    def __init__(self):
        movementPattern = [(0, 1)] 
        self.setAttributes(movementPattern, True, '\u2659' if UNICODE else 'P')

class Knight(Piece):
    def __init__(self):
        movementPattern = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        self.setAttributes(movementPattern, True,  '\u2658' if UNICODE else 'N')

class Queen(Piece):
    def __init__(self):
        movementPattern = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.setAttributes(movementPattern, False,  '\u2655' if UNICODE else 'Q')

class Bishop(Piece):
    def __init__(self):
        movementPattern = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        self.setAttributes(movementPattern, False,  '\u2657' if UNICODE else 'B')

class Rook(Piece):
    def __init__(self):
        movementPattern = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.setAttributes(movementPattern, False,  '\u2656' if UNICODE else 'R')

class King(Piece):
    def __init__(self):
        movementPattern = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.setAttributes(movementPattern, True,  '\u2654' if UNICODE else 'K')

