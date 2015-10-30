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

        xOffset = int(screenDimensions[0]//2 - tileWidth*8/2)
        yOffset = int(screenDimensions[1]//2 - tileHeight*8/2)
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
            print()
