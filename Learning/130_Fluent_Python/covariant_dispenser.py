# Example 15-9

from typing import TypeVar, Generic

class Beverage:
    """Any beverage."""

class Juice(Beverage):
    """Any fruit juice."""

class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""

T_co = TypeVar('T_co', covariant=True)

class BeverageDispenser(Generic[T_co]):
    """A dispenser parameterized on the beverage type."""

    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage

def install(dispenser: BeverageDispenser[Juice]) -> None:
    """Install a fruit juice dispenser."""

# :> means 'is a super-type of'
# Beverage :> Juice :> OrangeJuice
# Covariance: BeverageDispenser(Beverage) :> BeverageDispenser(Juice) :> BeverageDispenser(OrangeJuice)

juice_dispenser = BeverageDispenser(Juice())
install(juice_dispenser)

# Now it works, contrary to non_covariant_dispenser.py
# That’s covariance: the subtype relationship of the parameterized dispensers varies in the same direction
# as the subtype relationship of the type parameters.
orange_juice_dispenser = BeverageDispenser(OrangeJuice())
install(orange_juice_dispenser)

# A dispenser for an arbitrary Beverage is not acceptable
beverage_dispenser = BeverageDispenser(Beverage())
# install(beverage_dispenser)
