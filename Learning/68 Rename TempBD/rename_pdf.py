
import os, sys, shutil
import re
from typing import List
from common import *

source = r"W:\TempBD\final"
DO_IT = True

NUM_DOT_TITLE = re.compile("(\d+)\. ?(.+)")
NUM_DASH_TITLE = re.compile("(\d+) - (.+)")
HSNUM_DOT_TITLE = re.compile("HS(\d+)\. (.+)")

def rename(folderfp: str, oldname: str, newname: str):
    print(f'{oldname} -> {newname}')
    if DO_IT:
        os.rename(os.path.join(folderfp, oldname), os.path.join(folderfp, newname))

def format_num(num: str) -> str:
    return f"{int(num):02}"

def rename_file(folderfp: str, serie: str, file: str):
    basename, ext = os.path.splitext(file)
    if ma:=NUM_DOT_TITLE.fullmatch(basename):
        newname = serie+' - '+format_num(ma.group(1))+' - '+ma.group(2)+ext
        rename(folderfp, file, newname)
        return
    if ma:=NUM_DASH_TITLE.fullmatch(basename):
        if serie!='666':
            newname = serie+' - '+format_num(ma.group(1))+' - '+ma.group(2)+ext
            rename(folderfp, file, newname)
            return
    if ma:=HSNUM_DOT_TITLE.fullmatch(basename):
        newname = serie+' - HS '+format_num(ma.group(1))+' - '+ma.group(2)+ext
        rename(folderfp, file, newname)
        return
    if ma:=re.fullmatch(re.escape(serie)+' (\d+)\. (.+)', basename, flags=re.IGNORECASE):
        newname = serie+' - '+format_num(ma.group(1))+' - '+ma.group(2)+ext
        rename(folderfp, file, newname)
        return
    if ma:=re.fullmatch(re.escape(serie)+' (Vol(ume)? )?(\d+)', basename, flags=re.IGNORECASE):
        newname = serie+' - '+format_num(ma.group(3))+ext
        rename(folderfp, file, newname)
        return


for folder in get_folders(source):
    folderfp = os.path.join(source, folder)
    for file in get_files(folderfp):
        series_segments = folder.split(" - ")
        rename_file(folderfp, series_segments[0], file)