# Example 23-15. Experiments with a method

>>> word = Text('forward')
>>> word
Text('forward')
>>> word.reverse()
Text('drawrof')
>>> Text.reverse(Text('backward'))
Text('drawkcab')
>>> type(Text.reverse), type(word.reverse)
(<class 'function'>, <class 'method'>)
>>> list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')]))
['diaper', (30, 20, 10), Text('desserts')]
>>> Text.reverse.__get__(word)
<bound method Text.reverse of Text('forward')>
>>> Text.reverse.__get__(None, Text)
<function Text.reverse at 0x101244e18>
>>> word.reverse
<bound method Text.reverse of Text('forward')>
>>> word.reverse.__self__
Text('forward')
>>> word.reverse.__func__ is Text.reverse
True
