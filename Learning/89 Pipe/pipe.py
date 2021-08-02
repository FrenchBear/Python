# pipe.py
# play with pipeline architecture
# 2021-08-01    PV

from typing import Callable, Iterable, Iterator, Optional, TypeVar
from numbers import Number

T = TypeVar('T')
U = TypeVar('U')


class Pipe:
    def __init__(self, source: Iterable[T]) -> None:
        # Will raise a TypeError if source is not iterable
        self.iter = iter(source)

    def __iter__(self) -> Iterator[T]:
        return self.iter

    def pipe_where(self, predicate: Callable[[T], bool]) -> 'Pipe':
        def iter_where():
            for item in self.iter:
                if predicate(item):
                    yield item
        return Pipe(iter_where())

    def pipe_select(self, select: Callable[[T], U]) -> 'Pipe':
        def iter_select():
            for item in self.iter:
                yield select(item)
        return Pipe(iter_select())

    def pipe_first(self, predicate: Optional[Callable[[T], bool]] = None) -> 'Pipe':
        def first_or_none():
            for item in self.iter:
                if predicate:
                    if predicate(item):
                        yield item
                        return
                else:
                    yield item
                    return
            # Do not yield anything if there is no match for a first
        return Pipe(first_or_none())

    def pipe_sort(self, key = None, reverse: bool = False) -> 'Pipe':
        def sorter():
            l = list(self.iter)
            l.sort(key=key, reverse=reverse)
            yield from l
        return Pipe(sorter())

    def pipe_reverse(self) -> 'Pipe':
        def reverser():
            l = list(self.iter)
            l.reverse()
            yield from l
        return Pipe(reverser())

    def final_count(self, predicate: Optional[Callable[[T], bool]] = None) -> int:
        count = 0
        for item in self.iter:
            if predicate:
                if predicate(item):
                    count += 1
            else:
                count += 1
        return count

    def final_first_or_none(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        for item in self.iter:
            if predicate:
                if predicate(item):
                    return item
            else:
                return item
        # Return None if there is no match for a first
        return None

    def final_sum(self, predicate: Optional[Callable[[T], bool]] = None) -> Number:
        sum:Number = 0
        for item in self.iter:
            if predicate:
                if predicate(item):
                    sum += item
            else:
                sum += item
        return sum



animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']

p = Pipe(animaux).pipe_reverse()
r = ','.join(repr(a) for a in p)
print(f'[{r}]')

