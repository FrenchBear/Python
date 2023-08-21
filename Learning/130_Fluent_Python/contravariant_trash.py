# Example 15-20

from typing import TypeVar, Generic

class Refuse:
    """Any refuse."""

class Biodegradable(Refuse):
    """Biodegradable refuse."""

class Compostable(Biodegradable):
    """Compostable refuse."""

T_contra = TypeVar('T_contra', contravariant=True)

class TrashCan(Generic[T_contra]):
    def put(self, refuse: T_contra) -> None:
        """Store trash until dumped."""

def Deploy(trash_can: TrashCan[Biodegradable]):
    """Deploy a trash can for biodegradable refuse."""

# Refuse :> Biodegradable :> Compostable
# Contravariance: TrashCan(Refuse) <: TrashCan(Biodegradable) <: TrashCan(Compostable)


bio_can: TrashCan[Biodegradable] = TrashCan()
Deploy(bio_can)

# The more general TrashCan[Refuse] is acceptable because it can take any kind of refuse, including Biodegradable.
#           Refuse :> Biodegradable
# TrashCan[Refuse] <: TrashCan[Biodegradable]
trash_can: TrashCan[Refuse] = TrashCan()
Deploy(trash_can)

# A TrashCan[Compostable] will not do, because it cannot take Biodegradable
compost_can: TrashCan[Compostable] = TrashCan()
# Deploy(compost_can)
