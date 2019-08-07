# Beware: do not name this file random.py, otherwise "import random" import itself!!!

import random

g = []
n = []

mu = 2.0
si = 1.0
np = 10000

for i in range(np):
    g.append(random.gauss(mu, si))
    n.append(random.normalvariate(mu, si))

import numpy as np

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
