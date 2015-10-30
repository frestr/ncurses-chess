#!/usr/bin/env python3
import curses
import shutil
import board
from color import Color

def main():
    scrDimensions = shutil.get_terminal_size((80, 20))

    scr = curses.initscr()
    scr.border(0)
    curses.curs_set(False)

    Color.initPairs()
    brd = board.Board()
    brd.printBoard(scr, scrDimensions)

    scr.refresh()
    scr.getkey()
    curses.endwin()

if __name__ == '__main__':
    main()
