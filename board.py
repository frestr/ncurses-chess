from color import Color
import piecetype
from copy import deepcopy

class Tile():
    def __init__(self, tileColor, piece=None):
        self.tileColor = tileColor
        self.piece = piece

class Board():
    def __init__(self):
        initialPos = [piecetype.Rook, piecetype.Knight, piecetype.Bishop, piecetype.Queen,\
                      piecetype.King, piecetype.Bishop, piecetype.Knight, piecetype.Rook]
        self.board = [[None for x in range(8)] for y in range(8)]
        self.whitesTurn = True
        self.kingsPos = {'w': (), 'b': ()}
        self.inCheck = {'w': False, 'b': False}

        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                tileColor = ''
                if y % 2 == 0:
                    tileColor = 'w' if x % 2 == 0 else 'b'
                else:
                    tileColor = 'b' if x % 2 == 0 else 'w'

                pieceColor =  None
                if y == 0 or y == 1:
                    pieceColor = 'b'
                elif y == len(self.board[0]) - 2 or y == len(self.board[0]) - 1:
                    pieceColor = 'w'

                piece = None
                if y == 0 or y == len(self.board[0]) - 1:
                    piece = initialPos[x]()
                elif y == 1 or y == len(self.board[0]) - 2:
                    piece = piecetype.Pawn()
                
                if piece != None:
                    piece.setColor(pieceColor)
               
                if isinstance(piece, piecetype.King):
                    self.kingsPos[piece.color] = self.convertCoord((x, y))

                self.board[y][x] = Tile(tileColor, piece)

    def printBoard(self, screen, screenDimensions, tempMove=None):
        # tileHeight must be an odd number (or else the logic fails)
        tileHeight = 1 if screenDimensions[0] < 26 or screenDimensions[1] < 26 else 3
        tileWidth = tileHeight*2

        xOffset = int(screenDimensions[0]//2 - tileWidth*8//2)
        yOffset = int(screenDimensions[1]//2 - tileHeight*8//2)
        
        validMoves = []
        if tempMove != None:
            convCoord = self.convertCoord(tempMove)
            if self.board[convCoord[1]][convCoord[0]].piece == None:
                return False
            validMoves = self.getValidMoves(tempMove)

        # Draw tiles and pieces
        for y in range(tileHeight*8):
            for x in range(0, tileWidth*8, 2):
                tile = self.board[y//tileHeight][x//tileWidth]

                # Basically checks if the current x coordinate is in the middle of a tile
                if (x - tileWidth//2 + 1) % tileWidth == 0 and (y - tileHeight//2) % tileHeight == 0:
                    backgroundColor = tile.tileColor
                    convCoord = self.convertCoord((x//tileWidth, y//tileHeight))

                    if (convCoord == self.kingsPos['w'] and self.inCheck['w']) or \
                            (convCoord == self.kingsPos['b'] and self.inCheck['b']):
                        backgroundColor = 'c'
                    elif convCoord in validMoves:
                        backgroundColor = 'h'

                    if tile.piece != None:
                        screen.addch(yOffset + y, xOffset + x, tile.piece.symbol, \
                                     Color.pair[tile.piece.color + backgroundColor])
                    else:
                        screen.addch(yOffset + y, xOffset + x, ' ', \
                                     Color.pair[tile.tileColor + backgroundColor]) 
                else:
                    screen.addch(yOffset + y, xOffset + x, ' ', Color.pair[tile.tileColor])
                screen.addch(yOffset + y, xOffset + x + 1, ' ', Color.pair[tile.tileColor])

        # Draw board numbering a to b
        for x in range(tileWidth//2 - 1, len(self.board[0])*tileWidth, tileWidth):
            screen.addch(yOffset - tileHeight//2 - 1, xOffset + x, \
                    chr(ord('a')+x//tileWidth), Color.pair['numbering'])
            screen.addch(yOffset + tileHeight*len(self.board) + tileHeight//2, xOffset + x, \
                    chr(ord('a')+x//tileWidth), Color.pair['numbering'])

        # Draw board numbering 8 to 1
        for y in range(tileHeight//2, len(self.board)*tileHeight, tileHeight):
            screen.addch(yOffset + y, xOffset - tileWidth//2 - 1, \
                    str(8 - y//tileHeight), Color.pair['numbering'])
            screen.addch(yOffset + y, xOffset + tileWidth*len(self.board[0]) + tileWidth//2, \
                    str(8 - y//tileHeight), Color.pair['numbering'])

        screen.move(yOffset + tileHeight*8//2, xOffset + tileWidth*10)

    # This function changes the origin from being in the lower left (like a normal chess board),
    # to being in the upper left (to comply with how the 2D list of the board behaves)
    def convertCoord(self, coord):
        return (coord[0], len(self.board)-1 - coord[1])

    def getValidMoves(self, pos, kingThreatCheck=False, ignoreWhoseTurn=False):
        convPos = self.convertCoord(pos)
        tile = self.board[convPos[1]][convPos[0]]
        possibleMoves = []
        if kingThreatCheck:
            king = self.board[convPos[1]][convPos[0]].piece
            possibleMoves = king.getPossibleThreatPositions(pos)
        else:
            possibleMoves = tile.piece.getPossibleMoves(pos)
            if not ignoreWhoseTurn:
                if self.whitesTurn and tile.piece.color != 'w' or \
                        not self.whitesTurn and tile.piece.color == 'w':
                    return []
        
        validMoves = []
        for direction in possibleMoves:
            for i in range(len(direction)):
                coord = self.convertCoord(direction[i])
                targetTile = self.board[coord[1]][coord[0]]
                if targetTile.piece != None:
                    if isinstance(tile.piece, piecetype.Pawn):
                        break
                    
                    offset = 1
                    if targetTile.piece.color == tile.piece.color:
                        offset = 0
                    for move in direction[:i+offset]:
                        validMoves.append(move)
                    break
                else:
                    if i == len(direction)-1:
                        for move in direction:
                            validMoves.append(move)

        # Make pawns able to attack sideways 
        if isinstance(tile.piece, piecetype.Pawn):
            convPawnDirection = tile.piece.movementPattern[0][1] * -1
            targetPiece1, targetPiece2 = None, None
            if 0 <= convPos[1] + convPawnDirection < 8 and 0 <= convPos[0] - 1 < 8: 
                targetPiece1 = self.board[convPos[1] + convPawnDirection][convPos[0] - 1].piece
            if 0 <= convPos[1] + convPawnDirection < 8 and 0 <= convPos[0] + 1 < 8:
                targetPiece2 = self.board[convPos[1] + convPawnDirection][convPos[0] + 1].piece

            leftTarget = True if targetPiece1 != None and targetPiece1.color != tile.piece.color else False
            rightTarget = True if targetPiece2 != None and targetPiece2.color != tile.piece.color else False
            
            attackMoves = tile.piece.getAttackMoves(pos, leftTarget, rightTarget)
            if len(attackMoves) > 0:
                for move in attackMoves:
                    validMoves.append(move)

        return validMoves

    def movePiece(self, startPos, endPos):
        convStartPos, convEndPos = self.convertCoord(startPos), self.convertCoord(endPos)
        tile = self.board[convStartPos[1]][convStartPos[0]]
        if tile.piece == None or endPos not in self.getValidMoves(startPos): 
            return

        if isinstance(tile.piece, piecetype.King):
            self.kingsPos[tile.piece.color] = endPos
        
        startTileCopy = deepcopy(self.board[convStartPos[1]][convStartPos[0]])
        endTileCopy   = deepcopy(self.board[convEndPos[1]][convEndPos[0]])

        self.board[convEndPos[1]][convEndPos[0]].piece = tile.piece
        self.board[convStartPos[1]][convStartPos[0]].piece = None

        self.inCheck['w'] = True if self.isInCheck('w') else False
        self.inCheck['b'] = True if self.isInCheck('b') else False

        # Do not allow movement that doesn't move a player out of check, 
        # or movement that moves a player's own king into check
        if (self.whitesTurn and self.inCheck['w']) or \
                (not self.whitesTurn and self.inCheck['b']):
            self.board[convStartPos[1]][convStartPos[0]].piece = startTileCopy.piece
            self.board[convEndPos[1]][convEndPos[0]].piece = endTileCopy.piece

            if isinstance(tile.piece, piecetype.King):
                self.kingsPos[tile.piece.color] = startPos

            return

        if hasattr(tile.piece, 'hasMoved'):
            tile.piece.hasMoved = True
        self.whitesTurn = not self.whitesTurn

    def isInCheck(self, player):
        for pos in self.getValidMoves(self.kingsPos[player], kingThreatCheck=True):
            convPos = self.convertCoord(pos)
            possibleThreat = self.board[convPos[1]][convPos[0]].piece
            if possibleThreat != None and possibleThreat.color != player:
                possibleMoves = self.getValidMoves(pos, ignoreWhoseTurn=True)
                with open('log.txt', 'a') as f:
                    f.write('Possible threat pos: ' + str(pos) + '\n')
                    f.write('Possible threat moves: ' + str(possibleMoves) + '\n')
                    f.write('Kings pos (' + player + '): ' + str(self.kingsPos[player]) + '\n')
                if self.kingsPos[player] in possibleMoves:
                    return True
        return False
