# Analyse le contenu de fichiers rar
# 2020-03-05    PV

import os, shutil
import rarfile
import unicodedata
from typing import List, Tuple, TextIO

from common import *


"""
ne chercher que les formats d'image et PDF
Signater les archives contenant des PDF
Ignorer les dossiers __MACOSX
"""


DO_IT = True
source = r'W:\TempBD\archives'

rarfile.UNRAR_TOOL= r"c:\Program Files\WinRAR\rar.exe"


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
                if ext in ['.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.png', '.tif', '.tiff']:
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

created = []
dest = ''

def move(fullpath: str, subfolder: str):
    global dest
    dest = subfolder
    path, file = os.path.split(fullpath)
    print(f' -->  {subfolder:<8}')
    if DO_IT:
        if subfolder not in created:
            created.append(subfolder)
            if not os.path.exists(os.path.join(source, subfolder)):
                os.mkdir(os.path.join(source, subfolder))
        newname = get_safe_name(os.path.join(source, subfolder, file))
        os.rename(fullpath, newname)

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
                print(status,nf,ni,np,na,no,nm,so, end='')

                if status=='Error':
                    move(fullpath, "error")
                else:
                    if so.lower().find(".exe")>=0:
                        move(fullpath, "exe")
                    else:
                        if ni==0 and na==0 and np==1:
                            move(fullpath, "pdf1")
                        else:
                            if ni==0 and na==0 and np>1:
                                move(fullpath, "pdf")
                            else:
                                if nf==1 and np==0 and na==0 and ni>0:
                                    move(fullpath, "cbr1")
                                else:
                                    if nf>=1 and np==0 and na==0 and ni>0:
                                        move(fullpath, "cbrn")
                                    else:
                                        if ni==0 and np==0 and na==1:
                                            move(fullpath, "archive1")
                                        else:
                                            if ni==0 and np==0 and na>1:
                                                move(fullpath, "archiven")
                                            else:
                                                move(fullpath, "hyprid")

                out.write(f'{dest};{status};{file};{nf};{ni};{np};{na};{no};{nm};{so}\n')
                out.flush()


    if not DO_IT:
        print("No action: ", end='')
    print(f'{totf} fichiers analysés')


with open(r'analyze.txt', mode='w', encoding='utf-8') as out:
    analyse_archives(out)
