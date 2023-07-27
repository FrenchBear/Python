# aiguille_creyse.py
# Résolution du cryptogramme de l'aiguille creuse
#
# 2022-07-04 PV

import unicodedata


def sans_accent(mot: str) -> str:
    return ''.join(c for c in unicodedata.normalize("NFD", mot) if unicodedata.category(c) != 'Mn').casefold()

smf = set()
with open(r'words\words1.fr.txt', 'r', encoding='UTF-8') as f:
    smf |= set(sans_accent(mot) for mot in f.read().splitlines())
with open(r'words\words2.fr.txt', 'r', encoding='UTF-8') as f:
    smf |= set(sans_accent(mot) for mot in f.read().splitlines())
with open(r'words\extra.fr.txt', 'r', encoding='UTF-8') as f:
    smf |= set(sans_accent(mot) for mot in f.read().splitlines())

print(len(smf),"mots\n")


cons = 'bcdfghjklmnpqrstvwxz'
voyl = 'aeiouy'
def findmatch(w: str):

    filter=[]
    for i in range(len(w)):
        if w[i]=='.':
            filter.append(f'x[{i}] in cons')
        else:
            filter.append(f'x[{i}]=="{voyl[int(w[i])-1]}"')
    sfilter = "lambda x: " + " and ".join(filter) 
    #print(sfilter)
    f = eval(sfilter)

    print(w+':')
    li = len(w)
    for m in [mot for mot in smf if len(mot)==li and f(mot)]:
        print('  '+m)
    print()

# findmatch('2.1.1..2')
# findmatch('..2')
# findmatch('.1.')
findmatch('.1..')
findmatch('1...2.2.')
findmatch('.2.43.2..2.')
# findmatch('.45')
# findmatch('..')
# findmatch('2')
# findmatch('.')
findmatch('4...2..2.4..2')

findmatch('13.53..2')
findmatch('..25.2')
