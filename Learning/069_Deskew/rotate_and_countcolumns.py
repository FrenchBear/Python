# rotate_and_countcolumns.py
# After rotation, count black columns
#
# 2020-02-25    PV


import matplotlib.pyplot as plt         # type: ignore
import numpy as np
import skimage                          # type: ignore
import skimage.io                       # type: ignore
import skimage.transform                # type: ignore

filename = r'blocA.png'
image = skimage.io.imread(filename, as_gray=True)


# (height, width) = image.shape
# blackarea = image > 0.6
# bpc = np.sum(blackarea, axis=0)

# # skimage.io.imshow(blackarea)
# # skimage.io.show()

# condition = (bpc>=height*.75) & (bpc<=height*.95)
# bpc = np.extract(condition, bpc)

# plt.plot(bpc)
# plt.show()


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


x = []
y = []

ar:float = -1.0
iar = 0
while ar < 1:
    imager = skimage.transform.rotate(image, ar, resize=True, mode='edge', order=3)
    (height, width) = imager.shape

    blackarea = imager > 0.6
    bpc = np.sum(blackarea, axis=0)
    condition = bpc>=height*.8
    bpc = np.extract(condition, bpc)
    s = sum(bpc)
    l = bpc.shape[0]

    print(f"{ar:.3}  {s:>5}  {l}")

    x.append(ar)
    y.append(l)

    iar += 1
    ar += 0.05

plt.plot(x, y)
plt.show()
