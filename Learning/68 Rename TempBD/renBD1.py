# renbd1.py
# Rename BD files 1step after download in emule
# 2020-02-22    PV

import os, sys
import re
import unicodedata
import json
from typing import List

from common import *


DO_IT = True
source = r"D:\Downloads\eMule\BD1"
source = r"W:\TempBD\final.BDA"
outfile = r'c:\temp\names.txt'

#source = r'W:\TempBD'

with open(r'seriesvalidesavecnum.json', 'r', encoding='utf8') as infile:
    seriesvalidesavecnum = json.load(infile)

def Step1(out):
    nf = 0
    nr = 0
    for fullpath in get_all_files(source):
        nf += 1
        path, file = os.path.split(fullpath)
        basename, ext = os.path.splitext(file)

        newname = ' '+unicodedata.normalize('NFC', basename).translate(transtab)+' '
        newname = re.sub(r'\.', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'_', ' ', newname, flags=re.IGNORECASE)

        # Exceptions to . removan
        newname = re.sub(r'D Gray[- ]Man', 'D.Gray-Man', newname, flags=re.IGNORECASE)

        # Remove blocs between [] () {}
        newname = re.sub(r'\([^\)]+\)', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\{[^\}]+\}', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\[[^\]]+\]', ' ', newname, flags=re.IGNORECASE)

        # Normalizes -
        newname = re.sub(r'(( +-)|(- +))+', ' - ', newname, flags=re.IGNORECASE)

        # Renum T##
        def getnum(matchobj):
            n = int(matchobj.group(1))
            return f' {n:0>2} '
        newname = re.sub(r'T(\d?\d?\d)', getnum, newname, flags=re.IGNORECASE)
        newname = re.sub(r'Tome ', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Tomo ', '', newname, flags=re.IGNORECASE)

        # Remove specific strings
        newname = re.sub(r'(BD|Comics|Manga)[ \.-]*FR', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Pressecitron|iBooker|FRENCH|HYBRiD|eBook|WEBRip|BDPACK|STC|REPACK|RESCAN|BROKER|One shot|MagPF|Full Color|Adult Comic|Bdstudio|by 5Cobres|caso DKFR|DKFR', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r' OS | BDX FR | BDX | FR | HD | HQ | Pack ', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r' !', '!', newname, flags=re.IGNORECASE)
        newname = re.sub(r' Int ', ' Intégrale ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\d{4}px', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r'1920|1600', '', newname, flags=re.IGNORECASE)

        # Replace wrong accents
        newname = re.sub(r'ÃÂ©', 'é', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã£Â¨', 'è', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã£Âª', 'ê', newname, flags=re.IGNORECASE)
        newname = re.sub(r'ÃÂ«', 'ë', newname, flags=re.IGNORECASE)
        newname = re.sub(r'ÃÂ´', 'ô', newname, flags=re.IGNORECASE)
        newname = re.sub(r'ÃÂª', 'ê', newname, flags=re.IGNORECASE)
        newname = re.sub(r'ÃÂ', 'à', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¹', 'ù', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã»', 'û', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã©', 'é', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¨', 'è', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã´', 'ô', newname, flags=re.IGNORECASE)
        newname = re.sub(r"Ã'", 'ô', newname, flags=re.IGNORECASE)
        newname = re.sub(r"Ã¶", 'ö', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã®', 'î', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã«', 'ë', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¯', 'ï', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ãª', 'ê', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã', 'â', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã', 'à', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¢', 'â', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¤', 'ä', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã', 'é', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã§', 'ç', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã ', 'à ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'â', "'", newname, flags=re.IGNORECASE)
        newname = re.sub(r'â', "'", newname, flags=re.IGNORECASE)
        newname = re.sub(r'Å', 'oe', newname, flags=re.IGNORECASE)
        newname = re.sub(r'œ', 'oe', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Â°', '°', newname, flags=re.IGNORECASE)

        # Renum range
        def getnum2(matchobj):
            return matchobj.group(1)+'-'+matchobj.group(2)
        newname = re.sub(r'(\d) *[àaÃ] *(\d)', getnum2, newname, flags=re.IGNORECASE)

        # Replace numeric sequences
        newname = re.sub(r'^ *\d{2} \d{2} \d{4}', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r'^ *\d{2}[- ]\d{4}', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r'^ *\d{6}', '', newname, flags=re.IGNORECASE)

        # Series ending with numbers
        if (p := newname.find(" - "))<0:
            p = len(newname)
        nnt = newname[:p]
        if ma := re.fullmatch(r"(.*) (\d?\d\d)( *)", newname[:p]):
            newname = ma.group(1)+' - '+ma.group(2)+ma.group(3)+newname[p:]

        # Final clean-up
        newname = re.sub(r'[  \-]*$', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r'^[  \-]*', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r' +', ' ', newname, flags=re.IGNORECASE)
        newname = clean_file_name(newname)

        if file!=newname+ext.lower():
            print(f"{file:<120} |{newname}{ext.lower()}|")
            out.write(f"{file:<150} |{newname}{ext.lower()}|\n")
            nr += 1
            if DO_IT:
                try:
                    os.rename(os.path.join(path, file), os.path.join(path, newname+ext.lower()))
                except:
                    out.write("*** Err\n")
    if not DO_IT:
        print("No action: ", end='')
    print(f'{nf} fichiers analysés, {nr} renommé(s)')


with open(outfile, mode='w', encoding='utf-8') as out:
    Step1(out)
