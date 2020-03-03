import rarfile
import os
from typing import List
import unicodedata

def get_files(source: str) -> List[str]:
    return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])


def analyze_one_archive(archive: str) -> int:
    folders = set()
    rf = rarfile.RarFile(archive)
    for f in rf.infolist():
        if f.file_size > 0:
            fol, fil = os.path.split(f.filename)
            folders.add(fol)
    return len(folders)

def clean_file_name(s: str) -> str:
    res = ''.join(c for c in s if c in " ,.%!#&@$()[]¿°·½-+'" or unicodedata.category(c) in ['Ll', 'Lu', 'Nd'])
    return res

def is_clean_file(s: str) -> bool:
    cr = [c for c in s if c not in " ,.%!#&@$()[]¿°·½-+'" and unicodedata.category(c) not in ['Ll', 'Lu', 'Nd']]
    if len(cr)>0:
        print(s)
        for c in cr:
            print(c, unicodedata.category(c), end=' ')
        print()
        # breakpoint()
        # pass


source = r'W:\TempBD\cbr'
#source = r'C:\temp'

def clean_files():
    with open(r'analyze.txt', mode='w', encoding='utf-8') as out:
        for archive in get_files(source):
            _, ext = os.path.splitext(archive)
            if ext.lower() in ['.cbr', '.rar']:
                clean_name = clean_file_name(archive)
                if archive!=clean_name:
                    # print(f'{archive:<100}', end='')
                    # fullpath = os.path.join(source, archive)
                    # cnt = analyze_one_archive(fullpath)
                    # print(cnt)
                    cnt = 0
                    out.write(f'{cnt};{archive}\n')
                    print(f'{archive:<100} -> {clean_name}')
                    try:
                        os.rename(os.path.join(source, archive), os.path.join(source, clean_name))
                    except:
                        print("*** Err")

def analyse_archives():
    with open(r'analyze.txt', mode='w', encoding='utf-8') as out:
        for archive in get_files(source):
            _, ext = os.path.splitext(archive)
            if ext.lower() in ['.cbr', '.rar']:
                    print(f'{archive:<100}', end='')
                    fullpath = os.path.join(source, archive)
                    try:
                        cnt = analyze_one_archive(fullpath)
                    except:
                        cnt = -1
                    print(cnt)
                    out.write(f'{cnt};{archive}\n')
                    out.flush()

analyse_archives()
