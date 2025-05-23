import os
import matplotlib.pyplot as plt     # type: ignore
import matplotlib.image as mpimg    # type: ignore
import numpy as np
import math

pathfile = r'T:\Scans\THS32\3 BCI\THS32-005.png'
path, file = os.path.split(pathfile)
stem, ext = os.path.splitext(file)
numpage = int(stem[-3:])
print(numpage)

img = mpimg.imread(pathfile)[:, :, :3]
height = img.shape[0]
width = img.shape[1]
print(height, width)

yellow = np.array([0.7921569, 0.6392157, 0.27058825])
(rowmin, rowmax) = (5350, 5600)
(colminpair, colmaxpair) = (200, 550)
(colminimpair, colmaximpair) = (3320, 3820)


def dotdist(p1, p2):
    return np.linalg.norm(p2-p1)


def dotdistyellow(p):
    return math.sqrt((p[0]-yellow[0])**2+(p[1]-yellow[1])**2+(p[2]-yellow[2])**2)


def veclength(p):
    return math.sqrt(p[0]**2+p[1]**2+p[2]**2)


if numpage % 2 == 0:
    (colmin, colmax) = (colminpair, colmaxpair)
else:
    (colmin, colmax) = (colminimpair, colmaximpair)

area = img[rowmin:rowmax, colmin:colmax, :]
areaheight = area.shape[0]
areawidth = area.shape[1]

area = (area-yellow)**2
area = area.reshape(areawidth*areaheight, 3)
area = np.apply_along_axis(veclength, 1, area)
area = area.reshape(areaheight, areawidth)

plt.imshow(area, cmap='gray')
plt.show()

colp = None
rowp = None

dcol = []
if numpage % 2 == 0:
    r = range(0, areawidth)
else:
    r = range(areawidth-1, -1, -1)
for col in r:
    n = (area[:, col] < 0.1).sum()
    dcol.append(n)
    # if n >= 50:
    #     colp = col+colmin
    #     break

plt.plot(dcol)
plt.show()


for row in range(areaheight-1, 0, -1):
    n = (area[row, :] < 0.1).sum()
    if n >= 100:
        rowp = row+rowmin
        break

print(colp, ';', rowp)
