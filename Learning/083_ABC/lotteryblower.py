# lotteryblower is a valid exemple of class implementing Tombola interface popping from a random position
# 2021-04-28    PV

import random
from tombola import Tombola
from typing import Any, Iterable

class LotteryBlower(Tombola):
    def __init__(self, items: Iterable) -> None:
        self._balls = list(items)

    def load(self, items: Iterable) -> None:
        self._balls.extend(items)

    def pick(self) -> Any:
        if len(self._balls):
            return self._balls.pop(random.randrange(len(self._balls)))
        raise LookupError('pick from empty LotteryBlower')

    def loaded(self) -> bool:
        return bool(self._balls)
    
    def inspect(self) -> tuple:
        return tuple(sorted(self._balls))


if __name__=='__main__':
    lb = LotteryBlower(['do','ré','mi','fa','sol','la','si'])
    while lb.loaded():
        print(lb.pick())
