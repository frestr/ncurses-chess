# ncurses-chess
Basic chess game written using the ncurses binding for Python 3.

Features the most common features of chess, with the exception of castling, en passant, and check for stalemate.

Movement is done by directly typing the start and end position in algebraic notation. The game will highlight valid moves in green, and the king will be highlighted in purple if it is in check. The escape key clears the current input, and Ctrl+c quits the game.

Screenshots
-----------

The board automatically scales (at startup) between two sizes depending on the size of the terminal window. If the terminal window is larger than (or equal to) 56x28, the board will be drawn with big tiles, like in the following screenshot:

![Big board tiles](https://i.imgur.com/MaHqJQ7.png)

If either the width is under 56 or the height is under 28, the board will be drawn with small tiles:

![Small board tiles](https://i.imgur.com/asEj5JX.png)

Usage
-----
To run the game, simply do
```
python3 chess.py
```
or, alternatively:
```
chmod +x chess.py
./chess.py
```
