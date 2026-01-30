# sincos.py
# Computes sin and cos using Taylor function and Cordic (half-trig)
# Taylor: From Windows calculator C++ code, function _sinrat
# Cordic: Personal code
#
# 2023-04-20    PV      Taylor version only
# 2023-12-03    PV      Added CORDIC half-trig from C:\Development\GitHub\Visual-Studio-Projects\Net8\520-549\524b CS Cordic HalfTrig\524b CS Cordic HalfTrig.sln

import math
from typing import Tuple


def sin_taylor_base(x: float):
    x2 = x * x
    j = 0
    this_term = x
    somme = x
    for j in range(1, 100):
        next_term = -this_term * x2 / (2 * j * (2 * j + 1))
        next_somme = somme + next_term
        if somme == next_somme:
            break
        somme = next_somme
        this_term = next_term
    return somme

# Forces angle to be in [0..π] for more efficient computation
def sin_taylor(angle: float) -> float:
    invertSign = False

    if angle < 0:
        angle = -angle
        invertSign = True

    if angle >= math.pi * 2:
        angle %= 2 * math.pi
    if angle >= math.pi:
        angle -= math.pi
        invertSign ^= True

    if angle > math.pi / 2:
        angle = math.pi - angle

    return sin_taylor_base(angle)

def cos_taylor(angle: float) -> float:
    return sin_taylor(angle + math.pi / 2)



def sincos_cordic(angle: float) -> tuple[float, float]:
    """ Returns tuple (sin, cos) of angle radians computed using cordic algorithm

        Actual computing algorithm, sin and cos at the same time
        Angle must be between 0 and π/2
        Note that the table of decreasing sin/cos (π/2, π/4, π/8, ...) should be calculated only one time
        for efficiency, not recomputed each time as in this learning code
    """

    # Simple time-saver
    if angle == 0:
        return (1.0, 0.0)

    # Start at π/4, with both sin and cos = (√2)/2
    a = math.pi / 4
    s = math.sqrt(2.0) / 2.0
    c = s

    # Start with horizontal unitary vector for result
    cos = 1.0
    sin = 0.0

    while True:
        # If angle remaining to rotate is more than currently computed angle/s/c, we do the rotation
        if angle >= a:
            angle -= a

            # Coordinates before rotation
            x0 = cos
            y0 = sin

            # Standard rotation matrix times vector (cos, sin)
            cos = x0 * c - y0 * s
            sin = x0 * s + y0 * c

        # Compute sin and cos of half-angle for next step
        a /= 2.0
        if a < 1e-17:
            break

        # Half-trig computation, sin(a/2) and cos(a/2)
        c2 = c
        c = math.sqrt((c + 1.0) / 2.0)
        s /= math.sqrt(2 * (1.0 + c2))

    return (sin, cos)

def sin_cordic(angle: float) -> float:
    invertSign = False

    if angle < 0:
        angle = -angle
        invertSign = True

    if angle >= math.pi * 2:
        angle %= 2 * math.pi
    if angle >= math.pi:
        angle -= math.pi
        invertSign ^= True

    if angle > math.pi / 2:
        angle = math.pi - angle

    (sin, _) = sincos_cordic(angle)
    return sin


# Lazy implementation
def cos_cordic(angle: float) -> float:
    return sin_cordic(angle + math.pi / 2)



a0 = 1.1823614786
(sm, cm) = (math.sin(a0), math.cos(a0))
(sc, cc) = sincos_cordic(a0)
(st, ct) = (sin_taylor(a0), cos_taylor(a0))

print(f"a={a0}")
print("Maple:  c=0.378740326955891541643393287014\ts=0.925502979323861698653734026619")
print(f"Math:   c={cm}\t\t\ts={sm}\t\t\t(math.cos and math.sin)")
print(f"Cordic: c={cc}\t\t\ts={sc}\t\t\t(Cordic cos and sin)")
print(f"Taylor: c={ct}\t\t\ts={st}\t\t\t(Taylor cos and sin)")

# print(sin_taylor(math.pi / 4))
# print(math.sin(math.pi / 4))
