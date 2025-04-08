# pipe.py
# Play with pipeline model to chain transformations such as filtering or sorting easily
# No attempt is made to curcumvent the Python issue that an iterator can only be used once.
#
# ToDo later: implement group_by (not difficult)
#
# 2021-08-01    PV
# 2025-04-08    PV      Refactoring without TypeVar, it's not needed anymore

from typing import Callable, Iterable, Iterator, Optional, cast, Any

# A wrapper for iterable structure.  Member methods such as where or sort returns the output as
# a Pipe, enabling convenient chaining until (optional) final transformation that does not return
# a Pipe.
class Pipe[T]:
    def __init__(self, source: Iterable[T]) -> None:
        # Will raise a TypeError if source is not iterable
        self.iter = iter(source)

    def __iter__(self) -> Iterator[T]:
        return self.iter

    # Also used for str()
    def __repr__(self) -> str:
        l = []
        i = 0
        for item in self.iter:
            i += 1
            if i > 15:
                l.append('...')
                break
            l.append(repr(item))
        return '['+','.join(l)+']'


    # --------------------------------
    # Static methods of pipe (generators returning a pipe)

    @staticmethod
    def range(start: int, stop: Optional[int] = None, step: int = 1) -> 'Pipe':
        """Returns a pipe of integers using same parameters as Python builtin range([start=0], end, [step=1]), that is the sequence from start to end-1 by step."""
        if stop is None:
            start, stop = 0, start
        return Pipe(range(start, stop, step))

    @staticmethod
    def repeat(element: T, count: int) -> 'Pipe':
        """Returns an pipe containing element repeated count times"""
        def repeater():
            for i in range(count):
                yield element
        return Pipe(repeater())


    # --------------------------------
    # Tranformation functions of a pipe (returning a pipe)

    def where(self, predicate: Callable[[T], bool]) -> 'Pipe':
        """Filters elements of the pipe, only keeping the ones matching the preicate provided."""
        def iter_where():
            for item in self.iter:
                if predicate(item):
                    yield item
        return Pipe(iter_where())

    def select[U](self, select: Callable[[T], U]) -> 'Pipe':
        """Trasforms elements of the pipe using function provided."""
        def iter_select():
            for item in self.iter:
                yield select(item)
        return Pipe(iter_select())

    def sort(self, key=None, reverse: bool = False) -> 'Pipe':
        """Sorts elements of the pipe. If no key selector is provided, sorts on elements value. reverse argument reverses the sort."""
        def sorter():
            l = list(self.iter)
            l.sort(key=key, reverse=reverse)
            yield from l
        return Pipe(sorter())

    def reverse(self) -> 'Pipe':
        """Reverses elements of the pipe."""
        def reverser():
            l = list(self.iter)
            l.reverse()
            yield from l
        return Pipe(reverser())

    def concat(self, *iterables) -> 'Pipe':
        """Concatenates iterables to current pipe, keeping duplicates."""
        def concatener():
            yield from self
            for iterable in iterables:
                yield from iterable
        return Pipe(concatener())

    def distinct(self) -> 'Pipe':
        """Remove duplicate elements in the pipe."""
        def deduplicator():
            s = set(self.iter)
            yield from s
        return Pipe(deduplicator())

    def intersect(self, *iterables) -> 'Pipe':
        """Produces the pipe intersection of enumerables."""
        def intersector():
            s = set(self.iter).intersection(*iterables)
            yield from s
        return Pipe(intersector())

    def union(self, *iterables) -> 'Pipe':
        """Produces the pipe union of enumerables, removing duplicates."""
        def unionor():
            s = set(self.iter).union(*iterables)
            yield from s
        return Pipe(unionor())

    def skip(self, count: int) -> 'Pipe':
        """Bypasses a specified number of elements in a pipe and then returns the remaining elements."""
        def skipper():
            nonlocal count
            for item in self.iter:
                if count>0:
                    count-=1
                else:
                    yield item
        return Pipe(skipper())

    def skip_last(self, count: int) -> 'Pipe':
        """Returns a new pipe that contains the elements from source with the last count elements omitted."""
        def skipper_last():
            l = list(self.iter)
            yield from l[:-count]
        return Pipe(skipper_last())

    def take(self, count: int) -> 'Pipe':
        """Returns a specified number of contiguous elements from the start of a pipe."""
        def taker():
            nonlocal count
            for item in self.iter:
                if count>0:
                    yield item
                    count-=1
                else:
                    break
        return Pipe(taker())

    def take_last(self, count: int) -> 'Pipe':
        """Returns a new pipe that contains the last count elements from source."""
        def taker_last():
            l = list(self.iter)
            yield from l[-count:]
        return Pipe(taker_last())

    def take_while(self, predicate: Callable[[T], bool]) -> 'Pipe':
        """Returns elements from a sequence as long as a specified condition is true, and then skips the remaining elements."""
        def taker_while():
            for item in self.iter:
                if not predicate(item):
                    break
                yield item
        return Pipe(taker_while())

    def skip_while(self, predicate: Callable[[T], bool]) -> 'Pipe':
        """Bypasses elements in a pipe as long as a specified condition is true and then returns the remaining elements."""
        def skipper_while():
            do_yield = False
            for item in self.iter:
                if do_yield:
                    yield item
                else:
                    if not predicate(item):
                        do_yield = True
                        yield item
        return Pipe(skipper_while())

    def zip(self, *iterables) -> 'Pipe':
        """Produces a pipe of tuples with elements from the specified sequences. Stops at the end of shortest pipe."""
        def zipper():
            z = zip(self.iter, *iterables)
            yield from z
        return Pipe(zipper())

    def append(self, value: T) -> 'Pipe':
        """Adds a value to the end of the pipe."""
        def appender():
            yield from self.iter
            yield value
        return Pipe(appender())

    def prepend(self, value: T) -> 'Pipe':
        """Adds a value to the beginning of the pipe."""
        def prepender():
            yield value
            yield from self.iter
        return Pipe(prepender())


    # --------------------------------
    # Immediate (final) functions of a pipe (not returning a pipe)

    def count(self, predicate: Optional[Callable[[T], bool]] = None) -> int:
        """Returns number of elements of the pipe, or count only elements matching the predicate if it is provided.
        Immediate execution on call."""
        count = 0
        for item in self.iter:
            if predicate:
                if predicate(item):
                    count += 1
            else:
                count += 1
        return count

    def aggregate(self, aggregator: Callable, predicate: Optional[Callable[[T], bool]] = None) -> Any:
        """Aggregates a pipe of values, or only elements matching the predicate if it is provided, using aggregator.
        Immediate execution on call."""
        if predicate:
            return aggregator(item for item in self.iter if predicate(item))
        else:
            return aggregator(self.iter)

    def sum(self, predicate: Optional[Callable[[T], bool]] = None) -> float:
        """Sums all elements of a pipe of numbers, or only elements matching the predicate if it is provided.
        Immediate execution on call."""
        return self.aggregate(sum, predicate)

    def min(self, predicate: Optional[Callable[[T], bool]] = None) -> Any:
        """Returns min of a pipe of numbers, or only elements matching the predicate if it is provided.
        Immediate execution on call."""
        return self.aggregate(min, predicate)

    def max(self, predicate: Optional[Callable[[T], bool]] = None) -> Any:
        """Returns min of a pipe of numbers, or only elements matching the predicate if it is provided.
        Immediate execution on call."""
        return self.aggregate(max, predicate)

    def first_or_none(self, predicate: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        """Returns first element of the pipe, or the first element matching the predicate if it is provided. If pipe is empty or no matching element found, returns None.
        Immediate execution on call."""
        for item in self.iter:
            if predicate:
                if predicate(item):
                    return item
            else:
                return item
        # Return None if there is no match for a first
        return None

    def last_or_none(self, predicate: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        """Returns last element of the pipe, or the last element matching the predicate if it is provided. If pipe is empty or no matching element found, returns None.
        Immediate execution on call."""
        last = None
        for item in self.iter:
            if predicate:
                if predicate(item):
                    last = item
            else:
                last = item
        return last

    def join(self, separator: str, predicate: Optional[Callable[[str], bool]] = None) -> str:
        """Joins all elements of a pipe of strings into a string using separator, or only elements matching the predicate if it is provided.
        Immediate execution on call."""
        if predicate:
            return separator.join(item for item in cast(Iterator[str], self.iter) if predicate(item))
        else:
            return separator.join(cast(Iterator[str], self.iter))

    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """Without a predicate, checks if pipe contains at least one element.  With a predicate, checks if the pipe contains at least one element that matches the predicate.
        Immediate execution on call."""
        if predicate:
            for item in self.iter:
                if predicate(item):
                    return True
            return False
        else:
            try:
                _ = next(self.iter)
            except StopIteration:
                return False
            return True

    def all(self, predicate: Callable[[T], bool]) -> bool:
        """Checks if all elements of the pipe match the predicate. If the pipe is empty, returns True.
        Immediate execution on call."""
        for item in self.iter:
            if not predicate(item):
                return False
        return True

    def contains(self, value: T) -> bool:
        """Checks if the pipe contains value provided.
        Immediate execution on call."""
        for item in self.iter:
            if item==value:
                return True
        return False



# animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
# fruits = ['pomme', 'poire', 'ananas']
# couleurs = ['bleu', 'blanc', 'rouge']

#p = Pipe(animaux).concat(fruits, couleurs)
#print(p)
#print(Pipe.range(5).contains(9))
#print(Pipe(fruits).contains('poire'))
#print(Pipe([1,2,3]).any())
#print(Pipe([1,2,3]).any(lambda a: a==2))
#print(Pipe([1,2,3]).any(lambda a: a==5))
