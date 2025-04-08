# Parité Multiplication
# Calcule la proportion de multiplications paires et impaires
# Résultat, sur 100 multiplications de [0..9]x[0..9], 75 se terminent par un chiffre pair, 25 par un chiffre impair
#
# 2015-09-26    PV
# 2018-08-18    PV      Extension du nombre de méthodes au-delà des deux premières!
# 2025-04-08    PV      scipy.stats.itemfreq deprecated; numpy count unique is now np.unique_counts

import numpy as np
#from scipy.stats import itemfreq    # Deprecated
import collections

# Avec listcomp
# Liste des derniers chiffres des multiplications [0..9]x[0..9]
m = [str(x*y)[-1] for x in range(10) for y in range(10)]
f = [0]*10            # Initialise la table des fréquences des derniers chiffres à 0
for d1 in m:
    f[int(d1)] += 1    # Remplissage de la table des fréquences
# Nombre de multiplications se finissant par un chiffre pair
se = sum(f[0::2])
# Nombre de multiplications se finissant par un chiffre impair
so = sum(f[1::2])
print(f)
print('Pair', se, '   Impair', so)

# Avec genexp
f = [0]*10
for d2 in ((x*y) % 10 for x in range(10) for y in range(10)):
    f[d2] += 1
se, so = sum(f[0::2]), sum(f[1::2])
print(f)
print('Pair', se, '   Impair', so)

# Avec dictionnaire et set
ld = [(x*y) % 10 for x in range(10) for y in range(10)]
d3 = {x: ld.count(x) for x in set(ld)}
print(d3)

# Avec collections.Counter
co = collections.Counter([(x*y) % 10 for x in range(10) for y in range(10)])
kp = sum(co[x] for x in range(0, 10, 2))
ki = sum(co[x] for x in range(1, 10, 2))
print(co)
print('Pair', kp, '   Impair', ki)

# # Avec SciPy
# freq = itemfreq(ld)
# print(freq)
# print(freq[:, 1])    # Table des fréquences

# Avec numpy
print(np.bincount(ld))
print(np.unique_counts(ld))

# numpy at reduction: at(a, indices, b=None)
# Performs unbuffered in place operation on operand 'a' for elements specified by 'indices'.
# For addition ufunc, this method is equivalent to a[indices] += b, except that results are accumulated
# for elements that are indexed more than once. For example, a[[0,0]] += 1 will only increment the first element
# once because of buffering, whereas add.at(a, [0,0], 1) will increment the first element twice.
#
# This works whereas tf[ld] += 1 doesn't count multiple items
tf = np.zeros(10, dtype='int16')
np.add.at(tf, ld, 1)
print(tf)
