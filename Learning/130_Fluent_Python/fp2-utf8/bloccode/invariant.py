# Example 15-18. invariant.py: type definitions and install function

from typing import TypeVar, Generic

class Beverage:
    """Any beverage."""

class Juice(Beverage):
    """Any fruit juice."""

class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""

T = TypeVar('T')

class BeverageDispenser(Generic[T]):
    """A dispenser parameterized on the beverage type."""

    def __init__(self, beverage: T) -> None:
        self.beverage = beverage

    def dispense(self) -> T:
        return self.beverage

def install(dispenser: BeverageDispenser[Juice]) -> None:
    """Install a fruit juice dispenser."""
