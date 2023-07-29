import math

def module(z: complex) -> float:
    return math.hypot(z.real, z.imag)

print(module(3.0+0.j))
print(module(3.0))
print(module(3))

a=.2
