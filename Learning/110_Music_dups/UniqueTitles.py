# UniqueTitles.py
# Get only 1 copy of a title in a tree
#
# 2022-05-26    PV      First version

from collections import Counter
from json import tool
import shutil
import sys
from common_fs import *
from lev import *

def cleanprefix(f: str) -> str:
    f = f[:-4]  # Remove .mp3
    if len(f) > 5 and str.isdigit(f[0]) and str.isdigit(f[1]) and f[2:5] == " - ":  # Remove "nn - " prefix
        f = f[5:]
    return f

def process(source: str, destination: str):
    print('\nProcessing', filepart(destination))
    if not folder_exists(destination):
        os.mkdir(destination)

    files_fp = [f for f in get_all_files(source) if f.lower().endswith('.mp3')]
    print(len(files_fp), 'files found')

    dic: dict[str, list[str]] = {}
    for file in files_fp:
        key = cleanprefix(filepart(file)).lower()
        dic.setdefault(key, []).append(file)
    print(len(dic), 'unique titles')

    # c = Counter()
    # for k, v in dic.items():
    #     c[k] += len(v)
    # print(c.most_common())

    for k, v in dic.items():
        vs = [(file_size(file), file) for file in v]
        sf = sorted(vs, reverse=True)[0]
        f = sf[1]
        tf = os.path.join(destination, f'{len(v)} - '+cleanprefix(filepart(f))+'.mp3')
        #print(f, '->', tf)
        shutil.copy(f, tf)


process(source = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Dave', destination = r'C:\Temp\UniqueTitles\Dave')
process(source = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Michel Sardou - 1967-2010', destination = r'C:\Temp\UniqueTitles\Michel Sardou')
process(source = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Mort Shuman', destination = r'C:\Temp\UniqueTitles\Mort Shuman')
process(source = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Johnny Hallyday - 1959-2019', destination = r'C:\Temp\UniqueTitles\Johnny Hallyday')
process(source = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Tino Rossi', destination = r'C:\Temp\UniqueTitles\Tino Rossi')
process(source = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\ABBA - 1973-1981', destination = r'C:\Temp\UniqueTitles\ABBA')
process(source = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Queen - 1973-2007', destination = r'C:\Temp\UniqueTitles\Queen')
process(source = r'C:\Users\Pierr\OneDrive\MusicOD\A_Trier\A_Trier Préparé\Rika Zaraï', destination = r'C:\Temp\UniqueTitles\Rika Zaraï')
