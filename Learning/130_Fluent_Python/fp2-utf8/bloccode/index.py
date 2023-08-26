# Example 3-5. index.py uses dict.setdefault to fetch and update a list of word occurrences from the index in a single line; contrast with Example 3-4

"""Build an index mapping word -> list of occurrences"""

import re
import sys

WORD_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index.setdefault(word, []).append(location)

# display in alphabetical order
for word in sorted(index, key=str.upper):
    print(word, index[word])
