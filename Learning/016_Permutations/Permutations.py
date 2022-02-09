# 16 Permutations.py
# Variants of permutation in Python
#
# 2016-06-26    PV
# 2018-09-10    PV      measure_perf (instead of duplicating the code), itertools.permutations, Perm_Prod

import time

# Compute the list of all permutations of a list l (from Python language reference manual)


def Perm(l):
    if len(l) <= 1:
        return [l]
    r = []
    for i in range(len(l)):
        s = l[:i] + l[i+1:]
        p = Perm(s)
        for x in p:
            r.append(l[i:i+1] + x)
    return r


# A recursive iterator to produce all possible permutations of a list (my code)
def Permutator(t):
    if len(t) == 1:
        yield t
    else:
        for i in range(len(t)):
            for x in Permutator(t[:i] + t[i+1:]):
                yield t[i:i+1]+x


# Permutations already implemented in itertools, ready to use
import itertools

def Perm_IT(t):
    return itertools.permutations(t)


# Another algorithm, from Python itertools doc, based on product()
def Perm_Prod(iterable):
    pool = tuple(iterable)
    n = len(pool)
    for indices in itertools.product(range(n), repeat=n):
        if len(set(indices)) == n:
            yield tuple(pool[i] for i in indices)


# Compare performances
l = [1, 2, 3, 4, 5, 6, 7, 8]


def measure_perf(method):
    tstart = time.time()    # Stopwatch start
    ns = 0
    for _ in Perm(l):
        ns += 1
    duration = time.time()-tstart
    print(f"{method.__name__}: {ns} solution(s) found in {round(duration,1)}s")

measure_perf(Perm)
measure_perf(Permutator)
measure_perf(Perm_IT)
measure_perf(Perm_Prod)
