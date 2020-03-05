import rarfile
import os
from typing import List
import unicodedata


ne chercher que les formats d'image et PDF
Signater les archives contenant des PDF
Ignorer les dossiers __MACOSX

#source = r'W:\TempBD\cbr'
source = r'D:\Downloads\eMule\BD1'

# Juste les fichiers d'un dossier, juste les noms
def get_files(source: str) -> List[str]:
    return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])

# Chemin complet de tous les fichiers à partir d'une racine
def get_all_files(path: str) -> Iterable[str]:
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)


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
    return s==clean_file_name(s)
    # cr = [c for c in s if c not in " ,.%!#&@$()[]¿°·½-+'" and unicodedata.category(c) not in ['Ll', 'Lu', 'Nd']]
    # if len(cr)>0:
    #     print(s)
    #     for c in cr:
    #         print(c, unicodedata.category(c), end=' ')
    #     print()
    #     # breakpoint()
    #     # pass


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

#analyse_archives()
