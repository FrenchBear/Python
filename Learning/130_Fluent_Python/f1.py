# --follow-imports=skip

import os
import doctest
from typing import List


s = """
>>> import unicodedata, string
>>> def shave_marks(txt):
...     norm_txt = unicodedata.normalize('NFD', txt)  
...     shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))  
...     return unicodedata.normalize('NFC', shaved)  
>>> order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
>>> shave_marks(order)
'“Herr Voß: • ½ cup of Œtker™ caffe latte • bowl of acai.”'
>>> Greek = 'Ζέφυρος, Zéfiro'
>>> shave_marks(Greek)
'Ζεφυρος, Zefiro'

"""

filename = r'C:\Temp\p0.py'
with open(filename, "w", encoding='UTF-8') as fi:
    fi.write(s)
res = doctest.testfile(filename, report=False)

if res.failed==0:
    print("OK!")

os._exit(0)


# filename = r'C:\Temp\fp2\BlocInteractive-u8\Example 4-15.py'
# res = doctest.testfile(filename, report=False)


def get_files(source: str) -> List[str]:
    '''Retourne juste les fichiers d'un dossier, noms.ext sans chemins'''
    _1, _2, files = next(os.walk(source))
    return files

folder = r'C:\Temp\fp2\BlocInteractive-u8'
for file in list(get_files(folder)):
    f = os.path.join(folder, file)
    print(f'\n------------------------------------------------------------------------\n{f}\n')
    res = doctest.testfile(os.path.join(folder, file)) 
    if res.failed==0:
        os.remove(f)
    else:
        os._exit(0)
