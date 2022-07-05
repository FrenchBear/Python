# partitionnement d'un entier
#
# 2022-07-05    PV

from typing import Iterator


def partint(n: int) -> Iterator[list[int]]:
    if n==1:
        yield [1]
    else:
        for i in range(1,n):
            for l in partint(n-i):
                l.append(i)
                #l.insert(0, i)
                yield l
        yield [n]


n = 6
for l in partint(n):
    print(l)
    assert sum(l)==n

print('\ni\t#P(i)')
for n in range(1, 12):
    c = len(list(partint(n)))
    print(n,c,sep='\t')
