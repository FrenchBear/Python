# Example 13-13. double_protocol.py: definition of double using a Protocol

from typing import TypeVar, Protocol
T = TypeVar('T')

class Repeatable(Protocol):
    def __mul__(self: T, repeat_count: int) -> T: ...

RT = TypeVar('RT', bound=Repeatable)

def double(x: RT) -> RT:
    return x * 2
