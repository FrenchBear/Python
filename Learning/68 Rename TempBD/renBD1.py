# renbd1.py
# Rename BD files 1step after download in emule
# 2020-02-22    PV

import os, sys
import re
import unicodedata
from typing import List

source = r'D:\Downloads\eMule\BD1'
outfile = r'c:\temp\names.txt'

#source = r'W:\TempBD'

def get_files(source: str) -> List[str]:
    return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])

def clean_file_name(s: str) -> str:
    res = ''.join(c for c in s if c in " ,.%!#&@$()[]¿°·½-+'" or unicodedata.category(c) in ['Ll', 'Lu', 'Nd'])
    return res


def Step1(out):
    n = 0
    for file in get_files(source):
        basename, ext = os.path.splitext(file)
        newname = ' '+unicodedata.normalize('NFC', basename)+' '
        newname = re.sub('\xa0', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\.', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'–', '-', newname, flags=re.IGNORECASE)
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

        # Final clean-up
        newname = re.sub(r'[  \-]*$', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r'^[  \-]*', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r' +', ' ', newname, flags=re.IGNORECASE)
        newname = clean_file_name(newname)

        if file!=newname+ext.lower():
            print(f"{file:<120} |{newname}{ext.lower()}|")
            out.write(f"{file:<150} |{newname}{ext.lower()}|\n")

            try:
                os.rename(os.path.join(source, file), os.path.join(source, newname+ext.lower()))
            except:
                out.write("*** Err\n")


with open(outfile, mode='w', encoding='utf-8') as out:
    Step1(out)
