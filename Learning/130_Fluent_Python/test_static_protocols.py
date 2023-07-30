# test_static_protocols.py
# fluent python example 8-22

from collections.abc import Iterator
from collections.abc import Iterable
from typing import TypeVar, Protocol, Any, TYPE_CHECKING
import pytest

class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...

LT = TypeVar('LT', bound=SupportsLessThan)

def top(series: Iterable[LT], length: int) -> list[LT]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]

def test_top_tuples() -> None:
    fruit = 'mango pear apple kiwi banana'.split()
    series: Iterator[tuple[int, str]] = ((len(s), s) for s in fruit)
    # series = ((len(s), s) for s in fruit)
    length = 3
    expected = [(6, 'banana'), (5, 'mango'), (5, 'apple')]
    result = top(series, length)
    if TYPE_CHECKING:
        reveal_type(series)     # noqa
        reveal_type(expected)   # noqa
        reveal_type(result)     # noqa
    assert result == expected

# intentional type error
def test_top_objects_error() -> None:
    series = [object() for _ in range(4)]
    if TYPE_CHECKING:
        reveal_type(series)     # noqa
    with pytest.raises(TypeError) as excinfo:
        top(series, 3)
    assert "'<' not supported" in str(excinfo.value)

test_top_tuples()
test_top_objects_error()
