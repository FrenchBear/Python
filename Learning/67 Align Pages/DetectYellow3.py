import matplotlib.image as mpimg
import numpy as np
import math
import os
import sys
from dataclasses import dataclass
from typing import List, Optional


yellow = np.array([0.7921569, 0.6392157, 0.27058825])
(rowmin, rowmax) = (5350, 5600)
(colminpair, colmaxpair) = (200, 550)
(colminimpair, colmaximpair) = (3320, 3820)

rowpmax = 0
margebmax = 0
colppairmax = 0
colpimpairmax = 0
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

    img = mpimg.imread(file)[:,:,:3]
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
    rowp: Optional[int] = None

    if 4<numpage<168:
        if numpage % 2 == 0:
            r = range(0, areawidth)
        else:
            r = range(areawidth-1, -1, -1)
        for col in r:
            n = (area[:, col] < 0.075).sum()
            if n >= 50:
                colp = col+colmin
                break

        for row in range(areaheight-1, 0, -1):
            n = (area[row, :] < 0.075).sum()
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

    global colppairmax, colpimpairmax, margedmax, margegmax
    if colp:
        if numpage % 2 == 0:
            if colp > colppairmax:
                colppairmax = colp
        else:
            if colp > colpimpairmax:
                colpimpairmax = colp
            if width-colp > margedmax:
                margedmax = width-colp


def files1(path):
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

# Step 1, determine sizes and position of yellow rect
source=r'T:\Scans\THS32\3 BCI'
dest=r'T:\Scans\THS32\4 Align'
prefix='THS32'

# for pathfile in files1(source):
#     path, file = os.path.split(pathfile)
#     basename, ext = os.path.splitext(file)
#     if ext.lower() == '.png':
#         numpage = int(basename[-3:])
#         #if 5<=numpage<=10:
#         process(pathfile, numpage)
# print()
# print('rowpmax=', repr(rowpmax))
# print('colppairmax=', repr(colppairmax))
# print('colpimpairmax=', repr(colpimpairmax))
# print('margedmax=', repr(margedmax))
# print()
# for page in Pages:
#     print("Pages.append("+repr(page)+")")
# sys.exit(0)


# Precomputed in step 1
rowpmax= 5599
colppairmax= 379
colpimpairmax= 3819
margedmax= 336

Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-001.png', numpage=1, width=3809, height=5616, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-002.png', numpage=2, width=3746, height=5616, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-003.png', numpage=3, width=3711, height=5616, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-004.png', numpage=4, width=3680, height=5616, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-005.png', numpage=5, width=3854, height=5616, colp=3819, rowp=5498))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-006.png', numpage=6, width=3746, height=5616, colp=218, rowp=5487))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-007.png', numpage=7, width=3854, height=5616, colp=3548, rowp=5509))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-008.png', numpage=8, width=3746, height=5616, colp=200, rowp=5510))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-009.png', numpage=9, width=3854, height=5616, colp=3534, rowp=5512))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-010.png', numpage=10, width=3746, height=5616, colp=200, rowp=5496))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-011.png', numpage=11, width=3854, height=5616, colp=3565, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-012.png', numpage=12, width=3746, height=5616, colp=200, rowp=5509))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-013.png', numpage=13, width=3711, height=5616, colp=3519, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-014.png', numpage=14, width=3746, height=5616, colp=200, rowp=5499))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-015.png', numpage=15, width=3854, height=5616, colp=3551, rowp=5508))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-016.png', numpage=16, width=3746, height=5616, colp=212, rowp=5508))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-017.png', numpage=17, width=3727, height=5632, colp=3511, rowp=5515))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-018.png', numpage=18, width=3762, height=5632, colp=250, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-019.png', numpage=19, width=3727, height=5632, colp=3518, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-020.png', numpage=20, width=3762, height=5632, colp=218, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-021.png', numpage=21, width=3727, height=5632, colp=3504, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-022.png', numpage=22, width=3762, height=5632, colp=252, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-023.png', numpage=23, width=3727, height=5632, colp=3500, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-024.png', numpage=24, width=3762, height=5632, colp=220, rowp=5511))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-025.png', numpage=25, width=3727, height=5632, colp=3496, rowp=5515))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-026.png', numpage=26, width=3762, height=5632, colp=242, rowp=5506))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-027.png', numpage=27, width=3727, height=5632, colp=3491, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-028.png', numpage=28, width=3762, height=5632, colp=257, rowp=5515))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-029.png', numpage=29, width=3727, height=5632, colp=3483, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-030.png', numpage=30, width=3762, height=5632, colp=277, rowp=5511))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-031.png', numpage=31, width=3727, height=5632, colp=3486, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-032.png', numpage=32, width=3762, height=5632, colp=252, rowp=5510))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-033.png', numpage=33, width=3727, height=5632, colp=3474, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-034.png', numpage=34, width=3762, height=5632, colp=290, rowp=5504))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-035.png', numpage=35, width=3727, height=5632, colp=3473, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-036.png', numpage=36, width=3762, height=5632, colp=267, rowp=5506))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-037.png', numpage=37, width=3727, height=5632, colp=3473, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-038.png', numpage=38, width=3762, height=5632, colp=288, rowp=5506))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-039.png', numpage=39, width=3727, height=5632, colp=3474, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-040.png', numpage=40, width=3762, height=5632, colp=276, rowp=5511))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-041.png', numpage=41, width=3727, height=5632, colp=3462, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-042.png', numpage=42, width=3762, height=5632, colp=294, rowp=5505))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-043.png', numpage=43, width=3727, height=5632, colp=3469, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-044.png', numpage=44, width=3762, height=5632, colp=281, rowp=5503))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-045.png', numpage=45, width=3727, height=5632, colp=3726, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-046.png', numpage=46, width=3762, height=5632, colp=293, rowp=5505))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-047.png', numpage=47, width=3727, height=5632, colp=3461, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-048.png', numpage=48, width=3762, height=5632, colp=365, rowp=5502))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-049.png', numpage=49, width=3727, height=5632, colp=3449, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-050.png', numpage=50, width=3762, height=5632, colp=369, rowp=5505))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-051.png', numpage=51, width=3727, height=5632, colp=3455, rowp=5525))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-052.png', numpage=52, width=3762, height=5632, colp=291, rowp=5510))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-053.png', numpage=53, width=3708, height=5632, colp=3451, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-054.png', numpage=54, width=3762, height=5632, colp=318, rowp=5513))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-055.png', numpage=55, width=3727, height=5632, colp=3450, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-056.png', numpage=56, width=3806, height=5632, colp=298, rowp=5507))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-057.png', numpage=57, width=3727, height=5632, colp=3450, rowp=5522))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-058.png', numpage=58, width=3786, height=5632, colp=323, rowp=5496))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-059.png', numpage=59, width=3727, height=5632, colp=3447, rowp=5525))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-060.png', numpage=60, width=3762, height=5632, colp=296, rowp=5509))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-061.png', numpage=61, width=3727, height=5632, colp=3446, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-062.png', numpage=62, width=3762, height=5632, colp=322, rowp=5491))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-063.png', numpage=63, width=3727, height=5632, colp=3446, rowp=5511))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-064.png', numpage=64, width=3762, height=5632, colp=310, rowp=5494))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-065.png', numpage=65, width=3727, height=5632, colp=3437, rowp=5514))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-066.png', numpage=66, width=3762, height=5632, colp=328, rowp=5509))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-067.png', numpage=67, width=3727, height=5632, colp=3436, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-068.png', numpage=68, width=3762, height=5632, colp=307, rowp=5512))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-069.png', numpage=69, width=3727, height=5632, colp=3426, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-070.png', numpage=70, width=3762, height=5632, colp=335, rowp=5500))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-071.png', numpage=71, width=3727, height=5632, colp=3437, rowp=5527))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-072.png', numpage=72, width=3762, height=5632, colp=326, rowp=5492))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-073.png', numpage=73, width=3727, height=5632, colp=3433, rowp=5509))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-074.png', numpage=74, width=3762, height=5632, colp=341, rowp=5494))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-075.png', numpage=75, width=3727, height=5632, colp=3428, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-076.png', numpage=76, width=3762, height=5632, colp=310, rowp=5507))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-077.png', numpage=77, width=3727, height=5632, colp=3427, rowp=5504))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-078.png', numpage=78, width=3762, height=5632, colp=335, rowp=5503))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-079.png', numpage=79, width=3727, height=5632, colp=3425, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-080.png', numpage=80, width=3762, height=5632, colp=320, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-081.png', numpage=81, width=3727, height=5632, colp=3422, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-082.png', numpage=82, width=3762, height=5632, colp=337, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-083.png', numpage=83, width=3727, height=5632, colp=3422, rowp=5525))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-084.png', numpage=84, width=3762, height=5632, colp=320, rowp=5525))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-085.png', numpage=85, width=3744, height=5632, colp=3433, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-086.png', numpage=86, width=3797, height=5632, colp=341, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-087.png', numpage=87, width=3754, height=5632, colp=3435, rowp=5529))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-088.png', numpage=88, width=3769, height=5632, colp=328, rowp=5528))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-089.png', numpage=89, width=3723, height=5632, colp=3416, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-090.png', numpage=90, width=3798, height=5632, colp=354, rowp=5525))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-091.png', numpage=91, width=3755, height=5632, colp=3419, rowp=5522))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-092.png', numpage=92, width=3789, height=5632, colp=299, rowp=5527))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-093.png', numpage=93, width=3729, height=5632, colp=3456, rowp=5507))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-094.png', numpage=94, width=3832, height=5632, colp=379, rowp=5527))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-095.png', numpage=95, width=3727, height=5632, colp=3439, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-096.png', numpage=96, width=3762, height=5632, colp=306, rowp=5528))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-097.png', numpage=97, width=3727, height=5632, colp=3435, rowp=5517))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-098.png', numpage=98, width=3762, height=5632, colp=320, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-099.png', numpage=99, width=3727, height=5632, colp=3429, rowp=5531))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-100.png', numpage=100, width=3762, height=5632, colp=311, rowp=5530))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-101.png', numpage=101, width=3727, height=5632, colp=3425, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-102.png', numpage=102, width=3806, height=5632, colp=376, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-103.png', numpage=103, width=3727, height=5632, colp=3422, rowp=5530))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-104.png', numpage=104, width=3762, height=5632, colp=314, rowp=5532))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-105.png', numpage=105, width=3727, height=5632, colp=3419, rowp=5525))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-106.png', numpage=106, width=3762, height=5632, colp=327, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-107.png', numpage=107, width=3727, height=5632, colp=3422, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-108.png', numpage=108, width=3798, height=5632, colp=311, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-109.png', numpage=109, width=3727, height=5632, colp=3417, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-110.png', numpage=110, width=3762, height=5632, colp=336, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-111.png', numpage=111, width=3727, height=5632, colp=3425, rowp=5532))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-112.png', numpage=112, width=3762, height=5632, colp=314, rowp=5532))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-113.png', numpage=113, width=3743, height=5632, colp=3433, rowp=5522))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-114.png', numpage=114, width=3778, height=5632, colp=338, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-115.png', numpage=115, width=3743, height=5632, colp=3445, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-116.png', numpage=116, width=3778, height=5632, colp=318, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-117.png', numpage=117, width=3743, height=5632, colp=3443, rowp=5513))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-118.png', numpage=118, width=3778, height=5632, colp=334, rowp=5515))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-119.png', numpage=119, width=3743, height=5632, colp=3444, rowp=5527))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-120.png', numpage=120, width=3778, height=5632, colp=323, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-121.png', numpage=121, width=3743, height=5632, colp=3440, rowp=5522))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-122.png', numpage=122, width=3778, height=5632, colp=344, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-123.png', numpage=123, width=3743, height=5632, colp=3439, rowp=5529))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-124.png', numpage=124, width=3778, height=5632, colp=317, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-125.png', numpage=125, width=3743, height=5632, colp=3449, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-126.png', numpage=126, width=3778, height=5632, colp=338, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-127.png', numpage=127, width=3743, height=5632, colp=3448, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-128.png', numpage=128, width=3778, height=5632, colp=321, rowp=5508))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-129.png', numpage=129, width=3743, height=5632, colp=3451, rowp=5510))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-130.png', numpage=130, width=3778, height=5632, colp=335, rowp=5501))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-131.png', numpage=131, width=3743, height=5632, colp=3459, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-132.png', numpage=132, width=3760, height=5632, colp=322, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-133.png', numpage=133, width=3743, height=5632, colp=3742, rowp=5599))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-134.png', numpage=134, width=3778, height=5632, colp=322, rowp=5510))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-135.png', numpage=135, width=3743, height=5632, colp=3457, rowp=5532))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-136.png', numpage=136, width=3778, height=5632, colp=305, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-137.png', numpage=137, width=3743, height=5632, colp=3453, rowp=5517))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-138.png', numpage=138, width=3778, height=5632, colp=329, rowp=5509))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-139.png', numpage=139, width=3743, height=5632, colp=3456, rowp=5527))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-140.png', numpage=140, width=3778, height=5632, colp=302, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-141.png', numpage=141, width=3743, height=5632, colp=3462, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-142.png', numpage=142, width=3778, height=5632, colp=331, rowp=5504))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-143.png', numpage=143, width=3743, height=5632, colp=3467, rowp=5527))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-144.png', numpage=144, width=3757, height=5632, colp=309, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-145.png', numpage=145, width=3743, height=5632, colp=3459, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-146.png', numpage=146, width=3778, height=5632, colp=313, rowp=5490))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-147.png', numpage=147, width=3743, height=5632, colp=3463, rowp=5513))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-148.png', numpage=148, width=3748, height=5446, colp=310, rowp=5445))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-149.png', numpage=149, width=3743, height=5632, colp=3469, rowp=5509))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-150.png', numpage=150, width=3757, height=5632, colp=328, rowp=5498))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-151.png', numpage=151, width=3743, height=5632, colp=3473, rowp=5514))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-152.png', numpage=152, width=3746, height=5632, colp=296, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-153.png', numpage=153, width=3743, height=5632, colp=3476, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-154.png', numpage=154, width=3729, height=5632, colp=295, rowp=5515))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-155.png', numpage=155, width=3743, height=5632, colp=3490, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-156.png', numpage=156, width=3703, height=5632, colp=258, rowp=5509))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-157.png', numpage=157, width=3743, height=5632, colp=3494, rowp=5504))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-158.png', numpage=158, width=3746, height=5632, colp=297, rowp=5507))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-159.png', numpage=159, width=3743, height=5632, colp=3483, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-160.png', numpage=160, width=3714, height=5632, colp=276, rowp=5505))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-161.png', numpage=161, width=3743, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-162.png', numpage=162, width=3778, height=5632, colp=302, rowp=5514))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-163.png', numpage=163, width=3743, height=5632, colp=3491, rowp=5533))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-164.png', numpage=164, width=3778, height=5632, colp=273, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-165.png', numpage=165, width=3743, height=5632, colp=3500, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-166.png', numpage=166, width=3748, height=5632, colp=290, rowp=5517))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-167.png', numpage=167, width=3743, height=5632, colp=3506, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-168.png', numpage=168, width=3778, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-169.png', numpage=169, width=3743, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-170.png', numpage=170, width=3778, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-171.png', numpage=171, width=3743, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS32\\3 BCI\\THS32-172.png', numpage=172, width=3714, height=5632, colp=None, rowp=None))



# Step 2 process data
finalwidthimpair = colpimpairmax+margedmax
margebmax = max(page.height-page.rowp for page in Pages if page.rowp)
finalheight = rowpmax+margebmax
margegmax = max(colppairmax-page.colp for page in Pages if page.colp and page.numpage % 2 == 0)
finalwidthpair = max(page.width+colppairmax-page.colp for page in Pages if page.colp and page.numpage % 2 == 0)
finalwidth = max(finalwidthpair, finalwidthimpair)
print("finalwidth:", finalwidth)
print("finalheight:", finalheight)

for page in Pages:
    if page.numpage<=200:
        #print(page)
        if page.numpage % 2 == 1:
            if page.colp:
                addmargeg = colpimpairmax-page.colp
                addmarged = margedmax-(page.width-page.colp)
            else:
                addmargeg = (finalwidth-page.width)//2
                addmarged = finalwidth-page.width-addmargeg
            newwidth = page.width+addmargeg+addmarged
            addmargeg += (finalwidth-newwidth)//2
            addmarged += (finalwidth-page.width-addmargeg-addmarged)
            #print('addmargeg', addmargeg, '  addmarged', addmarged, '  newwidth', newwidth)
        else:
            if page.colp:
                addmargeg = colppairmax-page.colp
                addmarged = finalwidth-page.width-addmargeg
            else:
                addmargeg = (finalwidth-page.width)//2
                addmarged = finalwidth-page.width-addmargeg
            newwidth = page.width+addmargeg+addmarged
            addmargeg += (finalwidth-newwidth)//2
            addmarged += (finalwidth-page.width-addmargeg-addmarged)
            #print('addmargeg', addmargeg, '  addmarged', addmarged, '  newwidth', newwidth)

        if page.rowp:
            addmargeh = rowpmax-page.rowp
            addmargeb = margebmax-(page.height-page.rowp)
        else:
            addmargeh = (finalheight-page.height)//2
            addmargeb = finalheight-page.height-addmargeh
        newheight = page.height+addmargeh+addmargeb
        #print('addmargeh', addmargeh, '  addmargeb', addmargeb, '  newheight', newheight)

        print(f'convert "{page.file}" -background white -extent {finalwidth}x{finalheight}-{addmargeg}-{addmargeh} "{dest}\\{prefix}-{page.numpage:0>3}.png"')
