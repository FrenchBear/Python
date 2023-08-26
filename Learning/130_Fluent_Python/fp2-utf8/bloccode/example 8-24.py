# Example 8-24. Illustrating variance.

from collections.abc import Callable

def update(
        probe: Callable[[], float],
        display: Callable[[float], None]
    ) -> None:
    temperature = probe()
    # imagine lots of control code here
    display(temperature)

def probe_ok() -> int:
    return 42

def display_wrong(temperature: int) -> None:
    print(hex(temperature))

update(probe_ok, display_wrong)  # type error

def display_ok(temperature: complex) -> None:
    print(temperature)

update(probe_ok, display_ok)  # OK
