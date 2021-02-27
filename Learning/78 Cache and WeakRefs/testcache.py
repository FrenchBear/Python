# Test d'un cache en utilisant un weakref.WeakValueDictionary
# 2021-02-26    PV

import weakref
import collections
import random
import matplotlib.pyplot as plt
import math

# Classe objet arbitraire
class sprocket:
    def __init__(self, key: int) -> None:
        self.key = key


def test_cache(global_size:int, cache_size: int, rounds: int) -> float:
    # Les objects ne sont présents dans ce cache que s'ils existent dans cache_que.  Le test est rapide puisque c'est un dictionnaire
    cache_dic = weakref.WeakValueDictionary()
    # Simple queue de stockage des objets cachés, limitée à cache_size entrées
    cache_que = collections.deque(maxlen=cache_size)

    # Retourne le coût pour obtenir le sprocket de clé key, par convention la création de l'objet a un coût de 50 (ex: lecture BD) contre 1 s'il est dans le cache
    def build_item(key: int) -> int:
        if key in cache_dic:
            s = cache_dic[key]
            # On place l'objet en tête de cache, comme s'il venait d'être ajouté au cache pour la première fois
            cache_que.remove(s)
            cache_que.append(s)
            return 1
        s = sprocket(key)
        cache_que.append(s)
        cache_dic[key] = s
        return 50

    cost = 0
    for i in range(rounds):
        while True:
            # Deux modèle d'accès aléatoire aux clés, un modèle "loi normale" centrée en global_size/2, et un modèle uniforme
            k = math.floor(random.normalvariate(global_size/2,global_size/8))
            #k = random.randint(1, global_size)
            if 1<=k<=global_size: break
        cost += build_item(k)
    return cost/rounds


print(test_cache(10,10,100))

sizes = [5*i for i in range(0,20)]
costs = [test_cache(100,s,200) for s in sizes]

#print(sizes)
#print(costs)

"""
# Test d'une loi normale
b = 50
sizes = range(b+1)
costs = [0]*(b+1)
for i in range(100000):
    k = math.floor(random.normalvariate(b/2,b/8))
    if 0<=k<=b:
        costs[k]+=1
print(costs)
"""

plt.plot(sizes, costs)
plt.show()
