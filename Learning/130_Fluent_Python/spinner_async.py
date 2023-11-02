# Spinner with coroutines

import asyncio
import itertools
import math
#from isprime import is_prime

# async version of is_prime...  But calling regularly asyncio.sleep(0) slows down this function (it takes twice the time to run compared to the version without await call)
async def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
        if i % 100_000 == 1:
            await asyncio.sleep(0)
    return True

async def spin(msg: str) -> None:
    print('spin: start')
    for char in itertools.cycle(r'⡀⣀⣄⣤⣦⣶⣷⣿'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    print('slow: start')
    #await asyncio.sleep(3)      # And not time.sleep(.1) to avoid blocking other coroutines 
    ans = await is_prime(5_000_111_000_222_021)       # Need an async version of is_prime calling await regularly
    print('slow: after sleep')
    return ans

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))
    print(f'spinner object: {spinner}')
    result = await slow()
    spinner.cancel()
    return result

def main() -> None:
    result = asyncio.run(supervisor())
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()
