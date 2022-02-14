# perf.py
# Compare performance of multiplication algorithms
#
# 2022-02-14    PV

import random

from mult_classic import mult_classic
from mult_karatsuba import mult_karatsuba
from mult_fft import mult_fft

def mult_python(n1: str, n2:str) -> str:
    return str(int(n1)*int(n2))


def get_random_number(l: int) -> str:
    return ''.join(str(random.randint(0,9)) for _ in range(l))


for l in range(5,1000,25):
    n1 = get_random_number(l)
    n2 = get_random_number(l)

    rc = mult_classic(n1, n2)
    rk = mult_karatsuba(n1, n2)
    rf = mult_fft(n1, n2)
    rp = mult_python(n1, n2)

    print()
    print(f'{l=}')
    print(f'{n1=}')
    print(f'{n2=}')
    print(f'{rc=}')
    print(f'{rk=}')
    print(f'{rf=}')
    print(f'{rp=}')
    assert(rc==rk==rf==rp)
