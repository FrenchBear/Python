>>> import numpy
>>> floats = numpy.loadtxt('floats-10M-lines.txt')
>>> floats[-3:]
array([ 3016362.69195522,   535281.10514262,  4566560.44373946])
>>> floats *= .5
>>> floats[-3:]
array([ 1508181.34597761,   267640.55257131,  2283280.22186973])
>>> from time import perf_counter as pc
>>> t0 = pc(); floats /= 3; pc() - t0
0.03690556302899495
>>> numpy.save('floats-10M', floats)
>>> floats2 = numpy.load('floats-10M.npy', 'r+')
>>> floats2 *= 6
>>> floats2[-3:]
memmap([ 3016362.69195522,   535281.10514262,  4566560.44373946])
