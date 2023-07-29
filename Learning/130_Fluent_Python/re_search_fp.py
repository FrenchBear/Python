# re_search_fp
# Use a regex to search in Fluent Python text
#
# 2023-07-29    PV

import re

IMPORT_RE = re.compile(r'^>>> *import +[^ ,]+')

source = r"C:\DocumentsOD\Doc dev\Python\Fluent Python 2nd ed\Fluent Python (2nd ed^J 2022) - [O'Reilly] - Luciano Ramalho 86.txt"
with open(source, 'rt', encoding='utf-8') as sr:
    line: str
    for line in sr.readlines():
        if IMPORT_RE.match(line):
            print(line.rstrip())

