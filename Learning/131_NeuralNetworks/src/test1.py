import network
import mnist_loader
from pprint import pprint
import numpy as np

net = network.Network([2, 3, 1])
pprint(net.num_layers)
pprint(net.sizes)
print('\nBiases')
pprint(net.biases)
print('\nWeights')
pprint(net.weights)

# training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
# net = network.Network([784, 30, 10])
# net.SGD(training_data, 30, 10, 3.0, test_data=test_data)

