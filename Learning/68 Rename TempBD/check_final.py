import os, sys
from collections import defaultdict
import re
from typing import List

from common import *


source = r'W:\TempBD\final'

DO_IT = False


# for _1, folders, _2 in os.walk(source):
#     break
folders: List[str]
_1, folders, _2 = next(os.walk(source))
folders.sort()

with open(r'badseries.txt', 'w', encoding='utf8') as out1:
    with open(r'missing_in_series.txt', 'w', encoding='utf8') as out2:
        for folder in folders:
            folderfp = os.path.join(source, folder)
            files = get_files(folderfp)
            bad_serie_out = False
            min_num = 999
            max_num = -1
            nums = set()
            for file in files:
                if not file.lower().startswith('thumbs'):
                    file_valid = False
                    if ma:=re.fullmatch(r".* - (\d\d[a-zA0-9]?|Pub|HS|HS \d+|BO)( - .*)?", file):
                        file_valid = True
                        try:
                            n = int(ma.group(1))
                            min_num = min(min_num, n)
                            max_num = max(max_num, n)
                            nums.add(n)
                        except:
                            pass
                    else:
                        if re.findall(re.escape(folder)+r"( - .*|\.pdf)", file, flags=re.IGNORECASE):
                            file_valid = True
                    if not file_valid and not bad_serie_out:
                        bad_serie_out = True
                        print(f'{folder:<50} {file}')
                        out1.write(f'{folder:<50} {file}\n')
            if max_num-min_num >= 3 and len(nums) < max_num-min_num+1:
                out2.write(f'{folder:<50} ')
                for n in range(min_num, max_num+1):
                    if not n in nums:
                        out2.write(f'{n} ')
                out2.write('\n')
