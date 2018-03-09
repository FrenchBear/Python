import itertools
for n,ph in enumerate([" ".join(s) for s in itertools.permutations(['Belle marquise','vos beaux yeux','me font','mourir',"d'amour"])]):
    print(n, ph)
    
