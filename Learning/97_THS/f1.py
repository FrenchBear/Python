from common_fs import *

for file in get_files(r'C:\Users\Pierr\Desktop\Bibliothèque Tangente HS All'):
    for c in file:
        if c<' ' or c>'z':
            print(c, file)
