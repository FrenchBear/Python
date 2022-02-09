# KaratsubaMult multiplication algorithm, splitting in two parts


def nextPowerOf2(n):
    p = 1
    while True:
        if p >= n:
            return p
        p *= 2


def multKaratsuba(x, y):
    if x == 0 or y == 0:
        return 0

    # If 4 digits, use standard multiplication that fits on 32-bit hardware
    if x < 10000 and y < 10000:
        return x * y

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
    ac = 0 if a == 0 or c == 0 else multKaratsuba(a, c)
    bd = 0 if b == 0 or d == 0 else multKaratsuba(b, d)
    # Trick to compute middle element with two multiplications
    m = multKaratsuba(a + b, c + d) - ac - bd
    r = int(str(ac) + '0' * l) + int(str(m) + '0' * l2) + int(bd)
    return r


def testKaratsuba():
    a = 6463254768323
    b = 5426288911234

    print(a*b == multKaratsuba(a, b))
