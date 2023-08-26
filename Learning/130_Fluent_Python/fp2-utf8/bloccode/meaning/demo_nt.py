# Example 5-11. meaning/demo_nt.py: a class built with typing.NamedTuple

import typing
class DemoNTClass(typing.NamedTuple):
    a: int
    b: float = 1.1
    c = 'spam'
