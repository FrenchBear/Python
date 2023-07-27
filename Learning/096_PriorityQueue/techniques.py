# Various techniques from Programmer efficacement
# 2021-12-29    PV

import math
from typing import Any, DefaultDict, Iterable
from collections import defaultdict, Counter


def majority1(it: Iterable) -> Any:
    count:dict[Any, int] = {}
    for item in it:
        if item in count:
            count[item] += 1
        else:
            count[item] = 1
    countmax, itemmax = max((count[item], item) for item in count)
    return itemmax


def majority2(it: Iterable) -> Any:
    count:DefaultDict[Any, int] = defaultdict(int)
    for item in it:
        count[item] += 1
    return max((count[item], item) for item in count)[1]


def majority3(it: Iterable) -> Any:
    count:Counter = Counter()
    count.update(it)
    return count.most_common(1)[0][0]


m = 'abracadabra'
print(majority1(m))
print(majority2(m))
print(majority3(m))


# Find closest values in a list
def closest(li: list) -> tuple[Any, Any]:
    assert len(li) >= 2
    li.sort()
    valmin, ixmin = min((li[i]-li[i-1], i) for i in range(1, len(li)))
    return li[ixmin-1], li[ixmin]


li = [61, 69, 51, 27, 82, 25, 10, 2, 89, 70, 42, 24, 65, 91, 83, 97, 19, 59, 79, 11]
print(closest(li))


def max_interval_intersect(s: list[tuple[Any, Any]]) -> Any:
    b: list[tuple[Any, int]] = [(left, +1) for left, _ in s]+[(right, -1) for _, right in s]
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
