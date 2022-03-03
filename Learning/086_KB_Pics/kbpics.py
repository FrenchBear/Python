# kbpics.py
# Compte les fichiers images de KB par extension
# 2021-06-18    PV

from collections import Counter
from common_fs import *
import os

def process_folder(root: str):
    path, folder = os.path.split(root)
    folder2 = ''.join(chr(ord(c)^0x15) for c in folder)
    root = os.path.join(path, folder2)
    root = root.replace("{KB_HOME}", os.environ['KB_HOME'])
    dc: Counter = Counter()     
    for f in get_all_files(root):
        _, ext = os.path.splitext(f)
        dc.update([ext])
    _, folder = os.path.split(root)
    s = ' '.join([f'{k[1:]}:{v}' for k,v in dc.most_common()])
    print(folder+':', s)

process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Wpfa5Zs')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Qzrf')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\F~|{f5Vzef5X|y|a')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Azzyf')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Wptgf5t{q5wptgf')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Wptg5Ataf')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Qgtb|{rf')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\SS')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Xz{fapgf')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Za}pg')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Fpm')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\@gz')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Gpq5]ptqf')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Tgxe|af')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Wgppq|{r')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\R|s')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\_`f')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\WQFX5Ypta}pg')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Wptgf')
process_folder(r'{KB_HOME}\GoogleDrive\PicturesGDKB\Qzb{yztqf')
