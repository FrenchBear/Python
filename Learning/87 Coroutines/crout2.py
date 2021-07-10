# cout2.py
# Play with coroutines
# 2021-07-10    PV

from inspect import getgeneratorstate, trace

def simple_coro2(a):
    print('coro2: Started, a=', a)
    b = yield a
    print('coro2: Received, b=', b)
    c = yield a+b
    print('coro2: Received, c=', c)


my_coro2 = simple_coro2(14)             # Get generator object
print(getgeneratorstate(my_coro2))
print('Coroutine called')
print('->', next(my_coro2))             # priming
print(getgeneratorstate(my_coro2))
print('Coroutine primed')
print('->', my_coro2.send(28))
print(getgeneratorstate(my_coro2))

try:
    print('->', my_coro2.send(99))      # raises StopIteration
except:
    pass
print(getgeneratorstate(my_coro2))
