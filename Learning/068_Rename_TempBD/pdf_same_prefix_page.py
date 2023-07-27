import os
import re
from collections import defaultdict
from common_fs import get_files, file_size
from common_pdf import pdf_numpages

source = r'W:\TempBD\final\Astérix'


dicsp = defaultdict(set)
for file in get_files(source):
    if not file.lower().startswith('thumbs'):
        basename, _ = os.path.splitext(file)
        filefp = os.path.join(source, file)
        pages = pdf_numpages(filefp)
        print(f'{pages:>4}    {file}')
        if 4 <= pages <= 999:
            if ma := re.fullmatch(r"(.*)? - ((\d{2,3})[A-Z]?|Pub|HS|HS \d+|BO|BO \d+)( - .*)?", basename, re.IGNORECASE):
                prefix = ma.group(1).lower()+' - '+ma.group(2).lower()+f'|{pages}'
                dicsp[prefix].add(filefp)
for k, v in dicsp.items():
    if len(v) > 1:
        li = list(v)
        li.sort(key=lambda file: file_size(file))
        print(k)
        for f in li:
            print(f'  {file_size(f):>6} {f}')
