# Sous-programmes communs relatif au filesystem
# 2020-03-05    PV
# 2021-04-10    PV      Support du filesystem isolé sous common_fs.py

import os
import shutil
import unicodedata

from typing import List, Iterable, Tuple


# Juste les fichiers d'un dossier, noms sans chemins
def get_files(source: str) -> List[str]:
    #return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])
    _1, _2, files = next(os.walk(source))
    return files

# Juste les sous-dossiers d'un dossier, noms sans chemins
def get_folders(source: str) -> List[str]:
    #return list([f for f in os.listdir(source) if os.path.isdir(os.path.join(source, f))])
    _1, folders, _2 = next(os.walk(source))
    return folders

# Chemin complet de tous les fichiers à partir d'une racine
def get_all_files(path: str) -> Iterable[str]:
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

# Chemin complet de tous les dossiers à partir d'une racine
def get_all_folders(path: str) -> Iterable[str]:
    for root, folders, _ in os.walk(path):
        for folder in folders:
            yield os.path.join(root, folder)


def filepart(fullpath: str) -> str:
    _, file = os.path.split(fullpath)
    return file


if __name__=='__main__':
    print(filepart(r'c:\temp\f1.txt'))