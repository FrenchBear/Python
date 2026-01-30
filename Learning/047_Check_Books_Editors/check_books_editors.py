# Check Books Editors
# Example with regex, Levenshtein distance, collection.Counter, os.walk...
#
# 2018-09-01    PV
# 2022-07-17    PV      More tests

from email.policy import default
import os
import re
from collections import defaultdict, Counter
from collections import Counter

EDITOR_RE = re.compile(r'\[([^]]+)\]')

diffMax = 2
# Adapted from https://en.wikipedia.org/wiki/Levenshtein_distance and personal app DiffMP3Names


def LevenshteinDistance(s: str, t: str) -> int:
    # Optimisation perso, j'ai pas besoin des distances supérieures à diffMax
    if abs(len(s) - len(t)) > diffMax:
        return diffMax + 1

    # degenerate cases
    if s == t:
        return 0
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)

    # # convert to lowercase, we're doing case insensitive compare here
    # s = s.lower()
    # t = t.lower()

    # create two work vectors of integer distances
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    v0 = list(range(len(t)+1))
    v1 = [0] * (len(t)+1)

    for i in range(len(s)):
        # calculate v1 (current row distances) from the previous row v0

        # first element of v1 is A[i+1][0]
        # edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1

        # use formula to fill in the rest of the row
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


def tld(a, b, d):
    dc = LevenshteinDistance(a, b)
    if d != dc:
        print(a + ", "+b+", "+str(d)+", "+str(dc))


variants = defaultdict(set)
alled = set()

cc: Counter[str] = Counter()
for dirpath, dirname, filenames in os.walk(r'\\teraz\books\Livres'):
    for filename in filenames:
        ma = EDITOR_RE.search(filename)
        if ma:
            ed = ma.group(1)
            cc.update([ed])
            variants[ed.casefold()].add(ed)
            alled.add(ed)

l = list(cc.most_common())
for ed, f in l:
    print(f"{f}\t", end='')
    for v in variants[ed.casefold()]:
        print(v+'\t', end='')
    print()
print()


def testsuffix(e1: str, e2: str, suffix: str):
    return e1+suffix == e2 or e1+' '+suffix == e2 or e1 == e2+suffix or e1 == e2+' '+suffix


al = list(alled)
for i in range(len(al)):
    for j in range(i+1, len(al)):
        e1: str = al[i]
        e2: str = al[j]
        e1c = e1.casefold()
        e2c = e2.casefold()
        if LevenshteinDistance(e1, e2) <= 1 or e1c == e2c:
            print(f'{e1} ({cc[e1]})\t{e2} ({cc[e2]})')
            continue

        if e1c.replace('&',' and ').replace(' ','')==e2c.replace('&',' and ').replace(' ',''):
            print(f'{e1} ({cc[e1]})\t{e2} ({cc[e2]})')
            continue

        if testsuffix(e1c, e2c, 'press'):
            print(f'{e1} ({cc[e1]})\t{e2} ({cc[e2]})')
            continue

        if testsuffix(e1c, e2c, 'learning'):
            print(f'{e1} ({cc[e1]})\t{e2} ({cc[e2]})')
            continue

