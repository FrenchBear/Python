import matplotlib.image as mpimg
import numpy as np
import math
import os
from dataclasses import dataclass
from typing import List, Optional


yellow = np.array([0.7921569, 0.6392157, 0.27058825])
(rowmin, rowmax) = (5350, 5600)
(colminpair, colmaxpair) = (200, 550)
(colminimpair, colmaximpair) = (3320, 3820)

rowpmax = 0
margebmax = 0
colpmax = 0
margedmax = 0
margegmax = 0


@dataclass
class ScannedPage:
    file: str
    numpage: int
    width: int
    height: int
    colp: Optional[int]
    rowp: Optional[int]

    def is_pair(self) -> bool:
        return self.numpage % 2 == 0

    def is_impair(self) -> bool:
        return self.numpage % 2 == 1


Pages: List[ScannedPage] = []


def dotdist(p1, p2):
    return np.linalg.norm(p2-p1)


def veclength(p):
    return math.sqrt(p[0]**2+p[1]**2+p[2]**2)


def process(file: str, numpage: int):
    print(file, ';', numpage, ';', sep='', end='')

    img = mpimg.imread(file)
    width: int = img.shape[1]
    height: int = img.shape[0]
    print(width, ';', height, ';', sep='', end='')

    if numpage % 2 == 0:
        (colmin, colmax) = (colminpair, colmaxpair)
    else:
        (colmin, colmax) = (colminimpair, colmaximpair)

    area = img[rowmin:rowmax, colmin:colmax, :]
    areaheight: int = area.shape[0]
    areawidth: int = area.shape[1]

    area = (area-yellow)**2
    area = area.reshape(areawidth*areaheight, 3)
    area = np.apply_along_axis(veclength, 1, area)
    area = area.reshape(areaheight, areawidth)

    colp: Optional[int] = None
    if numpage % 2 == 0:
        r = range(0, areawidth)
    else:
        r = range(areawidth-1, -1, -1)
    for col in r:
        n = (area[:, col] < 0.05).sum()
        if n >= 50:
            colp = col+colmin
            break

    rowp: Optional[int] = None
    for row in range(areaheight-1, 0, -1):
        n = (area[row, :] < 0.05).sum()
        if n >= 100:
            rowp = row+rowmin
            break

    print(colp, ';', rowp, sep='')

    newpage = ScannedPage(file, numpage, width, height, colp, rowp)
    global Pages
    Pages.append(newpage)

    global rowpmax, margebmax
    if rowp:
        if rowp > rowpmax:
            rowpmax = rowp
        if height-rowp > margebmax:
            margebmax = height-rowp

    global colpmax, margedmax, margegmax
    if colp:
        if numpage % 2 == 0:
            if colp > margegmax:
                margegmax = colp
        else:
            if colp > colpmax:
                colpmax = colp
            if width-colp > margedmax:
                margedmax = width-colp


def files1(path):
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)


pagescount = 0
for pathfile in files1(rf'T:\Scans\THS67\2 Redressé'):
    path, file = os.path.split(pathfile)
    basename, ext = os.path.splitext(file)
    if ext.lower() == '.png':
        numpage = int(basename[-3:])
        process(pathfile, numpage)
        pagescount += 1
        if pagescount > 6:
            break

print()
print('rowpmax:', rowpmax, '  margebmax:', margebmax)
print('colpmax:', colpmax, '  margedmax:', margedmax)
print('margegmax:', margegmax)

print()
finalwidth = colpmax+margedmax
finalheight = rowpmax+margebmax
for page in Pages:
    print(page)
    if page.numpage % 2 == 1:
        if page.colp:
            addmargeg = colpmax-page.colp
            addmarged = margedmax-(page.width-page.colp)
        else:
            addmargeg = (finalwidth-page.width)//2
            addmarged = finalwidth-page.width-addmargeg
        newwidth = page.width+addmargeg+addmarged
        print('addmargeg', addmargeg, '  addmarged', addmarged, '  newwidth', newwidth)

        if page.rowp:
            addmargeh = rowpmax-page.rowp
            addmargeb = margebmax-(page.height-page.rowp)
        else:
            addmargeh = (finalheight-page.height)//2
            addmargeb = finalheight-page.height-addmargeh
        newheight = page.height+addmargeh+addmargeb
        print('addmargeh', addmargeh, '  addmargeb', addmargeb, '  newheight', newheight)
