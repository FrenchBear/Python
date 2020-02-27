import os
import os.path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.signal import find_peaks


def croppic(picin, picout):
    img = mpimg.imread(picin)
    width = img.shape[1]
    #print("width=", width)

    # Using matplotlib and the formula
    # Y' = 0.2989 R + 0.5870 G + 0.1140 B
    def rgb2gray(rgb):
        return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

    gray = rgb2gray(img)
    columns_average = np.median(gray, axis=0)

    def moving_average(a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    ca2 = moving_average(columns_average, 10)

    def difflist(ret, n):
        return np.abs(ret[n:] - ret[:-n])

    cd = difflist(ca2, 1)
    peaks, _ = find_peaks(cd, distance=150)

    pmin = 0
    pmax = 0
    for i in range(3):
        if cd[peaks[i]] > 1e-3:
            pmin = peaks[i]+20
            break
    for i in range(3):
        if cd[peaks[-i-1]] > 1e-3:
            pmax = peaks[-i-1]-5
            break

    if pmin > 275:
        pmin = 0
    if pmax < width-275:
        pmax = width

    #print("crop", pmin, "to", pmax)

    img2 = img[:, pmin:pmax, :]

    mpimg.imsave(picout, img2, dpi=600)

    #plt.imshow(img2)
    #plt.show()

#croppic('T18-006.png', 'T18-006-crop.png')

source = r'T:\Scans\THS23\1 Scans'
dest = r'C:\Scans\THS23\2 Crop'
files = [f for f in os.listdir(source) if f!='Thumbs.db' and os.path.isfile(os.path.join(source, f))]

for i in range(len(files)):
    picin = os.path.join(source, files[i])
    picout = os.path.join(dest, files[i])
    print(picin, '->', end='')
    croppic(picin, picout)
    print(picout)

