# Mulitplication.py
# Compare various multiplication algorithms
#
# Idea: https://www.codeandgadgets.com/karatsuba-multiplication-python/
# 
# 2018-02-12    PV  my own implementation
# 2018-07-30    PV  Optimize multKaratsuba when a part is 0 because of filling

import random
import string
from timeit import default_timer as timer

def chronoMult(f, a, b):
    start = timer()
    res = f(a,b)
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

def nextPowerOf2(n):
    p = 1
    while True:
        if p >= n: return p
        p *= 2

def multKaratsuba(x, y):
    if x==0 or y==0: return 0

    # If 4 digits, use standard multiplication that fits on 32-bit hardware
    if x < 10000 and y < 10000: return x * y

    # Otherwise use recursively Karatsuba algorithm
    strx = str(x)
    stry = str(y)
    lx = len(strx)
    ly = len(stry)
    
    # Align lengths of arguments to the next power of 2, left-padding with zeros
    l = nextPowerOf2(max(lx, ly))
    strx = '0'*(l-lx) + strx
    stry = '0'*(l-ly) + stry

    # Split numbers in two, x -> a*10^l2 + b, y -> c*10^l2 + d
    l2 = l >> 1
    a = int(strx[:l2])
    b = int(strx[l2:])
    c = int(stry[:l2])
    d = int(stry[l2:])

    # Compute ac, bd and m = ab + bc
    ac = 0 if a==0 or c==0 else multKaratsuba(a, c)
    bd = 0 if b==0 or d==0 else multKaratsuba(b, d)
    m = multKaratsuba(a + b, c + d) - ac - bd           # Trick to compute middle element with two multiplications
    r = int(str(ac) + '0' * l) + int(str(m) + '0' * l2) + int(bd)
    return r


# dev test
"""
a = 6463254768323
b = 5426288911234

print(a, ' * ', b)

c1 = multPython(a,b)
print('Python:    ', c1)

c2 = multSchool(a,b)
print('School:    ', c2)

c3 = multKaratsuba(a,b)
print('Karatsuba: ', c3)
"""



def testMult(n):
    a = getRandomLongNum(n)
    b = getRandomLongNum(n)

    print("Test n=", n)
    d1, m1 = chronoMult(multPython, a, b) 
    print('Python:    %8f' % d1)
    d2, m2 = chronoMult(multSchool, a, b) 
    print('School:    %8f' % d2)
    d3, m3 = chronoMult(multKaratsuba, a, b) 
    print('Karatsuba: %8f' % d3)

    print("ok" if m1==m2 and m1==m3 else "Problem")
    print()


testMult(1000)
