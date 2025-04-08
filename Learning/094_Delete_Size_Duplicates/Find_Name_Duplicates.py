# Find book files with duplicate names
#
# 2023-01-20    PV      First version

from common_fs import folder_exists, get_all_files
import re
import shutil
import os

source1 = r'W:\Livres\Informatique'         # Reference
source2 = r'C:\Temp\A_Trier'  # Books to check
trash = r'C:\temp\trash'

doit = False

sourcelist = []
bookname = re.compile(r"([^)]*)( \([^)]+\))? - \[([^]]+)\] - (.*)")

if doit:
    if not folder_exists(trash):
        os.mkdir(trash)


def clean(name: str) -> str:
    return name.replace(',', ' ').replace(',', ' ').replace('  ', ' ').casefold()


print('Indexing source books from', source1)
for filefp in get_all_files(source1):
    folder, file = os.path.split(filefp)
    bname, ext = os.path.splitext(file)
    if ext.casefold() == '.pdf':
        ma1 = bookname.fullmatch(bname)
        if ma1:
            ed = ma1.group(2)
            if ed:
                ed = ed.strip()
            b = (clean(ma1.group(1)), ed, ma1.group(3).casefold(), ma1.group(4).casefold(), folder, file)
            sourcelist.append(b)
            # auth:str = ma.group(4)
            # if ' and ' in auth.lower():
            #     print(filefp)

print('Checking folder', source2)
l2 = list(get_all_files(source2))
for filefp in l2:
    folder, file = os.path.split(filefp)
    bname, ext = os.path.splitext(file)
    if ext.casefold() == '.pdf':
        ma2: re.Match|None = bookname.fullmatch(bname)
        if ma2:
            title = clean(ma2.group(1))
            ed = ma2.group(2)
            if ed:
                ed = ed.strip()
            editor = ma2.group(3).casefold()
            authors = ma2.group(4).casefold()

            for b in sourcelist:
                if b[0] == title and (ed is None or ed == b[1]) and b[2] == editor:
                    print(b[5])
                    print(file)
                    print()
                    if doit:
                        try:
                            shutil.move(filefp, os.path.join(trash, file))
                        except:
                            pass
