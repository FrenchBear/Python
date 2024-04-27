# Rename Popular Science
#
# 2024-04-27    PV

import os
import re

from common_fs import get_all_files, file_part

source = r"C:\Users\Pierr\Downloads\A_Trier\!Large\Popular Science"

re1 = re.compile(r"Popular Science (\d\d\d\d) (\d\d)[^\.]*\.pdf")
re2 = re.compile(r"(\d\d)\. Popular Science - ([^ ]+) (\d\d\d\d) *\.pdf")

def monthmatch(mn: int, ms: str) -> bool:
    match ms:
        case "January": 
            return mn == 1
        case "February": 
            return mn == 2
        case "March": 
            return mn == 3
        case "April": 
            return mn == 4
        case "May": 
            return mn == 5
        case "June": 
            return mn == 6
        case "July": 
            return mn == 7
        case "August": 
            return mn == 8
        case "September": 
            return mn == 9
        case "October": 
            return mn == 10
        case "November": 
            return mn == 11
        case "December": 
            return mn == 12
        case _: 
            return False

listfiles = get_all_files(source)
for filefp in listfiles:
    folder, file = os.path.split(filefp)

    year = int(file_part(folder))
    if ma := re.fullmatch(re1, file):
        y = int(ma.group(1))
        m = int(ma.group(2))
        assert y == year
        assert 1 <= m <= 12
    elif ma := re.fullmatch(re2, file):
        m = int(ma.group(1))
        ms = ma.group(2)
        y = int(ma.group(3))
        assert y == year
        assert 1 <= m <= 12
        assert monthmatch(m, ms)
    else:
        print(filefp)
        breakpoint()
        pass

    newname = f"Popular Science - {y}-{m:02d}.pdf"
    print(newname)
    os.rename(filefp, os.path.join(source, newname))
