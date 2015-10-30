#!/usr/bin/env python3
import curses
import shutil

class Board():
    def __init__(self):
        self.board = [['X' for x in range(8)] for y in range(8)]

    def printBoard(self, screen, screenDimensions):
        xOffset = int(screenDimensions[0]//2 - 16/2)
        yOffset = int(screenDimensions[1]//2 - 8/2)
        for y in range(8):
            for x in range(0, 16, 2):
                screen.addch(yOffset + y, xOffset + x, self.board[y][x//2])
                screen.addch(yOffset + y, xOffset + x + 1, ' ')
            print()

class Piece():
    pass


scrDimensions = shutil.get_terminal_size((80, 20))

board = Board()

scr = curses.initscr()
scr.border(0)

board.printBoard(scr, scrDimensions)
scr.refresh()

scr.getkey()

curses.endwin()

