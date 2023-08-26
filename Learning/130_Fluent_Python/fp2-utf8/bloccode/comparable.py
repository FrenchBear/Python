# Example 8-20. comparable.py: definition of a SupportsLessThan Protocol type

from typing import Protocol, Any
class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...
