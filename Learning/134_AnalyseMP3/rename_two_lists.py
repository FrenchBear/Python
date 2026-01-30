# rename_two_lists.py
# Renomme des fichiers à partir de deux listes de fichiers (originale et corrigée)
#
# 2025-09-28    PV
# 2025-10-21    PV      Rename and cleanup
# 2025-11-03    PV      Support renaming directories

from collections import defaultdict, Counter
import os
import sys
from common_fs import file_exists, folder_exists, folder_part, file_part

# Step 0: Read data
with open(r"C:\Temp\original.txt", encoding="utf-8") as f:
    zold = f.readlines()
with open(r"C:\Temp\fixed.txt", encoding="utf-8") as f:
    znew = f.readlines()
assert len(zold) == len(znew)


class Renamer:
    def __init__(self, old, new) -> None:
        self.old = old
        self.new = new
        self.renamer: Renamer | None = None

        # Step 1, check that renamed parents have only one way to be renemed
        dicpaths: defaultdict[str, Counter[str]] = defaultdict(Counter)
        for i in range(len(old)):
            o = folder_part(old[i].strip())
            n = folder_part(new[i].strip())
            dicpaths[o].update([n])

        pb = False
        for d in dicpaths.keys():
            if len(dicpaths[d]) > 1:
                if not pb:
                    pb = True
                    print("Parents with mode than 1 rename:")
                print(d)
                for (ee, nn) in dicpaths[d].most_common():
                    print(f"  {nn}: {ee}")

        if pb:
            sys.exit(0)

        # Step 2, build mapping old parent -> new parent
        self.rename_parents: dict[str, str] = {}
        for d in dicpaths.keys():
            e = dicpaths[d].most_common()[0][0]
            if e != d:
                self.rename_parents[d] = e

        # print("Rename parents:", self.rename_parents)

        if len(self.rename_parents) > 0:
            self.renamer = Renamer(list(self.rename_parents.keys()), list(self.rename_parents.values()))

    def rename(self):
        if self.renamer:
            self.renamer.rename()

        for i in range(len(self.old)):
            o = self.old[i].strip()
            n = self.new[i].strip()
            of = file_part(o)
            nf = file_part(n)
            ro = os.path.join(folder_part(n), of)
            if of != nf and (folder_exists(ro) or file_exists(ro)):
                print(ro, " -> ", n)
                try:
                    os.rename(ro, n)
                except:
                    pass


r = Renamer(zold, znew)
r.rename()
