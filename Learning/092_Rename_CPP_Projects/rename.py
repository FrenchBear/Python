# rename.pyY
# Rename CPP projects
# 2021-09-14    PV

from common_fs import get_files, get_folders
import os

def read_all_text(file:str, encoding:str='utf-8') -> str:
    with open(file, encoding=encoding) as f:
        return f.read()

def write_all_text(file:str, s:str, encoding:str='utf-8'):
    with open(file, mode='w', encoding=encoding) as f:
        f.write(s)


def rename_project(folderFP: str, folder: str, old_project: str):
    print(f'Renaming {folder}/{old_project}.vcxproj')
    old_project_base, _ = os.path.splitext(old_project)
    new_project = folder+'.vcxproj'
    oldFP = os.path.join(folderFP, old_project)
    newFP = os.path.join(folderFP, new_project)
    print(f'{oldFP} -> {newFP}')
    print(f'{oldFP}.user -> {newFP}.user')      # May fail
    os.rename(oldFP, newFP)
    try:
        os.rename(oldFP+'.user', newFP+'.user')
    except Exception:
        pass

    sln = os.path.join(folderFP, folder+'.sln')
    s = read_all_text(sln, encoding='utf-8-sig').replace(old_project_base, folder)
    write_all_text(sln, s, encoding='utf-8-sig')

    root, _ = os.path.split(folderFP)
    sln = os.path.join(root, 'All.sln')
    s = read_all_text(sln, encoding='utf-8-sig').replace(old_project_base, folder)
    write_all_text(sln, s, encoding='utf-8-sig')


def convert_folder(folderFP: str, folder: str):
    # Check solution
    lfs = [file for file in get_files(folderFP) if file.lower().endswith('.sln')]
    if len(lfs) == 0:
        print(f'No .sln found in folder {folderFP}')
        return
    elif len(lfs) > 1:
        print(f'More than 1 .sln found in folder {folderFP}')
        return
    else:
        sln_base, sln_ext = os.path.splitext(lfs[0])
        if sln_base != folder:
            print(f'folder!=solution: {folder}!={sln_base}')
            return

    # Check project
    lfp = [file for file in get_files(folderFP) if file.lower().endswith('.vcxproj')]
    if len(lfp) == 0:
        print(f'No .vcxproj found in folder {folderFP}')
        return
    elif len(lfp) > 1:
        print(f'More than 1 .vcxproj found in folder {folderFP}')
        return
    else:
        proj_base, proj_ext = os.path.splitext(lfp[0])
        if proj_base != sln_base:
            rename_project(folderFP, folder, lfp[0])


root = r'C:\Development\GitHub\CPP'
for folder in get_folders(root):
    if not folder.startswith('.'):
        convert_folder(os.path.join(root, folder), folder)
