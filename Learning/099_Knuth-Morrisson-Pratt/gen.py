# gen.py
# Generation of sequences to test Knuth-Morris-Pratt search algorithm
#
# 2022-02-07    PV

import random
from kmp import computeLPSArray, KMPSearch

al = 'ABCD'

def gen(l):
    s = ''
    L = len(al)
    n = random.randint(0, L-1)
    for i in range(l):
        s = s+al[n]
        r = random.random()
        if r <= 0.5:
            pass
        elif r <= 0.8:
            n = (n+1) % L
        elif r <= 0.9:
            n = (n+2) % L
        else:
            n = random.randint(0, L-1)
    return s

pat = gen(6)
lps = computeLPSArray(pat)
print(pat)
print(lps)

txt = gen(1000)
print(txt[0:80])
KMPSearch(txt, pat, lps)
