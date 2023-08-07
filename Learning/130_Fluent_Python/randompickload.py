# Example 13-20

from typing import Protocol, runtime_checkable
from randompick import RandomPicker

@runtime_checkable      # If you want the derived protocol to be runtime checkable, you must apply the decorator again — its behavior is not inherited.
class LoadableRandomPicker(RandomPicker, Protocol):     # Every protocol must explicitly name typing.Protocol as one of its base classes in addition to the protocol we are extending. This is different from the way inheritance works in Python.
    def load(self, Iterable) -> None: ...   # we only need to declare the method that is new in this derived protocol. The pick method declaration is inherited from RandomPicker.
