# 1rst letter uppercase

from common_fs import get_files
import os


root = r"W:\Livres\A_Trier"

lf = list(get_files(root))
for f in lf:
    f2 = f[1].upper() + f[2:]
    print(f2)
    os.rename(os.path.join(root, f), os.path.join(root, f2))