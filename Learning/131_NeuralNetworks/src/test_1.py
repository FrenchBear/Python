# test1.py
# First test of neural network learning
#
# 2023-08-02    PV

import network
from pprint import pprint

net = network.Network([2, 3, 1])
pprint(net.num_layers)
pprint(net.sizes)
print('\nBiases')
pprint(net.biases)
print('\nWeights')
pprint(net.weights)
