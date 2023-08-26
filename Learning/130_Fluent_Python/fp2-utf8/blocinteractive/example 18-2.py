# Example 18-2. Test-driving the LookingGlass context manager class

>>> from mirror import LookingGlass
>>> with LookingGlass() as what:
...     print('Alice, Kitty and Snowdrop')
...     print(what)
...
pordwonS dna yttiK ,ecilA
YKCOWREBBAJ
>>> what
'JABBERWOCKY'
>>> print('Back to normal.')
Back to normal.
