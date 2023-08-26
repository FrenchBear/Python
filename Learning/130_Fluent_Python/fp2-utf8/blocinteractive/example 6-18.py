# Example 6-18. String literals may create shared objects

>>> t1 = (1, 2, 3)
>>> t3 = (1, 2, 3)
>>> t3 is t1
False
>>> s1 = 'ABC'
>>> s2 = 'ABC'
>>> s2 is s1
True
