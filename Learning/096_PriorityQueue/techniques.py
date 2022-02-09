# Various techniques from Programmer efficacement
# 2021-12-29    PV

import math
from typing import Any, Tuple
from collections import defaultdict, Counter


def majority1(l: list) -> Any:
    count = {}
    for item in l:
        if item in count:
            count[item] += 1
        else:
            count[item] = 1
    countmax, itemmax = max((count[item], item) for item in count)
    return itemmax


def majority2(l: list) -> Any:
    count = defaultdict(int)
    for item in l:
        count[item] += 1
    return max((count[item], item) for item in count)[1]


def majority3(l: list) -> Any:
    count = Counter()
    count.update(l)
    return count.most_common(1)[0][0]


m = 'abracadabra'
print(majority1(m))
print(majority2(m))
print(majority3(m))


# Find closest values in a list
def closest(l: list) -> Tuple[Any, Any]:
    assert len(l) >= 2
    l.sort()
    valmin, ixmin = min((l[i]-l[i-1], i) for i in range(1, len(l)))
    return l[ixmin-1], l[ixmin]


l = [61, 69, 51, 27, 82, 25, 10, 2, 89, 70, 42, 24, 65, 91, 83, 97, 19, 59, 79, 11]
print(closest(l))


def max_interval_intersect(s: list[Any, Any]) -> Any:
    b: list[Tuple[Any, int]] = [(left, +1) for left, _ in s]+[(right, -1) for _, right in s]
    b.sort()
    c = 0
    best = (c, None)
    for x, d in b:
        c += d
        if best[0] < c:
            best = (c, x)
    return best


intervals = [(12, 29), (51, 64), (53, 65), (91, 102), (48, 65), (11, 20), (80, 88), (41, 57), (43, 52), (74, 93)]
print(max_interval_intersect(intervals))    # (count_of_intervals, value)


# f is a function returning 0/1 or False/True, we want to find the lowest x in [lo, hi] such as f(x)=1/True
def continuous_binary_search(f, lo, hi):
    while hi-lo > 1e-6:   # precision can be adjusted
        mid = (lo+hi)/2.0
        if f(mid):
            hi = mid
        else:
            lo = mid
    return lo


# Application, compute a function using reciprocal (useful if reciprocal is much easier or faster to compute)
# For instance, compute log(2) using exponential
l2 = continuous_binary_search(lambda x: math.exp(x) > 2, 0.5, 1.5)
print(l2)
