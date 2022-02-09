# curses.py
# Leaning python, variations on curses module
# From "Your Guide to the Python Print Function", https://realpython.com/python-print/
#
# Need a pip install windows-curses
# Just a basic example, will crash when hitting screen limits
#
# 2019-08-28    PV

import curses
import time

# For some reason, getch() doesn't return values of curses.KEY_UP...
KEY_UP = 450
KEY_DOWN = 456
KEY_LEFT = 452
KEY_RIGHT = 454


def main(screen):
    curses.curs_set(0)      # Hide cursor
    screen.nodelay(True)    # Don't block I/O calls such as getch

    directions = {
        KEY_UP: (-1, 0),
        KEY_DOWN: (1, 0),
        KEY_LEFT: (0, -1),
        KEY_RIGHT: (0, 1)
    }

    direction = directions[KEY_RIGHT]
    snake = [(0, i) for i in reversed(range(20))]

    while True:
        screen.erase()

        # Draw the snake
        screen.addstr(*snake[0], '@')
        for segment in snake[1:]:
            screen.addstr(*segment, '*')

        # Move the snake
        snake.pop()
        snake.insert(0, tuple(map(sum, zip(snake[0], direction))))

        # Change the direction on arror keystroke
        direction = directions.get(screen.getch(), direction)   # By default, keep current direction

        screen.refresh()
        time.sleep(0.1)


if __name__ == '__main__':
    curses.wrapper(main)



# Print actual key codes for arrows

# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)

# while True:
#     cc = stdscr.getch()
#     if 32 <= cc <= 128:
#         break
#     if cc > 0:
#         stdscr.erase()
#         stdscr.addstr(10, 10, str(cc))

# curses.nocbreak()
# stdscr.keypad(False)
# curses.echo()
# curses.endwin()
