# pq.py
# Implémentation manuelle d'une Priority Queue du type heapq, avec remplacement possible
# Garde un dictionnaire en interne pour savoir où se trouve un élément quelconque à remplacer
# Utilise une liste (tableau dynamique) pour le stockage interne de l'arbre
# L'élément 0 n'est pas utilisé, ça rend la gestion des index plus simple
# L'élément [i] a (au max) deux fils, [2*i] et [2*i+1], et un père [i//2]
#
# 2021-12-28    PV      De 'Programmation efficace'
# 2022-06-27    PV      __str__

from typing import Any

from collections.abc import Iterable


class PriorityQueue:
    def __init__(self, items: Iterable[Any]|None = None) -> None:
        self.heap: list[Any] = [0]      # Element 0 is not used
        self.rank: dict[Any, int] = {}
        if items:
            for item in items:
                self.push(item)

    def __len__(self):
        return len(self.heap)-1         # Element 0 doesn't count

    def __str__(self) -> str:
        #return __class__.__name__ + ' '+str(self.heap[1:])             # mypy doesn't like __class__ (https://github.com/python/mypy/issues/4177)
        return type(self).__name__ + ' '+str(self.heap[1:])

    def push(self, item: Any):
        assert not item in self.rank
        ix = len(self.heap)
        self.heap.append(item)          # Nouvelle feuille
        self.rank[item] = ix
        self._up(ix)

    def pop(self) -> Any:
        root = self.heap[1]
        del self.rank[root]
        x = self.heap.pop()             # On enlève la dernière feuille
        if self:
            self.heap[1] = x            # Et on le met à la racine
            self.rank[x] = 1
            self._down(1)                # On rééquilibre
        return root

    # Helper, remonte l'élément d'index ix jusqu'à la position correcte O(log(n))
    def _up(self, ix: int):
        item = self.heap[ix]
        while ix > 1 and item < self.heap[ix//2]:
            self.heap[ix] = self.heap[ix//2]
            self.rank[self.heap[ix]] = ix
            ix //= 2
        self.heap[ix] = item
        self.rank[item] = ix

    # Helper, descend l'élément d'index ix jusqu'à la position correcte en gardant l'équilibre
    def _down(self, ix: int):
        item = self.heap[ix]
        n = len(self.heap)
        while True:
            left = 2*ix
            right = left+1
            # On commence par la droite s'il y a un fils à droite et que l'élement est plus grand que les fils gauche et droite
            if right < n and self.heap[right] < item and self.heap[right] < item and self.heap[right] < self.heap[left]:
                self.heap[ix] = self.heap[right]    # On monte le fils de droite
                self.rank[self.heap[right]] = ix
                ix = right
            elif left < n and self.heap[left] < item:  # Puis on tente de descendre à gauche
                self.heap[ix] = self.heap[left]
                self.rank[self.heap[left]] = ix
                ix = left
            else:                                   # Sinon on a trouvé la position et c'est fini
                self.heap[ix] = item
                self.rank[item] = ix
                return

    # Doesn't exist in heapq
    def update(self, old: Any, new: Any):
        ix = self.rank[old]
        del self.rank[old]
        self.heap[ix] = new
        self.rank[new] = ix
        if old < new:
            self._down(ix)
        else:
            self._up(ix)


if __name__ == "__main__":
    pq = PriorityQueue()
    pq.push(14)
    pq.push(2)
    pq.push(7)
    pq.push(17)
    pq.push(-3)
    print(pq, len(pq))
    while len(pq) > 0:
        print(pq.pop())
    print()

    pq = PriorityQueue([10, 4, 11, 9, 5, 2, 3])
    print(pq, len(pq))
    while pq:
        print(pq.pop())
    print()

    pq = PriorityQueue([10, 4, 11, 9, 5, 2, 3])
    pq.update(2, 6)
    while pq:
        print(pq.pop())
