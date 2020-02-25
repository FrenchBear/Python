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

    if 4<numpage<160:
        if numpage % 2 == 0:
            r = range(0, areawidth)
        else:
            r = range(areawidth-1, -1, -1)
        for col in r:
            n = (area[:, col] < 0.05).sum()
            if n >= 50:
                colp = col+colmin
                break

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
# source=r'C:\Scans\THS23\3 Crop Vt'
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
rowpmax= 5541
colppairmax= 391
colpimpairmax= 3700
margedmax= 325

Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-001.png', numpage=1, width=3858, height=5612, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-002.png', numpage=2, width=3801, height=5612, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-003.png', numpage=3, width=3789, height=5612, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-004.png', numpage=4, width=3874, height=5612, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-005.png', numpage=5, width=3892, height=5612, colp=3700, rowp=5494))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-006.png', numpage=6, width=3892, height=5612, colp=300, rowp=5495))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-007.png', numpage=7, width=3864, height=5612, colp=3575, rowp=5485))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-008.png', numpage=8, width=3793, height=5612, colp=242, rowp=5481))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-009.png', numpage=9, width=3864, height=5612, colp=3559, rowp=5495))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-010.png', numpage=10, width=3859, height=5612, colp=298, rowp=5485))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-011.png', numpage=11, width=3828, height=5612, colp=3540, rowp=5483))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-012.png', numpage=12, width=3867, height=5612, colp=300, rowp=5478))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-013.png', numpage=13, width=3854, height=5612, colp=3548, rowp=5497))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-014.png', numpage=14, width=3869, height=5612, colp=322, rowp=5487))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-015.png', numpage=15, width=3841, height=5612, colp=3544, rowp=5496))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-016.png', numpage=16, width=3865, height=5612, colp=286, rowp=5477))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-017.png', numpage=17, width=3845, height=5604, colp=3542, rowp=5495))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-018.png', numpage=18, width=3869, height=5612, colp=333, rowp=5483))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-019.png', numpage=19, width=3836, height=5612, colp=3532, rowp=5493))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-020.png', numpage=20, width=3839, height=5612, colp=298, rowp=5473))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-021.png', numpage=21, width=3845, height=5612, colp=3559, rowp=5503))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-022.png', numpage=22, width=3865, height=5612, colp=330, rowp=5491))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-023.png', numpage=23, width=3830, height=5612, colp=3531, rowp=5490))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-024.png', numpage=24, width=3853, height=5612, colp=297, rowp=5476))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-025.png', numpage=25, width=3823, height=5612, colp=3515, rowp=5503))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-026.png', numpage=26, width=3865, height=5612, colp=332, rowp=5487))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-027.png', numpage=27, width=3823, height=5612, colp=3531, rowp=5488))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-028.png', numpage=28, width=3845, height=5612, colp=307, rowp=5478))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-029.png', numpage=29, width=3791, height=5612, colp=3499, rowp=5503))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-030.png', numpage=30, width=3866, height=5612, colp=342, rowp=5480))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-031.png', numpage=31, width=3806, height=5612, colp=3515, rowp=5489))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-032.png', numpage=32, width=3814, height=5612, colp=285, rowp=5474))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-033.png', numpage=33, width=3806, height=5612, colp=3509, rowp=5507))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-034.png', numpage=34, width=3861, height=5612, colp=371, rowp=5485))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-035.png', numpage=35, width=3809, height=5612, colp=3510, rowp=5495))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-036.png', numpage=36, width=3863, height=5612, colp=331, rowp=5475))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-037.png', numpage=37, width=3794, height=5612, colp=3492, rowp=5505))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-038.png', numpage=38, width=3853, height=5612, colp=366, rowp=5484))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-039.png', numpage=39, width=3803, height=5612, colp=3505, rowp=5493))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-040.png', numpage=40, width=3855, height=5612, colp=332, rowp=5475))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-041.png', numpage=41, width=3801, height=5612, colp=3484, rowp=5516))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-042.png', numpage=42, width=3865, height=5612, colp=377, rowp=5491))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-043.png', numpage=43, width=3801, height=5612, colp=3496, rowp=5494))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-044.png', numpage=44, width=3863, height=5612, colp=339, rowp=5464))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-045.png', numpage=45, width=3797, height=5612, colp=3489, rowp=5505))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-046.png', numpage=46, width=3859, height=5612, colp=366, rowp=5485))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-047.png', numpage=47, width=3791, height=5612, colp=3489, rowp=5489))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-048.png', numpage=48, width=3863, height=5612, colp=346, rowp=5478))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-049.png', numpage=49, width=3791, height=5612, colp=3490, rowp=5507))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-050.png', numpage=50, width=3857, height=5612, colp=366, rowp=5499))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-051.png', numpage=51, width=3791, height=5612, colp=3504, rowp=5492))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-052.png', numpage=52, width=3864, height=5612, colp=363, rowp=5481))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-053.png', numpage=53, width=3782, height=5612, colp=3475, rowp=5508))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-054.png', numpage=54, width=3857, height=5612, colp=389, rowp=5493))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-055.png', numpage=55, width=3815, height=5612, colp=3518, rowp=5485))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-056.png', numpage=56, width=3864, height=5612, colp=354, rowp=5467))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-057.png', numpage=57, width=3779, height=5612, colp=3470, rowp=5491))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-058.png', numpage=58, width=3863, height=5612, colp=391, rowp=5476))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-059.png', numpage=59, width=3782, height=5612, colp=3468, rowp=5497))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-060.png', numpage=60, width=3837, height=5612, colp=339, rowp=5475))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-061.png', numpage=61, width=3774, height=5612, colp=3468, rowp=5498))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-062.png', numpage=62, width=3864, height=5612, colp=389, rowp=5484))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-063.png', numpage=63, width=3771, height=5612, colp=3458, rowp=5488))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-064.png', numpage=64, width=3865, height=5612, colp=373, rowp=5455))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-065.png', numpage=65, width=3777, height=5612, colp=3463, rowp=5500))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-066.png', numpage=66, width=3865, height=5612, colp=391, rowp=5470))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-067.png', numpage=67, width=3775, height=5612, colp=3469, rowp=5492))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-068.png', numpage=68, width=3786, height=5612, colp=295, rowp=5458))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-069.png', numpage=69, width=3773, height=5612, colp=3463, rowp=5504))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-070.png', numpage=70, width=3795, height=5612, colp=326, rowp=5488))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-071.png', numpage=71, width=3775, height=5612, colp=3458, rowp=5495))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-072.png', numpage=72, width=3844, height=5612, colp=343, rowp=5454))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-073.png', numpage=73, width=3760, height=5612, colp=3456, rowp=5496))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-074.png', numpage=74, width=3841, height=5612, colp=377, rowp=5465))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-075.png', numpage=75, width=3777, height=5612, colp=3473, rowp=5484))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-076.png', numpage=76, width=3841, height=5612, colp=338, rowp=5462))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-077.png', numpage=77, width=3775, height=5612, colp=3460, rowp=5492))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-078.png', numpage=78, width=3863, height=5612, colp=388, rowp=5414))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-079.png', numpage=79, width=3782, height=5612, colp=3470, rowp=5485))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-080.png', numpage=80, width=3802, height=5612, colp=316, rowp=5463))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-081.png', numpage=81, width=3771, height=5612, colp=3461, rowp=5495))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-082.png', numpage=82, width=3853, height=5612, colp=379, rowp=5478))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-083.png', numpage=83, width=3770, height=5612, colp=3477, rowp=5487))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-084.png', numpage=84, width=3855, height=5612, colp=358, rowp=5472))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-085.png', numpage=85, width=3773, height=5612, colp=3474, rowp=5500))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-086.png', numpage=86, width=3855, height=5612, colp=371, rowp=5480))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-087.png', numpage=87, width=3770, height=5612, colp=3468, rowp=5484))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-088.png', numpage=88, width=3855, height=5612, colp=364, rowp=5467))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-089.png', numpage=89, width=3770, height=5612, colp=3464, rowp=5495))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-090.png', numpage=90, width=3851, height=5612, colp=369, rowp=5477))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-091.png', numpage=91, width=3791, height=5642, colp=3486, rowp=5494))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-092.png', numpage=92, width=3790, height=5642, colp=308, rowp=5509))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-093.png', numpage=93, width=3814, height=5642, colp=3524, rowp=5509))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-094.png', numpage=94, width=3771, height=5642, colp=312, rowp=5521))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-095.png', numpage=95, width=3790, height=5642, colp=3501, rowp=5492))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-096.png', numpage=96, width=3764, height=5642, colp=285, rowp=5498))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-097.png', numpage=97, width=3782, height=5642, colp=3481, rowp=5503))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-098.png', numpage=98, width=3804, height=5642, colp=316, rowp=5524))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-099.png', numpage=99, width=3793, height=5642, colp=3486, rowp=5491))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-100.png', numpage=100, width=3790, height=5642, colp=295, rowp=5486))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-101.png', numpage=101, width=3785, height=5642, colp=3487, rowp=5500))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-102.png', numpage=102, width=3816, height=5642, colp=325, rowp=5513))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-103.png', numpage=103, width=3785, height=5642, colp=3490, rowp=5489))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-104.png', numpage=104, width=3751, height=5637, colp=287, rowp=5490))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-105.png', numpage=105, width=3776, height=5637, colp=3482, rowp=5497))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-106.png', numpage=106, width=3782, height=5642, colp=325, rowp=5517))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-107.png', numpage=107, width=3785, height=5642, colp=3482, rowp=5499))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-108.png', numpage=108, width=3797, height=5642, colp=304, rowp=5506))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-109.png', numpage=109, width=3790, height=5642, colp=3482, rowp=5513))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-110.png', numpage=110, width=3803, height=5642, colp=319, rowp=5541))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-111.png', numpage=111, width=3779, height=5642, colp=3482, rowp=5515))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-112.png', numpage=112, width=3802, height=5642, colp=299, rowp=5526))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-113.png', numpage=113, width=3782, height=5642, colp=3493, rowp=5505))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-114.png', numpage=114, width=3771, height=5642, colp=333, rowp=5524))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-115.png', numpage=115, width=3773, height=5642, colp=3482, rowp=5490))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-116.png', numpage=116, width=3800, height=5642, colp=286, rowp=5498))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-117.png', numpage=117, width=3692, height=5642, colp=3404, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-118.png', numpage=118, width=3795, height=5642, colp=314, rowp=5523))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-119.png', numpage=119, width=3793, height=5642, colp=3495, rowp=5487))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-120.png', numpage=120, width=3793, height=5642, colp=288, rowp=5499))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-121.png', numpage=121, width=3789, height=5642, colp=3493, rowp=5500))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-122.png', numpage=122, width=3800, height=5642, colp=318, rowp=5519))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-123.png', numpage=123, width=3814, height=5642, colp=3499, rowp=5495))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-124.png', numpage=124, width=3797, height=5642, colp=284, rowp=5498))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-125.png', numpage=125, width=3779, height=5642, colp=3489, rowp=5510))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-126.png', numpage=126, width=3759, height=5642, colp=293, rowp=5533))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-127.png', numpage=127, width=3788, height=5642, colp=3506, rowp=5501))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-128.png', numpage=128, width=3764, height=5625, colp=291, rowp=5516))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-129.png', numpage=129, width=3779, height=5642, colp=3497, rowp=5515))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-130.png', numpage=130, width=3813, height=5642, colp=323, rowp=5516))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-131.png', numpage=131, width=3834, height=5642, colp=3509, rowp=5493))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-132.png', numpage=132, width=3776, height=5642, colp=303, rowp=5492))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-133.png', numpage=133, width=3783, height=5642, colp=3488, rowp=5511))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-134.png', numpage=134, width=3747, height=5637, colp=292, rowp=5506))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-135.png', numpage=135, width=3814, height=5642, colp=3517, rowp=5491))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-136.png', numpage=136, width=3813, height=5642, colp=280, rowp=5479))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-137.png', numpage=137, width=3816, height=5642, colp=3519, rowp=5506))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-138.png', numpage=138, width=3803, height=5642, colp=307, rowp=5508))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-139.png', numpage=139, width=3825, height=5642, colp=3522, rowp=5493))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-140.png', numpage=140, width=3773, height=5642, colp=287, rowp=5489))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-141.png', numpage=141, width=3816, height=5642, colp=3519, rowp=5508))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-142.png', numpage=142, width=3776, height=5642, colp=316, rowp=5515))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-143.png', numpage=143, width=3837, height=5642, colp=3531, rowp=5496))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-144.png', numpage=144, width=3776, height=5642, colp=283, rowp=5487))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-145.png', numpage=145, width=3825, height=5642, colp=3530, rowp=5508))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-146.png', numpage=146, width=3831, height=5642, colp=309, rowp=5517))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-147.png', numpage=147, width=3828, height=5642, colp=3535, rowp=5492))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-148.png', numpage=148, width=3805, height=5642, colp=294, rowp=5500))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-149.png', numpage=149, width=3842, height=5642, colp=3541, rowp=5506))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-150.png', numpage=150, width=3814, height=5642, colp=313, rowp=5520))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-151.png', numpage=151, width=3845, height=5642, colp=3547, rowp=5491))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-152.png', numpage=152, width=3799, height=5634, colp=291, rowp=5493))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-153.png', numpage=153, width=3828, height=5642, colp=3543, rowp=5506))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-154.png', numpage=154, width=3861, height=5642, colp=314, rowp=5521))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-155.png', numpage=155, width=3845, height=5642, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-156.png', numpage=156, width=3866, height=5642, colp=307, rowp=5500))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-157.png', numpage=157, width=3873, height=5642, colp=3556, rowp=5509))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-158.png', numpage=158, width=3846, height=5642, colp=313, rowp=5515))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-159.png', numpage=159, width=3873, height=5642, colp=3550, rowp=5516))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-160.png', numpage=160, width=3881, height=5642, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-161.png', numpage=161, width=3867, height=5642, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-162.png', numpage=162, width=3814, height=5616, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-163.png', numpage=163, width=3813, height=5642, colp=None, rowp=None))
Pages.append(ScannedPage(file='C:\\Scans\\THS23\\3 Crop Vt\\THS23-164.png', numpage=164, width=3815, height=5642, colp=None, rowp=None))



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

        print(f'convert "{page.file}" -background white -extent {finalwidth}x{finalheight}-{addmargeg}-{addmargeh} "C:\\Scans\\THS23\\4 Align Resize\\THS23-{page.numpage:0>3}.png"')
