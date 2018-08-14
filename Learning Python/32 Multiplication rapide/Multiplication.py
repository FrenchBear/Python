# Mulitplication.py
# Compare various multiplication algorithms
#
# Ideas: 
# https://www.codeandgadgets.com/karatsuba-multiplication-python/
# Le fascinant nombre Pi, 2è ed, JP Delahaye
#
# 2018-02-12    PV  my own implementation
# 2018-07-30    PV  Optimize multKaratsuba when a part is 0 because of filling
# 2018-08-14    PV  Added Polynomial multiplication algorithm and split source code

import random
import string
from timeit import default_timer as timer

from KaratsubaMult import multKaratsuba
from PolynomialMult import multPolynomial


def chronoMult(f, a, b):
    start = timer()
    res = f(a, b)
    end = timer()
    return (end-start, res)


def getRandomLongNum(length=10):
    return int(''.join(random.choices(string.digits, k=length)))


def multPython(a, b):
    return a * b


def multSchool(a, b):
    t = 0
    stra = str(a)
    for d in reversed(str(b)):
        t += int(stra) * int(d)
        stra += '0'
    return t


# Dev tests
a = 6463254768323
b = 5426288911234

print(a, ' * ', b)

c1 = multPython(a, b)
print('Python:    ', c1)

c2 = multSchool(a, b)
print('School:    ', c2)

c3 = multKaratsuba(a, b)
print('Karatsuba: ', c3)

c4 = multPolynomial(a, b)
print('Polynomial:', c4)


def testMult(n):
    a = getRandomLongNum(n)
    b = getRandomLongNum(n)

    print("Test n=", n)
    d1, m1 = chronoMult(multPython, a, b)
    print('Python:     %8f' % d1)
    d2, m2 = chronoMult(multSchool, a, b)
    print('School:     %8f' % d2)
    d3, m3 = chronoMult(multKaratsuba, a, b)
    print('Karatsuba:  %8f' % d3)
    d4, m4 = chronoMult(multPolynomial, a, b)
    print('Polynomial: %8f' % d4)

    print("ok" if m1 == m2 and m1 == m3 and m1 == m4 else "Problem")
    print()


testMult(1000)
