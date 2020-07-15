import os
from typing import List, Tuple, Iterable
from common import *


source = r'W:\TempBD\archives'
DO_IT = True


for root, subs, files in os.walk(source, False):
    for file in files:
        basename, ext = os.path.splitext(file)
        if ext.lower()=='.pdf':
            imagefilefp = os.path.join(root, basename+".jpg")
            if os.path.exists(imagefilefp):
                print(f'del "{imagefilefp}"')
                if DO_IT:
                    os.remove(imagefilefp)
