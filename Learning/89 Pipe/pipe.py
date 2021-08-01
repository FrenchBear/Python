# pipe.py
# play with pipeline architecture
# 2021-08-01    PV

from typing import Callable, Iterable, Iterator, Optional, TypeVar
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


animaux = ['chien', 'chat', 'ours', 'âne', 'porc', 'boeuf']

p = Pipe(animaux) \
    .pipe_select(lambda a: len(a))  \
    .pipe_where(lambda l: l % 2 == 0)  \
    .final_count(lambda l: l>=6)
print(p)

p = Pipe(animaux)   \
    .pipe_first(lambda a: a.startswith('z'))
for a in p:
    print(a)

print(Pipe(animaux).final_first_or_none(lambda a: a.startswith('s')))
