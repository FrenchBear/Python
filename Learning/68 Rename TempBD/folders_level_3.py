
import os, sys, shutil
import subprocess
from typing import List, TextIO

from common import *


source = r'W:\TempBD\cbrn.BDA'
target = r'W:\TempBD\cbrn.BDA.rerar'
DO_IT = False

rar = r"c:\Program Files\WinRAR\rar.exe"

def move_folder_content_up(parent: str, folderfp: str):
    for root, subs, files in os.walk(folderfp):
        for sub in subs:
            if DO_IT:
                os.rename(os.path.join(root, sub), os.path.join(parent, sub))
            else:
                print(f'rename {os.path.join(root, sub)}  -->  {os.path.join(parent, sub)}')
        # print('subs ', end='')
        for file in files:
            if DO_IT:
                os.rename(os.path.join(root, file), os.path.join(parent, file))
            else:
                print(f'rename {os.path.join(root, file)}  -->  {os.path.join(parent, file)}')
        # print('files ', end='')
        if DO_IT:
            #os.remove(folderfp)
            shutil.rmtree(folderfp)
        else:
            print(f'rmdir {folderfp}')
        # print('rmdir')
        return


def make_archive(out: TextIO, sourcefp: str):
    destfp = target + sourcefp[len(source):]
    destfolder, _ = os.path.split(destfp)
    try:
        os.mkdir(destfolder)
    except:
        pass
    print(sourcefp,'->', end=' ')
    if os.path.exists(destfp+'.rar'):
        print('Rar exists')
        out.write("-1;{sourcefp}\n")
    else:
        process = subprocess.run([rar, 'a', '-ep', destfp+'.rar', sourcefp], stdout=subprocess.PIPE, universal_newlines=True, encoding='cp437')
        print(process.returncode)
        out.write(f'{process.returncode};{sourcefp}\n')
    out.flush()

with open(r'rerar.txt', 'w', encoding='utf8') as out:
    for folder in get_folders(source):
        folderfp = os.path.join(source, folder)
        folders2 = get_folders(folderfp)
        if len(folders2)==0:
            make_archive(out, folderfp)
        else:
            for folder2 in folders2:
                folder2fp = os.path.join(folderfp, folder2)
                #folders3 = get_folders(folder2fp)
                # if len(folders3)>0:
                #     print(folder2fp)
                # if len(folders3)==1 and len(get_files(folder2fp))==0:
                #     move_folder_content_up(folder2fp, os.path.join(folder2fp, folders3[0]))
                make_archive(out, folder2fp)