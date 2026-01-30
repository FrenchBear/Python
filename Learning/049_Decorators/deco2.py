# deco.py
# Exercices on decorators
# Check @wraps work
#
# 2021-07-11    PV

import time
from functools import wraps
import inspect
from collections.abc import Callable

def measure_time(func: Callable) -> Callable:
    """Display function execution time at the end"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        starttime = time.perf_counter()
        func(*args, **kwargs)
        endtime = time.perf_counter()
        print(f"Elapled: {endtime-starttime} s")

    return wrapper


@measure_time
def wastetime(n: int):
    """A simple test function"""
    sum(i**2 for i in range(n))


wastetime(100_000)

# Check that @wraps restore initial function name, doc and arguments despite @measure_time wrapper
print(wastetime.__name__)
print(wastetime.__doc__)
print(inspect.signature(wastetime).parameters)
