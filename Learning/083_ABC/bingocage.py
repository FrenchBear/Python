# bingocage is a valid exemple of class implementing Tombola interface using a shuffled list and popping last item
# 2021-04-28    PV

import random
from tombola import Tombola
from typing import Any

from collections.abc import Iterable

class BingoCage(Tombola):
    def __init__(self, items: Iterable) -> None:
        self._randomizer = random.SystemRandom()
        self._items: list[Any] = []
        self.load(items)

    def load(self, items: Iterable) -> None:
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self) -> Any:
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    
    def __call__(self):
        self.pick()


if __name__=='__main__':
    bc = BingoCage(['do','ré','mi','fa','sol','la','si'])
    while bc.loaded():
        print(bc.pick())
