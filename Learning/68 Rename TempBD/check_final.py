import os, sys, shutil
from collections import defaultdict
import re
from typing import List

from common import *

source = r'W:\TempBD\final'
DO_IT = False

for _, folders, _ in os.walk(source):
    break

series = defaultdict(int)

for folder in folders:
    folderfp = os.path.join(source, folder)
    files = get_files(folderfp)
    ok = True
    for file in files:
        if re.findall(".* - \d\d[a-zA0-9]? - .*", file):
            ok = False
            break
    if not ok:
        print(folder)
