# rename_litt.py
# Various rename operations on ebooks folders and files
#
# 2022-07-05    PV

from collections import defaultdict
from collections import Counter
from ntpath import join
from posixpath import split
from typing import Tuple, Counter
from common_fs import *
import unicodedata
import shutil

doit = False

# rename folders from "lastname, firstname" into "firstname lastname"
def reorder_folders():
    root = f'D:\Littérature francaise'
    for folder in list(get_folders(root)):
        ts = folder.split(', ')
        if len(ts) == 2:
            nn = ts[1]+' '+ts[0]
            print(folder, '->', nn)
            if doit:
                shutil.move(os.path.join(root, folder), os.path.join(root, nn))

#reorder_folders()

def reorder_files():
    root = f'D:\Littérature francaise'
    np=0
    for filefp in get_all_files(root):
        folder, file = os.path.split(filefp)
        base, ext = os.path.splitext(file)

        def fixname(s:str):
            ts = s.split(', ')
            if len(ts)==1:
                ts = s.split(',')
            if len(ts) == 2:
                return (ts[1]+' '+ts[0]).strip().replace('  ',' ')
            else:
                return s

        ts = base.split(' - ')
        if len(ts) != 2:
            print(filefp)
            np+=1
        else:
            nn = ts[0]+' - '+fixname(ts[1])+ext
            print(file,'->',nn)
            if doit:
                shutil.move(os.path.join(folder, file), os.path.join(folder, nn))
    print('\n',np,' problems')

#reorder_files()

def find_dups():
    d: dict[str, str] = {}
    root = f'D:\Littérature francaise'
    nd = 0
    for filefp in get_all_files(root):
        folder, file = os.path.split(filefp)
        base, ext = os.path.splitext(file)

        if file.lower() in d:
            print(file)
            print('  '+folder)
            print('  '+d[file.lower()])
            print()
            nd += 1

            def add_suffix(fo: str, fi: str, su: str):
                ts = fi.split(' - ')
                ts[0] += ' '+su
                nn = ' - '.join(ts)
                ofp = os.path.join(fo, fi)
                nfp = os.path.join(fo, nn)
                print(ofp, '->', nfp)
                if doit:
                    if file_exists(ofp):
                        shutil.move(ofp, nfp)
            add_suffix(folder, file, 'v1')
            add_suffix(d[file.lower()], file, 'v2')
        else:
            d[file.lower()] = folder
    print(nd, 'dups')

#find_dups()

def first_maj():
    root = f'D:\Littérature francaise'
    for filefp in get_all_files(root):
        folder, file = os.path.split(filefp)
        base, ext = os.path.splitext(file)

        if (not 'A'<=file[0]<='Z') or file[0:2]=='A ':
            nn = file[0].upper()+file[1:]
            if nn[0:2]=='A ':
                nn='À'+nn[1:]
            print(file,'->',nn)
            if doit:
                shutil.move(os.path.join(folder, file), os.path.join(folder, nn))

# first_maj()

