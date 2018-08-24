import os
import os.path
import shutil

path = r'U:\Sonos\Pierre\Lists\Recent'
p2 = r'U:\Sonos\Pierre\Lists'
files = os.listdir(path)

for i,f in enumerate(files):
    nd = os.path.join(p2, str(i))
    print(nd)
    os.mkdir(nd)
    of = os.path.join(path, f)
    nf = os.path.join(nd, f)
    shutil.copyfile(of, nf)
    
    
