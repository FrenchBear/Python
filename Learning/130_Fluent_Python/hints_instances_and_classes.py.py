# hints_instances_and_classes.py
# From https://stackoverflow.com/questions/69334475/how-to-hint-at-number-types-i-e-subclasses-of-number-not-numbers-themselv/69383462#69383462
#
# 2023-08-07    PV

from collections import UserString
from decimal import Decimal
from fractions import Fraction
from numbers import Number
from typing import SupportsFloat, TypeVar



def accepts_int_instances(x: int) -> None:
    pass

class IntSubclass(int):
    pass

accepts_int_instances(42) # passes MyPy (an instance of `int`)
accepts_int_instances(IntSubclass(666)) # passes MyPy (an instance of a subclass of `int`)
accepts_int_instances(3.14) # fails MyPy (an instance of `float` — `float` is not a subclass of `int`)


def accepts_int_and_subclasses(x: type[int]) -> None:
    pass

accepts_int_and_subclasses(int) # passes MyPy 
accepts_int_and_subclasses(float) # fails Mypy (not a subclass of `int`)
accepts_int_and_subclasses(IntSubclass) # passes MyPy




# SupportsFloat protocol means that the class has a __float__ method
NT = TypeVar('NT', bound=SupportsFloat)

def foo(bar: NT) -> NT:
    return bar

foo(2)
foo(3.14)
foo(Fraction(355,113))
foo(Decimal(1.666666666667))
foo(UserString('1.414'))        # UserString has a __float__ method...

NT2 = SupportsFloat|complex|Number

def foo2(bar: NT2) -> NT2:
    return bar

class RomanNumber(Number):
    def __init__(self, n) -> None:
        self.value=n
    def __hash__(self) -> int:      # Abstract method of Number, must be implemented
        return hash(self.value)

foo2(2)
foo2(3.14)
foo2(Fraction(355,113))
foo2(Decimal(1.666666666667))
foo2(3+4j)
foo2(RomanNumber(1))
