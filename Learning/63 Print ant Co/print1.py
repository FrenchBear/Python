# print1.py
# Leaning python, variations on print
#
# 2019-08-28    PV


# Using partial to wrap print into convenient helpers
from functools import partial
import sys
redirect = lambda function, stream: partial(function, file=stream)
prefix = lambda function, prefix: partial(function, prefix)
error = prefix(redirect(print, sys.stderr), '[ERROR]')
error('Something went wrong')

# Redefine print
import builtins
println = builtins.print        # Access to standard print
def print(*args, **kwargs):     # Print without final \n
    builtins.print(*args, **kwargs, end='')
print("hello")
print(" world")
println("!")
del print

# Pretty printing: pprint use repr() instead of str
from pprint import pprint
data = {'pow8': [8**x for x in range(11)], 'pow9': [9**x for x in range(11)]}
print(data)
pprint(data)

# Printing json data
import json
data = {'username': 'pierre', 'password': 's3cret'}
print(json.dumps(data))
print(json.dumps(data, indent=4, sort_keys=True))

# Colors
import colorama
colorama.init() # On Windows, calling init() will filter ANSI escape sequences out of any text sent to stdout or stderr, and replace them with equivalent Win32 calls
# Note that with new Windows Terminal, colorama is not needed anymore, it event prevent use of underline attribute
# Using colorama helpers:
# - Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# - Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# - Style: DIM, NORMAL, BRIGHT, RESET_ALL
from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Back.YELLOW + 'and with a green background')
print(Style.BRIGHT + 'and in bright text')
print(Style.RESET_ALL, end='')
print('back to normal now')
# Using directly ANSI sequences
print('\033[31m' + 'some red text')
print('\033[30m') # and reset to default color

def ansi(code):
    return f'\033[{code}m'
print(ansi('31;1;4')+'really'+ansi(0)+' important\n')

# Also works with termcolor
from termcolor import colored
print(colored('Hello, World!', 'green', 'on_red'))
