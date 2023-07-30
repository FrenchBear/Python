# somme.py
# Example of typing.Protocol to implement Addable, used to constraint a generic type to support __add__
# Ok for Mypy, Jedi and Ruff, but Pylance doesn't understand it
#
# 2023-07-30    PV

from collections.abc import Iterable
from collections import Counter
from collections.abc import Sequence
from typing import TypeVar, Protocol, TypeAlias


T = TypeVar("T")


class Addable(Protocol):
    pass
    def __add__(self: T, other: T) -> T: ...


TADD = TypeVar('TADD', bound=Addable)
TADD_SEQUENCE: TypeAlias = Sequence[TADD]


def somme(data: TADD_SEQUENCE, init: TADD) -> TADD:
    s: TADD = init
    item: TADD
    for item in data:
        s += item
    return s


s = somme(range(1, 101), 0)
print(s)

t = somme(["bon", "jour", "!"], '')
print(t)


# T is local to function definition (not the same T used in class Addable)
def mode(data: Iterable[T]) -> T:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]


print(mode('anticonstitutionnellement'))
