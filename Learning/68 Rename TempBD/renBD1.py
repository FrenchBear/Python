# renbd1.py
# Rename BD files 1step after download in eMULE
# 2020-02-22    PV

import os, sys
import re
from unicodedata import normalize
from typing import List

source = r'D:\Downloads\eMule\BD1'
outfile = r'c:\temp\names.txt'

#source = r'W:\TempBD'

def GetFiles(source: str) -> List[str]:
    return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])

def Step1(out):
    n = 0
    for file in GetFiles(source):
        basename, ext = os.path.splitext(file)
        newname = ' '+normalize('NFC', basename)+' '
        newname = re.sub('\xa0', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\.', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'_', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'(( +-)|(- +))+', ' - ', newname, flags=re.IGNORECASE)

        # Exceptions to . removan
        newname = re.sub(r'D Gray-Man', 'D.Gray-Man', newname, flags=re.IGNORECASE)
        

        # Remove blocs between [] () {}
        newname = re.sub(r'\([^\)]+\)', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\{[^\}]+\}', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\[[^\]]+\]', ' ', newname, flags=re.IGNORECASE)

        # Renum T##
        def getnum(matchobj):
            return ' '+(matchobj.group(1) if len(matchobj.group(1))==2 else '0'+matchobj.group(1))+' '
        newname = re.sub(r' T(\d?\d) ', getnum, newname, flags=re.IGNORECASE)
        newname = re.sub(r'Tome ', '', newname, flags=re.IGNORECASE)

        # Remove specific strings
        newname = re.sub(r'(BD|Comics|Manga)[ \.-]*FR', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Pressecitron|iBooker|FRENCH|HYBRiD|eBook|WEBRip|BDPACK|STC|REPACK|RESCAN|BROKER|One shot|MagPF|Full Color|Adult Comic', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r' OS | BD | BDX FR | BDX | FR | HD | HQ ', ' ', newname, flags=re.IGNORECASE)
        newname = re.sub(r' !', '!', newname, flags=re.IGNORECASE)
        newname = re.sub(r'\d{4}px', '', newname, flags=re.IGNORECASE)
        newname = re.sub(r'1920|1600', '', newname, flags=re.IGNORECASE)

        # Replace wrong accents
        newname = re.sub(r'ÃÂ©', 'é', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã£Â¨', 'è', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã£Âª', 'ê', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã©', 'é', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¨', 'è', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã´', 'ô', newname, flags=re.IGNORECASE)
        newname = re.sub(r"Ã'", 'ô', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã®', 'î', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¯', 'ï', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ãª', 'ê', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã', 'â', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¢', 'â', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã¤', 'ä', newname, flags=re.IGNORECASE)
        newname = re.sub(r'Ã', 'é', newname, flags=re.IGNORECASE)
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

        if basename!=newname:
            print(f"{basename:<120} |{newname}|")
            out.write(f"{basename:<150} |{newname}|\n")

            try:
                os.rename(os.path.join(source, file), os.path.join(source, newname+ext))
            except:
                out.write("*** Err\n")


with open(outfile, mode='w', encoding='utf-8') as out:
    Step1(out)
