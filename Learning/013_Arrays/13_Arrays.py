# Arrays
# Learning Python
# 2015-05-03    PV

# Simple array
myList = []
for i in range(10):
    # mylist[i]=1           # IndexError: list assignment index out of range
    myList.append(1)

myList = [i*i for i in range(10)]  # Array of squares [0, ..., 81]

# Creates a list containing 5 lists initialized to 0 using a comprehension
Matrix = [[0 for x in range(5)] for x in range(5)]
Matrix[0][0] = 1
Matrix[4][0] = 5
print(Matrix[0][0])         # prints 1
print(Matrix[4][0])         # prints 5

# Retrieve a column as a list
j = 0
col = [row[j] for row in Matrix]

# Transpose a matrix
t = [[row[i] for row in Matrix]
     for i in range(len(Matrix))]

# shorter notation for initializing a list of lists:
m = [[0]*5 for i in range(5)]

# Unfortunately shortening this to something like 5*[5*[0]] doesn't really work because you end up with 5 copies of the same list, so when you modify one of them they all change, for example:
matrix = 5*[5*[0]]
print(matrix)
# [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]l
matrix[4][4] = 2
print(matrix)
# [[0, 0, 0, 0, 2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 2]]


# With numpy
import numpy as np

print(np.zeros((3, 3)))  # Array of doubles
print(np.matrix([[1, 2], [3, 4]]))
print(np.matrix('1 2; 3 4'))
print(np.arange(9).reshape((3, 3)))
print(np.array(range(9)).reshape((3, 3)))
print(np.ndarray((3, 3)))


# Real arrays, compare size with list
print()
import array, sys
tl = [2,3,5,7,11,13,17,19,23,27]
ta = array.array('i', tl)
tn = np.array(tl, dtype=int)
print(tl, sys.getsizeof(tl))
print(ta, sys.getsizeof(ta))
print(tn, sys.getsizeof(tn))

