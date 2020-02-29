# align_series.py
# Ensure that BD series (part of name before first " - ") are homogeneous
# 2020-02-28    PV

import os, sys
import re
from collections import defaultdict
from typing import Dict, List, Tuple, DefaultDict, Iterable
import json
import re
import unicodedata


REBUILDFILESLIST = False

source = r'W:\TempBD'

def GetFiles(source: str) -> List[str]:
    return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])

if REBUILDFILESLIST:
    print("Reading files...")
    files = GetFiles(source)
    print(f"Wrting {len(files)} in cache files.json")
    with open(r'files.json', 'w') as outfile:
        json.dump(files, outfile, indent=4)
    print("Done.")
    #sys.exit(0)
else:
    with open(r'files.json', 'r') as infile:
        files = json.load(infile)



def lower_noaccent(s: str) -> str:
    # Mn = Mark, Nonspacing = combining latin characters accents
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c)!='Mn')       

print("Grouping files...")
series: DefaultDict[str, set] = defaultdict(set)
nf = 0
for file in files:
    nf += 1
    # if nf>100: break
    basename, ext = os.path.splitext(file)
    segments = basename.split(" - ")
    serie = segments[0]
    serie_lna = lower_noaccent(serie)
    series[serie_lna].add(serie)
# Replace set by list to serialize
# Or check https://stackoverflow.com/questions/8230315/how-to-json-serialize-sets
series2 = {k:list(v) for (k,v) in series.items()}
# with open(r'series.json', 'w') as outfile:
#     json.dump(series2, outfile, indent=4)

print(f'{nf} fichiers')
print(f'{len(series)} séries')



def FindSeriesWithMultipleSpellings():
    print("Series with multiple spellings")
    seriesm: List[List[str]] = []
    with open(r'spellings.txt', mode='w', encoding='utf-8') as out:
        for (k,v) in series.items():
            if len(v)>1:
                seriesm.append(list(v))
                print(f'{k:<100} {len(v)}')
                for spelling in v:
                    out.write(spelling+';')
                out.write('\n')
    with open(r'spellings.json', 'w') as outfile:
        json.dump(seriesm, outfile, indent=4)
    print(f"Written {len(seriesm)} series with 2 or more spellings in spellings.txt and spellings.json")

#FindSeriesWithMultipleSpellings()


def RenameSeriesUsingOfficialSpelling():
    # Load official spellings
    spo = []
    with open(r'spellingsofficiel.json', 'r') as infile:
        spo = json.load(infile)    
    dicspo = {}
    for spelling in spo:
        dicspo[lower_noaccent(spelling)] = spelling

    # Rename series using official spelling
    for file in files:
        basename, ext = os.path.splitext(file)
        segments = basename.split(" - ")
        serie = segments[0]
        serie_lna = lower_noaccent(serie)
        if serie_lna in dicspo.keys():
            if segments[0] != dicspo[serie_lna]:
                segments[0] = dicspo[serie_lna]
                newname = " - ".join(segments)+ext.lower()
                print(f'{file:<100} -> {newname}')
                try:
                    os.rename(os.path.join(source, file), os.path.join(source, newname))
                except:
                    print("*** Err")

#RenameSeriesUsingOfficialSpelling()


def FindSeriesEndingWithNumbers():
    print("Series ending with numbers")
    ENDDIGITS_RE = re.compile(r".*[ 0-9]+")
    with open(r'seriesvalidesavecnum.json', 'r') as infile:
        seriesvalidesavecnum = json.load(infile)
    snum = []
    for (k,_) in series.items():
        if ENDDIGITS_RE.fullmatch(k):
            if not k in seriesvalidesavecnum:
                snum.append(k)
    with open(r'seriesendnum.txt', 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(sorted(snum)))
    print(f'{len(snum)} series written in seriesendnum.txt')

FindSeriesEndingWithNumbers()
