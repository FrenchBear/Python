# rename_series_officiel.py
# Ensure that BD series (part of name before first " - ") are homogeneous
# 2020-02-28    PV

import os
import sys
import re
from collections import defaultdict
from typing import Dict, List, Tuple, DefaultDict, Iterable, TextIO
import json
import re
import unicodedata

from common import *


source = r"D:\Downloads\eMule\BD1"
#source = r"W:\TempBD\final"
DO_IT = True


files: List[str]
folders: List[str]
files = list(get_all_files(source))
_1, folders, _2 = next(os.walk(source))

glolbal_rename: List[Tuple[str, str]] = [
    ('Bande Dessinée', 'BD'),
    ('Bande Dessinee', 'BD'),
    ('Spirou & Fantasio', 'Spirou et Fantasio'),
    ('Blake & Mortimer', 'Blake et Mortimer'),
    ('Far West', 'Far-West'),
    ('^PFA ', 'BDA - PFA '),
    ('^Priodique ', 'Périodique '),
    ('^Périodique ', 'Périodique '),
    ('^Periodique ', 'Periodique '),
    ('^Périodique PFA ', 'BDA - Périodique PFA '),
    ('^Terrificolor ', 'BDA - Terrificolor '),
    ('^Contes Malicieux ', 'BDA - Contes Malicieux '),
    ('^Luciféra ', 'BDA - Luciféra'),
    ('^Lucifera ', 'BDA - Luciféra'),
    ('^Revue - DBD ', 'dBD '),
    ('^Revue - Fluide glacial ', 'Fluide glacial '),
    ('^Revue - Les cahiers de la BD', 'Les cahiers de la BD'),
    ('^Revue - Métal Hurlant ', 'Métal Hurlant '),
    ('^Revue - Pif Gadget ', 'Pif Gadget '),
    ('^Revue - Pilote ', 'Pilote '),
    ("L'ile", "L'île"),
    ("Les iles", "Les îles"),
    ('maitre', 'maître'),
]


# Load official spellings
spo = []
with open(r'spellings_officiel.json', 'r', encoding='utf-8_sig') as infile:
    spo = json.load(infile)
dicspo = {}
for spelling in spo:
    dicspo[normalize_serie(spelling)] = spelling


# Rename series using official spelling
def rename_series(out: TextIO):
    nf = nr = 0
    for fullpath in files:
        nf += 1
        path, file = os.path.split(fullpath)
        basename, ext = os.path.splitext(file)

        # First process general substitutions
        to_rename = False
        for before, after in glolbal_rename:
            newname = re.sub(before, after, basename, flags=re.IGNORECASE)
            if basename!=newname:
                basename=newname
                to_rename=True

        segments = basename.split(" - ")
        serie = segments[0]
        serie_lna = normalize_serie(serie)

        if serie_lna in dicspo.keys():
            if segments[0] != dicspo[serie_lna]:
                segments[0] = dicspo[serie_lna]
                to_rename = True

        if to_rename:
            nr += 1
            newname = " - ".join(segments)+ext.lower()
            newname
            print(f'{file:<70} -> {newname}')
            out.write(f'{file:<70} -> {newname}\n')
            if DO_IT:
                try:
                    os.rename(fullpath, get_safe_name(os.path.join(path, newname)))
                except:
                    print("*** Err")
    if not DO_IT:
        print("No action: ", end='')
    print(f'{nf} fichiers analysés, {nr} renommé(s)')


def rename_folders(out: TextIO):
    nf = nr = 0
    for folder in folders:
        nf += 1
        folder_lna = normalize_serie(folder)
        if folder_lna in dicspo.keys():
            if folder != dicspo[folder_lna]:
                newname = dicspo[folder_lna]
                print(f'{folder:<70} -> {newname}')
                out.write(f'{folder:<70} -> {newname}\n')
                nr += 1
                if DO_IT:
                    folderfp = os.path.join(source, folder)
                    try:
                        os.rename(folderfp, get_safe_name(os.path.join(source, newname)))
                    except:
                        print("*** Err")
    if not DO_IT:
        print("No action: ", end='')
    print(f'{nf} dossiers analysés, {nr} renommé(s)')


with open('rename.txt', 'w', encoding='utf-8') as out:
    rename_series(out)
    out.write('\n\n----------------------------------\n\n')
    rename_folders(out)
