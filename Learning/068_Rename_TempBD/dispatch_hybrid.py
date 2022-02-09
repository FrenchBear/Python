import os
import re
from typing import List
from common import *


source = r"W:\TempBD\archives\hybrid"
DO_IT = True

PICTURE_EXT = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.webp']
ARCHIVE_EXT = ['.cbr', '.cbz', '.rar', '.zip']
PDF_EXT = ['.epub', '.pdf']
IGNORE_EXT = ['.db']

nArc = nPdf = 0
for sourcefilefp in get_all_files(source):
    _, ext = os.path.splitext(sourcefilefp)
    ext = ext.lower()
    targetroot = ''
    if ext in ARCHIVE_EXT:
        targetroot = source+'.cbr'
        nArc += 1
    if ext in PDF_EXT:
        targetroot = source+'.pdf'
        nPdf += 1
    if ext in IGNORE_EXT:
        continue
    if targetroot=='':
        breakpoint()
    targetfilefp = targetroot + sourcefilefp[len(source):]
    if DO_IT:
        targetfolderfp, _ = os.path.split(targetfilefp)
        if not os.path.exists(targetfolderfp):
            os.makedirs(targetfolderfp)
        os.rename(sourcefilefp, targetfilefp)
        try:
            parentsourcefp, _ = os.path.split(sourcefilefp)
            os.rmdir(parentsourcefp)
        except:
            pass

print(f'{nArc} archives déplacées, {nPdf} pdf déplacés')
