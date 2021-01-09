import os
import shutil
import unicodedata

from typing import List, Iterable, Tuple, Dict


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

def filepart(filefp: str) -> str:
    _, file = os.path.split(filefp)
    return file
   


source = r'W:\Livres\Informatique'
allfiles = list(get_all_files(source))
lref: Dict[int, str] = {}
for file in allfiles:
    if not '!a_trier' in file.lower():
        size = os.stat(file).st_size
        if size in lref:
            print(f'dup size {size}:\n  {lref[size]}\n  {file}\n')
        else:
            lref[size] = file

for file in allfiles:
    if '!a_trier' in file.lower():
        size = os.stat(file).st_size
        if size in lref and filepart(file).lower()==filepart(lref[size]).lower():
            #print(f'dup size and name {size}:\n  {lref[size]}\n  {file}\n')
            print('del "'+file+'"')
