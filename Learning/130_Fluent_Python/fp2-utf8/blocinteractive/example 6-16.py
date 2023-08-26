# Example 6-16. Watching the end of an object when no more references point to it

>>> import weakref
>>> s1 = {1, 2, 3}
>>> s2 = s1
>>> def bye():
...     print('...like tears in the rain.')
...
>>> ender = weakref.finalize(s1, bye)
>>> ender.alive
True
>>> del s1
>>> ender.alive
True
>>> s2 = 'spam'
...like tears in the rain.
>>> ender.alive
False
