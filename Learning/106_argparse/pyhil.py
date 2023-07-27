# pyhil.py: Test argparse module to replace getopt
# Exemple similar to DevForFun app pihil.py
#
# 2022-03-16    PV

import argparse
from common_argparse import int_range

parser = argparse.ArgumentParser(description='Generation and text drawing of a Hilbert curve (Python version)', 
    formatter_class=argparse.RawDescriptionHelpFormatter, epilog='''
Use chcp 65001 for styles s/b/d/r on Windows.
┌─┐ ┌─┐  ┏━┓ ┏━┓  ╔═╗ ╔═╗  ╭─╮ ╭─╮
│ └─┘ │  ┃ ┗━┛ ┃  ║ ╚═╝ ║  │ ╰─╯ │
└─┐ ┌─┘  ┗━┓ ┏━┛  ╚═╗ ╔═╝  ╰─╮ ╭─╯
──┘ └──  ━━┛ ┗━━  ══╝ ╚══  ──╯ ╰──
Simple   Bold     Double   Rounded''')
parser.add_argument('-a', '--ascii', help='Simple print (ASCII only)', action='store_true')
parser.add_argument('-b', '--border', help='Border style, s=Simple, b=Bold, d=Double, r=Rounded',
                    type=str.lower, choices="sbdr", default='s')
parser.add_argument('-d', '--depth', help='Depth level in [1..8], default 4',  type=lambda arg: int_range(arg, 1, 8))
parser.add_argument('depth2', metavar='depth', nargs='?', help='Depth level in [1..8], default 4',  type=lambda arg: int_range(arg, 1, 8))

args = parser.parse_args()

# Merge depth option and depth2 optional positional argument, handle default value
if args.depth and args.depth2:
    parser.error('Use either -d or an extra numeric argument to specify depth')
if args.depth2:
    args.depth=args.depth2
if not args.depth:
    args.depth=4

print(f'{args.border=}')
print(f'{args.depth=}')
