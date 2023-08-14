# Example 15-2, 15-3
# imports and definitions omitted, see next listing

from collections.abc import Callable, Iterable
from typing import Protocol, Any, TypeVar, overload, Union

class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...

T = TypeVar('T')
LT = TypeVar('LT', bound=SupportsLessThan)
DT = TypeVar('DT')

MISSING = object()
EMPTY_MSG = 'max() arg is an empty sequence'

@overload
def max(__arg1: LT, __arg2: LT, *args: LT, key: None = ...) -> LT:
    ...
@overload
def max(__arg1: T, __arg2: T, *args: T, key: Callable[[T], LT]) -> T:
    ...
@overload
def max(__iterable: Iterable[LT], *, key: None = ...) -> LT:
    ...
@overload
def max(__iterable: Iterable[T], *, key: Callable[[T], LT]) -> T:
    ...
@overload
def max(__iterable: Iterable[LT], *, key: None = ..., default: DT) -> Union[LT, DT]:
    ...
@overload
def max(__iterable: Iterable[T], *, key: Callable[[T], LT], default: DT) -> Union[T, DT]:
    ...

def max(first, *args, key=None, default=MISSING):
    if args:
        series = args
        candidate = first
    else:
        series = iter(first)
        try:
            candidate = next(series)
        except StopIteration:
            if default is not MISSING:
                return default
            raise ValueError(EMPTY_MSG) from None
    if key is None:
        for current in series:
            if candidate < current:
                candidate = current
    else:
        candidate_key = key(candidate)
        for current in series:
            current_key = key(current)
            if candidate_key < current_key:
                candidate = current
                candidate_key = current_key
    return candidate

# Arguments implementing SupportsLessThan, but key and default not provided
print(max(1,2,3))
print(max(['Go','Python','Rust']))

# Without redefining abs in a basic way, MyPy find 6 errors (3 times 2 errors using key=abs):
# mymax.py:72: error: Value of type variable "LT" of "max" cannot be "_T"  [type-var]
# mymax.py:72: error: Argument "key" to "max" has incompatible type "Callable[[SupportsAbs[_T]], _T]"; expected "Callable[[int], _T]"  [arg-type]
def abs(x):
     return x if x>=0 else -x

# Argument key provided, but no default
print(max(1, 2, -3, key=abs))
print(max(['Go', 'Python', 'Rust'], key=len))

# Argument default provided, but no key
print(max([1, 2, -3], default=0))  # returns 2
print(max([], default=None))  # returns None

# Arguments key and default provided
print(max([1, 2, -3], key=abs, default=None))  # returns -3
print(max([], key=abs, default=None))  # returns None
