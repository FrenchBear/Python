# Example 16-16. Using += and *= with Vector instances

>>> v1 = Vector([1, 2, 3])
>>> v1_alias = v1
>>> id(v1)
4302860128
>>> v1 += Vector([4, 5, 6])
>>> v1
Vector([5.0, 7.0, 9.0])
>>> id(v1)
4302859904
>>> v1_alias
Vector([1.0, 2.0, 3.0])
>>> v1 *= 11
>>> v1
Vector([55.0, 77.0, 99.0])
>>> id(v1)
4302858336
