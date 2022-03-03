# Beware: do not name this file random.py, otherwise "import random" import itself!!!

import random
import numpy as np


g = []
n = []

mu = 2.0
si = 1.0
num = 10000

for i in range(num):
    g.append(random.gauss(mu, si))
    n.append(random.normalvariate(mu, si))

ag = np.mean(g)
an = np.mean(n)

sg = np.std(g)
sn = np.std(n)

print("gauss:")
print("mean=", ag)
print("std dev=", sg)

print()
print("normalvariate:")
print("mean=", an)
print("std dev=", sn)
