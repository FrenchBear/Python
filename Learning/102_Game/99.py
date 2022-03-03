# somme égale à 99
# 2021-02-28    PV

import itertools
from typing import Iterator, Tuple


def sublists(l: list) -> Iterator[Tuple]:
    """Iterator, returns all (2ⁿ) sublists of a list"""
    for i in range(len(l) + 1):
        for s in itertools.combinations(l, i):
            yield s

l = [27, 33, 38, 40, 15, 24, 29]
for s in sublists(l):
#    print(s)
    if sum(s) == 99:
        print(s)
