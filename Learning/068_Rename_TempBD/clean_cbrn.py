import os
import re
from collections import Counter
from common_fs import get_all_files

source = r'W:\TempBD\archives'
DO_IT = True

keep = ['.jpg', '.jpeg', '.png', '.gif', '.cbr', '.cbz', '.rar', '.zip', '.bmp', '.tif', '.epub', '.pdf', '.webp']
keepcounter: Counter[str] = Counter()
delcounter: Counter[str] = Counter()

with open(r'deleted.txt', mode='w', encoding='utf-8') as out:
    for i, fullpath in enumerate(get_all_files(source)):
        if i % 1000 == 0:
            print('.', end='')
        _, ext = os.path.splitext(fullpath)
        ext = ext.lower()
        if ext in keep or re.fullmatch(r'\.r\d{2,3}', ext):
            keepcounter.update([ext])
            if ext == '.epub':
                print(fullpath)
        else:
            #print(f'del "{fullpath}"')
            out.write(fullpath+'\n')
            delcounter.update([ext])
            if DO_IT:
                os.remove(fullpath)
print()
print('kept files:', keepcounter.most_common())
print()
print('deleted files', delcounter.most_common())
