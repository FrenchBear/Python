import os, sys, shutil
from collections import defaultdict
import re
from typing import List

from common import *

source = r'W:\TempBD\final'
DO_IT = False


for _, folders, _ in os.walk(source):
    break

folders.sort()
series = defaultdict(int)

with open(r'badseries.txt', 'w', encoding='utf8') as out:
    for folder in folders:
        folderfp = os.path.join(source, folder)
        files = get_files(folderfp)
        ok = True
        for file in files:
            if not file.lower().startswith('thumbs'):
                file_valid = False
                if re.findall(r".* - (\d\d[a-zA0-9]?|Pub|HS|HS \d+|BO)( - .*)?", file):
                    file_valid = True
                else:
                    if re.findall(re.escape(folder)+r"( - .*|\.pdf)", file, flags=re.IGNORECASE):
                        file_valid = True
                if not file_valid:
                    print(f'{folder:<50} {file}')
                    out.write(f'{folder:<50} {file}\n')
                    break
