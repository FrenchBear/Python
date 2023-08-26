# Example 3-7. When searching for a non-string key, StrKeyDict0 converts it to str when it is not found

Tests for item retrieval using `d[key]` notation::
    >>> d = StrKeyDict0([('2', 'two'), ('4', 'four')])
    >>> d['2']
    'two'
    >>> d[4]
    'four'
    >>> d[1]
    Traceback (most recent call last):
      ...
    KeyError: '1'

Tests for item retrieval using `d.get(key)` notation::
    >>> d.get('2')
    'two'
    >>> d.get(4)
    'four'
    >>> d.get(1, 'N/A')
    'N/A'

Tests for the `in` operator::
    >>> 2 in d
    True
    >>> 1 in d
    False
