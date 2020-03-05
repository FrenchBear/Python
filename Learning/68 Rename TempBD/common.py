# Sous-programmes communs du projet RenameTempBD
# 2020-03-05    PV

import sys
import os
import unicodedata
from typing import List, Iterable, Tuple


# Juste les fichiers d'un dossier, juste les noms
def get_files(source: str) -> List[str]:
    return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])

# Chemin complet de tous les fichiers à partir d'une racine
def get_all_files(path: str) -> Iterable[str]:
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)


# Replace special quotes by normal one, and unbreakable space by space
intab = "`‘’\xa0‽⁉“”−—º"
outtab = "''' ⁈⁈''--°"
transtab = str.maketrans(intab, outtab)


# On ne conserve que des caractères valides pour uun nom de BD
def clean_file_name(s: str) -> str:
    s = unicodedata.normalize("NFC", s).translate(transtab)
    res = ''.join(c for c in s if 32 <= ord(
        c) < 127 or c in "¿¡⁈°·¼½¾…«»€§¬" or unicodedata.category(c) in ['Ll', 'Lu', 'Nd'])
    return res

# Performance hlper
def memoize_normalize_serie(f):
    memory = {}

    def inner(s):
        if s not in memory:
            memory[s] = f(s)
        return memory[s]
    return inner

# Retourne une version caconisée du nom de série, en minuscule, sans accents, en enlevant certains préfixes et suffies
@memoize_normalize_serie
def normalize_serie(serie: str) -> str:
    # Mn = Mark, Nonspacing = combining latin characters accents
    serie = ''.join(c for c in unicodedata.normalize("NFD", serie.lower())
                    if unicodedata.category(c) != 'Mn' and c != ',')
    for prefix in ['les aventures de ', "les aventures d'", 'une aventure de ', "une aventure d'", "la legende de ", "la legende des ", "la legende d'", "legende de ", "legende des ", "legende d'", "legendes de ", "legendes des ", "legendes d'", 'le ', 'la ', 'les ', "l'", 'un ', 'une ']:
        if serie.startswith(prefix):
            serie = serie[len(prefix):]
    for suffix in [' - pdf', ' - rar', ' - zip', ' pdf', ' rar', ' zip']:
        if serie.endswith(suffix):
            # A vérifier
            serie = serie[:-len(suffix)]
    subst: Tuple[str, str]
    for subst in [
        (' & ', ' et '),
    ]:
        serie = serie.replace(subst[0], subst[1])
    return serie
