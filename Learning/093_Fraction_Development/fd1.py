# Fraction Development 1
# 2021-10-23    PV      First version with dictionary and string, O(d) memory and O(d) time
# 2021-11-05    PV      Fixed bug 679/550 1.23[45]; Sign; /0; tests

import time


def develop(n: int, d: int) -> str:
    if d == 0:
        return '/0 error' if n != 0 else '0/0 undefined'
    dic: dict[int, int] = {}
    sint = ''
    if n < 0 or d < 0:
        if n*d < 0:
            sint = "-"
        n = abs(n)
        d = abs(d)
    sint += str(n//d)
    n %= d
    if n == 0:
        return sint
    sint += '.'
    sfrac = ''
    for i in range(d):
        if n == 0:    # division ends
            return sint+sfrac

        if n in dic:    # found period
            return sint+sfrac[:dic[n]]+'['+sfrac[dic[n]:]+']'

        # record position for reminder and decimal, and continue to next decimal
        dic[n] = i

        n *= 10
        dec = n//d
        n %= d

        sfrac += str(dec)

    return ''

# print(develop(1,9801))
# Decimals .[00 01 02 03 ... 96 97 99]
# 0.[000102030405060708091011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889909192939495969799]


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

t: float = time.perf_counter_ns()
for i in range(100000):
    _ = develop(100, 23)
t = (time.perf_counter_ns()-t)/1_000_000_000
print(f'\nElapsed #1: {int(t)}.{int(1000*t)%1000:0>3} s')
