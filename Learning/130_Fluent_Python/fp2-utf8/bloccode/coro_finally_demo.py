# Example 31-12. coro_finally_demo.py: use of try/finally to perform actions on coroutine termination

class DemoException(Exception):
    """An exception type for the demonstration."""


def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...')
            else:
                print(f'-> coroutine received: {x!r}')
    finally:
        print('-> coroutine ending')
