import shutil
from common_fs import *

source = r'\\teraz\torrents\Albums Spirou\Le Journal de Spirou\Albums Du Journal'
test = r'C:\Temp\Converti\Albums Du Journal'
dest = r'C:\Temp\Albums'

ls = list(get_files(source))
lt = list(get_files(test))
ld = list(get_files(dest))

for f in ls:
    nn = basename(f)+'.pdf'
    if not nn in lt and not nn in ld:
        print('copy '+f)
        s = os.path.join(source, f)
        d = os.path.join(dest, f)
        shutil.copyfile(s, d)
