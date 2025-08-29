# test_rotate.py
# Experiments various options for mode parameter of skimage.transform.rotate
#
# 2024-08-29    PV      First version

import numpy as np
from skimage.transform import rotate
from skimage.io import imread, imsave

source = r"C:\PicturesODMisc\THS\Scans\T77\T77P017.jpg"
modes = ['constant', 'edge', 'symmetric', 'reflect', 'wrap']

for mode in modes:
    print(f"Mode: {mode}")
    rotated_img = rotate(imread(source), 10, resize=True, mode=mode)
    imsave(rf"C:\Temp\T77P017_rotated_{mode}.png", (rotated_img * 255).astype(np.uint8))
