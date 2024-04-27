# Rename BBC Science Focus
#
# 2024-04-27    PV

import os
import re

from common_fs import get_all_files, file_part

source = r"C:\Users\Pierr\Downloads\A_Trier\!Large\BBC Science Focus"

reg = re.compile(r"Science Focus (\d\d\d\d) №(\d\d\d) ([^\.]+)\.pdf")

def monthnumstr(ms: str) -> str:
    match ms:
        case "January": 
            return "01"
        case "February": 
            return "02"
        case "March": 
            return "03"
        case "April": 
            return "04"
        case "May": 
            return "05"
        case "June": 
            return "06"
        case "July": 
            return "07"
        case "August": 
            return "08"
        case "September": 
            return "09"
        case "October": 
            return "10"
        case "November": 
            return "11"
        case "December": 
            return "12"
        case "Summer" | "New Year": 
            return ms
        case _: 
            breakpoint()
            pass

listfiles = get_all_files(source)
for filefp in listfiles:
    folder, file = os.path.split(filefp)

    year = int(file_part(folder))
    if ma := re.fullmatch(reg, file):
        y = int(ma.group(1))
        no = int(ma.group(2))
        ms = ma.group(3)
        assert y == year
        mns = monthnumstr(ms)
    else:
        print(filefp)
        breakpoint()
        pass

    newname = f"Science Focus n°{no} - {y}-{mns}.pdf"
    print(newname)
    os.rename(filefp, os.path.join(source, newname))
