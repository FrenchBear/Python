import os

d = {
1: 'Dudley Détraqué', 
2: 'Crises de bec', 
3: 'La garde rapprochée', 
4: '12, square Grimmaurd', 
5: 'L''Ordre du Phénix', 
6: 'La noble et très ancienne maison des Black', 
7: 'Le ministère de la Magie', 
8: 'L''audience', 
9: 'Les malheurs de Mrs Weasley', 
10: 'Luna Lovegood', 
11: 'La nouvelle chanson du Choixpeau magique', 
12: 'Le professeur Ombrage', 
13: 'Retenue douloureuse avec Dolores', 
14: 'Percy et Patmol', 
15: 'La Grande Inquisitrice de Poudlard', 
16: 'À la Tête de Sanglier', 
17: 'Décret d''éducation numéro vingt-quatre', 
18: 'L''armée de Dumbledore', 
19: 'Le lion et le serpent', 
20: 'Le récit de Hagrid', 
21: 'L''oeil du serpent', 
22: 'L''hôpital Ste Mangouste pour les maladies et blessures magiques', 
23: 'Noël dans la salle spéciale', 
24: 'Occlumancie', 
25: 'Le scarabée sous contrôle', 
26: 'Vu et imprévu', 
27: 'Le centaure et le cafard', 
28: 'Le pire souvenir de Rogue', 
29: 'Conseils d''orientation', 
30: 'Graup', 
31: 'Buse', 
32: 'Hors du feu', 
33: 'Lutte et fugue', 
34: 'Le Département des Mystères', 
35: 'Au-delà du voile', 
36: 'Le seul qu''il ait jamais craint', 
37: 'La prophétie perdue', 
38: 'La deuxième guerre commence',
     }

path = r"C:\MusicGD\AudioBooks\Harry Potter\05 Harry Potter et l'Ordre du Phénix"

for f in os.listdir(path):
    i = int(f[:2])
    nn = f[:2]+" - "+d[i]+".mp3"
    print(nn)
    os.rename(os.path.join(path, f), os.path.join(path, nn))
    