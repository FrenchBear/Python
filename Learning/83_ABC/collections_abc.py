# Collections ABCs
# 2021-04-30    PV

from collections.abc import *
from collections import *
from typing import Type, Union, Any
from types import MappingProxyType
import math
from array import array

# Any beacuse of Hashable
lb: list[Union[Type,Any]] = [MutableSequence, MutableMapping, MutableSet, ItemsView, ValuesView, KeysView, Sequence, Mapping, Set, MappingView, Iterator, Iterable, Container, Sized, Callable, Hashable]

def test(x) -> None:
    print("{:<15.15} {:<11.11}".format(str(x), type(x).__name__), end='')
    for abc in lb:
        print("{:^8} ".format('X' if isinstance(x, abc) else ' '), end='')
    print()


print('Value           Class      ', end='')
for abc in lb:
    print("{:^8.8} ".format(abc.__name__), end='')
print()
print('                           ', end='')
for abc in lb:
    print("{:^8.8} ".format(abc.__name__[8:]), end='')
print()

# Collections
d = {1:'one', 2:'two'}
test(d)
test(d.items())
test(d.keys())
test(d.values())
test(set(range(3)))
test([1,2,3])
test(UserList(range(3)))
test((1,2,3))
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
