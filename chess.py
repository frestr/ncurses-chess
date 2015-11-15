#!/usr/bin/env python3
import curses
import shutil
import board
from color import Color

def convertInput(inpList):
    cInpList = []
    for inp in inpList:
        if inp.isalpha():
            cInpList.append(ord(inp) - ord('a'))
        else:
            cInpList.append(int(inp) - 1)
    return (cInpList[0], cInpList[1])

def getMove(scr):
    validInput = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', \
                  '1', '2', '3', '4', '5', '6', '7', '8']
    inpList = []
    while len(inpList) < 2:
        inp = ''
        while inp not in validInput:
            try:
                inp = scr.getkey()
            except KeyboardInterrupt:
                quit()
            if inp == '\x1b': # Escape key
                return None
        inpList.append(inp)
    cInp = convertInput(inpList)
    return cInp

def getPromotionChoice(scr, scrDim):
    string = "Press 'q', 'n', 'r' or 'b' to promote pawn"
    scr.addstr(scrDim[1]//2 - 1, scrDim[0]//2 - len(string)//2, string)

    validInput = ['q', 'n', 'r', 'b']
    inp = ''
    while inp not in validInput:
        try:
            inp = scr.getkey()
        except KeyboardInterrupt:
            quit()
    return inp

def announceWinner(scr, scrDim, winner):
    winningPlayer = 'White' if winner == 'w' else 'Black'
    string = 'Checkmate! {} player won!'.format(winningPlayer)
    scr.addstr(scrDim[1]//2 - 1, scrDim[0]//2 - len(string)//2, string)

def main(scr):
    scrDimensions = shutil.get_terminal_size((80, 20))
    if scrDimensions[0] < 10*2 or scrDimensions[1] < 10:
        curses.endwin()
        print('Terminal window is too small')
        quit()

    scr.border(0)
    curses.curs_set(False)

    Color.initPairs()
    brd = board.Board()

    while True:
        brd.printBoard(scr, scrDimensions)
        
        moveStart = getMove(scr)
        if moveStart == None:
            continue

        if brd.printBoard(scr, scrDimensions, moveStart) == False:
            continue

        moveEnd = getMove(scr)
        if moveEnd == None:
            continue

        brd.movePiece(moveStart, moveEnd)
        if brd.checkmate:
            brd.printBoard(scr, scrDimensions)
            announceWinner(scr, scrDimensions, brd.winner)
            try:
                scr.getch() # Wait for a key to be pressed before quitting
            except KeyboardInterrupt:
                pass
            break
        elif brd.pawnPromotion:
            promotion = getPromotionChoice(scr, scrDimensions)
            brd.promotePawn(promotion) 

if __name__ == '__main__':
    curses.wrapper(main)
