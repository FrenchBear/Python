# perf.py
# Compare performance of multiplication algorithms
#
# 2022-02-14    PV

import timeit
import random
import statistics

from mult_classic import mult_classic
from mult_karatsuba import mult_karatsuba
from mult_fft import mult_fft

def mult_python(n1: str, n2:str) -> str:
    return str(int(n1)*int(n2))


def get_random_number(l: int) -> str:
    return ''.join(str(random.randint(0,9)) for _ in range(l))


def test1():
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


def perf_classic(n1: str, n2: str, res:str) -> float:
    setupcode = 'from mult_classic import mult_classic\nn1=' + repr(n1) + '\nn2=' + repr(n2)
    testcode = 'rc = mult_classic(n1, n2)\nassert(rc==' + repr(res) + ')'
    t = timeit.repeat(stmt=testcode, setup=setupcode, repeat=3, number=10)
    return statistics.median(t)

def perf_karatsuba(n1: str, n2: str, res:str) -> float:
    setupcode = 'from mult_karatsuba import mult_karatsuba\nn1=' + repr(n1) + '\nn2=' + repr(n2)
    testcode = 'rc = mult_karatsuba(n1, n2)\nassert(rc==' + repr(res) + ')'
    t = timeit.repeat(stmt=testcode, setup=setupcode, repeat=3, number=10)
    return statistics.median(t)

def perf_fft(n1: str, n2: str, res:str) -> float:
    setupcode = 'from mult_fft import mult_fft\nn1=' + repr(n1) + '\nn2=' + repr(n2)
    testcode = 'rc = mult_fft(n1, n2)\nassert(rc==' + repr(res) + ')'
    t = timeit.repeat(stmt=testcode, setup=setupcode, repeat=3, number=10)
    return statistics.median(t)

def perf_python(n1: str, n2: str, res:str) -> float:
    setupcode = 'from mult_python import mult_python\nn1=' + repr(n1) + '\nn2=' + repr(n2)
    testcode = 'rc = mult_python(n1, n2)\nassert(rc==' + repr(res) + ')'
    t = timeit.repeat(stmt=testcode, setup=setupcode, repeat=1, number=1)
    return statistics.median(t)
    


l = 2000
n1 = get_random_number(l)
n2 = get_random_number(l)
res = str(int(n1)*int(n2))
print(f'{l=}')
print('Classic:   ', perf_classic(n1, n2, res))
print('Karatsuba: ', perf_karatsuba(n1, n2, res))
print('FFT:       ', perf_fft(n1, n2, res))
print('Python:    ', perf_fft(n1, n2, res))

'''
Test on Krema
l=2000
Classic:    7.25604760000715
Karatsuba:  3.078994800001965
FFT:        0.6981029000016861
Python:     0.6984193999960553
'''