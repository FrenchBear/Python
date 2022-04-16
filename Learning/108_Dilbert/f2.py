import numpy as np
import matplotlib.image as mpimg    # type: ignore

# img = np.array([[1, 2], [3, 4], [5, 6]])    # BW
# x = np.sum(img>3, axis=1)
# print(x)

img = mpimg.imread(r'D:\Scans\Images\Dilbert2\1\Scan0009.jpg')
x = np.sum(img<10, axis=1)
print(x[200:300])