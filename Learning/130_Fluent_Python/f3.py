from typing import TypeVar, Protocol, Iterable, cast

T = TypeVar('T')

class SupportsAdd(Protocol):
    def __add__(self: T, other: T) -> T: ...

TA = TypeVar('TA', bound=SupportsAdd)

def mysum(it: Iterable[TA], init:TA|None = None) -> TA:
    s:TA
    if init is not None:
        s = init
    else:
        s = cast(TA, 0)
    item: TA
    for item in it:
        s = s+item
    return s

print(mysum(range(1,11)))
print(mysum(['a','b','c'], ''))
