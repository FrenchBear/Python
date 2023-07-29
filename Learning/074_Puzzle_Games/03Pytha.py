# Pythagora Triangles Puzzles (§?)
# Construire tous les triangles isocèles dont les sommets sont des noeuds (dont A (6,0))
# et donc la longueur d'un des côtés est √34
# 2020-09-26    PV

import math
import itertools

noeuds = []
for x in range(7):
    for y in range(7):
        if (x, y) != (6, 0):
            noeuds.append((x, y))

C = (6, 0)
r34 = math.sqrt(34)
for (A, B) in itertools.combinations(noeuds, 2):
    dAB = math.dist(A, B)
    dAC = math.dist(A, C)
    dBC = math.dist(B, C)
    if math.isclose(dAB, dAC) or math.isclose(dAB, dBC) or math.isclose(dAC, dBC):
        if math.isclose(dAB, r34) or math.isclose(dAC, r34) or math.isclose(dBC, r34):
            print(A, B, C)
