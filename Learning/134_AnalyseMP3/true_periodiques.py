# trie_périodiques
# Trie les BD du dossier W:\BD\Revues\!Périodiques par série
#
# 2025-11-03    PV

from collections import Counter
import os
import shutil
from common_fs import get_files, file_part


source = r"W:\BD\Revues\!Périodiques"

files = list(get_files(source, True))


c: Counter = Counter()
for filefp in files:
    file = file_part(filefp)
    serie = file.split(" - ")[0]
    c.update([serie])

series_to_move = [s for s, n in c.items() if n >= 5]

print(series_to_move)

for filefp in files:
    file = file_part(filefp)
    serie = file.split(" - ")[0]
    if serie in series_to_move:
        td = os.path.join(source, serie)
        os.makedirs(td, exist_ok=True)
        shutil.move(filefp, td)
