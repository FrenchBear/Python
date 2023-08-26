# Example 9-1. A decorator usually replaces a function with a different one

>>> def deco(func):
...     def inner():
...         print('running inner()')
...     return inner
...
>>> @deco
... def target():
...     print('running target()')
...
>>> target()
running inner()
>>> target
<function deco.<locals>.inner at 0x10063b598>
