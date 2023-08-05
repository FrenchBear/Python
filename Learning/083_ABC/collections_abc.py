# Collections ABCs
#
# 2021-04-30    PV
# 2023-07-29    PV      Better output, SplitName, specific imports

from collections.abc import MutableSequence, MutableMapping, MutableSet, ItemsView, ValuesView, KeysView, \
    Sequence, Mapping, Set, MappingView, Iterator, Iterable, Container, Sized, Callable, Hashable
from collections import UserList, deque, defaultdict, OrderedDict, ChainMap, Counter, UserDict, UserString
from typing import Any
from types import MappingProxyType
import math
from array import array

# Any beacuse of Hashable
lb: list = [MutableSequence, MutableMapping, MutableSet, ItemsView, ValuesView, KeysView,
            Sequence, Mapping, Set, MappingView, Iterator, Iterable, Container, Sized, Callable, Hashable]


def test(x: Any) -> None:
    print("{:<15.15} {:<11.11}|".format(str(x), type(x).__name__), end='')
    for abc in lb:
        print("{:^8}|".format('X' if isinstance(x, abc) else ' '), end='')
    print()


def SplitName(s) -> tuple[str, str]:
    if len(s) < 0:
        return (s, '')
    for i in range(3, len(s)-2):
        if 'A' <= s[i] <= 'Z':
            return (s[:i], s[i:])
    return (s[:8], s[8:])


print('Value           Class      |', end='')
for abc in lb:
    s = SplitName(abc.__name__)
    print("{:^8.8}|".format(s[0]), end='')
print()
print('                           |', end='')
for abc in lb:
    s = SplitName(abc.__name__)
    print("{:^8.8}|".format(s[1]), end='')
print()

# Collections
d = {1: 'one', 2: 'two'}
test(d)
test(d.items())
test(d.keys())
test(d.values())
test(set(range(3)))
test([1, 2, 3])
test(UserList(range(3)))
test((1, 2, 3))
test(deque())
test(range(3))
test(array('i', range(3)))

# Stuff
g = (i for i in range(3))
test(g)                     # generator
test(g.__iter__)            # method_wrapper (?)
test(iter(range(3)))        # range_iterator
test(lambda x: 2*x)         # function
test(math)                  # module
test(list)                  # type

# Specialized dicts
test(defaultdict(int))      # Provide a default value
test(OrderedDict())         # keep insertion odrer
test(ChainMap())            # search in multiple dictionaries
test(Counter())             # Count elements
test(UserDict())            # Same as dict, but written in Python, can inherit from it
test(MappingProxyType(d))   # Readonly dictionary

# strings
test('zap')
test(UserString('zap'))
test("""xxx""")
