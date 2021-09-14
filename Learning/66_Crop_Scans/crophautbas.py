import os
import os.path
import numpy as np
import matplotlib.image as mpimg

def croppic(index, picin, picout):
    img = mpimg.imread(picin)
    (height,widt,depth) = img.shape

    if index%2==1:
        img = img[:-20,2:-2,:]
    else:
        img = img[20:,2:-2,:]

    mpimg.imsave(picout, img, dpi=600)


source = r'C:\Scans\THS23\2 Crop Hz'
dest = r'C:\Scans\THS23\3 Crop Vt'
files = [f for f in os.listdir(source) if f!='Thumbs.db' and os.path.isfile(os.path.join(source, f))]

for i in range(len(files)):
    picin = os.path.join(source, files[i])
    picout = os.path.join(dest, files[i])
    print(picin, '->', end='')
    croppic(i+1, picin, picout)
    print(picout)
