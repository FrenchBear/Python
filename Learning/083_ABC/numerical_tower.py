# Numerical Tower
# Test of numerical ABCs
# 2021-04-26    PV

import builtins
import numbers
import fractions
import decimal
import datetime

from typing import Type


lb: list[type] = [builtins.object, numbers.Number, numbers.Complex, numbers.Real, numbers.Rational, numbers.Integral, bool]

def test(x) -> None:
    print(f"{str(x):<10.10} {type(x).__name__:<10} ", end='')
    for abc in lb:
        print("{:^10}".format('X' if isinstance(x, abc) else ' '), end='')
    print()


print('Value      Class     ', end='')
for abc in lb:
    print(f"{abc.__name__:^10}", end='')
print()

test(False)
test(123)
fr = fractions.Fraction(2,3)
test(fr)
test(float(1.414))
test(2+3j)
d = decimal.Decimal(3.1416) # A decimal is a number, bt not a real!
test(d)
bs = bytes(1)               # Beware, bytes is actually a 'string of bytes', not a byte number
test(bs)
test('z')
n = datetime.datetime.now()
test(n)
