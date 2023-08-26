# Example 16-17. The + operator creates a new AddableBingoCage instance

>>> vowels = 'AEIOU'
>>> globe = AddableBingoCage(vowels)
>>> globe.inspect()
('A', 'E', 'I', 'O', 'U')
>>> globe.pick() in vowels
True
>>> len(globe.inspect())
4
>>> globe2 = AddableBingoCage('XYZ')
>>> globe3 = globe + globe2
>>> len(globe3.inspect())
7
>>> void = globe + [10, 20]
Traceback (most recent call last):
  ...
TypeError: unsupported operand type(s) for +: 'AddableBingoCage' and 'list'
