# quatuor.py
# Programme Python trouvant les solutions du problème du quatuor
#
# On peut accélérer le programme en construisant l'historique des états par lesquels on est déjà passé
# de façon à éviter les séquences "stupides" contenant des boucles comme A G->D->G->D.  Comme on arrête l'analyse
# au-delà de 20 min, cette optimisation est optionnelle.  Elle rend le programme quasi instantané, même s'il est
# un peu moins élégant.
#
# 2018-08-04    PV

"""
Un quatuor doit donner un concert dans 17 minutes de l’autre coté d’un pont qu’ils doivent traverser. 
Il fait nuit et ils n’ont qu’une lampe torche. Un maximum de deux personnes peut traverser simultanément le pont.
Toute personne ou couple traversant le pont doit avoir la lampe, et celle-ci ne peut être lancée d’un bord à l’autre.
Chaque membre du quatuor a une vitesse différente, et lorsqu’ils traversent en couple, c’est le plus lent
qui détermine le temps de passage.
Si André met une minute pour traverser, Bertrand deux minutes, Claude cinq minutes et Daniel dix minutes,
pouvez-vous trouver les deux façons de faire traverser le pont au quatuor pour commencer le concert à l’heure,
c’est à dire au plus 17 minutes après ?
"""

# itertools.combinations(l, r) retourne la liste des combinaisons de r éléments pris dans l
import itertools


# 2è partie de move, indépendante du sens du déplacement.
# Détecte les solutions (newLeft est vide) et les ajoute à la variable globale solutions.
# Poursuit récursivement l'exploration (en appelant move) tant que le temps total est inférieur à 21 minutes.
def move2(newLeft, newRight, s, leftToRight, totalTime, seq):
    global solutions
    newTotalTime = totalTime+max(speed[x] for x in s)
    if newTotalTime <= 20:
        seq2 = list(seq)
        seq2.append(('G->D ' if leftToRight else 'D->G ')+str(s))
        if len(newLeft) == 0:
            solutions.append((newTotalTime, seq2))
        move(newLeft, newRight, not leftToRight, newTotalTime, seq2)


# 1ère partie de move, en partant de l'état left et right, explore tous les déplacements possibles.
# Si leftToRight est vrai, analyse les déplacements G->D, sinon D->G.
# totalTime est le temps total du parcours à ce stade.
# seq est la séquence des opérations ayant conduit à l'état de départ
def move(left, right, leftToRight, totalTime, seq):
    if leftToRight:
        for s in itertools.chain(itertools.combinations(left, 2), itertools.combinations(left, 1)):
            newLeft = [x for x in left if x not in s]
            newRight = list(right)
            newRight.extend(s)
            move2(newLeft, newRight, s, leftToRight, totalTime, seq)
    else:
        for s in itertools.chain(itertools.combinations(right, 1), itertools.combinations(right, 2)):
            newLeft = list(left)
            newLeft.extend(s)
            newRight = [x for x in right if x not in s]
            move2(newLeft, newRight, s, leftToRight, totalTime, seq)


# Données du problème et état initial
speed = {'A': 1, 'B': 2, 'C': 5, 'D': 10}
solutions: list[tuple[int, list]] = []

# Résolution
move(['A', 'B', 'C', 'D'], [], True, 0, [])
tmin = min(t for t, _ in solutions)             # Temps optimal
for s in [s for t, s in solutions if t == tmin]:
    print(tmin, s)
