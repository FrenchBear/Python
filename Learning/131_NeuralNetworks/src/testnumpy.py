# testnumpy.py
# Tests using numpy to understand the basics of neural network calculations
#
# 2023-08-03    PV

import numpy as np
from pprint import pprint

# Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))

a = np.array([2,3]).reshape(2,1) # Column vector 2 elements
b = np.array([0.2,0.7,0.3]).reshape(3,1) # Column vector 3 elements
w = np.array([0.1,0.2,0.3,0.4,0.5,0.6]).reshape(3,2)  # Matrix 3 rows 2 columns

print('\na')
pprint(a)
print('\nb')
pprint(b)
print('\nw')
pprint(w)

a2 = np.dot(w,a)+b
print('\na2')
pprint(a2)

a3 = sigmoid(a2)
print('\na3')
pprint(a3)
