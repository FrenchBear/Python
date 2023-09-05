# contextmanager.py
# Simple example of contextlib.contextmanager (similar to fluent python 2 example 18-5)
# https://docs.python.org/3/library/contextlib.html
#
# 2023-09-01    PV

from contextlib import contextmanager
import math
from time import perf_counter

@contextmanager
def time_it():
    resource = perf_counter()
    try:
        yield resource  # Actually not really useful...  Just yield something.
    except Exception as ex:
        print('Exception during time_it:', str(ex))
    finally:
        # Nothing to release in this example
        elapsed = perf_counter() - resource
        print(f"Duration: {elapsed:.3f}s")

with time_it():
    for i in range(1_000_000):
        r = math.sqrt(i)
    #d = 1/0

