# TronqueSonos
# Limite les noms de fichiers Sonos
# 2020-08-16    PV


import os
from collections import defaultdict
from collections.abc import Iterable


source = r'\\teraz\music\Sonos\Pierre\Complete'

# Chemin complet de tous les fichiers à partir d'une racine


def get_all_files(path: str) -> Iterable[str]:
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)


def compte_len():
    co = defaultdict(int)

    for fullpath in get_all_files(source):
        path, file = os.path.split(fullpath)
        li = len(file)
        co[li] += 1

    ks = sorted(co.keys(), reverse=True)
    for k in ks:
        print(k, ";", co[k])


def truncate():
    lmax = 150
    nr = 0
    for fullpath in list(get_all_files(source)):
        path, file = os.path.split(fullpath)
        li = len(file)
        if li > lmax:
            stem, ext = os.path.splitext(file)
            newname = (stem[:lmax-len(ext)]).strip()+ext
            newfullpath = os.path.join(path, newname)
            os.rename(fullpath, newfullpath)
            nr += 1
    print(nr, 'files truncated')


compte_len()
