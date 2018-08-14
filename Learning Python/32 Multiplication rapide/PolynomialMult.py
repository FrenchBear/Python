# Multiplication of large numbers using polynomials
# This method has a cost in n.ln(n).ln(ln(n)) multiplying large numbers, while traditional multiplication has a n² cost,
# and Karatsuba algorithm is in n^1.58
# Ideas:
# - number can be converted into a polynomial and back: 315 <-> 3x²+x5, with carry handling when converting polynomial -> number
# - a polynomial of degree n is uniquely defined by its value in (n+1) points. Lagrange interpolation converts (n+1) couples (x,y) into a polynomial
# - multiplication of polynomials can be done by multiplying values in several points: [PQ](x) = P(x).Q(x)
# - evaluation of a polynomial on (n+1) roots of unity can be done in n.ln(n) (Horner method is in n, and doing it on 2n values has a complexity of n²)
#
# 2018-08-13    PV

import numpy as np
from numpy.linalg import inv
import math


# Normalization function to convert back a polynomial into a number, propagating carry
def polytonum(p):
    n = ""
    r = 0
    for i in reversed(p.c):
        assert abs(i.imag)<1e-6                     # Safeguard, in this code, complex part of p coefficients must be almost nul
        assert abs(i.real - int(i.real+1e-6))<1e-6  # and real part must be integers
        r, d = divmod(int(i.real+1e-6)+r, 10)
        n = str(d) + n
    if r > 0:
        n = str(r) + n
    return int(n)

# Helper number -> polynomial


def numtopoly(n):
    return np.poly1d([int(c) for c in str(n)])

# Compute roots of unity.  Returns 1 as the last root.


def nthRootsOfUnity1(n):  # linear space, parallelizable
    return np.exp(2j * np.pi / n * np.arange(1, n+1))

# Helper, compare lists of complexes, sometimes difficult to read and compare on screen


def cmplc(l1, l2):
    if len(l1) != len(l2):
        return False, "Different length"
    for i in range(len(l1)):
        if abs(l1[i]-l2[i]) > 1e-6:
            return False, "Different values at index "+str(i)
    return True, ""

# Personal implementation of Lagrange interpolation since scipy.interpolate.lgrange is unstable according to documentation
# and can't be user on more than 20 values. Indeed doesn't give correct results when mult result is over 32th root of unit.
# Use vandermonde matrix to interpolate, we have Y = M x P where M is vandermonde(X) and P a vector form of the polynomial
# so P = inv(M) x Y, returned as a poly1d
# Implemented this way it has a high cost of inverting a matrix


def lagrangeVDM(x, y):
    mint = inv(np.vander(x))
    return np.poly1d(mint.dot(y))

# Efficient polynomial evaluation at the nth values of (n+1) roots of the unit using FFT type recursion, when (n+1) is a power of 2
# In actual fast multiplication, a recurse algorithm should probably not be used
# x1 contains all the roots ending by 1 to simplify code, but polynomial is not evaluated for this value


def epex(p, x1):
    # If polynomial is small, direct evaluation
    if len(p.c) <= 3:
        #print("$1: ", p.c)
        return p(x1[:-1])

    # Recursive evaluation, posing p(x) = x*r(x²)+q(x²)
    # q = polynomial(coefficients of even powers of p), contains constant coefficient (power 0)
    # r = polynomial(coefficients of odd powers of p)
    # x² = x[0, 2, 4...] modulo n since elements of x are unity roots
    if len(p.c) % 2 == 1:
        q = np.poly1d(p.c[::2])
        r = np.poly1d(p.c[1::2])
    else:
        q = np.poly1d(p.c[1::2])
        r = np.poly1d(p.c[::2])
    x2 = np.append(x1[1::2], x1[1::2])
    return x1[:-1]*epex(r, x2) + epex(q, x2)

# Final application, multiply two large numbers


def multPolynomial(a, b):
    pa = numtopoly(a)
    pb = numtopoly(b)
    l = math.ceil(math.log(len(pa.c)+len(pb.c))/math.log(2))
    n = 2**l-1
    x = nthRootsOfUnity1(n+1)

    ea = epex(pa, x)
    eb = epex(pb, x)
    y = ea*eb
    pm = lagrangeVDM(x[:-1], y)
    m = polytonum(pm)
    return m


"""
# This test fails with scipy.interpolate.lgrange
a = 12345678901234567
b = 98765432109876543
m1 = multPolynomial(a,b)
m2 = a*b
print(m1)
print(m2)
print(m1==m2)
"""

# Many tests, up to 50x50 digits
def testMultPolynomial():
    sa = "1234567890"*5
    sb = "9876543210"*5

    for i in range(len(sa)):
        a = int(sa[:i+1])
        b = int(sb[:i+1])
        m = multPolynomial(a, b)
        print(i+1, a, b, a*b == m)

testMultPolynomial()