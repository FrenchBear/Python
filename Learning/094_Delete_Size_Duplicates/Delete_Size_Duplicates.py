# New version of Delete Size Duplicates, different from the one in 68_Rename_Temp_BD
# More complete
#
# 2021-12-26    PV
# 2021-12-28    PV      Keep at least 1 version
# 2022-06-20    PV      Print delete count

from collections import defaultdict
from common_fs import get_all_files
import os

# source = r'W:\Livres'
# extensions = ['.pdf', '.epub']

source = r'D:\Kaforas\OneDrive\PicturesODKB'
extensions = ['.gif', '*.webp', '*.mp4']

doit = False

dic: defaultdict[int, list[str]] = defaultdict(list)

for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    _, ext = os.path.splitext(file)
    if ext.casefold() in extensions:
        s = os.path.getsize(filefp)
        dic[s].append(filefp)

ndel = 0
dups = [v for v in dic.values() if len(v) > 1]
print(f'{len(dups)} size duplicates group(s) found.')
for lst in dups:
    print()
    d = lst[:]

    # First delete extra copies in a_trier\new, keep at least 1
    for file in lst:
        if 'a_trier\\new' in file.casefold():
            if doit:
                os.remove(file)
            print(f'del1 "{file}"')
            d.remove(file)
            ndel += 1
            if len(d) == 1:
                break

    # Then delete extra copies in a_trier, keep at least 1
    if len(d) > 1:
        for file in lst:
            if 'a_trier' in file.casefold():
                if doit:
                    os.remove(file)
                print(f'del2 "{file}"')
                d.remove(file)
                ndel += 1
            if len(d) == 1:
                break

    # Then delete any extra remaining copies, keep at least 1
    while len(d) > 1:
        if doit:
            os.remove(d[0])
        print(f'del3 "{d[0]}"')
        d.remove(d[0])
        ndel += 1

    print(f'keep {d[0]}')

print(ndel, 'fichier(s) effacé(s)')
