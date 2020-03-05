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


REBUILD_FILES_LIST = True
DO_IT = True

source = r'D:\Downloads\eMule\BD1'
#source = r'W:\TempBD\raw'
#source = r'W:\TempBD\archives'


if REBUILD_FILES_LIST:
    print("Reading files...")
    files = get_files(source)
    print(f"Wrting {len(files)} in cache files.json")
    with open(r'files.json', 'w', encoding='utf8') as outfile:
        json.dump(files, outfile, indent=4, ensure_ascii=False)
    print("Done.")
    # sys.exit(0)
else:
    with open(r'files.json', 'r', encoding='utf8') as infile:
        files = json.load(infile)


extra_rename = [
    ('Les Cahiers De La Bande Dessinée', 'Les cahiers de la BD'),
    ('Petite bédéthèque des savoirs', 'La petite bédéthèque des savoirs'),
    ('Spirou & Fantasio', 'Spirou et Fantasio'),
]


def rename_series():
    # Load official spellings
    spo = []
    with open(r'casing_officiel.json', 'r', encoding='utf8') as infile:
        spo = json.load(infile)
    dicspo = {}
    for spelling in spo:
        dicspo[normalize_serie(spelling)] = spelling

    dicren = {}
    for bad, good in extra_rename:
        dicren[bad.lower()] = good

    # Rename series using official spelling
    for file in files:
        # if file=='Les Cahiers De La Bande Dessinée - 25 - Giraud.cbr':
        #     breakpoint()
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
            newname = " - ".join(segments)+ext.lower()
            newname
            print(f'{file:<100} -> {newname}')
            if DO_IT:
                try:
                    os.rename(os.path.join(source, file), os.path.join(source, newname))
                except:
                    print("*** Err")

rename_series()
