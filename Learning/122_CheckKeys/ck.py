# CheckKeys
# Check that source code does not contains keys or passwords
#
# 2023-02-11    PV

from collections import defaultdict
import os
from common_fs import get_files, extension_part, get_all_files, file_readalltext, file_readalltext_encoding

source = r'C:\Development'

# exts = defaultdict(int)
# for file in get_all_files(source):
#     ext = extension(file).casefold()
#     exts[ext]+=1
# with open(r'c:\temp\ext.txt', 'w') as out:
#     for k,v in sorted(exts.items(), key = lambda x: x[1], reverse=True):
#         out.write(f'{k}\t{v}\n')

encod = defaultdict(int)
keys: dict[str, str] = {}
for file in get_files(r'C:\Utils\Local'):
    keys[file.casefold()] = file_readalltext(os.path.join(r'C:\Utils\Local', file))

def is_source(filefp: str) -> bool:
    ext =  extension_part(filefp).lower()
    return ext in ['.py', '.cs', '.go', '.c', '.cpp', '.java', '.js', '.json', '.ini', '.yaml', '.html', '.xaml']

for filefp in get_all_files(source):
    if is_source(filefp):
        src, enc = file_readalltext_encoding(filefp)
        encod[enc] += 1
        for f,k in keys.items():
            if k in src:
                print('***',f,'found in', filefp)
print()
print(encod)