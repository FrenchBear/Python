# Spinner with processes

import itertools
import time
from multiprocessing import Process, Event
from multiprocessing import synchronize
from primes import is_prime

def spin(msg: str, done: synchronize.Event) -> None:
    #for char in itertools.cycle(r'\|/-'):
    for char in itertools.cycle(r'⡀⣀⣄⣤⣦⣶⣷⣿'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

def slow() -> int:
    #time.sleep(3)
    #return 42
    return is_prime(5_000_111_000_222_021)

def supervisor() -> int:
    done = Event()
    spinner = Process(target=spin, args=('thinking!', done))
    print(f'spinner object: {spinner}')
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

def main() -> None:
    result = supervisor()
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()
