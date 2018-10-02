# deco.py
# Exercices on decorators
#
# 2018-09-03    PV
# 2018-09-07    PV      Variant with a class
# 2018-10-01    PV      Expanded with execution time and following code


import functools


def uppercase(func):
    # Preserve __name__ and __doc__ of original function in the decorated version
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        original_result = func(*args, **kwargs)
        modified_result = original_result.upper()
        return modified_result
    return wrapper


def strong(func):
    def wrapper():
        return '<strong>' + func() + '</strong>'
    return wrapper


def emphasis(func):
    def wrapper():
        return '<em>' + func() + '</em>'
    return wrapper


@strong
@emphasis
@uppercase
def greet():
    return 'Hello!'


print(greet())


@uppercase
def hello(name: str) -> str:
    """This is a polite function to say hello"""
    return 'Hello '+name+'!'


print(hello('Pierre'))
print("name:", hello.__name__)
print("doc:", hello.__doc__)


def trace(func):
    def wrapper(*args, **kwargs):
        print(f'TRACE: calling {func.__name__}() with {args}, {kwargs}')
        original_result = func(*args, **kwargs)
        print(f'TRACE: {func.__name__}() returned {original_result!r}')
        return original_result
    return wrapper


@trace
def say(name, line):
    return f'{name}: {line}'


print(say('Jane', 'Hello, World'))


# Variant, with a class
# While a function embedded in a function gets a closer with outer function parameters, there is
# no such thing here, and self.original is a "manual closure"

class SkipLines():
    def __init__(self, n):
        self.n = n
        self.original = None

    # Callable that handles registration
    def __call__(self, f):
        self.original = f
        return self.relay

    def relay(self, *args, **kwargs):
        for _ in range(self.n):
            print('-'*20)
        self.original(*args, **kwargs)
        for _ in range(self.n):
            print('-'*20)

@SkipLines(2)
def PrintHello(n):
    print("Hello,", n)

PrintHello("Pierre")


# ----------------------------------------------
# Decorator to output running time of a function
# Use @functools.wraps(func) to preserve __name__ and  __doc__ of decorated function

import time
import functools

print("\nMeasuring execution time")


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked


# Second version, parameterizable: decorator is a function returning a decorator!
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock2(fmt=DEFAULT_FMT):
    def decorate(func):
        @functools.wraps(func)
        def clocked(*posargs, **kwargs):
            t0 = time.perf_counter()
            result = func(*posargs, **kwargs)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            arg_lst = []
            if posargs:
                arg_lst.append(', '.join(repr(arg) for arg in posargs))
            if kwargs:
                pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
                arg_lst.append(', '.join(pairs))
            args = ', '.join(arg_lst)
            print(fmt.format(**locals()))       # locals() is a dictionary of local variables
            return result
        return clocked
    return decorate


@clock
def snooze(seconds):
    time.sleep(seconds)


@clock2()
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)


print('Calling {}(0.25)'.format(snooze.__name__))
snooze(0.25)

print('Calling factorial(6)')
f6 = factorial(n=6)


# ----------------------------------------------
# Use of @functools.lru_cache() to implement a cache of recent calls to avoid executing again
# Artificial but impressive example


print("\n@functools.lru_cache()")


@clock
def fibo1(n):
    if n < 2:
        return n
    return fibo1(n-2) + fibo1(n-1)


print('calling fibo1(6)')
print(fibo1(6))


@functools.lru_cache()
@clock
def fibo2(n):
    if n < 2:
        return n
    return fibo2(n-2) + fibo2(n-1)


print('calling fibo2(6)')
print(fibo2(6))


# ----------------------------------------------
# Use of singledispatch to provide 'overrides' on 1st parameter type

import math
import scipy.special


print("\n@functools.singledispatch")


@functools.singledispatch
def generalized_factorial(obj):
    raise ValueError()


@generalized_factorial.register(int)
def fact_i(n):
    # print('fact_i')
    return 1 if n < 2 else n*fact_i(n-1)


@generalized_factorial.register(float)
def fact_f(x):
    # print('fact_f')
    return math.gamma(x+1)


@generalized_factorial.register(complex)
def fact_c(x):
    return scipy.special.gamma(x+1)


print('3! =', generalized_factorial(3))
print('3.5! =', generalized_factorial(3.5))
print('4! =', generalized_factorial(4))
print('(4+0.01j)! =', generalized_factorial(4+0.01j))
