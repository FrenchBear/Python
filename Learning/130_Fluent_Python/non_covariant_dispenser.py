# Example 15-18

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


juice_dispenser = BeverageDispenser(Juice())
install(juice_dispenser)            # Accepted

beverage_dispenser = BeverageDispenser(Beverage())
install(beverage_dispenser)         # Not legal, that's normal

# By default, generic types are invariant
orange_juice_dispenser = BeverageDispenser(OrangeJuice())
install(orange_juice_dispenser)     # Not legal, despite the fact that OrangeJuice is a juice!
