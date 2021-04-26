# Numerical Tower
# Test of numarical ABCs
# 2021-04-26    PV

import builtins
import numbers
import fractions
import decimal
import datetime

lb = [builtins.object, numbers.Number, numbers.Complex, numbers.Real, numbers.Rational, numbers.Integral]

def test(x) -> None:
    print("{:<10.10} {:<10} ".format(str(x), type(x).__name__), end='')
    for abc in lb:
        print("{:^10}".format('X' if isinstance(x, abc) else ' '), end='')
    print()


print('Value      Class     ', end='')
for abc in lb:
    print("{:^10}".format(abc.__name__), end='')
print()

test(False)
test(123)
fr = fractions.Fraction(2,3)
test(fr)
test(float(1.414))
test(2+3j)
d = decimal.Decimal(3.1416)
test(d)
bs = bytes(1)
test(bs)
test('z')
n = datetime.datetime.now()
test(n)
