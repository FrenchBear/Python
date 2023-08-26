# Example 2-22. Basic operations with rows and columns in a numpy.ndarray

>>> import numpy as np
>>> a = np.arange(12)
>>> a
array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])
>>> type(a)
<class 'numpy.ndarray'>
>>> a.shape
(12,)
>>> a.shape = 3, 4
>>> a
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
>>> a[2]
array([ 8,  9, 10, 11])
>>> a[2, 1]
9
>>> a[:, 1]
array([1, 5, 9])
>>> a.transpose()
array([[ 0,  4,  8],
       [ 1,  5,  9],
       [ 2,  6, 10],
       [ 3,  7, 11]])
