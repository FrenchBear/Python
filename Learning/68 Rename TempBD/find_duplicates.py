import os
from collections import defaultdict
from typing import Iterable, List
from common import *

source = r'W:\TempBD\final'

DO_IT = False


# Chemin complet de tous les fichiers à partir d'une racine
def get_all_folders(path: str) -> Iterable[str]:
    for root, folders, _ in os.walk(path):
        for folder in folders:
            yield os.path.join(root, folder)

def basename(filefp: str) -> str:
    _, file = os.path.split(filefp)
    basename, _ = os.path.splitext(file)
    return basename.lower()

nd = 0
for folder in get_folders(source):
    folderfp = os.path.join(source, folder)
    ds = defaultdict(list)
    with os.scandir(folderfp) as it:
        entry: os.DirEntry
        for entry in it:
            if entry.is_file():
                ds[entry.stat().st_size].append(entry.path)
    dups = [v for k,v in ds.items() if len(v)>1]
    if dups:
        s: List[str]
        for s in dups:
            s.sort(key=lambda x: basename(x))
            for file in s[1:]:
                print(file)
                nd += 1
                if DO_IT:
                    os.remove(file)

print(f'{nd} duplicates deleted')
