# test2.py
# Test of neural network learning
#
# 2023-08-02    PV

import network
import mnist_loader
import reprlib

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
#print('training_data\n', reprlib.repr(training_data), end='\n\n')
#print('validation_data\n', reprlib.repr(validation_data), end='\n\n')
#print('test_data\n', reprlib.repr(test_data), end='\n\n')

net = network.Network([784, 30, 10])
net.SGD(training_data, 30, 10, 3.0, test_data=test_data)

