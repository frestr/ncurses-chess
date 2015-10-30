import curses

class Color():
    """ Simple wrapper for using colors with curses. Use by first calling initPairs(), and
        then directly accessing pair """

    pair = {}

    def initPairs():
        curses.start_color()
        curses.use_default_colors()

        # bb = black piece on black background, bw = black on white etc.
        colorIndex = {'bb': 1, 'bw': 2, 'wb': 3, 'ww': 4, 'b': 5, 'w': 6}
        curses.init_pair(colorIndex['bb'], curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(colorIndex['bw'], curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(colorIndex['wb'], curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(colorIndex['ww'], curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(colorIndex['b'], curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(colorIndex['w'], curses.COLOR_WHITE, curses.COLOR_WHITE)

        for color, value in colorIndex.items():
            Color.pair[color] = curses.color_pair(value)

