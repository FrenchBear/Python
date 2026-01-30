# pipeline.py
# Another try to simulate C# Enumerable class and its convenient chainable methods
#
# 2023-08-26    PV      Already done in the past with more complex code, but a simple class can do it...

import itertools
from typing import Any, TypeVar, Protocol

from collections.abc import Callable, Iterable


# Pipeline in Python
# Equivalent of C#
# var l = Enumerable.Range(0, 50).Select(x => x*x).Where(x => x%2==1).OrderBy(x => Math.Sin(x));
l1 = range(50)
l2 = map(lambda x: x * x, l1)
l3 = filter(lambda x: x % 2 == 1, l2)
l4 = sorted(l3, key=str)
print(l4)

# Using generator expressions
l1b = range(50)
l2b = (i * i for i in l1b)
l3b = (i for i in l2b if i % 2 == 1)
l4b = sorted(l3b, key=str)
print(l4b)


# According to https://stackoverflow.com/questions/73504314/type-hint-for-can-be-compared-objects
# for sorting with the builtin sorted() function, __eq__ and __lt__ suffice.
T_co = TypeVar('T_co', covariant=True)
class Sortable(Protocol[T_co]):
    def __eq__(self: T_co, other: Any) -> bool: ...
    def __lt__(self: T_co, other: Any) -> bool: ...

TSortable = TypeVar('TSortable', bound=Sortable)      # Type comparable (actually, sortable)


class Pipe:
    def __init__(self, value: Iterable) -> None:
        self.value = value

    def __iter__(self):
        return iter(self.value)

    def Top(self, n: int) -> Pipe:
        return Pipe(itertools.islice(self.value, n))

    def Where(self, predicate: Callable[[Any], bool]) -> Pipe:
        return Pipe(filter(predicate, self.value))

    def Select(self, fn: Callable) -> Pipe:
        return Pipe(map(fn, self.value))

    def OrderBy(self, key: Callable[[Any], TSortable], reverse=False) -> Pipe:
        return Pipe(sorted(self.value, key=key, reverse=reverse))


p = Pipe(range(1, 21))
print(list(p))
print(list(p.Top(15)))
print(list(p.Top(15).Where(lambda x: x % 2 == 0)))
print(list(p.Top(15).Where(lambda x: x % 2 == 0).Select(lambda x: x * x)))
print(list(p.Top(15).Where(lambda x: x % 2 == 0).Select(lambda x: x * x).OrderBy(str)))
