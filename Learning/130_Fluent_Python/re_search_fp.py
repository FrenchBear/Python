# re_search_fp
# Use a regex to search in Fluent Python text
#
# 2023-07-29    PV

import re

# IMPORT_RE = re.compile(r'^>>> *import +[^ ,]+')
BINARY_RE = re.compile(r'[\x01-\x1f]')

def print_special(line: str) -> None:
    for c in line:
        if c < ' ' and c!='\x0a':
            print(f'«{ord(c):02X}»', end='')
        else:
            print(c, end='')
    print()


source = r"C:\DocumentsOD\Doc dev\Python\Fluent Python 2nd ed\Fluent Python (2nd ed, 2022) - [O'Reilly] - Luciano Ramalho 89.txt"
ln = 0
with open(source, 'rt', encoding='utf-8') as sr:
    line: str
    for line in sr.readlines():
        ln += 1
        l = line[:-1]
        if BINARY_RE.match(l):
            print(f'{ln:>6} ', end='')
            print_special(l)
