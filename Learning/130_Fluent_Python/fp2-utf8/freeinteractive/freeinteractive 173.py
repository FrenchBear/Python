>>> s3 = Sentence('Life of Brian')
>>> it = iter(s3)
>>> it  # doctest: +ELLIPSIS
<iterator object at 0x...>
>>> next(it)
'Life'
>>> next(it)
'of'
>>> next(it)
'Brian'
>>> next(it)
Traceback (most recent call last):
  ...
StopIteration
>>> list(it)
[]
>>> list(iter(s3))
['Life', 'of', 'Brian']
