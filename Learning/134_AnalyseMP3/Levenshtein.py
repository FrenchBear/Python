# Levenshtein.py
# Distance de Levenshtein
#
# 2017-08-17    PV

import unicodedata

def Lowercase_no_diacritic(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != 'Mn')       # Mn =  "Mark, nonspacing."

# Adapted from https://en.wikipedia.org/wiki/Levenshtein_distance and personal app DiffMP3Names
def LevenshteinDistance(s: str, t: str, diffMax=1):
    # Personal optimization, I don't need distances greater than diffMax
    if abs(len(s) - len(t)) > diffMax:
        return diffMax + 1

    # degenerate cases
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)

    # convert to lowercase, we're doing case insensitive compare here
    s = Lowercase_no_diacritic(s)
    t = Lowercase_no_diacritic(t)

    if s == t:
        return 0

    # create two work vectors of integer distances
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    v0 = list(range(len(t) + 1))
    v1 = [0] * (len(t) + 1)

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
