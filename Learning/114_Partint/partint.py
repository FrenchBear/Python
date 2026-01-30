# Partitionnement d'un entier
#
# 2022-07-05    PV
# 2025-04-08    PV      Fixed type hints errors

import collections
from typing import Deque

from collections.abc import Callable, Iterator

# recursive iterator
def partint1(n: int) -> Iterator[list[int]]:
    if n == 1:
        yield [1]
    else:
        for i in range(1, n):
            for l in partint1(n - i):
                l.append(i)
                yield l
        yield [n]

# simple iterator using a stack
def partint2(n: int) -> Iterator[list[int]]:
    st: Deque[list[int]] = collections.deque()
    st.append([n])
    while st:  # .count > 0:
        l = st.pop()
        rem = l[0]
        if rem == 0:
            yield l[1:]
        else:
            for i in range(1, rem + 1):
                t = list(l)
                t[0] = rem - i
                t.append(i)
                st.append(t)

def test(partint: Callable[[int], Iterator[list[int]]]) -> None:
    print("Test", partint.__name__)
    n = 5
    for l in partint(n):
        print(l)
        assert sum(l) == n
    print()

    print('i\t#P(i)')
    for n in range(1, 12):
        c = len(list(partint(n)))
        print(n, c, sep='\t')
        assert c == 2**(n - 1)
    print()


test(partint1)
test(partint2)
