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


# for pathfile in files1(rf'T:\Scans\THS67\2 Redressé'):
#     path, file = os.path.split(pathfile)
#     basename, ext = os.path.splitext(file)
#     if ext.lower() == '.png':
#         numpage = int(basename[-3:])
#         #if 5<=numpage<=10:
#         process(pathfile, numpage)

rowpmax= 5588
colppairmax= 393
colpimpairmax= 3595
margedmax= 387

Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-001.png', numpage=1, width=3907, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-003.png', numpage=3, width=3853, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-005.png', numpage=5, width=3875, height=5632, colp=3538, rowp=5477))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-007.png', numpage=7, width=3895, height=5632, colp=3590, rowp=5506))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-009.png', numpage=9, width=3887, height=5632, colp=3595, rowp=5535))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-011.png', numpage=11, width=3844, height=5632, colp=3553, rowp=5552))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-013.png', numpage=13, width=3844, height=5632, colp=3549, rowp=5574))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-015.png', numpage=15, width=3841, height=5632, colp=3541, rowp=5548))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-017.png', numpage=17, width=3861, height=5632, colp=3555, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-019.png', numpage=19, width=3833, height=5632, colp=3491, rowp=5557))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-021.png', numpage=21, width=3841, height=5632, colp=3501, rowp=5588))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-023.png', numpage=23, width=3812, height=5632, colp=3460, rowp=5566))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-025.png', numpage=25, width=3781, height=5632, colp=3424, rowp=5545))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-027.png', numpage=27, width=3813, height=5632, colp=3465, rowp=5528))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-029.png', numpage=29, width=3830, height=5632, colp=3455, rowp=5507))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-031.png', numpage=31, width=3813, height=5632, colp=3473, rowp=5507))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-033.png', numpage=33, width=3818, height=5632, colp=3456, rowp=5536))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-035.png', numpage=35, width=3766, height=5598, colp=3441, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-037.png', numpage=37, width=3832, height=5632, colp=3486, rowp=5504))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-039.png', numpage=39, width=3841, height=5632, colp=3506, rowp=5511))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-041.png', numpage=41, width=3832, height=5632, colp=3510, rowp=5529))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-043.png', numpage=43, width=3818, height=5632, colp=3509, rowp=5530))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-045.png', numpage=45, width=3829, height=5632, colp=3515, rowp=5546))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-047.png', numpage=47, width=3806, height=5632, colp=3482, rowp=5544))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-049.png', numpage=49, width=3818, height=5632, colp=3502, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-051.png', numpage=51, width=3821, height=5632, colp=3470, rowp=5529))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-053.png', numpage=53, width=3829, height=5632, colp=3473, rowp=5563))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-055.png', numpage=55, width=3841, height=5632, colp=3470, rowp=5566))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-057.png', numpage=57, width=3818, height=5632, colp=3445, rowp=5553))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-059.png', numpage=59, width=3812, height=5632, colp=3441, rowp=5546))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-061.png', numpage=61, width=3855, height=5586, colp=3490, rowp=5527))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-063.png', numpage=63, width=3821, height=5632, colp=3459, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-065.png', numpage=65, width=3829, height=5632, colp=3442, rowp=5541))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-067.png', numpage=67, width=3841, height=5632, colp=3480, rowp=5569))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-069.png', numpage=69, width=3829, height=5632, colp=3469, rowp=5535))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-071.png', numpage=71, width=3809, height=5632, colp=3490, rowp=5546))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-073.png', numpage=73, width=3818, height=5632, colp=3494, rowp=5583))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-075.png', numpage=75, width=3826, height=5632, colp=3518, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-077.png', numpage=77, width=3838, height=5632, colp=3527, rowp=5546))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-079.png', numpage=79, width=3826, height=5632, colp=3519, rowp=5536))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-081.png', numpage=81, width=3826, height=5632, colp=3521, rowp=5504))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-083.png', numpage=83, width=3826, height=5632, colp=3482, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-085.png', numpage=85, width=3826, height=5632, colp=3479, rowp=5556))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-087.png', numpage=87, width=3821, height=5632, colp=3472, rowp=5546))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-089.png', numpage=89, width=3810, height=5632, colp=3461, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-091.png', numpage=91, width=3861, height=5632, colp=3507, rowp=5565))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-093.png', numpage=93, width=3830, height=5632, colp=3464, rowp=5546))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-095.png', numpage=95, width=3784, height=5632, colp=3444, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-097.png', numpage=97, width=3838, height=5632, colp=3482, rowp=5557))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-099.png', numpage=99, width=3841, height=5632, colp=3494, rowp=5532))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-101.png', numpage=101, width=3841, height=5632, colp=3513, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-103.png', numpage=103, width=3841, height=5632, colp=3520, rowp=5547))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-105.png', numpage=105, width=3844, height=5632, colp=3546, rowp=5556))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-107.png', numpage=107, width=3830, height=5632, colp=3547, rowp=5535))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-109.png', numpage=109, width=3838, height=5632, colp=3550, rowp=5544))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-111.png', numpage=111, width=3830, height=5632, colp=3533, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-113.png', numpage=113, width=3858, height=5632, colp=3562, rowp=5515))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-115.png', numpage=115, width=3827, height=5632, colp=3478, rowp=5546))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-117.png', numpage=117, width=3832, height=5632, colp=3485, rowp=5553))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-119.png', numpage=119, width=3881, height=5632, colp=3505, rowp=5552))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-121.png', numpage=121, width=3841, height=5632, colp=3475, rowp=5540))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-123.png', numpage=123, width=3829, height=5632, colp=3464, rowp=5550))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-125.png', numpage=125, width=3832, height=5632, colp=3471, rowp=5538))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-127.png', numpage=127, width=3841, height=5632, colp=3491, rowp=5542))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-129.png', numpage=129, width=3824, height=5632, colp=3474, rowp=5545))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-131.png', numpage=131, width=3844, height=5632, colp=3493, rowp=5538))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-133.png', numpage=133, width=3841, height=5632, colp=3486, rowp=5538))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-135.png', numpage=135, width=3838, height=5632, colp=3525, rowp=5544))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-137.png', numpage=137, width=3844, height=5632, colp=3537, rowp=5549))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-139.png', numpage=139, width=3852, height=5632, colp=3545, rowp=5530))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-141.png', numpage=141, width=3850, height=5632, colp=3545, rowp=5534))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-143.png', numpage=143, width=3856, height=5632, colp=3552, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-145.png', numpage=145, width=3861, height=5632, colp=3550, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-147.png', numpage=147, width=3869, height=5632, colp=3516, rowp=5540))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-149.png', numpage=149, width=3861, height=5632, colp=3502, rowp=5549))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-151.png', numpage=151, width=3867, height=5632, colp=3501, rowp=5535))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-153.png', numpage=153, width=3884, height=5632, colp=3519, rowp=5536))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-155.png', numpage=155, width=3867, height=5632, colp=3506, rowp=5552))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-157.png', numpage=157, width=3873, height=5632, colp=3488, rowp=5553))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-159.png', numpage=159, width=3893, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-161.png', numpage=161, width=3812, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\1\\THS67-163.png', numpage=163, width=3960, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-002.png', numpage=2, width=3944, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-004.png', numpage=4, width=3820, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-006.png', numpage=6, width=3916, height=5632, colp=334, rowp=5504))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-008.png', numpage=8, width=3870, height=5632, colp=319, rowp=5483))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-010.png', numpage=10, width=3875, height=5632, colp=309, rowp=5510))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-012.png', numpage=12, width=3884, height=5632, colp=310, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-014.png', numpage=14, width=3893, height=5632, colp=307, rowp=5543))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-016.png', numpage=16, width=3849, height=5627, colp=306, rowp=5565))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-018.png', numpage=18, width=3849, height=5632, colp=307, rowp=5544))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-020.png', numpage=20, width=3873, height=5632, colp=367, rowp=5531))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-022.png', numpage=22, width=3864, height=5632, colp=359, rowp=5557))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-024.png', numpage=24, width=3852, height=5632, colp=374, rowp=5587))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-026.png', numpage=26, width=3855, height=5632, colp=376, rowp=5564))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-028.png', numpage=28, width=3864, height=5632, colp=376, rowp=5550))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-030.png', numpage=30, width=3864, height=5632, colp=393, rowp=5517))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-032.png', numpage=32, width=3887, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-034.png', numpage=34, width=3841, height=5632, colp=360, rowp=5507))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-036.png', numpage=36, width=3818, height=5632, colp=322, rowp=5515))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-038.png', numpage=38, width=3861, height=5632, colp=356, rowp=5493))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-040.png', numpage=40, width=3873, height=5632, colp=345, rowp=5497))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-042.png', numpage=42, width=3861, height=5632, colp=335, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-044.png', numpage=44, width=3852, height=5632, colp=335, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-046.png', numpage=46, width=3873, height=5632, colp=340, rowp=5541))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-048.png', numpage=48, width=3861, height=5632, colp=346, rowp=5541))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-050.png', numpage=50, width=3852, height=5632, colp=327, rowp=5514))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-052.png', numpage=52, width=3852, height=5632, colp=367, rowp=5518))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-054.png', numpage=54, width=3841, height=5632, colp=352, rowp=5553))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-056.png', numpage=56, width=3812, height=5632, colp=347, rowp=5558))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-058.png', numpage=58, width=3829, height=5632, colp=363, rowp=5546))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-060.png', numpage=60, width=3850, height=5632, colp=383, rowp=5547))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-062.png', numpage=62, width=3820, height=5632, colp=370, rowp=5513))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-064.png', numpage=64, width=3820, height=5632, colp=362, rowp=5503))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-066.png', numpage=66, width=3841, height=5632, colp=382, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-068.png', numpage=68, width=3818, height=5632, colp=338, rowp=5557))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-070.png', numpage=70, width=3833, height=5632, colp=350, rowp=5529))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-072.png', numpage=72, width=3850, height=5632, colp=350, rowp=5523))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-074.png', numpage=74, width=3873, height=5632, colp=348, rowp=5548))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-076.png', numpage=76, width=3861, height=5632, colp=339, rowp=5494))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-078.png', numpage=78, width=3841, height=5632, colp=314, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-080.png', numpage=80, width=3855, height=5632, colp=318, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-082.png', numpage=82, width=3853, height=5632, colp=313, rowp=5497))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-084.png', numpage=84, width=3832, height=5632, colp=350, rowp=5492))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-086.png', numpage=86, width=3853, height=5632, colp=361, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-088.png', numpage=88, width=3838, height=5632, colp=364, rowp=5541))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-090.png', numpage=90, width=3861, height=5632, colp=369, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-092.png', numpage=92, width=3832, height=5632, colp=353, rowp=5570))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-094.png', numpage=94, width=3821, height=5632, colp=366, rowp=5531))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-096.png', numpage=96, width=3870, height=5632, colp=393, rowp=5492))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-098.png', numpage=98, width=3861, height=5632, colp=387, rowp=5538))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-100.png', numpage=100, width=3872, height=5632, colp=375, rowp=5528))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-102.png', numpage=102, width=3830, height=5632, colp=340, rowp=5525))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-104.png', numpage=104, width=3841, height=5632, colp=338, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-106.png', numpage=106, width=3826, height=5632, colp=310, rowp=5527))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-108.png', numpage=108, width=3824, height=5632, colp=295, rowp=5511))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-110.png', numpage=110, width=3841, height=5632, colp=305, rowp=5519))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-112.png', numpage=112, width=3841, height=5632, colp=309, rowp=5534))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-114.png', numpage=114, width=3821, height=5632, colp=296, rowp=5525))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-116.png', numpage=116, width=3853, height=5632, colp=379, rowp=5520))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-118.png', numpage=118, width=3829, height=5632, colp=354, rowp=5532))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-120.png', numpage=120, width=3829, height=5632, colp=362, rowp=5553))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-122.png', numpage=122, width=3829, height=5632, colp=366, rowp=5548))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-124.png', numpage=124, width=3841, height=5632, colp=376, rowp=5560))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-126.png', numpage=126, width=3861, height=5632, colp=379, rowp=5544))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-128.png', numpage=128, width=3841, height=5632, colp=367, rowp=5501))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-130.png', numpage=130, width=3849, height=5632, colp=380, rowp=5507))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-132.png', numpage=132, width=3861, height=5632, colp=373, rowp=5513))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-134.png', numpage=134, width=3861, height=5632, colp=378, rowp=5530))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-136.png', numpage=136, width=3844, height=5632, colp=323, rowp=5531))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-138.png', numpage=138, width=3853, height=5632, colp=313, rowp=5528))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-140.png', numpage=140, width=3856, height=5632, colp=322, rowp=5505))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-142.png', numpage=142, width=3855, height=5632, colp=317, rowp=5513))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-144.png', numpage=144, width=3833, height=5632, colp=308, rowp=5516))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-146.png', numpage=146, width=3856, height=5632, colp=311, rowp=5510))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-148.png', numpage=148, width=3861, height=5632, colp=355, rowp=5526))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-150.png', numpage=150, width=3884, height=5632, colp=362, rowp=5521))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-152.png', numpage=152, width=3904, height=5632, colp=382, rowp=5524))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-154.png', numpage=154, width=3881, height=5632, colp=376, rowp=5529))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-156.png', numpage=156, width=3852, height=5632, colp=343, rowp=5545))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-158.png', numpage=158, width=3916, height=5624, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-160.png', numpage=160, width=3907, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-162.png', numpage=162, width=3960, height=5632, colp=None, rowp=None))
Pages.append(ScannedPage(file='T:\\Scans\\THS67\\2 Redressé\\2\\THS67-164.png', numpage=164, width=3861, height=5632, colp=None, rowp=None))

# print()
# print('rowpmax=', repr(rowpmax))
# print('colppairmax=', repr(colppairmax))
# print('colpimpairmax=', repr(colpimpairmax))
# print('margedmax=', repr(margedmax))

print()

# for page in Pages:
#     print("Pages.append("+repr(page)+")")

finalwidthimpair = colpimpairmax+margedmax
finalheight = rowpmax+margebmax
margegmax = max(colppairmax-page.colp for page in Pages if page.colp and page.numpage % 2 == 0)
margebmax = max(page.height-page.rowp for page in Pages if page.rowp)
finalwidthpair = max(page.width+colppairmax-page.colp for page in Pages if page.colp and page.numpage % 2 == 0)
finalwidth = max(finalwidthpair, finalwidthimpair)
print("finalwidth:", finalwidth)

for page in Pages:
    if page.numpage<=20:
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

        print(f'convert "{page.file}" -background red -extent {finalwidth}x{finalheight}-{addmargeg}-{addmargeh} C:\\temp\\page{page.numpage:0>3}.png')
