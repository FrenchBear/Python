# rename_series_officiel.py
# Ensure that BD series (part of name before first " - ") are homogeneous
# 2020-02-28    PV

import os
import sys
import re
from collections import defaultdict
from typing import Dict, List, Tuple, DefaultDict, Iterable
import json
import re
import unicodedata

from common import *


#REBUILD_FILES_LIST = True
DO_IT = True

source = r"D:\Downloads\eMule\BD1"
#source = r"W:\TempBD\final"

# if REBUILD_FILES_LIST:
#     print("Reading files hierarchy...")
#     files = list(get_all_files(source))
#     print(f"Wrting {len(files)} records in cache filesH.json")
#     with open(r'filesH.json', 'w', encoding='utf8') as outfile:
#         json.dump(files, outfile, indent=4, ensure_ascii=False)
#     print("Done.")
# else:
#     with open(r'filesH.json', 'r', encoding='utf-8') as infile:
#         files = json.load(infile)
#     print(f"Loaded {len(files)} records from filesH.json")

files = list(get_all_files(source))


extra_rename = [
    ('Les Cahiers De La Bande Dessinée', 'Les cahiers de la BD'),
    ('Petite bédéthèque des savoirs', 'La petite bédéthèque des savoirs'),
    ('Spirou & Fantasio', 'Spirou et Fantasio'),
]


def rename_series():
    # Load official spellings
    spo = []
    with open(r'spellings_officiel.json', 'r', encoding='utf8') as infile:
        spo = json.load(infile)
    dicspo = {}
    for spelling in spo:
        dicspo[normalize_serie(spelling)] = spelling

    dicren = {}
    for bad, good in extra_rename:
        dicren[bad.lower()] = good

    nf = 0
    nr = 0

    # Rename series using official spelling
    for fullpath in files:
        nf += 1
        path, file = os.path.split(fullpath)
        basename, ext = os.path.splitext(file)
        segments = basename.split(" - ")
        serie = segments[0]
        serie_lna = normalize_serie(serie)

        to_rename = False
        if serie_lna in dicspo.keys():
            if segments[0] != dicspo[serie_lna]:
                segments[0] = dicspo[serie_lna]
                to_rename = True
        else:
            if serie.lower() in dicren.keys():
                segments[0] = dicren[serie.lower()]
                to_rename = True

        if to_rename:
            nr += 1
            newname = " - ".join(segments)+ext.lower()
            newname
            print(f'{file:<100} -> {newname}')
            if DO_IT:
                try:
                    os.rename(fullpath, os.path.join(path, newname))
                except:
                    print("*** Err")
    if not DO_IT:
        print("No action: ", end='')
    print(f'{nf} fichiers analysés, {nr} renommé(s)')

rename_series()
