from copy import deepcopy

UNICODE = False

class Piece():
    def setAttributes(self, movementPattern, bounded, symbol):
        self.movementPattern = movementPattern
        self.bounded = bounded
        self.symbol = symbol

    def setColor(self, color):
        self.color = color
        if isinstance(self, Pawn):
            self.movementPattern = [(0, 1)] if self.color == 'w' else [(0, -1)]

    def getPossibleMoves(self, currPos):
        possibleMoves = []
        movementPattern = self.movementPattern
           
        for direction in movementPattern:
            dirLine = []
            i = 1 
            while True:
                newPos = (currPos[0] + direction[0]*i, currPos[1] + direction[1]*i)
                if 0 <= newPos[0] < 8 and 0 <= newPos[1] < 8:
                    dirLine.append(newPos)
                    if isinstance(self, Pawn) and not self.hasMoved and i == 1:
                        i += 1
                    elif self.bounded:
                        break
                    else:
                        i += 1
                else:
                    break
            if len(dirLine) > 0:
                possibleMoves.append(dirLine)
        return possibleMoves

class Pawn(Piece):
    # (0, 1) means "stay at x-axis, move one up at y-axis"
    def __init__(self):
        movementPattern = [(0, 1)] 
        self.setAttributes(movementPattern, True, '\u2659' if UNICODE else 'P')
        self.hasMoved = False

    def getAttackMoves(self, currPos, leftTarget, rightTarget):
        yDir = self.movementPattern[0][1]
        attackMoves = []
        if leftTarget:
            if 0 <= currPos[0]-1 < 8 and 0 <= currPos[1]+yDir < 8:
                attackMoves.append((currPos[0]-1, currPos[1]+yDir))
        if rightTarget:
            if 0 <= currPos[0]+1 < 8 and 0 <= currPos[1]+yDir < 8:
                attackMoves.append((currPos[0]+1, currPos[1]+yDir))

        return attackMoves

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

    def getPossibleThreatPositions(self, pos):
        self.bounded = False
        moves = self.getPossibleMoves(pos)
        self.bounded = True

        # The moves of all pieces except the knight is in included in the "moves" list,
        # so add the movement pattern of the knight explicitly
        dummyKnight = Knight()
        for move in dummyKnight.getPossibleMoves(pos):
            moves.append(move)
        return moves
