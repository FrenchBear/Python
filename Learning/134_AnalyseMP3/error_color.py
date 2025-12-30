# error_color.py
# Standard colorization of errors and warnings
#
# 2025-12-29    PV      First version

def print_ansi(code: str, *args):
    print(f'\033[{code}m', end='')
    print(*args, end='')
    print('\033[0m')

def print_error(*args):
    print_ansi('31;1', *args)   # red, bright

def print_warning(*args):
    print_ansi('33', *args)     # yellow
