# Fraction Development 2
# 2021-11-03    PV      Second version using O(1) memory (sint does not really count) but O(d²) time

def develop2(n: int, d: int) -> str:
    sint = str(n//d) + '.'
    n %= d

    n0 = n
    k = 0
    for i in range(d):
        n *= 10
        dec = n//d
        n %= d

        if n == 0:    # division ends
            k = 1
            break

        m = n0
        for j in range(i):
            m *= 10
            decl = m//d
            m %= d
            if n == m:
                # Found a repeating remainder, it's periodic
                k = 2
                break
        if k > 0:
            break

    n = n0
    if k == 2:
        sint += "["
    for i in range(d):
        n *= 10
        dec = n//d
        n %= d
        if n == m and i>0:
            return sint+']'
        sint += str(dec)
        if n == 0:
            return sint


# Decimals .[00 01 02 03 ... 96 97 99]
# 0.[000102030405060708091011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889909192939495969799]
print(develop2(100, 23))
