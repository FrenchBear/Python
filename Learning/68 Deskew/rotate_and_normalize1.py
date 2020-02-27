# rotate_and_normalize1.py
# confirm that rotation creates gray
# 2020-02-25    PV


import matplotlib.pyplot as plt
import numpy as np
import os
import scipy
import skimage, skimage.io, skimage.transform
# from skimage.io import imread, imshow, show, imsave
# from skimage.transform import rotate
# from skimage import img_as_ubyte
# from skimage.filters import gaussian, threshold_otsu

filename = r'blocB.png'
image = skimage.io.imread(filename, as_gray=True)
s0 = np.mean(image)


# thresh = threshold_otsu(image)
# image = image > thresh

# # gaussian blur
# image = gaussian(image, 1)

# imshow(image)
# show()

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


x = []
y = []
yc = []
yd = []
ar = -1
iar = 0
while ar<1:
    imager = skimage.transform.rotate(image, ar, resize=True, mode='edge', order=3)
    (height, width) = imager.shape
    # deltarows = 4

    # delta = np.abs(imager[deltarows:]-imager[:-deltarows])
    # s = np.sum(delta)

    s = np.mean(imager)

    def gammafix(g):
        corrected = skimage.exposure.adjust_gamma(imager, g)
        return np.mean(corrected)-s0

    sol = scipy.optimize.root_scalar(gammafix, bracket=[0.8, 1.2])
    imagerc = skimage.exposure.adjust_gamma(imager, sol.root)
    sc = np.mean(imagerc)
    print(ar, sol.root, s, sc)


    deltarows = 4
    delta = np.abs(imagerc[deltarows:]-imagerc[:-deltarows])
    sd = np.sum(delta)

    x.append(ar)
    y.append(s)
    yc.append(sc)
    yd.append(sd)
    # imshow(delta)
    # show()

    # newfile = f"blocB{ar:.2f}.png"
    # print(newfile)
    # imsave(newfile, imager)

    iar += 1
    ar += 0.05

# x = moving_average(x)
# y = moving_average(y)
# ixmin = np.where(y == np.amin(y))[0][0]
# print('min index', ixmin, ' x=', x[ixmin], ' y=', y[ixmin])

# plt.plot(x, y)
# plt.plot(x, yc)
plt.plot(x, yd)
plt.show()
