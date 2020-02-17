import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy
import math

file = r'T:\Scans\THS67\2 Redressé\1\THS67-007.png'

img = mpimg.imread(file)
height = img.shape[0]
width = img.shape[1]
print(height, width)

yellow = np.array([0.7921569, 0.6392157, 0.27058825])
(rowmin, rowmax) = (5350, 5600)
(colminp, colmaxp) = (200, 550)
(colmini, colmaxi) = (3320, 3820)

def dotdist(p1, p2):
    return np.linalg.norm(p2-p1)

def dotdistyellow(p):
    return math.sqrt((p[0]-yellow[0])**2+(p[1]-yellow[1])**2+(p[2]-yellow[2])**2)

def veclength(p):
    return math.sqrt(p[0]**2+p[1]**2+p[2]**2)

area = img[rowmin:rowmax, colmini:colmaxi, :]
areaheight = area.shape[0]
areawidth = area.shape[1]

area = (area-yellow)**2
area = area.reshape(areawidth*areaheight, 3)
area = np.apply_along_axis(veclength, 1, area)
area = area.reshape(areaheight, areawidth)

#plt.imshow(a2, cmap='gray')
#plt.show()

colp = 0
for col in range(areawidth-1, 0, -1):
    n = (area[:, col]<0.05).sum()
    if n>=50:
        colp = col+colmini
        break

colp2 = 0
for x in range(colmaxi, colmini, -1):
    rowdist = [math.sqrt((img[y, x, 0]-yellow[0])**2+(img[y, x, 1]-yellow[1])**2+(img[y, x, 2]-yellow[2])**2) for y in range(rowmin, rowmax)]
    n = sum(1 if d<0.05 else 0 for d in rowdist)
    if n>=50:
        colp2 = x
        break

rowp = 0
for row in range(areaheight-1, 0, -1):
    n = (area[row, :]<0.05).sum()
    if n>=100:
        rowp = row+rowmin
        break

rowp2 = 0
for y in range(rowmax, rowmin, -1):
    coldist = [dotdist(img[y, x], yellow) for x in range(colmini, colmaxi)]
    n = sum(1 if d<0.05 else 0 for d in coldist)
    if n>=100:
        rowp2 = y
        break

print(colp, colp2, rowp, rowp2)
