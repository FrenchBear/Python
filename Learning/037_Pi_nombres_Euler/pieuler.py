# Nombres d'Euler
# Calcul des nombres d'Euler (dernier chiffre de chaque itération) par simple additions
# vérifiant π = lim(2.n.e(n-1,n-1)/e(n,n))
# D'après Le fascinant nombre π, 2è ed, p. 33
#
# 2018-07-23    PV

l = [1]
for n in range(12):
    nl = [0]
    for m in range(len(l)):
        nl.append(sum(l[-m-1:]))
    print(nl)
    print(2*(n+1)*nl[1]/nl[-1])
    l = nl
