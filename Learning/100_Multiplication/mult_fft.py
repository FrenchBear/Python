# mult_fft.py
# Multiplication using FFT
#
# To mult n1 and n2:
# N1, N2 = FFT(n1), FFT(n2)
# RES = N1xN2 using term-to-term multiplication
# res = FFT⁻¹(RES)
#
# 2022-02-14    PV

import math
from operator import le

#nab_max = 2048


def fft(f: list[complex], n: int, isign: int):
    pi = math.copysign(math.pi, isign)
    m = n
    while m > 1:
        mh = m//2
        phi = pi/mh
        for j in range(mh):
            p = phi * j
            cs = complex(math.cos(p), math.sin(p))

            t1 = j
            while t1 < j+n:
                u = f[t1]
                v = f[t1+mh]
                f[t1] = u+v
                f[t1+mh] = (u-v)*cs

                t1 += m
        m //= 2

    # Reordering
    j = 0
    for m in range(1, n-1):
        k = n >> 1
        while True:
            j ^= k
            if (j & k) != 0:
                break
            k >>= 1
        if j > m:
            f[m], f[j] = f[j], f[m]

    # Normalize backwards transform
    if isign < 0:
        for k in range(n):
            f[k] /= n


def mult_fft(n1: str, n2: str) -> str:
    # 1. Set-up multiplicands
    a = [0] * len(n1)
    b = [0] * len(n2)
    base = 10

    def getdigs(n: str, base: int, a: list[int]) -> int:
        l = len(n)
        for i in range(l):
            a[i] = int(n[i])
        return l

    na = getdigs(n1, base, a)
    nb = getdigs(n2, base, b)
    nc = na+nb

    # 2. Find nf = smallest power of 2 >= nc
    nf = 2     # Length of complex arrays fa and fb
    while nf < nc:
        nf += nf

    # print(f'{na=}')
    # print(f'{nb=}')
    # print(f'{nf=}')

    # 3. Copy a[] to complex array fa[], justify left, pad zeros to the right, also b[] to fb[]
    fa = [complex(0)] * nf
    for i in range(na):
        fa[i] = complex(a[i])
    fb = [complex(0)] * nf
    for i in range(nb):
        fb[i] = complex(b[i])

    # print(f'{fa=}')
    # print(f'{fb=}')

    # 4. Perform FFT on fa[] and fb[]
    fft(fa, nf, +1)
    fft(fb, nf, +1)
    # print(f'After FFT {fa=}')
    # print(f'After FFT {fb=}')

    # 5. Multiply elementwise: fa[k] = fa[k]*fb[k]
    for k in range(nf):
        fa[k] *= fb[k]
    # print(f'After memberwise mult {fa=}')

    # 6. Perform FFT⁻¹ including normalization
    fft(fa, nf, -1)
    # print(f'After FFT⁻¹ {fa=}')

    # 7. Copy fa[] to real array c
    c = [0]*nc
    for k in range(nc):
        c[k] = int(fa[k].real + 0.5)
    # print(f'Real product {c=}')

    # 8. Shift by one, the lease significant is c[nc-2]
    k = nc-2
    while k >= 0:
        c[k+1] = c[k]
        k -= 1
    c[0] = 0
    # print(f'After shift, {c=}')

    # 9. Carry
    k = nc-1
    while k >= 1:
        carry = c[k]//base
        c[k] -= carry*base
        c[k-1] += carry
        k -= 1

    # print(f'Final, {c=}')

    res = ''.join(str(d) for d in c)
    return res.lstrip('0')


if __name__ == '__main__':
    n1 = '1238746590095067166634254'
    n2 = '5678130678529731459014859'

    r1 = mult_fft(n1, n2)
    r2 = str(int(n1)*int(n2))
    print(r1)
    print(r2)
    print('Ok' if r1==r2 else 'FAIL!')
