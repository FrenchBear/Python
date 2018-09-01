# Check Books Editors
# Example with regex, Levenshtein distance, collection.Counter, os.walk...
#
# 2018-09-01    PV


import os
import re
import collections

EDITOR_RE = re.compile(r'\[([^]]+)\]')


# Version case-sensitive

diffMax = 2
# Adapted from https://en.wikipedia.org/wiki/Levenshtein_distance and personal app DiffMP3Names
def LevenshteinDistance(s, t):
    # Optimisation perso, j'ai pas besoin des distances supérieures à diffMax
    if abs(len(s) - len(t)) > diffMax: return diffMax + 1

    # degenerate cases
    if s == t: return 0
    if len(s) == 0: return t.Length
    if len(t) == 0: return s.Length

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

def tld(a,b,d):
    dc = LevenshteinDistance(a,b)
    if d!=dc: print(a + ", "+b+", "+str(d)+", "+str(dc))

"""
# Some tests
tld("Pomme","Pome",1)
tld("Il était un petit navire", "Il était un petit navire", 0)
tld("Il était une petit navire", "Il était un petit navire", 1)
tld("Il était un petit navire", "Il était une petit navire", 1)
tld("Il étai un petit naavire", "Il était un petit navire", 2)
tld("Il était un petit navire", "Il était u petit naavire", 2)
"""


cc = collections.Counter()
for dirpath, dirname, filenames in os.walk(r'W:\Livres'):       #\informatique'):
    for filename in filenames:
        ma = EDITOR_RE.search(filename)
        if ma:
            cc.update([ma.group(1)])

l = list(cc.most_common())
for ed, f in l:
    print(f"{f};{ed}")
print()

for i in range(len(l)):
    for j in range(i+1, len(l)):
        e1 = l[i][0]
        e2 = l[j][0]
        if LevenshteinDistance(e1, e2)==1:
            print(e1,e2)
