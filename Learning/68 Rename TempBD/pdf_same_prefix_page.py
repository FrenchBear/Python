import os
import re
from collections import defaultdict
from PyPDF2 import PdfFileReader
from common import *
from common_pdf import *

source = r'W:\TempBD\final\Astérix'


dicsp = defaultdict(set)
for file in get_files(source):
    if not file.lower().startswith('thumbs'):
        basename, _ = os.path.splitext(file)
        filefp = os.path.join(source, file)
        pages = pdf_numpages(filefp)
        print(f'{pages:>4}    {file}')
        if 4<=pages<=999:
            if ma:=re.fullmatch(r"(.*)? - ((\d{2,3})[A-Z]?|Pub|HS|HS \d+|BO|BO \d+)( - .*)?", basename, re.IGNORECASE):
                prefix = ma.group(1).lower()+' - '+ma.group(2).lower()+f'|{pages}'
                dicsp[prefix].add(filefp)
for k, v in dicsp.items():
    if len(v)>1:
        l = list(v)
        l.sort(key = lambda file: file_length(file))
        print(k)
        for f in l:
            print(f'  {file_length(f):>6} {f}')
