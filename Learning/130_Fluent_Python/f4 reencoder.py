# Reencode extracts from utf-16 to utf-8

from common_fs import get_all_files, folder_part
import os

for filefp in get_all_files(r'c:\temp\fp2'):
    print(filefp)
    with open(filefp, 'r', encoding='utf-16') as fi:
        s = fi.read()
    newfilefp = filefp.replace(r'\fp2', r'\fp2-utf8').lower()
    os.makedirs(folder_part(newfilefp), exist_ok=True)
    with open(newfilefp, 'w', encoding='utf-8') as fo:
        fo.write(s)
