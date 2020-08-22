# it.py
# Essais sur les itertools
#
# 2018-08-30    PV
# 2018-09-01    PV      Use itertools.islice instead of top

from itertools import *
from typing import Dict, Iterable, Any
import collections
import functools
import operator
import math
import random

# Helper to limit the size of an interable to the first n elements


# use islice instead
# def top(seq: Iterable, n: int):
#     for item in seq:
#         if n <= 0:
#             return
#         n -= 1
#         yield item


# Infinite iterators
print(list(islice(count(10, 3), 20)))
print(list(islice(cycle("ABCD"), 20)))
print(list(repeat(3.14, 20)))

# Iterators terminating on the shortest input sequence:
print(list(accumulate([1, 2, 3, 4, 5, 6])))       # Default: func=operator.add
# Same thing but returns last element
print(functools.reduce(operator.add, ([1, 2, 3, 4, 5, 6])))
print(list(accumulate([1, 2, 3, 4, 5, 6], lambda a, b: a+b**2)))
# Same thing but returns last element
print(functools.reduce(lambda a, b: a+b**2, ([1, 2, 3, 4, 5, 6])))
print(list(chain("ABC", [1, 2, 3], (False, True))))
print(list(chain.from_iterable(["ABC", [1, 2, 3], (False, True)])))
print(list(compress("ABCDEFG", [1, 0, 1, 0, 0, 1, 1, 0])))
print(list(dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1])))
print(list(filterfalse(lambda x: x % 2, range(10))))
print(list(filter(lambda x: x % 2, range(10))))

# groupby needs input list pre-sorted by key, so it's not that convenient...
# You can build tuples containing key to calculate it once such as in this example,
# or compute key twice, one to sort the list, one to call groupby
# Advantage of groupby: limited memory use since there is no storage at all, just
# iterators progressing sequentilly on input data.  Can be used with infinite iterators.
lf = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
gi = groupby(
    sorted([(v % 3, v) for v in lf], key=lambda tup: tup[0]), lambda tup: tup[0])
for key, group in gi:
    print("Fib %3=", key, ": ", end='')
    for i in group:
        print(i[1], end=' ')
    print()

# My version, uses more memory (builds lists) but easier to use


def mygroupby(list: Iterable, key):
    dic: Dict[Any, Any] = {}
    for item in list:
        k = key(item)
        if k in dic:
            dic[k].append(item)
        else:
            dic[k] = [item]
    return dic.items()


for key, group in mygroupby(lf, lambda v: v % 3):
    print("Fib %3=", key, ": ", end='')
    for i in group:
        print(i, end=' ')
    print()

print(list(islice('ABCDEFG', 2, None, 2)))
print(list(starmap(pow, [(2, 5), (3, 2), (10, 3)])))
print(list(takewhile(lambda x: x < 5, [1, 4, 6, 4, 1])))

w1, w2, w3 = tee("ABC", 3)
print(list(w1), list(w2), list(w3))

print(list(zip_longest('ABCD', 'xy', fillvalue='-')))

for x in product("AB", [1, 2], (False, True)):
    print(x)

print(list(permutations("ABCD", 3)))
print(list(combinations("ABCD", 3)))
print(list(combinations_with_replacement("ABCD", 3)))

# Pipeline in Python
# Equivalent of C#
# var l = Enumerable.Range(0, 50).Select(x => x*x).Where(x => x%2==1).OrderBy(x => Math.Sin(x));
l1 = range(50)
l2 = map(lambda x: x*x, l1)
l3 = filter(lambda x: x % 2 == 1, l2)
l4 = sorted(l3, key=math.sin)
print(l4)

# Using generator expressions
l1b = range(50)
l2b = (i * i for i in l1b)
l3b = (i for i in l2b if i % 2 == 1)
l4b = sorted(l3b, key=math.sin)
print(l4b)


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


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def prepend(value, iterator):
    "Prepend a single value in front of an iterator"
    # prepend(1, [2, 3, 4]) -> 1 2 3 4
    return chain([value], iterator)


def tabulate(function, start=0):
    "Return function(0), function(1), ..."
    return map(function, count(start))


def tail(n, iterable):
    "Return an iterator over the last n items"
    # tail(3, 'ABCDEFG') --> E F G
    return iter(collections.deque(iterable, maxlen=n))


def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)


def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def quantify(iterable, pred=bool):
    "Count how many times the predicate is true"
    return sum(map(pred, iterable))


def padnone(iterable):
    """Returns the sequence elements and then returns None indefinitely.
    Useful for emulating the behavior of the built-in map() function.
    """
    return chain(iterable, repeat(None))


def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(tuple(iterable), n))


def dotproduct(vec1, vec2):
    return sum(map(operator.mul, vec1, vec2))


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.
    Example:  repeatfunc(random.random)
    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))


def partition(pred, iterable):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
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
    return map(next, map(operator.itemgetter(1), groupby(iterable, key)))


def iter_except(func, exception, first=None):
    """ Call a function repeatedly until an exception is raised.

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
            yield first()            # For database APIs needing an initial cast to db.first()
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
    'Equivalent to list(combinations(iterable, r))[index]'
    pool = tuple(iterable)
    n = len(pool)
    if r < 0 or r > n:
        raise ValueError
    c = 1
    k = min(r, n-r)
    for i in range(1, k+1):
        c = c * (n - k + i) // i
    if index < 0:
        index += c
    if index < 0 or index >= c:
        raise IndexError
    result = []
    while r:
        c, n, r = c*r//n, n-1, r-1
        while index >= c:
            index -= c
            c, n = c*(n-r)//n, n-1
        result.append(pool[-1-n])
    return tuple(result)


print(take(10, repeatfunc(random.random)))
print(random_product("ABC", "xyz", "123"))
