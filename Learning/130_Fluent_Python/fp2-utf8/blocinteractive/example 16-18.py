# Example 16-18. An existing AddableBingoCage can be loaded with += (continuing from Example 16-17)

>>> globe_orig = globe
>>> len(globe.inspect())
4
>>> globe += globe2
>>> len(globe.inspect())
7
>>> globe += ['M', 'N']
>>> len(globe.inspect())
9
>>> globe is globe_orig
True
>>> globe += 1
Traceback (most recent call last):
  ...
TypeError: right operand in += must be 'Tombola' or an iterable
