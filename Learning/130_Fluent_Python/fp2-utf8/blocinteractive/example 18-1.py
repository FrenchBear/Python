# Example 18-1. Demonstration of a file object as a context manager

>>> with open('mirror.py') as fp:
...     src = fp.read(60)
...
>>> len(src)
60
>>> fp
<_io.TextIOWrapper name='mirror.py' mode='r' encoding='UTF-8'>
>>> fp.closed, fp.encoding
(True, 'UTF-8')
>>> fp.read(60)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file.
