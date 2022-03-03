# plsscr.py
# Plus longue sous-séquence croissante
# Etant donné une séquence de n entiers, trouver une sous-séquence de longueur maximale et croissante
# Programmation efficace p.55
#
# 2022-02-25    PV

from bisect import bisect_left


def plsscr(x: list[int]) -> list[int]:
    n = len(x)
    p = [None] * n
    h: list = [None]
    b = [float('-inf')]
    for i in range(n):
        if x[i] > b[-1]:
            p[i] = h[-1]
            h.append(i)
            b.append(x[i])
        else:
            # recherche dichotomoqie b[k-1]<=k[k]
            k = bisect_left(b, x[i])
            h[k] = i
            b[k] = x[i]
            p[i] = h[k-1]
    # on extrait la solution
    q = h[-1]
    s = []
    while q:
        s.append(x[q])
        q = p[q]
    return s[::-1]


l = [9, 3, 1, 4, 1, 5, 9, 2, 6, 5, 4, 5, 3, 9, 7, 9]
print(plsscr(l))
