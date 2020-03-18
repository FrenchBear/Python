import os, sys
from collections import defaultdict
import re
from typing import List, DefaultDict

from common import *


source = r'W:\TempBD\final'
extra_sources = [r'W:\BD\Classique', r'W:\BD\Adulte', r'W:\BD\Ancien', r'W:\BD\Extra', r'W:\BD\Comics']


folders: List[str]
_1, folders, _2 = next(os.walk(source))
folders.sort()

min_num: int
max_num: int
nums: set

def process_folder(folderfp: str):
    global min_num, max_num, nums
    files = get_files(folderfp)
    for file in files:
        basename, _ = os.path.splitext(file)
        if basename.lower().startswith('thumbs'):
            # try:
            #     os.remove(os.path.join(folderfp, file))
            # except:
                pass
        else:
            if ma:=re.fullmatch(r".*? - ((\d\d+)[a-zA0-9]?|Pub|HS|HS \d+|BO)( - .*)?", basename):
                try:
                    n = int(ma.group(2))
                    min_num = min(min_num, n)
                    max_num = max(max_num, n)
                    nums.add(n)
                except:
                    pass

#with open(r'badseries.txt', 'w', encoding='utf8') as out1:
with open(r'missing_in_series.txt', 'w', encoding='utf8') as out2:
    for folder in folders:
        min_num = 999
        max_num = -1
        nums = set()
        folderfp = os.path.join(source, folder)
        process_folder(folderfp)
        for extra_source in extra_sources:
            extra_folderfp = os.path.join(extra_source, folder)
            if os.path.exists(extra_folderfp):
                process_folder(extra_folderfp)
            else:
                extra_folderfp = os.path.join(extra_source, folder+' ꜰ')
                if os.path.exists(extra_folderfp):
                    process_folder(extra_folderfp)

        if min_num<=2 and max_num-min_num >= 3 and max_num-min_num <= len(nums) < max_num-min_num+1:
            print(folder)
            out2.write(f'{folder:<50} ')
            for n in range(min_num, max_num+1):
                if not n in nums:
                    out2.write(f'{n:>02} ')
            out2.write(f'     {min_num:>02}..{max_num:>02}\n')
