# swapbooks.py
# Backups books that exists in W:\livres and C:\Temp\PDF tree from W:\Livres to  W:\livres.old then moves books from C:\Temp\PDF to W:\livres
# 2021-01-09    PV

from common_fs import get_all_files
import os
import shutil

wroot = r"W:\livres"
croot = r"C:\Temp\PDF"
broot = r"W:\Livres_Large"

clist = get_all_files(croot)
for cfile in clist:
    print(cfile)
    wfile = cfile.replace(croot, wroot)
    if not os.path.exists(wfile):
        breakpoint()
    bfile = cfile.replace(croot, broot)
    bfolder = os.path.dirname(bfile)
    if not os.path.exists(bfolder):
        os.makedirs(bfolder)
    shutil.move(wfile, bfile)
    shutil.copy(cfile, wfile)
