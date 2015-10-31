#!/usr/bin/env python3
import curses
import shutil
import board
from color import Color

# TODO:
# - Check if the move is valid
# - Alternate between white and black's turn
# - Check if a player is in check
# - Check fi a player is in check mate

def convertInput(inpList):
    cInpList = []
    for inp in inpList:
        if inp.isalpha():
            cInpList.append(ord(inp) - ord('a'))
        else:
            cInpList.append(int(inp) - 1)
    return [(cInpList[0], cInpList[1]), (cInpList[2], cInpList[3])]

def getMove(scr):
    validInput = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', \
                  '1', '2', '3', '4', '5', '6', '7', '8']
    inpList = []
    while len(inpList) < 4:
        inp = ''
        while inp not in validInput:
            inp = scr.getkey()
        inpList.append(inp)

    cInp = convertInput(inpList)
    return cInp

def main(scr):
    scrDimensions = shutil.get_terminal_size((80, 20))

    scr.border(0)
    curses.curs_set(False)

    Color.initPairs()
    brd = board.Board()

    while True:
        brd.printBoard(scr, scrDimensions)
        move = getMove(scr)
        brd.movePiece(move[0], move[1])

if __name__ == '__main__':
    curses.wrapper(main)
