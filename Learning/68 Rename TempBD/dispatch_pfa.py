import os
import re
from typing import List
from common import *

source = r'W:\TempBD\archives\cbr2\ElviFrance - Terrificolor'

"""
NUM = re.compile(r"(\d+)\.jpg", re.IGNORECASE)

folders = get_folders(source)
for file in get_files(source):
    if ma:=NUM.fullmatch(file):
        for folder in folders:
            fs = f'{int(ma.group(1)):>02} '
            if folder.startswith(fs):
                print(file, ' -> ', folder)
                filefp = os.path.join(source, file)
                dest = os.path.join(source, folder, file)
                os.rename(filefp, dest)
                break

"""

NUM = re.compile(r"(\d+)-(\d+) (.*)\.jpg", re.IGNORECASE)

for file in get_files(source):
    if ma:=NUM.fullmatch(file):
        folder = f'{int(ma.group(1)):>02}'+' - '+ma.group(3)
        folderfp = os.path.join(source, folder)
        if not os.path.exists(folderfp):
            os.mkdir(folderfp)
        filefp = os.path.join(source, file)
        dest = os.path.join(folderfp, file)
        os.rename(filefp, dest)
        print(folder, '    ', file)
