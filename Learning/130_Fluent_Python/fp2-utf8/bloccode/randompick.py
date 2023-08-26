# Example 13-18. randompick.py: definition of RandomPicker

from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class RandomPicker(Protocol):
    def pick(self) -> Any: ...
