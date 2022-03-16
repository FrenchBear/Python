# laby.py: Test argparse module to replace getopt
# Exemple similar to DevForFun app laby.py
#
# 2022-03-16    PV

import argparse


def int_range(arg: str, low: int, high: int):
    def raise_err():
        raise argparse.ArgumentTypeError(f"Must be an integer beween {low} and {high}")

    try:
        n = int(arg)
    except ValueError:
        raise_err()
    if not low <= n <= high:
        raise_err()
    return n


parser = argparse.ArgumentParser(description='Generation of a random labyrinth, and optionally show solution path (Python version)')
parser.add_argument('-a', '--ascii', help='Simple print (ASCII only)', action='store_true')
parser.add_argument('-b', '--border', help=' Border style, a=ASCII, s=Simple, b=Bold, d=Double, r=Rounded (use chcp 65001 for styles s/b/d/r on Windows)',
                    type=str.lower, choices="asbdr", default='a')
parser.add_argument('-r', '--rows', help='Number of rows in [5..100], default 10',  type=lambda arg: int_range(arg, 5, 100), default=10)
parser.add_argument('-c', '--cols', help='Number of columns in [5..100], default 20', type=lambda arg: int_range(arg, 5, 100), default=20)
parser.add_argument('-s', '--solution', help='Show solution', action='store_true')
parser.add_argument('-m', '--monochrome', help='If solution is shown, monochrome (no color) solution output', action='store_true')
parser.add_argument('-d', '--shuffle', help='Shuffle random generator', action='store_true')

args = parser.parse_args()

if args.monochrome and not args.solution:
    parser.error('-m requires -s option')

print(f'{args.ascii=}')
print(f'{args.border=}')
print(f'{args.rows=}')
print(f'{args.cols=}')
print(f'{args.solution=}')
print(f'{args.monochrome=}')
print(f'{args.shuffle=}')
