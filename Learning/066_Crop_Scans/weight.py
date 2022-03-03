import matplotlib.pyplot as plt         # type: ignore
import matplotlib.image as mpimg        # type: ignore
import numpy as np
from scipy.signal import find_peaks     # type: ignore

img = mpimg.imread('T18-050.png')
# print(img.shape)
width = img.shape[1]
print("width=", width)

# Using matplotlib and the formula
# Y' = 0.2989 R + 0.5870 G + 0.1140 B


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


gray = rgb2gray(img)
# print(gray)
#plt.imshow(gray, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
# plt.show()

#columns_average = gray.mean(axis=0)
columns_average = np.median(gray, axis=0)
print(columns_average)
print(columns_average.shape)

#plt.plot(columns_average)
#plt.show()


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


ca2 = moving_average(columns_average, 10)
#plt.plot(ca2)
#plt.show()


def difflist(ret, n):
    return np.abs(ret[n:] - ret[:-n])

cd = difflist(ca2, 1)
peaks, _ = find_peaks(cd, distance=150)
# difference between peaks is >= 150
print(peaks)
print(cd[peaks])

plt.plot(cd)
plt.plot(peaks, cd[peaks], 'x')
plt.show()

pmin = 0
pmax = 0
for i in range(3):
    if cd[peaks[i]] > 1e-3:
        pmin = peaks[i]+18
        break
for i in range(3):
    if cd[peaks[-i-1]] > 1e-3:
        pmax = peaks[-i-1]
        break

#pmin = peaks[0]+15
#pmax = peaks[-1]

if pmin > 275:
    pmin = 0
if pmax < width-275:
    pmax = width

print("crop", pmin, "to", pmax)

#img[:,0:pmin,1] = 1
#img[:,pmax:width,1] = 1
# print(img)

img2 = img[:, pmin:pmax, :]
plt.imshow(img2)
plt.show()
