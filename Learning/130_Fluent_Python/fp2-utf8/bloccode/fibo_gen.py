# Example 17-35. fibo_gen.py: fibonacci returns a generator of integers

from collections.abc import Iterator

def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
