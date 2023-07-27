# renpat1.py
# reformat book names such as
# 01 castellia memotech plus electrotechnique.pdf
#
# 2021-01-14    PV
# 2021-05-13    PV      Filtre .pdf

from common_fs import get_files
import os
import re

source = r"D:\Downloads\A_Trier\!A_Trier"
doit = False

ED = re.compile(r" (\d+)ed$")


def added(s: str) -> str:
    ma = ED.search(s)
    if ma:
        s = s[: -len(ma.group(0))] + " (" + ma.group(1) + "è ed, X)"
    else:
        s = s + " ()"
    return s


for file in list(get_files(source)):
    if file.lower().endswith(".pdf"):
        basename, ext = os.path.splitext(file)
        ts = basename.split(" ")
        editeur = ts[1]
        newname = added(" ".join(ts[2:])) + " - [" + editeur.title() + "] - X.pdf"
        newname = newname[0].upper() + newname[1:]
        print("-> " + newname)
        if doit:
            os.rename(os.path.join(source, file), os.path.join(source, newname))