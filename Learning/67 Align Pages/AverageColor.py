import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.signal import find_peaks

img = mpimg.imread('YellowRect.png')
print(img)

avg = np.median(img, axis=(0,1))
print(avg)

yellow = np.array([0.7921569, 0.6392157, 0.27058825])
print(yellow)

