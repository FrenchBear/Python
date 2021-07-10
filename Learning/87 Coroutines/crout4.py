# cout4.py
# Play with coroutines
# 2021-07-10    PV

from functools import wraps

def coroutine(func: callable):
    """Decorator: primes 'func' by advancing to first yield"""
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

# averager using a coroutine
@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count


coro_avg = averager()
# No need for priming

print(coro_avg.send(10))
print(coro_avg.send(30))
print(coro_avg.send(5))
