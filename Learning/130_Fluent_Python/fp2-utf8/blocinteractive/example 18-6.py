# Example 18-6. Test-driving the looking_glass context manager function

>>> from mirror_gen import looking_glass
>>> with looking_glass() as what:
...     print('Alice, Kitty and Snowdrop')
...     print(what)
...
pordwonS dna yttiK ,ecilA
YKCOWREBBAJ
>>> what
'JABBERWOCKY'
>>> print('back to normal')
back to normal
