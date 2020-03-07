
import os, sys, shutil
from typing import List
from common import *

source = r'W:\TempBD\archives\cbrn'
DO_IT = True

for folder in get_folders(source):
    folderfp = os.path.join(source, folder)
    print(folderfp, end=' -> ')
    lst = get_folders(folderfp)
    if len(lst)==0:
        print('no sf')
    else:
        if len(lst)>1:
            print('multiple sf')
        else:
            onefolder = os.path.join(folderfp, lst[0])
            print('one sf, moving up... ', end='')
            for root, subs, files in os.walk(onefolder):
                for sub in subs:
                    if DO_IT:
                        os.rename(os.path.join(root, sub), os.path.join(folderfp, sub))
                    # else:
                    #     print(f'rename {os.path.join(root, sub)}  -->  {os.path.join(folderfp, sub)}')
                print('subs ', end='')
                for file in files:
                    if DO_IT:
                        os.rename(os.path.join(root, file), os.path.join(folderfp, file))
                    # else:
                    #     print(f'rename {os.path.join(root, file)}  -->  {os.path.join(folderfp, file)}')
                print('files ', end='')
                if DO_IT:
                    shutil.rmtree(onefolder)
                print('rmdir')
                break
