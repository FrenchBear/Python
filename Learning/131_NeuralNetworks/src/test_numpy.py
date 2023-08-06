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

# Example for n=2 inputs of m=3 neurons
# a = colon vector[n] = numpy array(n,1), a(i) = input i [0..n[
# b = colon vector[m] = numpy array(m,1), b(j) = biases j [0..m[
# w = matrix[m,n] = numpy array(m,n), w(i,j) = weight of input j [0..m[ for neuron i [0..m[
#
#                                ⎡a⎤ ↑
#                                ⎢ ⎥  n inputs
#         ⎛                      ⎣ ⎦ ↓                ⎞
#         ⎜          ↑ ⎡w     ⎤        ⎡b⎤ ↑         ⎟
#  a' = σ ⎜   m neurons ⎢      ⎥      + ⎢ ⎥  m neurons ⎟
#         ⎜          ↓ ⎣      ⎦        ⎣ ⎦ ↓         ⎟
#         ⎝             <-  n ->                       ⎠
#                         inputs
#
# Using compact form, a' = σ(w×a + b)
#
# Expanded form: a'[x] = σ( Σ(i=0..n-1)w[x,i]*a[i,0] + b[x,0] )
# : output of neuron x = σ( Σ(i=input neuron)(weight of input i * value of input i) + bias(neuron x) )


a = np.array([2, 3]).reshape(2, 1)  # Column vector 2 elements
b = np.array([0.2, 0.7, 0.3]).reshape(3, 1)  # Column vector 3 elements
w = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]).reshape(3, 2)  # Matrix 3 rows 2 columns

print('\na')
pprint(a)
print('\nb')
pprint(b)
print('\nw')
pprint(w)

a2 = np.dot(w, a) + b
print('\na2 = w×a + b')
pprint(a2)

#a2alt = w @ a + b
#assert all(a2 == a2alt)
#pprint(a2alt)

a3 = sigmoid(a2)
print('\na3 = σ(a2)')
pprint(a3)
