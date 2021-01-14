# renpat1.py
# reformat book names such as
# 01 castellia memotech plus electrotechnique.pdf
# 2021-01-14    PV

from vlib import *
from typing import Dict
import os, shutil

source = r'D:\Downloads\A_Trier\!A_Trier_Livres\Pat1'

for file in list(get_files(source)):
    basename, ext = os.path.splitext(file)
    ts = basename.split(' ')
    editeur = ts[1]
    newname = ' '.join(ts[2:]) + ' () - [' + editeur.title() + '] - X.pdf'
    print(newname)
    os.rename(os.path.join(source, file), os.path.join(source, newname))