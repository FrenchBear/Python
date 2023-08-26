# Example 15-22. generic_randompick.py: definition of generic RandomPicker

from typing import Protocol, runtime_checkable, TypeVar

T_co = TypeVar('T_co', covariant=True)

@runtime_checkable
class RandomPicker(Protocol[T_co]):
    def pick(self) -> T_co: ...
