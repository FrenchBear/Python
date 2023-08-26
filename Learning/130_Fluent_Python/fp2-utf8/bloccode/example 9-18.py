# Example 9-18. Faster implementation using caching

import functools
from clockdeco import clock

@functools.cache
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == '__main__':
    print(fibonacci(6))
