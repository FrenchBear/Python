# Queues
# Learning Python
#
# 2018-09-11    PV


# Stacks
print("Stack using a list")
sl = []
sl.append("apple")
sl.append("pear")
sl.append("ananas")
sl.append("kiwi")
try:
    while True:
        print(sl.pop())
except IndexError:
    print("---")

print("Stack using deque")
from collections import deque
s2 = deque()
s2.append("apple")
s2.append("pear")
s2.append("ananas")
s2.append("kiwi")
try:
    while True:
        print(s2.pop())
except IndexError:
    print("---")

print("Stack using queue.LifoQueue")
# Support multiple concurrent producers and consumers
# get() on an empty LifoQueue waits forever, while get_nowait() raises an exception
from queue import LifoQueue
s3 = LifoQueue()
s3.put("apple")
s3.put("pear")
s3.put("ananas")
s3.put("kiwi")
try:
    while True:
        print(s3.get_nowait())
except Exception as ex:
    print("---")


print("Queue using deque")
from collections import deque
q1 = deque()
q1.append("apple")
q1.append("pear")
q1.append("ananas")
q1.append("kiwi")
try:
    while True:
        print(q1.popleft())
except IndexError:
    print("---")


print("Queue using queue.Queue")
# Support multiple concurrent producers and consumers
# get() on an empty Queue waits forever, while get_nowait() raises an exception
from queue import Queue
q2 = Queue()
q2.put("apple")
q2.put("pear")
q2.put("ananas")
q2.put("kiwi")
try:
    while True:
        print(q2.get_nowait())
except Exception as ex:
    print("---")

# Also multiprocessing.Queue
