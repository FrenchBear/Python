# all_smaller.py
# Find folders in QFinal with files all smaller than existing one
#
# 2024-02-12    PV

import os
import re
import shutil
from common_fs import get_files, get_folders, file_size, folder_exists

NUMBER = re.compile(r'\D+(\d{2,3}[ABCDTabcdt]?)( |\.).*')


def check_folder(existing: str, qfinal: str) -> bool:
    exist_dic: dict[str, int] = {}
    for file in get_files(existing):
        ma = NUMBER.fullmatch(file)
        if not ma:
            continue
        num = ma.group(1).lower()
        if num in exist_dic:
            return False
        exist_dic[num] = file_size(os.path.join(existing, file))

    for file in get_files(qfinal):
        ma = NUMBER.fullmatch(file)
        if not ma:
            return False     # If not numbered, must check manually
        num = ma.group(1).lower()
        if num not in exist_dic:
            return False     # New issue?
        if file_size(os.path.join(qfinal, file))>1.05*exist_dic[num]:
            return False     # Larger file in QFinal
        
    return True

for folder in get_folders(r'W:\BD2\QFinal'):
    if folder=="Le déclic": breakpoint()
    if folder_exists(os.path.join(r'W:\BD\Extra', folder)):
        existing = os.path.join(r'W:\BD\Extra', folder)
    elif folder_exists(os.path.join(r'W:\BD\Classique', folder)):
        existing = os.path.join(r'W:\BD\Classique', folder)
    elif folder_exists(os.path.join(r'W:\BD\Ancien', folder)):
        existing = os.path.join(r'W:\BD\Ancien', folder)
    elif folder_exists(os.path.join(r'W:\BD\Adulte', folder)):
        existing = os.path.join(r'W:\BD\Adulte', folder)
    else:
        continue

    qf = os.path.join(r'W:\BD2\QFinal', folder)
    if check_folder(existing, qf):
        shutil.move(qf, r'W:\BD2\QFinal.Smaller')

