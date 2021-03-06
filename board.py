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
        self.pawnPromotion = False
        self.kingsPos = {'w': (), 'b': ()}
        self.inCheck = {'w': False, 'b': False}
        self.checkmate = False
        self.winner = ''

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
        tileHeight = 1 if screenDimensions[0] < 28*2 or screenDimensions[1] < 28 else 3
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

        # If the king is in check, also check if it is checkmated
        if self.inCheck['w'] or self.inCheck['b']:
            checkmated = False
            if self.whitesTurn:
                checkmated = self.isCheckmated('b')
            else:
                checkmated = self.isCheckmated('w')
           
            if checkmated:
                self.checkmate = True
                self.winner = 'w' if self.whitesTurn else 'b'
                return

        # Do not allow movement that doesn't move a player out of check, 
        # or movement that moves a player's own king into check
        if (self.whitesTurn and self.inCheck['w']) or \
                (not self.whitesTurn and self.inCheck['b']):
            self.board[convStartPos[1]][convStartPos[0]].piece = startTileCopy.piece
            self.board[convEndPos[1]][convEndPos[0]].piece = endTileCopy.piece

            if isinstance(tile.piece, piecetype.King):
                self.kingsPos[tile.piece.color] = startPos

            return

        if isinstance(self.board[convEndPos[1]][convEndPos[0]].piece, piecetype.Pawn):
            self.board[convEndPos[1]][convEndPos[0]].piece.hasMoved = True
            if endPos[1] == 0 or endPos[1] == 7:
                self.pawnPromotion = True

        self.whitesTurn = not self.whitesTurn

    def isInCheck(self, player, getPositions=False):
        threatPositions = []
        for pos in self.getValidMoves(self.kingsPos[player], kingThreatCheck=True):
            convPos = self.convertCoord(pos)
            possibleThreat = self.board[convPos[1]][convPos[0]].piece
            if possibleThreat != None and possibleThreat.color != player:
                possibleMoves = self.getValidMoves(pos, ignoreWhoseTurn=True)
                if self.kingsPos[player] in possibleMoves:
                    if getPositions:
                        threatPositions.append(pos)
                    else: 
                        return True
        return threatPositions if getPositions else False
   
    def isCheckmated(self, player):
        def canMoveWithoutCheck(startPos, endPos, player):
            startCoord = self.convertCoord(startPos)
            endCoord = self.convertCoord(endPos)

            startTileCopy = deepcopy(self.board[startCoord[1]][startCoord[0]])
            endTileCopy = deepcopy(self.board[endCoord[1]][endCoord[0]])
            kingPosCopy = deepcopy(self.kingsPos[player])

            if isinstance(startTileCopy.piece, piecetype.King):
                self.kingsPos[player] = endPos
            self.board[endCoord[1]][endCoord[0]].piece = self.board[startCoord[1]][startCoord[0]].piece
            self.board[startCoord[1]][startCoord[0]].piece = None
            
            check = False
            if self.isInCheck(player):
                check = True

            self.board[startCoord[1]][startCoord[0]] = startTileCopy
            self.board[endCoord[1]][endCoord[0]] = endTileCopy
            self.kingsPos[player] = kingPosCopy
            return not check

        threats = self.isInCheck(player, getPositions=True)
        if len(threats) == 0:
            return False

        exposedCoords = []
        kingsPos = self.kingsPos[player]
        
        # Get all the tile positions that are in the "attack direction" towards the king
        for threatPos in threats:
            exposedCoords.append(threatPos)
            convPos = self.convertCoord(threatPos)
            threatPiece = self.board[convPos[1]][convPos[0]].piece
            for dirLine in threatPiece.getPossibleMoves(threatPos):
                if kingsPos in dirLine:
                    for pos in dirLine: 
                        exposedCoords.append(pos)

        # This checks if there is a safe coord the king can move to directly
        checkmate = True
        for move in self.getValidMoves(kingsPos, ignoreWhoseTurn=True):
            if (move not in exposedCoords or move in threats) and canMoveWithoutCheck(kingsPos, move, player):
                checkmate = False

        # If the king is in check by multiple pieces, there is no other way to avoid checkmate
        if checkmate and len(threats) > 1:
            return True
        elif not checkmate:
            return False

        # Get all valid moves that can be made by friendly pieces
        # (and also save the location of the piece that can make the corresponding moves)
        allPositions = []
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                piece = self.board[y][x].piece
                if piece != None and not isinstance(piece, piecetype.King) and piece.color == player:
                    convCoord = self.convertCoord((x, y))
                    positions = [convCoord] # The piece's position is always the first element
                    for position in self.getValidMoves(convCoord, ignoreWhoseTurn=True):
                        positions.append(position)
                    allPositions.append(positions)

        # Check if one of the moves can be used to block/capture the piece causing the check,
        # and check if that move is valid, i.e. doesn't cause another check
        checkmate = True
        for exposedCoord in exposedCoords:
            for positions in allPositions:
                if exposedCoord in positions and canMoveWithoutCheck(positions[0], exposedCoord, player):
                    checkmate = False
                    break

        return checkmate

    def promotePawn(self, promotionChoice):
        # This method works, because a pawn promotion has to be done immediately, and
        # there can therefore at most be one pawn in the 1st or 8th row
        for y in [0, 7]:
            for x in range(len(self.board[0])):
                if isinstance(self.board[y][x].piece, piecetype.Pawn):
                    pawn = self.board[y][x].piece
                    choice = {'q': piecetype.Queen, 'n': piecetype.Knight, \
                              'r': piecetype.Rook, 'b': piecetype.Bishop}
                    newPiece = choice[promotionChoice]()
                    newPiece.setColor(pawn.color)
                    self.board[y][x].piece = newPiece
                    self.pawnPromotion = False
