# Pythagora Triangles Puzzles (§3)
# 2020-09-13    PV

import math
import itertools


def find_isoceles(sommets: list[tuple[int, int]]):
    for tri in itertools.combinations(sommets, 3):
        s0 = tri[0]
        s1 = tri[1]
        s2 = tri[2]
        d01 = math.dist(s0, s1)
        d02 = math.dist(s0, s2)
        d12 = math.dist(s1, s2)
        if math.isclose(d01, d02) or math.isclose(d01, d12) or math.isclose(d02, d12):
            print(tri)


sommets3_7 = [(1, 1), (2, 2), (6, 1), (5, 2), (3, 4), (3, 5)]
# find_isoceles(sommets3_7)

sommets3_8 = [(0, 1), (1, 1), (3, 0), (4, 1), (4, 6), (6, 2), (6, 4)]
find_isoceles(sommets3_8)
