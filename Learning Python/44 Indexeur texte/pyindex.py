# Indexeur texte
# Variations sur le thème  du ti et de l'indexation de texte
#
# 2018-08-14    PV


import re
import collections

import locale
import functools

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


"""
l = ['a', 'à', 'A', 'Â', 'b', 'c', 'ç', 'C', 'Ç', 'd', 'boeuf', 'bœuf', 'boev']
l.sort(key=functools.cmp_to_key(locale.strcoll))
print(l)
"""

"""
d = {"trois":3, "quatre":4, "cinq":5, "six":6}
print(list(filter(lambda key: d[key]>=5, d)))
e = {key: value for (key, value) in d.items() if value>=5}
print(e)
"""


WORD_RE = re.compile(r"[\w’]+")
DIGITSONLY_RE = re.compile(r'\d+')

index = collections.defaultdict(list)
with open("t2.txt", "r", encoding="utf-8-sig") as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group().lower()
            if not DIGITSONLY_RE.fullmatch(word):
                column_no = match.start()+1
                location = (line_no, column_no)
                index[word].append(location)

print("Index size:", len(index))

def top(seq, n):
    for item in seq:
        if n<=0: return
        n-=1
        yield item

# print in alphabetical order
# Reduce index to entries seen at least 10 times
ir = {key:value for (key, value) in index.items() if len(value)>=10}
for word in  top(sorted(ir, key=str.upper), 100):
    print(word, len(ir[word]))



"""
# print by frequency descending
nw = 0
for word, count in sorted([(word, len(loc)) for word, loc in index.items()], key=lambda tup: tup[1], reverse=True):
    print(word, count)
    nw += 1
    if nw > 100:
        break
"""