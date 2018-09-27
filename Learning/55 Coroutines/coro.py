# coroutines in Python
# Learning python
# Totally empiric code after reading a mention of "yield from" and doing a google search
# https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3
#
# 2018-09-28    PV


def writer():
    print("writer starts")
    """A coroutine that writes data *sent* to it to fd, socket, etc."""
    while True:
        try:
            w = (yield)
            print('>> ', w)
        except StopIteration:
            break
    print("writer ends")


print("$1")
w = writer()
print("$2")
w.send(None)  # "prime" the coroutine
print("$3")
for i in range(4):
    w.send(i)
print("$4")
w.throw(StopIteration)
print("$4")
