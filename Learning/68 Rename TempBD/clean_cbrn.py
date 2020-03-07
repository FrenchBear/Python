
import os, sys
import re
import unicodedata
import json
from typing import List

from common import *

source = r'W:\TempBD\archives\cbrn'
keep = ['.jpg', '.jpeg', '.png', '.gif', '.jpe', '.cbr', '.cbz', '.rar', '.zip', '.bmp', '.tif', '.epub']

for fullpath in get_all_files(source):
    _, ext = os.path.splitext(fullpath)
    if not ext.lower() in keep:
        print(f'del "{fullpath}"')
        os.remove(fullpath)
