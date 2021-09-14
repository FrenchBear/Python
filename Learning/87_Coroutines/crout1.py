# cout1.py
# Play with coroutines
# 2021-07-10    PV

def simple_coroutine():
    print('Coroutine started')
    x = yield
    print('Coroutine received:', x)

my_coro = simple_coroutine()    # Get generator object
print('Coroutine called')
next(my_coro)                   # priming
print('Coroutine primed')
my_coro.send(42)                # raises StopIteration, that's normal
