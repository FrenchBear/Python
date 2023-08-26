>>> s = 'ABC'
>>> it = iter(s)
>>> while True:
...     try:
...         print(next(it))
...     except StopIteration:
...         del it
...         break
A
B
C
