@runtime_checkable
class SupportsAbs(Protocol[T_co]):
    """An ABC with one abstract method __abs__ that is covariant in its return type."""

    __slots__ = ()

    @abstractmethod
    def __abs__(self) -> T_co:
        pass
