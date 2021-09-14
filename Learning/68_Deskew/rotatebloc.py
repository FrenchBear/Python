from skimage.io import imread, imshow, show, imsave
from skimage.transform import rotate
from skimage import img_as_ubyte
import matplotlib.pyplot as plt
import numpy as np
import os

filename = r'blocB.png'
image = imread(filename, as_gray=True)


from skimage.filters import gaussian, threshold_otsu

thresh = threshold_otsu(image)
image = image > thresh

# gaussian blur
image = gaussian(image, 1)

imshow(image)
show()

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


x = []
y = []
ar = -1
iar = 0
while ar<1:
    imager = rotate(image, ar, resize=True, mode='edge', order=3)
    (height, width) = imager.shape
    deltarows = 4

    delta = np.abs(imager[deltarows:]-imager[:-deltarows])
    s = np.sum(delta)
    x.append(ar)
    y.append(s)
    print(ar, s)
    
    # imshow(delta)
    # show()

    # newfile = f"blocB{ar:.2f}.png"
    # print(newfile)
    # imsave(newfile, imager)

    iar += 1
    ar += 0.05

x = moving_average(x)
y = moving_average(y)

ixmin = np.where(y == np.amin(y))[0][0]
print('min index', ixmin, ' x=', x[ixmin], ' y=', y[ixmin])

plt.plot(x, y)
plt.show()
