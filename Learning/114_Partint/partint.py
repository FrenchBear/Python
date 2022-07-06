# partitionnement d'un entier
#
# 2022-07-05    PV

from typing import Iterator

def partint1(n: int) -> Iterator[list[int]]:
    if n==1:
        yield [1]
    else:
        for i in range(1,n):
            for l in partint1(n-i):
                l.append(i)
                yield l
        yield [n]

def test(partint: Iterator[list[int]]):
    print("Test", partint.__name__)
    n = 5
    for l in partint(n):
        print(l)
        assert sum(l)==n
    print()

    print('i\t#P(i)')
    for n in range(1, 12):
        c = len(list(partint1(n)))
        print(n,c,sep='\t')
    print()

test(partint1)
