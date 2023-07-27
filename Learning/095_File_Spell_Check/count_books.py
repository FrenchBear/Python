# count_books.py
# Compte les titres de livres bien formattés
#
# 2022-01-04    PV

from common_fs import get_all_files
import os

source = r'W:\Livres\A_Trier'
dest = r'W:\Livres\A_Trier2'

tot = 0
tots = [0, 0, 0, 0]
auth = 0
authx = 0
for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    bname, ext = os.path.splitext(file)
    tot += 1

    ts = bname.split(' - ')
    if 1 <= len(ts) <= 3:
        tots[len(ts)] += 1
    else:
        tots[0] += 1

    if len(ts) == 3:
        a = ts[2]
        if a == 'X':
            authx += 1
        else:
            auth += 1
            newloc = os.path.join(dest, file)
            os.rename(filefp, newloc)

print(f'{tot} total files')
print(f'Sections: 1={tots[1]}, 2={tots[2]}, 3={tots[3]}, Autre={tots[0]}')
print(f'Authors defined={auth}, X={authx}, undefined={sum(tots[:3])}')
