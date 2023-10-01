# Spinner with coroutines

import asyncio
import itertools

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
    await asyncio.sleep(3)      # And not time.sleep(.1) to avoid blocking other coroutines 
    print('slow: after sleep')
    return 42

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
