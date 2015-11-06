import curses

class Color():
    """ Simple wrapper for using colors with curses. Use by first calling initPairs(), and
        then directly accessing pair """

    pair = {}

    def initPairs():
        curses.use_default_colors()

        # b = black, w = white, h = hightlight, c = in check
        # bb = black piece on black background, bw = black on white etc.
        colorCombos = ['bb', 'bw', 'wb', 'ww', 'b', 'w', 'numbering', 'bh', 'wh', 'wc', 'bc']
        colorIndex = {item: int(index)+1 for index, item in enumerate(colorCombos)}

        curses.init_pair(colorIndex['bb'], curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(colorIndex['bw'], curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(colorIndex['wb'], curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(colorIndex['ww'], curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(colorIndex['b'], curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(colorIndex['w'], curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(colorIndex['numbering'], curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(colorIndex['bh'], curses.COLOR_RED, curses.COLOR_GREEN)
        curses.init_pair(colorIndex['wh'], curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(colorIndex['wc'], curses.COLOR_YELLOW, curses.COLOR_MAGENTA)
        curses.init_pair(colorIndex['bc'], curses.COLOR_RED, curses.COLOR_MAGENTA)

        for color, value in colorIndex.items():
            Color.pair[color] = curses.color_pair(value)

