# Fraction Development 2
# 2021-11-03    PV      Second version using O(1) memory (sint does not really count) but O(d²) time
# 2021-11-05    PV      Sign; /0; tests

def develop(n: int, d: int) -> str:
    if d==0:
        return '/0 error' if n!=0 else '0/0 undefined'
    sint = ''
    if n<0 or d < 0:
        if n*d<0:
            sint = "-"
        n = abs(n)
        d = abs(d)
    sint += str(n//d)
    n %= d
    if n == 0:
        return sint
    sint += '.'

    n0 = n
    k = 0
    for i in range(d):
        if n == 0:    # division ends
            k = 1
            break

        m = n0%d
        for j in range(i):
            if n == m:
                # Found a repeating remainder, it's periodic
                k = 2
                break
            m *= 10
            decl = m//d
            m %= d

        if k > 0:
            break

        n *= 10
        dec = n//d
        n %= d

    n = n0 % d
    for i in range(d):
        if k == 2 and i==j:
            sint += "["
        n *= 10
        dec = n//d
        n %= d
        sint += str(dec)
        if n == m and i>=j:
            return sint+']'
        if n == 0:
            return sint


# print(develop(1,9801))
# Decimals .[00 01 02 03 ... 96 97 99]
# 0.[000102030405060708091011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889909192939495969799]

print(develop(1,3))


def test(n: int, d: int, r: str):
    x = develop(n, d)
    if x == r:
        print('Ok: ', n, '/', d, ' = ', r, sep='')
    else:
        print('KO: ', n, '/', d, ' found ', x, ' expected ', r, sep='')

test(100, 250, "0.4")
test(100, 4, "25")
test(8, 2, "4")
test(1, 3, "0.[3]")
test(-1, 3, "-0.[3]")
test(1, -3, "-0.[3]")
test(-1, -3, "0.[3]")
test(1, 5, "0.2")
test(1, 7, "0.[142857]")
test(100, 23, "4.[3478260869565217391304]")
test(679, 550, "1.23[45]")
test(0, 5, "0")
test(5, 0, "/0 error")
test(0, 0, "0/0 undefined")
