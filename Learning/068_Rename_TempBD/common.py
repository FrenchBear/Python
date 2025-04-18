# Sous-programmes communs du projet RenameTempBD
# 2020-03-05    PV

import os
import shutil
import unicodedata

from typing import Iterable


# Juste les fichiers d'un dossier, noms sans chemins
def get_files(source: str) -> list[str]:
    # return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])
    _1, _2, files = next(os.walk(source))
    return files


# Juste les sous-dossiers d'un dossier, noms sans chemins
def get_folders(source: str) -> list[str]:
    # return list([f for f in os.listdir(source) if os.path.isdir(os.path.join(source, f))])
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


# Replace special quotes by normal one, and unbreakable space by space
intab = "`‘’\xa0‽⁉“”−—º"
outtab = "''' ⁈⁈''--°"
transtab = str.maketrans(intab, outtab)


# On ne conserve que des caractères valides pour uun nom de BD
def clean_file_name(s: str) -> str:
    s = unicodedata.normalize("NFC", s).translate(transtab)
    res = "".join(
        c
        for c in s
        if 32 <= ord(c) < 127
        or c in "¿¡⁈°·¼½¾…«»€§¬"
        or unicodedata.category(c) in ["Ll", "Lu", "Nd"]
    )
    return res


# Performance hlper


def memoize_normalize_serie(f):
    memory = {}

    def inner(s):
        if s not in memory:
            memory[s] = f(s)
        return memory[s]

    return inner


# Retourne une version canonisée du nom de série, en minuscule, sans accents, en enlevant certains préfixes et suffies
@memoize_normalize_serie
def normalize_serie(serie: str) -> str:
    # Mn = Mark, Nonspacing = combining latin characters accents
    serie = "".join(
        c
        for c in unicodedata.normalize("NFD", serie.lower())
        if unicodedata.category(c) != "Mn" and c != ","
    )
    for prefix in [
        "les aventures de ",
        "les aventures d'",
        "une aventure de ",
        "une aventure d'",
        "la legende de ",
        "la legende des ",
        "la legende d'",
        "legende de ",
        "legende des ",
        "legende d'",
        "legendes de ",
        "legendes des ",
        "legendes d'",
        "le ",
        "la ",
        "les ",
        "l'",
        "un ",
        "une ",
    ]:
        if serie.startswith(prefix) and serie not in [
            "voyageur",
            "le voyageur",
            "jojo",
            "les aventures de jojo",
        ]:
            serie = serie[len(prefix) :]
    for suffix in [" - pdf", " - rar", " - zip", " pdf", " rar", " zip"]:
        if serie.endswith(suffix):
            # A vérifier
            serie = serie[: -len(suffix)]
    subst: tuple[str, str]
    for subst in [
        (" & ", " et "),
    ]:
        serie = serie.replace(subst[0], subst[1])
    return serie


def merge_folders(
    sourcefolderfp: str, targetfolderfp: str, DO_IT: bool = False
) -> tuple[int, int, int]:
    nfm = 0  # Number of files moved
    ndn = 0  # Number of duplicates name, renamed
    nds = 0  # number of duplicates name+size, not moved
    nfnm = 0  # Number of files not moved
    for file in get_files(sourcefolderfp):
        nfm += 1
        stem, ext = os.path.splitext(file)
        if ext.lower() != ".db":
            sourcefilefp = os.path.join(sourcefolderfp, file)
            targetfilefp = os.path.join(targetfolderfp, file)
            to_move = True
            if os.path.exists(targetfilefp):
                if os.path.getsize(sourcefilefp) == os.path.getsize(targetfilefp):
                    nds += 1
                    nfnm += 1
                    to_move = False
                else:
                    ndn += 1
                    for suffix in ["Bis", "Ter", "Quater", "5", "6"]:
                        targetfilefp = os.path.join(
                            targetfolderfp, stem + " - " + suffix + ext
                        )
                        if not os.path.exists(targetfilefp):
                            break
            if to_move:
                print(f"  {sourcefilefp}  ->  {targetfilefp}")
                if DO_IT:
                    try:
                        os.rename(sourcefilefp, targetfilefp)
                    except Exception:
                        print(f"*** Err renaming {sourcefilefp} into {targetfilefp}")

    # Cleanup
    if DO_IT:
        lr = get_files(sourcefolderfp)
        if len(lr) < nfnm or len(lr) > nfnm + 1:  # +1 for thumbs.db
            breakpoint()
        shutil.rmtree(sourcefolderfp)

    return nfm, ndn, nds


def get_safe_name(namefp: str, original: str|None = None) -> str:
    if not os.path.exists(namefp):
        return namefp
    if original and original != namefp and original.lower() == namefp.lower():
        return namefp
    folder, file = os.path.split(namefp)
    stem, ext = os.path.splitext(file)
    for suffix in ["Bis", "Ter", "Quater", "5", "6"]:
        targetfilefp = os.path.join(folder, stem + " - " + suffix + ext)
        if not os.path.exists(targetfilefp):
            return targetfilefp
    return os.path.join(folder, stem + " - 999" + ext)


def file_length(pathfp: str) -> int:
    sr = os.stat(pathfp)
    return sr.st_size
