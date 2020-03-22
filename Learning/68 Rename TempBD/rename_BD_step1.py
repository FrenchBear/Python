# rename_BD_step1.py
# Rename BD files 1st step after download in emule
# 2020-02-22    PV

import os, sys
import re
import unicodedata
import json
from typing import List, TextIO

from common import *


source = r"D:\Downloads\eMule\BD1"
outfile = r'names.txt'

DO_IT = True


with open(r'series_avec_num.json', 'r', encoding='utf8') as infile:
    series_avec_num = json.load(infile)

def Step1(out: TextIO):
    nf = 0
    nr = 0
    for fullpath in get_all_files(source):
        nf += 1
        path, file = os.path.split(fullpath)
        basename, ext = os.path.splitext(file)

        newname = ' '+unicodedata.normalize('NFC', basename).translate(transtab)+' '
        newname = re.sub(r'\.', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'_', ' ', newname, flags=re.IGNORECASE)

        # Exceptions to . removal
        newname = re.sub(r'D Gray[- ]Man', 'D.Gray-Man', newname, flags=re.IGNORECASE)

        # Remove blocs between [] () {}
        newname = re.sub(r'\([^\)]+\)', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\{[^\}]+\}', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\[[^\]]+\]', ' ', newname, flags=re.IGNORECASE)

        # Normalizes -
        newname = re.sub(r'(( +-)|(- +))+', ' - ', newname, flags=re.IGNORECASE)

        # Protect series with num, replace space by _
        segment1 = newname.split(" - ")[0].strip()
        segment1_normalized = normalize_serie(segment1)
        if segment1_normalized in series_avec_num:
            segment1_prot = segment1.replace(' ', '_')
            newname = newname.replace(segment1, segment1_prot)

        # Renum T##
        def getnum(matchobj):
            n = int(matchobj.group(1))
            return f' {n:0>2} '
        newname = re.sub(r'T(\d?\d?\d)', getnum, newname, flags=re.IGNORECASE)
        newname = re.sub(r' Tome ', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Tomo ', '', newname, flags=re.IGNORECASE)

        # Remove specific strings
        newname = re.sub(r'(BD|Comics|Manga)[ \.-]*FR', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Pressecitron|iBooker|FRENCH|\bHYBRiD\b|eBook|WEBRip|BDPACK|STC|REPACK|RESCAN|BROKER|One shot|MagPF|Full Color|Adult Comic|Bdstudio|by 5Cobres|By Le mulot|caso DKFR|DKFR', '', newname, flags=re.IGNORECASE)
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

        # Rename THS
        newname = re.sub(r' THS ', ' HS ', newname, flags=re.IGNORECASE)
        def getnum5(matchobj):
            return ' HS '+matchobj.group(1)+' '
        newname = re.sub(r' HS(\d\d) ', getnum5, newname, flags=re.IGNORECASE)

        # Remove n° prefix
        def getnum4(matchobj):
            return ' - '+matchobj.group(1)+' '
        newname = re.sub(r' n°?(\d\d+) ', getnum4, newname, flags=re.IGNORECASE)

        # Remove non-significant zeros for numeric sequences of 3 or more
        def getnum3(matchobj):
            return ' '+matchobj.group(1)+' '
        newname = re.sub(r' 0+(\d\d+) ', getnum3, newname, flags=re.IGNORECASE)

        # Series ending with numbers
        if (p := newname.find(" - "))<0:
            p = len(newname)
        nnt = newname[:p]
        if ma := re.fullmatch(r"(.*) (\d?\d\d)( *)", newname[:p]):
            newname = ma.group(1)+' - '+ma.group(2)+ma.group(3)+newname[p:]

        # Final clean-up
        newname = re.sub('_', ' ', newname)     # Unprotect series with num
        newname = re.sub(r'[  \-]*$', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r'^[  \-]*', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r' +', ' ', newname, flags=re.IGNORECASE)
        newname = clean_file_name(newname)

        # Each segment starts with uppercase
        segments = newname.split(" - ")
        def fix_case(s: str) -> str:
            if len(s)>0 and not s in ['dBD']:
                return s[0].upper()+s[1:]
            else:
                return s
        newname = " - ".join(fix_case(segment) for segment in segments)

        # Special rename patterns
        if ma:=re.fullmatch(r"(.*), (\d\d) FRN( |,)+", newname, re.IGNORECASE):         # "Agharta, 05 FRN , ,"
            newname = ma.group(1)+' - '+ma.group(2)
        if ma:=re.fullmatch(r"(.*), (\d\d) (.+), FRN( |,)+", newname, re.IGNORECASE):   # "Asphodele, 03 L'ange noir, FRN , ,"
            newname = ma.group(1)+' - '+ma.group(2)+' - '+ma.group(3)
        if ma:=re.fullmatch(r"(.*) (- )?µ.*", newname):       # "Agharta, 05 FRN , ,"
            newname = ma.group(1)
        if ma:=re.fullmatch(r"(.*\d\d) & (\d\d.*)", newname, re.IGNORECASE):
            newname = ma.group(1)+'-'+ma.group(2)
        if ma:=re.fullmatch(r"(.*) \)", newname):
            newname = "BDA - "+ma.group(1)

        if file!=newname+ext.lower():
            print(f"{file:<120} |{newname}{ext.lower()}|")
            out.write(f"{file:<150} |{newname}{ext.lower()}|\n")
            nr += 1
            if DO_IT:
                try:
                    os.rename(os.path.join(path, file), get_safe_name(os.path.join(path, newname+ext.lower())))
                except:
                    out.write("*** Err\n")
    if not DO_IT:
        print("No action: ", end='')
    print(f'{nf} fichiers analysés, {nr} renommé(s)')


with open(outfile, mode='w', encoding='utf-8') as out:
    Step1(out)
