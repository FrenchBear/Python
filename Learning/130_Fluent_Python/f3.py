from typing import Iterator
class Test():
    def __init__(self, iterable):
        _ = len(iterable)
        self._balls = list(iterable)

def generator() -> Iterator[int]:
    i = 0
    while True:
        yield i
        i += 1


t = Test([1, 2, 3])
u = Test(generator())
