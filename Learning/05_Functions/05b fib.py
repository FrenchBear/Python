# Functions.py
# Simple example of functions, Fibonacci suite
#
# 2015-05-02    PV


import sys


def fib(n):
    if n >= 0:
        fn2 = 0
        print(fn2, end=',')
    if n >= 1:
        fn1 = 1
        print(fn1, end=',')
    for _ in range(2, n+1):
        fn = fn1 + fn2
        print(fn, end=',')
        fn2 = fn1
        fn1 = fn
    print()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 10
    print(fib(n))
