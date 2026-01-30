import os
import shutil

from common_fs import get_files, get_folders


source = r'W:\TempBD\!!cbrn.Adult'

DO_IT = False


# ToDo: manage name conflicts in move_folder_content_up
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
            # os.remove(folderfp)
            shutil.rmtree(folderfp)
        else:
            print(f'rmdir {folderfp}')
        # print('rmdir')
        return


def count_pics(folderfp: str) -> int:
    nPics = 0
    for file in get_files(folderfp):
        _, ext = os.path.splitext(file)
        if ext.lower() in ['.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.png', '.tif', '.tiff']:
            nPics += 1
    return nPics


with open(r'check_level3.txt', 'w', encoding='utf8') as out:
    for folder in get_folders(source):
        folderfp = os.path.join(source, folder)
        folders2 = get_folders(folderfp)
        if len(folders2) > 0:
            if count_pics(folderfp) > 0:
                print("Pics and subfolders", folderfp)
                out.write("HYB;"+folderfp+'\n')
            for folder2 in folders2:
                folder2fp = os.path.join(folderfp, folder2)
                folders3 = get_folders(folder2fp)
                if len(folders3) > 0:
                    print("Folders at level 3", folder2fp)
                    out.write("FL3;"+folder2fp+'\n')
                    out.flush()
                # Move level 3 subfolders one level up if there is only 1 folder at level 3
                # ToDo: manage name conflicts in move_folder_content_up
                # if len(folders3)==1 and len(get_files(folder2fp))==0:
                #     print('  Move up '+folders3[0])
                #     move_folder_content_up(folder2fp, os.path.join(folder2fp, folders3[0]))
