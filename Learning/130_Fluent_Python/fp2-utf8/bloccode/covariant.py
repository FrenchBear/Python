# Example 15-19. covariant.py: type definitions and install function

T_co = TypeVar('T_co', covariant=True)

class BeverageDispenser(Generic[T_co]):
    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage

def install(dispenser: BeverageDispenser[Juice]) -> None:
    """Install a fruit juice dispenser."""
