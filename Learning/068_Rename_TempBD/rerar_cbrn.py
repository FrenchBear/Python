import os
import subprocess
from typing import TextIO

from common_fs import get_folders


source = r'W:\TempBD\archives\cbrn'
target = r'W:\TempBD\archives\cbrn.rerar'
backup = r'W:\TempBD\archives\cbrn.bak'


rar = r"c:\Program Files\WinRAR\rar.exe"

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
        process = subprocess.run([rar, 'a', '-ep', destfp+'.rar', sourcefp], stdout=subprocess.PIPE, text=True, encoding='cp437')
        print(process.returncode)
        out.write(f'{process.returncode};{sourcefp}\n')
    out.flush()
    backupfp = os.path.join(backup, sourcefp[len(source)+1:])
    backup_folder, _ = os.path.split(backupfp)
    if not os.path.exists(backup_folder):
        os.mkdir(backup_folder)
    try:
        os.rename(sourcefp, backupfp)
    except Exception as ex:
        msg = f'  *** Failed to move folder {sourcefp} to {backup}: {ex}'
        print(msg)
        out.write(msg+'\n')
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
                make_archive(out, folder2fp)
            try:
                os.rmdir(folderfp)
            except:
                pass
