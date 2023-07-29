# re_search_sources
# Use a regex to search in all python sources
#
# 2023-07-29    PV

from common_fs import get_all_files, extension_part
import re
from enum import Enum


class MutableString:
    def __init__(self, s: str):
        self.l = list(s)

    def __str__(self):
        return ''.join(self.l)

    def __getitem__(self, key):
        return self.l.__getitem__(key)

    def __setitem__(self, key, value):
        return self.l.__setitem__(key, value)

    def __delitem__(self, key):
        self.l.__delitem__(key)


class State(Enum):
    PythonCode = 1
    InComment = 2
    inSimpleQuote = 3
    inDoubleQuote = 4
    InTripleSimpleQuote = 5
    InTripleDoubleQuote = 6


def MaskPythonStringsAndComments(source: str) -> str:
    res = MutableString(source)
    state = State.PythonCode
    pos = 0
    while pos < len(source):
        lastpos = pos
        c1 = source[pos:pos+1]
        c2 = source[pos:pos+2]
        c3 = source[pos:pos+3]

        match state:
            case State.PythonCode:
                if c1 == '#':
                    state = State.InComment
                    pos += 1
                elif c1 == "'":
                    state = State.inSimpleQuote
                    pos += 1
                elif c1 == '"':
                    state = State.inDoubleQuote
                    pos += 1
                elif c3 == "'''":
                    state = State.InTripleSimpleQuote
                    pos += 3
                elif c3 == '"""':
                    state = State.InTripleDoubleQuote
                    pos += 3
                else:
                    pos += 1

            case State.InComment:
                if c1 == '\r' or c1 == '\n':
                    state = State.PythonCode
                else:
                    res[pos] = ' '
                pos += 1

            case State.inSimpleQuote:
                if c2 == r"\'":
                    pos += 2
                elif c1 == "'":
                    state = State.PythonCode
                    pos += 1
                else:
                    res[pos] = ' '
                    pos += 1

            case State.inDoubleQuote:
                if c2 == r'\"':
                    pos += 2
                elif c1 == '"':
                    state = State.PythonCode
                    pos += 1
                else:
                    res[pos] = ' '
                    pos += 1

            case State.InTripleSimpleQuote:
                if c2 == r"\'":
                    pos += 2
                elif c3 == "'''":
                    state = State.PythonCode
                    pos += 3
                else:
                    res[pos] = ' '
                    pos += 1

            case State.InTripleDoubleQuote:
                if c2 == r'\"':
                    pos += 2
                elif c3 == '"""':
                    state = State.PythonCode
                    pos += 3
                else:
                    res[pos] = ' '
                    pos += 1

        assert pos != lastpos

    return str(res)


TYPING_TYPES_RE = re.compile(r'\b(List|Set|Frozenset|Deque|MutableSequence|Sequence|AbstractSet|MutableSet)\b')

# line = 'def download_all_sites_synchronous(sites: List[str]):'
# print(TYPING_TYPES_RE.search(line))

root = r'C:\Development\GitHub\Python\Learning'
for file in [f for f in get_all_files(root) if extension_part(f) == '.py']:
    with open(file, 'rt', encoding='utf-8') as sr:
        source = sr.read().replace('\r\n', '\n').replace('\r', '\n')
        masked = MaskPythonStringsAndComments(source)
        source_lines = source.split('\n')
        masked_lines = masked.split('\n')
        line: str
        for (i, line) in enumerate(masked_lines):
            if TYPING_TYPES_RE.search(line):
                print(file, source_lines[i], sep='\t')
