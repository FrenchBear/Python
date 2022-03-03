# Date_Des.py
# Affiche toutes les dates avec deux dés
# J'ai trouvé la solution de tête en tapant ce commentaire, 6 et 9 ne nécessitent pas deux faces de dé!
#
# 2022-02-25    PV

l1 = [1, 6, 9, 2, 0, 7, 8]
l2 = [1, 5, 2, 0, 3, 4]

l = [10*c1+c2 for c1 in l1 for c2 in l2]
l.extend(10*c2+c1 for c1 in l1 for c2 in l2)
l = list(set(l))
l.sort()
print(l)

ok = all(d in l for d in range(1, 32))
print(ok)
