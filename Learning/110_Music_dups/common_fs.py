# Sous-programmes communs relatif au filesystem
#
# 2020-03-05    PV
# 2021-04-10    PV      Support du filesystem isolé sous common_fs.py
# 2022-01-06    PV      Version avec commentaires
# 2022-01-08    PV      basename
# 2022-05-26    PV      file_exists et folder_exists

"""
Function 	        Copies      Copies          Uses file       Destination
                    metadata 	permissions 	object 	        may be directory
shutil.copy 	    No          Yes             No              Yes
shutil.copyfile 	No          No              No              No
shutil.copy2 	    Yes         Yes             No              Yes
shutil.copyfileobj 	No          No              Yes             No
"""

import os
from typing import List, Iterable


def get_files(source: str) -> List[str]:
    '''Retourne juste les fichiers d'un dossier, noms.ext sans chemins'''
    _1, _2, files = next(os.walk(source))
    return files

def get_folders(source: str) -> List[str]:
    '''Retourne juste les sous-dossiers d'un dossier, noms sans chemins'''
    _1, folders, _2 = next(os.walk(source))
    return folders

def get_all_files(path: str) -> Iterable[str]:
    '''Retourne un itérateur produisant tous les fichiers à partir d'une racine, chemin complet'''
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

def get_all_folders(path: str) -> Iterable[str]:
    '''Retourne un itérateur produisant tous les dossiers à partir d'une racine, chemin complet'''
    for root, folders, _ in os.walk(path):
        for folder in folders:
            yield os.path.join(root, folder)

# Simple helpers
def filepart(fullpath: str) -> str:
    '''Retourne un nom de fichier sans son chemin'''
    _, file = os.path.split(fullpath)
    return file

def basename(filewithext: str) -> str:
    '''Retourne le nom de fichier sans extension'''
    base, _ = os.path.splitext(filewithext)
    return base

def file_exists(fullpath: str) -> bool:
    '''Teste si un fichier existe'''
    return os.path.exists(fullpath) and os.path.isfile(fullpath)

def folder_exists(fullpath: str) -> bool:
    '''Teste si un dossier existe'''
    return os.path.exists(fullpath) and os.path.isdir(fullpath)

def file_size(fullpath: str) -> int:
    '''Retourne la taille d'un fichier en octets'''
    return os.stat(fullpath).st_size

if __name__=='__main__':
    print(filepart(r'c:\temp\f1.txt'))          # f1.txt
    print(basename('nom_de_fichier.ext'))       # nom_de_fichier
