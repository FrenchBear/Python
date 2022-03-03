import matplotlib.image as mpimg        # type: ignore
import numpy as np

img = mpimg.imread('YellowRect.png')
print(img)

avg = np.median(img, axis=(0,1))
print(avg)

yellow = np.array([0.7921569, 0.6392157, 0.27058825])
print(yellow)

