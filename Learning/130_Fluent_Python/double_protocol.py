# double_protocol
# Example 13-13

from typing import TypeVar, Protocol

T = TypeVar('T')

class SupportsMul(Protocol):
    def __mul__(self: T, count: int) -> T: ...


TM = TypeVar('TM', bound=SupportsMul)

def double(x: TM) -> TM:
    return x * 2
