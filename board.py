from color import Color
import piecetype

class Tile():
    def __init__(self, tileColor, piece=None):
        self.tileColor = tileColor
        self.piece = piece

class Board():
    def __init__(self):
        initialPos = [piecetype.Rook, piecetype.Knight, piecetype.Bishop, piecetype.Queen,\
                      piecetype.King, piecetype.Bishop, piecetype.Knight, piecetype.Rook]
        self.board = [[None for x in range(8)] for y in range(8)]

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
                
                self.board[y][x] = Tile(tileColor, piece)

    def printBoard(self, screen, screenDimensions):
        # tileHeight must be an odd number (or else the logic fails)
        tileHeight = 1 if screenDimensions[0] < 26 or screenDimensions[1] < 26 else 3
        tileWidth = tileHeight*2

        xOffset = int(screenDimensions[0]//2 - tileWidth*8//2)
        yOffset = int(screenDimensions[1]//2 - tileHeight*8//2)

        # Draw tiles and pieces
        for y in range(tileHeight*8):
            for x in range(0, tileWidth*8, 2):
                tile = self.board[y//tileHeight][x//tileWidth]
                # Basically checks if the current x coordinate is in the middle of a tile
                if tile.piece != None and \
                        (x - tileWidth//2 + 1) % tileWidth == 0 and \
                        (y - tileHeight//2) % tileHeight == 0:
                    screen.addch(yOffset + y, xOffset + x, tile.piece.symbol, \
                                 Color.pair[tile.piece.color + tile.tileColor])
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

    def movePiece(self, startPos, endPos):
        convStartPos, convEndPos = self.convertCoord(startPos), self.convertCoord(endPos)
        tile = self.board[convStartPos[1]][convStartPos[0]]
        if tile.piece == None:
            return

        possibleMoves = tile.piece.getPossibleMoves(startPos)
        validMoves = []
        for direction in possibleMoves:
            for i in range(len(direction)):
                coord = self.convertCoord(direction[i])
                targetTile = self.board[coord[1]][coord[0]]
                if targetTile.piece != None:
                    offset = 1
                    if targetTile.piece.color == tile.piece.color:
                        if len(direction[:i]) > 0:
                            offset = 0
                    for move in direction[:i+offset]:
                        validMoves.append(move)
                    break
                else:
                    if i == len(direction)-1:
                        for move in direction:
                            validMoves.append(move)

        if endPos in validMoves:
            self.board[convEndPos[1]][convEndPos[0]].piece = tile.piece
            self.board[convStartPos[1]][convStartPos[0]].piece = None
