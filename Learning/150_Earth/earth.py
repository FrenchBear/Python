# earth.py
# Measuring earth using Cassini data
# From Programmation python avancée, 2è ed
#
# 2025-07-18    PV

from math import sin, cos, radians

# Read triangles.txt, containing angles between three points
# This file contains triplets of lines with the format:
# point (20 char)         angle_deg angle_min angle_sec
# Now we don't need to store the angles, we just need to calculate the distances

def process_line(line: str) -> tuple[str, float]:
    """Process a line from triangles.txt and return point name and angle in degrees."""
    point = line[0:20].strip()
    ta = line[20:].split()
    assert len(ta) == 3
    angle = float(ta[0]) + float(ta[1]) / 60.0 + float(ta[2]) / 3600.0
    return point, angle


distancesDic: dict[tuple, float] = {}
distancesDic["Juvisy", "Villejuif"] = 5748
distancesDic["Sig.Nord", "Sig.Sud"] = 7928 + 5 / 6

print(f"Distance between Juvisy and Villejuif: {distancesDic["Juvisy", "Villejuif"]:.2f} toises")
print(f"Distance between Sig.Nord and Sig.Sud: {distancesDic["Sig.Nord", "Sig.Sud"]:.2f} toises")
nt = 0
with open("triangles.txt", "r") as file:
    while line := file.readline():
        if len(line) < 10:
            continue
        nt += 1
        p1, a1 = process_line(line)
        line = file.readline()
        p2, a2 = process_line(line)
        line = file.readline()
        p3, a3 = process_line(line)
        d3 = distancesDic.get((p1, p2), None)
        if d3 is None:
            d3 = distancesDic.get((p2, p1), None)
        assert d3 is not None, f"Step 1, Distance not found for {p1} and {p2}"
        if abs(a1 + a2 + a3 - 180) > 0.1:
            print(f"Warning: angles {a1}, {a2}, {a3} do not sum to 180 degrees for triangle {p1}, {p2}, {p3}")

       # Calculate the distances
        d1d3 = sin(radians(a2)) * d3 / sin(radians(a3))
        d2d3 = sin(radians(a1)) * d3 / sin(radians(a3))
        distancesDic[p1, p3] = d1d3
        distancesDic[p2, p3] = d2d3
        print(f"Distance between {p1} and {p3}: {d1d3:.2f} toises")
        print(f"Distance between {p2} and {p3}: {d2d3:.2f} toises")
print(nt, " triangles read")


# Then read angles between two points and a N-S meridian from inclinaisons.txt
# This file contains lines with the format:
# p1 (20 char)         p2 (20 char)      angle_deg angle_min angle_sec
total = 0.0
with open("inclinaisons.txt", "r") as file:
    for line in file:
        if len(line) > 40:
            p1 = line[0:20].strip()
            p2 = line[20:40].strip()
            ta = line[40:].split()
            assert len(ta) == 3
            angle = radians( float(ta[0]) + float(ta[1]) / 60.0 + float(ta[2]) / 3600.0)
            d = distancesDic.get((p1, p2), None)
            if d is None:
                d = distancesDic.get((p2, p1), None)
            assert d is not None, f"Step 2, Distance not found for {p1} and {p2}"
            # Calculate the distance to the meridian
            dMeridian = d * cos(angle)
            total += dMeridian

# Convert toises to meters (1 toise = 1.949 m)
totalMeters = total * 1.949

# Now totalMeters is the total distance to the meridian between Dunkerque and Perpignan

latitudes = [
[2, 11, 50, 17], # Dunkerque -- Observatoire
[1, 45, 7, 20], # Observatoire -- Bourges
[2, 43, 51, 5], # Bourges -- Rodez
[1, 39, 11, 12], # Perpignan -- Rodez
]

angle = sum(a[0] for a in latitudes) # degrés
angle += sum(a[1] for a in latitudes) / 60 # minutes
angle += sum(a[2] for a in latitudes) / 3600 # secondes
angle += sum(a[3] for a in latitudes) / 216000 # tierces

print("Rayon de la terre: {:.4g} km".format(totalMeters / radians(angle) / 1000))
