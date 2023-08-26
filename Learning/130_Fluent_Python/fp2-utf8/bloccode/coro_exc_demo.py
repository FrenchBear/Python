# Example 31-8. coro_exc_demo.py: test code for studying exception handling in a coroutine

class DemoException(Exception):
    """An exception type for the demonstration."""

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print(f'-> coroutine received: {x!r}')
    raise RuntimeError('This line should never run.')
