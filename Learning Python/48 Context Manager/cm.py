# Context Manager Examples
# 2018-09-02    PV

import time, math, random
from contextlib import contextmanager


class Indenter():
    def __init__(self, *args, **kwargs):
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print(self, *s):
        print('  '*(self.level-1), end='')
        print(*s)

def test_indenter():
    with Indenter() as indent:
        indent.print('hi!')
        with indent:
            indent.print('hello')
            with indent:
                indent.print('bonjour')
        indent.print('hey')


class ExecTimer1():
    def __init__(self):
        self.tstart = 0
    
    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, exct, excv, exctb):
        t = time.time()-self.tstart
        print(f"Duration: {t:.2f}")

def test_timer1():
    with ExecTimer1():
        l = list(range(100))
        for _ in range(1000):
            random.shuffle(l)
            list.sort(l)


@contextmanager
def ExecTimer2():
    try:
        tstart = time.time()
        yield None
    finally:
        t = time.time()-tstart
        print(f"Duration: {t:.2f}")

def test_timer2():
    with ExecTimer2():
        l = list(range(100))
        for _ in range(1000):
            random.shuffle(l)
            list.sort(l)


test_timer1()
test_timer2()
