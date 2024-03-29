# it.py
# Essais sur les itertools
#
# 2018-08-30    PV
# 2018-09-01    PV      Use itertools.islice instead of top
# 2023-08-26    PV      Added some type hints; skip from islice; pairwise (python 3.10) example, deep_flatten

import itertools
from typing import Any, TypeVar, List
from collections.abc import Callable, Iterable, Iterator, ItemsView
import collections
import functools
import operator
import random

T = TypeVar('T')
U = TypeVar('U')

# Helper to limit the size of an interable to the first n elements
# Actually use islice(seq, n) instead
def top(seq: Iterable[T], n: int) -> Iterable[T]:
    for item in seq:
        if n <= 0:
            return
        n -= 1
        yield item

print(list(itertools.islice(range(10), 5)))
print(list(top(range(10), 5)))
print()

# Infinite iterators
print(list(itertools.islice(itertools.count(10, 3), 20)))  # count is endless, islice limit number of items
print(list(itertools.takewhile(lambda x: x < 18, itertools.count(10, 3))))  # or takewhile only returns while lambra predicate is true
print(list(itertools.islice(itertools.cycle("ABCD"), 20)))
print(list(itertools.repeat(3.14, 20)))

# Iterators terminating on the shortest input sequence:
print(list(itertools.accumulate([1, 2, 3, 4, 5, 6])))  # Default: func=operator.add
# Same thing but returns last element
print(functools.reduce(operator.add, ([1, 2, 3, 4, 5, 6])))
print(list(itertools.accumulate([1, 2, 3, 4, 5, 6], lambda a, b: a + b**2)))
print(list(itertools.accumulate(range(1, 11), operator.mul)))
# Same thing but returns last element
print(functools.reduce(lambda a, b: a + b**2, ([1, 2, 3, 4, 5, 6])))
print(list(itertools.chain("ABC", [1, 2, 3], (False, True))))
print(list(itertools.chain.from_iterable(["ABC", [1, 2, 3], (False, True)])))
print(list(itertools.compress("ABCDEFG", [1, 0, 1, 0, 0, 1, 1, 0])))
print(list(itertools.dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1])))
print(list(itertools.filterfalse(lambda x: x % 2, range(10))))
print(list(filter(lambda x: x % 2, range(10))))

# groupby needs input list pre-sorted by key, so it's not that convenient...
# You can build tuples containing key to calculate it once such as in this example,
# or compute key twice, one to sort the list, one to call groupby
# Advantage of groupby: limited memory use since there is no storage at all, just
# iterators progressing sequentilly on input data.  Can be used with infinite iterators.
lf = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
gi = itertools.groupby(sorted([(v % 3, v) for v in lf], key=lambda tup: tup[0]), lambda tup: tup[0])
for key, group in gi:
    print("Fib %3=", key, ": ", end="")
    for i in group:
        print(i[1], end=" ")
    print()

# My version, uses more memory (builds lists) but easier to use
def my_groupby(list: Iterable[T], key: Callable[[T], U]) -> ItemsView[U, list[T]]:
    dic: dict[U, List[T]] = {}      # For some reason, Mypy rejects list[T]: Variable "list" is not valid as a type
    for item in list:
        k = key(item)
        if k in dic:
            dic[k].append(item)
        else:
            dic[k] = [item]
    return dic.items()


for key2, group2 in my_groupby(lf, lambda v: v % 3):
    print("Fib %3=", key2, ": ", end="")
    for i2 in group2:
        print(i2, end=" ")
    print()

print(list(itertools.islice("ABCDEFG", 2, None, 2)))
print(list(itertools.starmap(pow, [(2, 5), (3, 2), (10, 3)])))
print(list(itertools.takewhile(lambda x: x < 5, [1, 4, 6, 4, 1])))

print(list(itertools.pairwise("ABCD")))  # [('A', 'B'), ('B', 'C'), ('C', 'D')]

# tee is actually powerful, since it returns multiple copies of an iterator, which can all be iterated over independently.
# After calling tee, the iterator used as an argument shouldn't be used.
# Internally tee keeps a list containing objects returned by the most advanced output iterator which haven't been consumed
# by the slowest iterator yet, so it may consume memory for large iterables and iterators of different pace.
# Note that clone() can't be used with generators (current state of iterator is not stored in a private property such
# as index but by the  state machine implementation of a generator)
w1, w2, w3 = itertools.tee("ABC", 3)
print(list(w1), list(w2), list(w3))

print(list(itertools.zip_longest("ABCD", "xy", fillvalue="-")))  # [('A', 'x'), ('B', 'y'), ('C', '-'), ('D', '-')]
print()

# Combinatorics generators
for x in itertools.product("AB", [1, 2], (False, True)):
    print(x)    # ('A', 1, False) ('A', 1, True) ('A', 2, False) ('A', 2, True) ('B', 1, False) ('B', 1, True) ('B', 2, False) ('B', 2, True)
print()
for y in itertools.product(['rond', 'carré', 'triangle'], repeat=3):
    print(y)    # ('rond', 'rond', 'rond') ('rond', 'rond', 'carré') ('rond', 'rond', 'triangle') ('rond', 'carré', 'rond') ...
print()

print(list(itertools.permutations("ABCD", 3)))  # [('A', 'B', 'C'), ('A', 'B', 'D'), ('A', 'C', 'B'), ('A', 'C', 'D'), ('A', 'D', 'B'), ...
print(list(itertools.combinations("ABCD", 3)))  # [('A', 'B', 'C'), ('A', 'B', 'D'), ('A', 'C', 'D'), ('B', 'C', 'D')]
# [('A', 'A', 'A'), ('A', 'A', 'B'), ('A', 'A', 'C'), ('A', 'A', 'D'), ('A', 'B', 'B'), ('A', 'B', 'C'), ...
print(list(itertools.combinations_with_replacement("ABCD", 3)))


# Recipes from Python doc

"""
10.1.2. Itertools Recipes

This section shows recipes for creating an extended toolset using the existing itertools as building blocks.

The extended tools offer the same high performance as the underlying toolset. The superior memory performance is kept by
processing elements one at a time rather than bringing the whole iterable into memory all at once. Code volume is kept
small by linking the tools together in a functional style which helps eliminate temporary variables. High speed is
retained by preferring “vectorized” building blocks over the use of for-loops and generators which incur interpreter
overhead.
"""


def take(n: int, iterable: Iterable[T]) -> list[T]:
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))              # List[] is not needed, the islice object is iterable

print(take(5, itertools.count(0.2, 0.2)))   # [0.2, 0.4, 0.6000000000000001, 0.8, 1.0]


def prepend(value: Any, iterable: Iterable) -> Iterable:
    "Prepend a single value in front of an iterable"
    # prepend(1, [2, 3, 4]) -> 1 2 3 4
    return itertools.chain([value], iterable)

print(list(prepend(0, [1, 2, 3])))    # [0, 1, 2, 3]


def tabulate(function: Callable[[int], T], start=0) -> Iterable[T]:
    "Return function(0), function(1), ..."
    return map(function, itertools.count(start))

print(list(take(10, tabulate(lambda x: x * 7, 1))))    # [7, 14, 21, 28, 35, 42, 49, 56, 63, 70]


def tail(n: int, iterable: Iterable[T]) -> Iterable[T]:
    "Return an iterator over the last n items"
    return iter(collections.deque(iterable, maxlen=n))

print(list(tail(3, 'ABCDEFG')))     # ['E', 'F', 'G']


def consume(iterator: Iterable[T], n=None) -> None:
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(itertools.islice(iterator, n, n), None)


def nth(iterable: Iterable[T], n: int, default: U | None = None) -> T | U | None:
    "Returns the nth (starts at 0) item or a default value: returns iterable[n] even though iterable doesn't support indexing"
    return next(itertools.islice(iterable, n, None), default)

print(nth(range(20), 7))     # 7


def all_equal(iterable: Iterable) -> bool:
    "Returns True if all the elements are equal to each other"
    g: Iterator = itertools.groupby(iterable)
    return next(g, True) and not next(g, False)

print(all_equal([42,42,40+2,44-2]))     # True


def quantify(iterable: Iterable[T], pred: Callable[[T], bool]=bool) -> int:
    "Count how many times the predicate is true"
    return sum(map(pred, iterable))

print(quantify([1,1,2,3,5,8,13], lambda x:x%2==0))    # 2


def padnone(iterable: Iterable) -> Iterable:
    """Returns the sequence elements and then returns None indefinitely.
    Useful for emulating the behavior of the built-in map() function.
    """
    return itertools.chain(iterable, itertools.repeat(None))


def ncycles(iterable: Iterable, n: int) -> Iterable:
    "Returns the sequence elements n times"
    return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))

print(list(ncycles(['Pomme', 3.14, True], 4)))    # ['Pomme', 3.14, True, 'Pomme', 3.14, True, 'Pomme', 3.14, True, 'Pomme', 3.14, True]


N=TypeVar('N', complex, float)  # Doesn't work with numpy tupes, but if we use numpy, we don't need this function!
def dotproduct(vec1: Iterable['N'], vec2: Iterable['N']) -> N:
    return sum(map(operator.mul, vec1, vec2))

v1 = (1.2, -3.1, 5.0)
v2 = (0.5, 0, -1)
print(dotproduct(v1,v2))    # -4.4

# See also deep_platten at the end
def flatten(listOfLists: Iterable[Iterable]) -> Iterable:
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(listOfLists)

print(list(flatten([(1,2),[3,4,5], (6,)])))     # [1, 2, 3, 4, 5, 6]


def repeatfunc(func: Callable, times:int|None=None, *args) -> Any:
    """Repeat calls to func with specified arguments.
    Example:  repeatfunc(random.random)
    """
    if times is None:
        return itertools.starmap(func, itertools.repeat(args))
    return itertools.starmap(func, itertools.repeat(args, times))

print(list(take(5, repeatfunc(random.random))))    # [0.3397989174275057, 0.49333666028669054, 0.7170501884654843, 0.5892154468459484, 0.7140313769040765]


def my_pairwise(iterable: Iterable) -> Iterable[tuple[Any, Any]]:
    "s -> (s0,s1), (s1,s2), (s2,s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

print(list(my_pairwise((1,2,'A', True))))    # [(1, 2), (2, 'A'), ('A', True)]


def grouper(iterable: Iterable, n: int, fillvalue=None) -> Iterable[tuple]:
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n    # nx the same iterator object
    return itertools.zip_longest(*args, fillvalue=fillvalue)

print(list(grouper('ABCDEFG', 3, 'x')))    # [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = itertools.cycle(itertools.islice(nexts, num_active))


def partition(pred, iterable):
    "Use a predicate to partition entries into false entries and true entries"
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = itertools.tee(iterable)
    return itertools.filterfalse(pred, t1), filter(pred, t2)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def unique_justseen(iterable, key=None):
    "List unique elements, preserving order. Remember only the element just seen."
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBCcAD', str.lower) --> A B C A D
    return map(next, map(operator.itemgetter(1), itertools.groupby(iterable, key)))


def iter_except(func, exception, first=None):
    """Call a function repeatedly until an exception is raised.

    Converts a call-until-exception interface to an iterator interface.
    Like builtins.iter(func, sentinel) but uses an exception instead of a sentinel to end the loop.
    Examples:
        iter_except(functools.partial(heappop, h), IndexError)   # priority queue iterator
        iter_except(d.popitem, KeyError)                         # non-blocking dict iterator
        iter_except(d.popleft, IndexError)                       # non-blocking deque iterator
        iter_except(q.get_nowait, Queue.Empty)                   # loop over a producer Queue
        iter_except(s.pop, KeyError)                             # non-blocking set iteratorauto
    """
    try:
        if first is not None:
            yield first()  # For database APIs needing an initial cast to db.first()
        while True:
            yield func()
    except exception:
        pass


def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*
    If *pred* is not None, returns the first item for which pred(item) is true.
    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)


def random_product(*args, repeat=1):
    "Random selection from product(*args, **kwds)"
    pools = [tuple(pool) for pool in args] * repeat
    return tuple(random.choice(pool) for pool in pools)


def random_permutation(iterable, r=None):
    "Random selection from permutations(iterable, r)"
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))


def random_combination(iterable, r):
    "Random selection from combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)


def random_combination_with_replacement(iterable, r):
    "Random selection from combinations_with_replacement(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.randrange(n) for i in range(r))
    return tuple(pool[i] for i in indices)


def nth_combination(iterable, r, index):
    "Equivalent to list(combinations(iterable, r))[index]"
    pool = tuple(iterable)
    n = len(pool)
    if r < 0 or r > n:
        raise ValueError
    c = 1
    k = min(r, n - r)
    for i in range(1, k + 1):
        c = c * (n - k + i) // i
    if index < 0:
        index += c
    if index < 0 or index >= c:
        raise IndexError
    result = []
    while r:
        c, n, r = c * r // n, n - 1, r - 1
        while index >= c:
            index -= c
            c, n = c * (n - r) // n, n - 1
        result.append(pool[-1 - n])
    return tuple(result)


print(take(10, repeatfunc(random.random)))
print(random_product("ABC", "xyz", "123"))

# Skip n first elements of an iterable
def skip(n: int, iterable: Iterable[T]) -> Iterable[T]:
    "Skip first n items of the iterable"
    return itertools.islice(iterable, n, None)


print(list(skip(10, range(21))))

# Multi-level flattening (recursive)
def deep_flatten(*args) -> Iterable:
    for l in args:
        try:
            it = iter(l)
            yield from deep_flatten(*it)
        except TypeError:
            yield l

print(list(deep_flatten([1], 2, (3,4), [[5, [6,7]], (8, (9, (10,)))])))
