# FindDups.py
# Find almost-duplicates in music files
#
# 2022-05-25    PV      First version

from common_fs import get_all_files, file_part
from lev import levenshtein

root = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Queen - 1973-2007'


def cleanprefix(f: str) -> str:
    f = f[:-4]  # Remove .mp3
    if len(f) > 5 and str.isdigit(f[0]) and str.isdigit(f[1]) and f[2:5] == " - ":  # Remove "nn - " prefix
        f = f[5:]
    return f

# s = '08 - Michel Sardou - Je vous ai bien eus.mp3'
# t = cleanprefix(s)

files_fp = [f for f in get_all_files(root) if f.lower().endswith('.mp3')]
print(len(files_fp),'files found')
files = [cleanprefix(file_part(f)) for f in files_fp]
print('Start searching for almost duplicates')
for i in range(len(files)):
    fi = files[i]
    for j in range(i+1, len(files)):
        fj = files[j]
        if abs(len(fi)-len(fj)) <= 1:
            if levenshtein(fi, fj) == 1:
                print(files[i])
                print(files[j])
                print()
print('Done.')
