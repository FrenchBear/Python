# ResizeDilbert
# Final processing of pages
#
# 2022-01-06    PV      Complete version
# 2022-01-07    PV      Yellow autocalibration
# 2022-01-08    PV      Multiple values for num_backcolor
# 2022-03-21    PV      TangenteHS version simplified for Dilbert, just cropping, with BW support and crop optimizations.  Use PIL.Image for BW save in a grayscale jpg

import os
from dataclasses import dataclass
import numpy as np
import matplotlib.image as mpimg  # type: ignore
import cropimage
from common_fs import get_all_files
import PIL.Image as Image


def crop_white_borders_bw(img: np.ndarray) -> np.ndarray:
    BLACK_THRESHOLD = 10
    BLACK_COUNT = 20
    MAX_BORDER = 300

    emptypass = 0
    while True:
        # Crop top and bottom
        blackrows = np.sum(img < BLACK_THRESHOLD, axis=1)
        for top in range(MAX_BORDER):  # range(img.shape[0]//2):
            if blackrows[top] > BLACK_COUNT:
                break
        else:
            top = 0
        for bottom in range(MAX_BORDER):
            if blackrows[-1 - bottom] > BLACK_COUNT:
                break
        else:
            bottom = 0
        if top == 0 and bottom == 0:
            emptypass += 1
            if emptypass >= 2:
                break
        else:
            emptypass = 0
            if bottom > 0:
                img = img[: -1 - bottom + 1, :]
            if top > 0:
                img = img[top:, :]

        # crop left and right
        blackcols = np.sum(img < BLACK_THRESHOLD, axis=0)
        for left in range(MAX_BORDER):
            if blackcols[left] > BLACK_COUNT:
                break
        else:
            left = 0
        for right in range(MAX_BORDER):
            if blackcols[-1 - right] > BLACK_COUNT:
                break
        else:
            right = 0
        if left == 0 and right == 0:
            emptypass += 1
            if emptypass >= 2:
                break
        else:
            emptypass = 0
            if right > 0:
                img = img[:, : -1 - right]
            if left > 0:
                img = img[:, left:]

    return img


"""
source = r'D:\Scans\Images\Dilbert3\1\Scan0017.jpg'
target = r'D:\Scans\Images\Dilbert3\2\Scan0017.jpg'
buffer = mpimg.imread(source)
if len(buffer.shape) == 3:
    img = buffer[:, :, :3]
    color = True
else:
    #img = buffer[:, :]
    img = buffer
    color = False

if color:
    img = (np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])+0.5).astype(int)
    color = False
img = crop_white_borders_bw(img)

width: int = img.shape[1]
height: int = img.shape[0]

width_m = 2460
height_m = 3530

tins = (height_m-height)//2
bins = height_m-height-tins
lins = (width_m-width)//2
rins = width_m-width-lins

tins = bins = lins = rins = 0

if color:
    img = cropimage.crop_color_image(img, tins, bins, lins, rins)
else:
    img = cropimage.crop_bw_image_white_borders(img, tins, bins, lins, rins)

# Save
if color:
    mpimg.imsave(target, img, format='jpg', dpi=300, cmap='gray')
else:
    pimg = Image.fromarray(img)
    pimg.save(r'target', dpi=(300,300), quality=80)

sys.exit(0)
"""


@dataclass
class ScannedPage:
    file: str
    numfile: int
    width: int
    height: int
    color: bool


Pages = []


def process(file: str, numfile: int):
    print(file, "\t", sep="", end="")

    global Pages
    color: bool
    buffer = mpimg.imread(file)
    if len(buffer.shape) == 3:
        img = buffer[:, :, :3]
        color = True
    else:
        img = buffer[:, :]
        color = False

    width: int = img.shape[1]
    height: int = img.shape[0]
    print(width, "x", height, "\t", "Color" if color else "BW", "\t", sep="", end="")

    newpage = ScannedPage(file, numfile, width, height, color)
    Pages.append(newpage)


def process_root(root: str):
    """
    global Pages

    source = os.path.join(root, '1')
    dest = os.path.join(root, '2')

    if not os.path.isdir(dest):
        os.mkdir(dest)

    for filefp in get_all_files(source):
        path, filename = os.path.split(filefp)
        base, ext = os.path.splitext(filename)
        if ext.lower() == '.jpg':
            nf = int(base[-3:])
            process(filefp, nf)
        print()

    # Determinate median value for cropping
    widths = []
    heights = []
    for page in Pages:
        widths.append(page.width)
        heights.append(page.height)

    width_m = int(statistics.median(widths))
    height_m = int(statistics.median(heights))

    breakpoint()

    print(f'{width_m=}')
    print(f'{height_m=}')

    with open(os.path.join(root, 'Pages.py'), 'w', encoding='utf-8') as fout:
        for page in Pages:
            print(repr(page).replace('ScannedPage', 'p'))
            fout.write(repr(page).replace('ScannedPage', 'p')+'\n')
        fout.write('\n')
        fout.write(f'{width_m=}\n')
        fout.write(f'{height_m=}\n')
    """

    # Finally fixed the value, identical for all books
    width_m = 2460
    height_m = 3530

    source = os.path.join(root, "1")
    dest = os.path.join(root, "2")
    if not os.path.isdir(dest):
        os.mkdir(dest)

    for ix, filefp in enumerate(get_all_files(source)):
        path, filename = os.path.split(filefp)
        base, ext = os.path.splitext(filename)
        if ext.lower() == ".jpg":
            print(filename)
            target = os.path.join(dest, filename)

            # If the target already exist and is more recent than source, no need to do it again
            # if os.path.isfile(target) and os.path.getmtime(target) > os.path.getmtime(page.file):
            #     continue

            color: bool
            buffer = mpimg.imread(filefp)
            if len(buffer.shape) == 3:
                img = buffer[:, :, :3]
                color = True
            else:
                img = buffer[:, :]
                color = False

            pmax = 91
            pmax = 83  # For # 7
            if 0 < ix < pmax and color:
                img = (np.dot(img[..., :3], [0.2989, 0.5870, 0.1140]) + 0.5).astype(
                    np.uint8
                )
                color = False

            if not color:
                img = crop_white_borders_bw(img)

            width: int = img.shape[1]
            height: int = img.shape[0]

            tins = (height_m - height) // 2
            bins = height_m - height - tins
            lins = (width_m - width) // 2
            rins = width_m - width - lins

            if color:
                img = cropimage.crop_color_image(img, tins, bins, lins, rins)
            else:
                img = cropimage.crop_bw_image_white_borders(img, tins, bins, lins, rins)

            if color:
                mpimg.imsave(target, img, format="jpg", dpi=300)
            else:
                # use PIL.image to save a real grayscale jpg, since mpimg.save always create a 24-bit depth jpg
                pimg = Image.fromarray(img)
                pimg.save(target, dpi=(300, 300), quality=80)


process_root("D:\Scans\Images\Dilbert8")
