# Analyse le contenu de fichiers rar
# 2020-03-05    PV

import os
import rarfile
import unicodedata
from typing import List, Tuple, TextIO

from common import *


"""
ne chercher que les formats d'image et PDF
Signater les archives contenant des PDF
Ignorer les dossiers __MACOSX
"""


DO_IT = False
source = r'W:\TempBD'


def analyze_one_archive(archive: str) -> Tuple[int, int, int, int, int, int, str]:
    folders = set()
    other = set()
    n_image = 0
    n_pdf = 0
    n_archive = 0
    n_other = 0
    n_mac = 0
    rf = rarfile.RarFile(archive)
    for f in rf.infolist():
        if f.file_size > 0:
            if f.filename.find("__MACOSX")>=0:
                n_mac += 1
            else:
                folder, filename = os.path.split(f.filename)
                basename, ext = os.path.splitext(filename)
                ext=ext.lower()
                folders.add(folder)
                type = ''
                if ext in ['.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.png']:
                    type='image'
                    n_image += 1
                else:
                    if ext=='.pdf':
                        type='pdf'
                        n_pdf += 1
                    else:
                        if ext in ['.cbr', '.rar', '.cbz', '.zip']:
                            type='archive'
                            n_archive += 1
                        else:
                            type='other'
                            n_other += 1
                            other.add(ext)
    rf.close()
    if other:
        sother = str(other)
    else:
        sother = '{}'
    return len(folders), n_image, n_pdf, n_archive, n_other, n_mac, sother


def analyse_archives(out: TextIO):
    totf = 0
    for fullpath in get_all_files(source):
        totf += 1
        path, file = os.path.split(fullpath)
        basename, ext = os.path.splitext(file)
        if ext.lower() in ['.cbr', '.rar']:
                print(f'{file:<100}', end='')
                try:
                    status='Ok'
                    nf,ni,np,na,no,nm,so = analyze_one_archive(fullpath)
                except:
                    status = 'Error'
                    nf,ni,np,na,no,nm,so = (0,0,0,0,0,0,'')
                print(status,nf,ni,np,na,no,nm,so)
                out.write(f'{status};{file};{nf};{ni};{np};{na};{no};{nm};{so}\n')
                out.flush()
    if not DO_IT:
        print("No action: ", end='')
    print(f'{totf} fichiers analysés')


with open(r'analyze.txt', mode='w', encoding='utf-8') as out:
    analyse_archives(out)
