# Example 18-8. The looking_glass context manager also works as a decorator

>>> @looking_glass()
... def verse():
...     print('The time has come')
...
>>> verse()
emoc sah emit ehT
>>> print('back to normal')
back to normal
