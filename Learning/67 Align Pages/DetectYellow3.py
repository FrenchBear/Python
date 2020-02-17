import matplotlib.image as mpimg
import numpy as np
import math

yellow = np.array([0.7921569, 0.6392157, 0.27058825])
(rowmin, rowmax) = (5350, 5600)
(colminp, colmaxp) = (200, 550)
(colmini, colmaxi) = (3320, 3820)

def dotdist(p1, p2):
    return np.linalg.norm(p2-p1)

def veclength(p):
    return math.sqrt(p[0]**2+p[1]**2+p[2]**2)

for p in range(1, 164, 2):
    file = rf'T:\Scans\THS67\2 Redressé\1\THS67-{p:0>3}.png'
    print(file, ' ', end='')

    img = mpimg.imread(file)
    width = img.shape[1]
    height = img.shape[0]
    print(width, height, ' ', end='')

    area = img[rowmin:rowmax, colmini:colmaxi, :]
    areaheight = area.shape[0]
    areawidth = area.shape[1]

    area = (area-yellow)**2
    area = area.reshape(areawidth*areaheight, 3)
    area = np.apply_along_axis(veclength, 1, area)
    area = area.reshape(areaheight, areawidth)

    colp = 0
    for col in range(areawidth-1, 0, -1):
        n = (area[:, col]<0.05).sum()
        if n>=50:
            colp = col+colmini
            break

    rowp = 0
    for row in range(areaheight-1, 0, -1):
        n = (area[row, :]<0.05).sum()
        if n>=100:
            rowp = row+rowmin
            break

    print(colp, rowp)
