# pihuit.py
# Simple calcul de pi en comptant les points dans un 8è de cercle
# On compte les couples (x,y) avec 0 ≤ x ≤ y ≤ n tels que x²+y²<n²
# D'après Le fascinant nombre π, 2è ed, p. 16
#
# 2018-07-23    PV

def pihuit(n):
    n2 = n * n
    p = sum(1 for x in range(n + 1) for y in range(x + 1) if x * x + y * y < n2)
    return 8 * p / n2

n = 1000
print("π=", pihuit(n), " calcul avec n=",n)
