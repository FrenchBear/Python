# sendgen.py: Send values to generator
# Learning python
# writer: Empiric code after reading a mention of "yield from" and doing a google search
# https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3
# simple_coro: after reading pylint comments on error E1111
#
# But pylint (at least version 2.1.1) doesn't like to call a function that does not contain a return statement...
#
# 2018-09-28    PV

# pylint: disable=assignment-from-no-return


def writer():
    print("writer starts")
    """A generator that writes data *sent* to it to fd, socket, etc."""
    while True:
        try:
            w = (yield)
            print('>> ', w)
        except StopIteration:
            break
    print("writer ends")


#def test_writer():
print("$1")
w = writer()
print("$2")
w.send(None)  # start the generator
print("$3")
for i in range(4):
    w.send(i)
print("$4")
w.throw(StopIteration)
print("$4")


#test_writer()

# import asyncio


# async def simple_coro():
#     await asyncio.sleep(0.1)
#     print("awake!")

# loop = asyncio.get_event_loop()
# coro1 = simple_coro()
# coro2 = simple_coro()
# loop.run_until_complete(asyncio.gather(coro1, coro2))
# loop.close()
