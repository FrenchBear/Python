# somme égale à 99
# 2021-02-28    PV

import itertools
from typing import Iterator


def sublists(li: list) -> Iterator[tuple]:
    """Iterator, returns all (2ⁿ) sublists of a list"""
    for i in range(len(li) + 1):
        for s in itertools.combinations(li, i):
            yield s

li = [27, 33, 38, 40, 15, 24, 29]
for s in sublists(li):
#    print(s)
    if sum(s) == 99:
        print(s)
