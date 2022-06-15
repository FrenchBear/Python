# vlib.py
# Ma bibliothèque de fonctions Python
# 2020-03-05    PV      Première version dans Rename TempBD
# 2021-01-01    PV      Version commune. filepart.


import os
import shutil
import unicodedata

from typing import List, Iterable


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

# Retourne juste le nom de fichier (equivalent of os.path.dirname but for filename)
def filenamepart(fileandpathname: str) -> str:
    _, filename = os.path.split(fileandpathname)
    return filename
