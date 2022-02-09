# cout3.py
# Play with coroutines: three versions of an averager
# 2021-07-10    PV

from functools import total_ordering
from typing import Counter


# using a coroutine
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
next(coro_avg)          # priming

print(coro_avg.send(10))
print(coro_avg.send(30))
print(coro_avg.send(5))
print()


# using a class
class averager_class():
    def __init__(self) -> None:
        self.total = 0.0
        self.count = 0

    def add(self, a: float) -> float:
        self.total += a
        self.count += 1
        return self.total/self.count

class_avg = averager_class()
print(class_avg.add(10))
print(class_avg.add(30))
print(class_avg.add(5))
print()


# using a capture
def averager_capture():
    total = 0.0
    count = 0

    def add(a: float) -> float:
        nonlocal total, count
        total += a
        count += 1
        return total/count

    return add    

capture_avg = averager_capture()
print(capture_avg(10))
print(capture_avg(30))
print(capture_avg(5))
print()
