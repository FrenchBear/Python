# pq.py
# Implémentation manuelle d'une Priority Queue du type heapq
# Utilise une liste (tableau dynamique) pour le stockage interne de l'arbre
# L'élément 0 n'est pas utilisé
# L'élément [i] a (au max) deux fils, [2*i] et [2*i+1], et un père [i//2]
#
# 2021-12-28    PV      De 'Programmation efficace'

from typing import Any, Iterable


class PriorityQueue:
    def __init__(self, items: Iterable[Any] = None) -> None:
        self.l = [0]                # Element 0 is not used
        if items:
            for item in items:
                self.push(item)

    def __len__(self):
        return len(self.l)-1

    def push(self, item: Any):
        assert not item in self.l
        ix = len(self.l)
        self.l.append(item)         # Nouvelle feuille
        self._up(ix)

    def pop(self) -> Any:
        root = self.l[1]
        x = self.l.pop()            # Dernière feuille
        if self:
            self.l[1] = x           # On le met à la racine
            self._down(1)
        return root

    def _up(self, ix: int):
        x = self.l[ix]
        while ix > 1 and x < self.l[ix//2]:
            self.l[ix] = self.l[ix//2]
            ix //= 2
        self.l[ix] = x

    def _down(self, ix: int):
        x = self.l[ix]
        n = len(self.l)
        while True:
            left = 2*ix
            right = left+1
            if right < n and self.l[right] < x and self.l[right] < x and self.l[right] < self.l[left]:
                self.l[ix] = self.l[right]      # On monte le fils de droite
                ix = right
            elif left < n and self.l[left] < x:
                self.l[ix] = self.l[left]
                ix = left
            else:
                self.l[ix] = x
                return


pq = PriorityQueue([10, 4, 11, 9, 5, 2, 3])
while pq:
    print(pq.pop())
