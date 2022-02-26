# Dés non transitifs
# 2022-02-26    PV

import math

A = [2, 2, 4, 4, 9, 9]
B = [1, 1, 6, 6, 8, 8]
C = [3, 3, 5, 5, 7, 7]


def fracsimpl(n1: int, n2: int) -> str:
    pgdc = math.gcd(n1, n2)
    return f'{n1//pgdc}/{n2//pgdc}'


def fight(d1: list[int], d2: list[int], n1: str, n2: str) -> str:
    w1 = w2 = 0     # win1, win2
    for i1 in d1:
        for i2 in d2:
            if i1 > i2:
                w1 += 1
            elif i2 > i1:
                w2 += 1
    if w1 == w2:
        return f'{n1}={n2}: chacun gagne {w1} cas sur {w1+w2}'
    elif w1 > w2:
        return f'{n1}>{n2}: {n1} gagne {w1} cas sur {w1+w2} = {fracsimpl(w1,w1+w2)}, {n2} gagne {w2} cas'
    else:
        return f'{n1}<{n2}: {n1} gagne {w1} cas, {n2} gagne {w2} cas sur {w1+w2} = {fracsimpl(w2,w1+w2)}'


print(fight(A, B, 'A', 'B'))
print(fight(B, C, 'B', 'C'))
print(fight(C, A, 'C', 'A'))
