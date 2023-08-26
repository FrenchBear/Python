# Example 21-17. More experiments, continuing from Example 21-16

>>> probe('python.org')
<coroutine object probe at 0x10e313740>
>>> multi_probe(names)
<async_generator object multi_probe at 0x10e246b80>
>>> for r in multi_probe(names):
...     print(r)
...
Traceback (most recent call last):
  ...
TypeError: 'async_generator' object is not iterable
