# Collections ABCs
# 2021-04-30    PV

from collections.abc import *
from collections import deque, defaultdict
from typing import Type


lb: list[Type] = [MutableSequence, MutableMapping, MutableSet, ItemsView, ValuesView, KeysView, Sequence, Mapping, Set, MappingView, Iterator, Iterable, Container, Sized, Callable, Hashable]

def test(x) -> None:
    print("{:<15.15} {:<11.11}".format(str(x), type(x).__name__), end='')
    for abc in lb:
        print("{:^9}".format('X' if isinstance(x, abc) else ' '), end='')
    print()


print('Value           Class      ', end='')
for abc in lb:
    print("{:^8.8} ".format(abc.__name__), end='')
print()
print('                           ', end='')
for abc in lb:
    print("{:^8.8} ".format(abc.__name__[8:]), end='')
print()

d = {1:'one', 2:'two'}
test(d)
test(d.items())
test(d.keys())
test(d.values())
test(set(range(3)))
test([1,2,3])
test((1,2,3))
test(deque())
test(defaultdict(int))
test(range(3))
