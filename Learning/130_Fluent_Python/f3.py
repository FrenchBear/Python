from collections.abc import Iterable
from collections import Counter
from collections.abc import Sequence
from typing import TypeVar

ST = TypeVar('ST', int, float, str)
#ST = TypeVar('ST')

def somme(data: Sequence[ST], init: ST) -> ST:
    s: ST = init
    item: ST
    for item in data:
        s += item
    return s

T = TypeVar('T')

def pareil(a: T, b: T) -> bool:
    return a == b


s = somme(range(1, 101), 0)
print(s)

t = somme(["bon", "jour", "!"], '')
print(t)


def mode(data: Iterable[T]) -> T:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]


print(mode('anticonstitutionnellement'))
